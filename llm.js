/* DziobSi – wbudowany mózg AI (model językowy uruchamiany w telefonie, bez internetu).
   Model pobiera się raz z Hugging Face i zostaje w pamięci telefonu. */
import { Wllama, LoggerWithoutDebug } from './vendor/wllama/wllama.js';

// Polski model Bielik 1.5B v3.0 Instruct (SpeakLeash), kwantyzacja Q4_K_M (~973 MB)
const MODEL = { repo: 'second-state/Bielik-1.5B-v3.0-Instruct-GGUF', file: 'Bielik-1.5B-v3.0-Instruct-Q4_K_M.gguf' };
const KEY = 'dziobsi:llm:installed';

const SYSTEM = `Jesteś DziobSi (Dziob Inteligence) – miła polska sztuczna inteligencja z telefonu, z ptasim dziobem. Znasz 500 000 polskich słów.
Zawsze piszesz WYŁĄCZNIE po polsku, nigdy po angielsku. Odpowiadasz krótko (1–3 zdania) i od razu na temat. Gdy ktoś nie pyta, po prostu ciepło rozmawiasz. Bez wulgaryzmów, najwyżej jedna emotka. Nie przedstawiasz się i nie dopisujesz „jeśli masz pytania”.`;
// przykładowa wymiana – ustawia polski język i krótki, ciepły styl
const SEED = [
  { role: 'user', content: 'Hej, byłem dziś w parku.' },
  { role: 'assistant', content: 'Super! Spacer w parku to świetny pomysł. Co tam było najfajniejsze?' },
];
// odpowiedź po angielsku? (brak polskich znaków, dużo angielskich słówek)
const english = t => !/[ąćęłńóśźż]/i.test(t) && (t.match(/\b(the|and|is|are|you|your|what|it's|with|of|to|i|my|love|great)\b/gi) || []).length >= 3;

let wllama = null;
const has = () => { try { return !!localStorage.getItem(KEY); } catch (e) { return false; } };
let state = has() ? 'installed' : 'none'; // none | installed | downloading | loading | ready | error
let progress = 0;
let gpuLayers;
let lastTimings = null;

// Prawdziwa karta graficzna (WebGPU) = szybko. Programowa „karta” (SwiftShader) jest wolniejsza niż procesor – wtedy liczymy na CPU.
async function pickGpu() {
  try {
    if (!navigator.gpu) return 0;
    const a = await navigator.gpu.requestAdapter();
    if (!a || a.isFallbackAdapter) return 0;
    const i = a.info || {};
    if (/swiftshader|llvmpipe|software|lavapipe/i.test([i.vendor, i.architecture, i.device, i.description].join(' '))) return 0;
    return undefined; // wszystkie warstwy na GPU
  } catch (e) { return 0; }
}
// Wykrywanie zapętlenia (np. ta sama emotka w kółko)
function looping(t) {
  return /(.{1,3})\1{5,}$/su.test(t) || /(.{8,40}?)\1{2,}$/su.test(t);
}
let noCache = false; // true = model działa, ale nie zmieścił się w pamięci (pobierze się znowu po restarcie)
let convo = []; // rozmowa widziana przez model – rośnie od końca, by nie przeliczać jej od nowa
let error = '';
const listeners = new Set();
const emit = () => listeners.forEach(fn => { try { fn(api.info()); } catch (e) { /* nic */ } });

async function generate(turns, onText) {
  const messages = [{ role: 'system', content: SYSTEM }, ...SEED, ...turns];
  const ctrl = new AbortController();
  const stream = await wllama.createChatCompletion({
    messages, max_tokens: 160, temperature: 0.6, top_p: 0.9, top_k: 40,
    penalty_repeat: 1.15, penalty_last_n: 64, frequency_penalty: 0.3,
    stream: true, abortSignal: ctrl.signal,
  });
  let text = '';
  try {
    for await (const chunk of stream) {
      if (chunk.timings) lastTimings = chunk.timings;
      const piece = chunk.choices && chunk.choices[0] && chunk.choices[0].delta && chunk.choices[0].delta.content;
      if (piece) {
        text += piece;
        if (looping(text)) { ctrl.abort(); break; }
        onText && onText(text);
      }
    }
  } catch (e) {
    if (!ctrl.signal.aborted) throw e;
  }
  // usuń zapętlony ogon
  return text.replace(/(.{1,3})\1{3,}$/su, '$1').replace(/(.{8,40}?)\1+$/su, '$1').trim();
}

const api = {
  info: () => ({ state, progress, error, noCache, gpu: gpuLayers !== 0, threads: self.crossOriginIsolated ? (navigator.hardwareConcurrency || 1) : 1, lastTimings, ready: state === 'ready' }),
  onChange(fn) { listeners.add(fn); fn(api.info()); return () => listeners.delete(fn); },
  get ready() { return state === 'ready'; },

  async load() {
    if (['downloading', 'loading', 'ready'].includes(state)) return;
    const wasInstalled = has();
    state = wasInstalled ? 'loading' : 'downloading'; progress = 0; error = ''; emit();
    try {
      wllama = new Wllama({ default: new URL('./vendor/wllama/wllama.wasm', import.meta.url).href }, { logger: LoggerWithoutDebug });
      try { if (navigator.storage && navigator.storage.persist) await navigator.storage.persist(); } catch (e) { /* nic */ }
      gpuLayers = await pickGpu();
      const opts = {
        n_ctx: 2048,
        ...(gpuLayers === 0 ? { n_gpu_layers: 0 } : {}),
        progressCallback: ({ loaded, total }) => {
          progress = total ? loaded / total : 0;
          if (progress >= 0.999) state = 'loading';
          emit();
        },
      };
      try {
        await wllama.loadModelFromHF(MODEL, opts);
      } catch (e) {
        // za mało miejsca na zapis – uruchom model bez zapisywania w pamięci telefonu
        if (!/quota|storage|space/i.test(String(e && e.message))) throw e;
        console.warn('Brak miejsca na zapis modelu – wczytuję bez zapisu', e);
        state = 'downloading'; progress = 0; emit();
        await wllama.loadModelFromHF(MODEL, { ...opts, useCache: false });
        noCache = true;
      }
      if (!noCache) { try { localStorage.setItem(KEY, '1'); } catch (e) { /* brak */ } }
      // rozgrzewka: przelicz instrukcję od razu, żeby pierwsza odpowiedź była szybsza
      state = 'loading'; emit();
      try { await wllama.createChatCompletion({ messages: [{ role: 'system', content: SYSTEM }, ...SEED, { role: 'user', content: 'cześć' }], max_tokens: 1 }); } catch (e) { /* nic */ }
      state = 'ready'; progress = 1; emit();
    } catch (e) {
      state = 'error'; error = (e && e.message) || String(e); emit();
    }
  },

  async remove() {
    try { if (wllama) { await wllama.exit(); } } catch (e) { /* nic */ }
    try { const w = wllama || new Wllama({ default: new URL('./vendor/wllama/wllama.wasm', import.meta.url).href }); await w.cacheManager.clear(); } catch (e) { /* nic */ }
    try { localStorage.removeItem(KEY); } catch (e) { /* brak */ }
    wllama = null; state = 'none'; progress = 0; emit();
  },

  reset() { convo = []; },

  async chat(userText, onText) {
    if (state !== 'ready') throw new Error('Mózg AI nie jest gotowy');
    // za długa rozmowa -> zacznij kontekst od nowa (zostaw ostatnią wymianę)
    if (convo.reduce((n, m) => n + m.content.length, 0) > 1400) convo = convo.slice(-2);
    let text = await generate([...convo, { role: 'user', content: userText }], onText);
    if (english(text)) {
      // model odpłynął na angielski – zapytaj jeszcze raz, prosząc o polski
      onText && onText('');
      text = await generate([...convo, { role: 'user', content: userText + '\n(Odpowiedz po polsku.)' }], onText);
    }
    if (english(text)) return ''; // nadal nie po polsku – aplikacja odpowie mózgiem na regułach
    convo.push({ role: 'user', content: userText }, { role: 'assistant', content: text });
    return text;
  },
};

window.DziobLLM = api;
window.dispatchEvent(new Event('dziobllm'));
if (state === 'installed') api.load(); // model już pobrany – wczytaj z pamięci telefonu
