/* DziobSi – wbudowany mózg AI (model językowy uruchamiany w telefonie, bez internetu).
   Model pobiera się raz z Hugging Face i zostaje w pamięci telefonu. */
import { Wllama, LoggerWithoutDebug } from './vendor/wllama/wllama.js';

// Polski model Bielik 1.5B v3.0 Instruct (SpeakLeash), kwantyzacja Q4_K_M (~973 MB)
const MODEL = { repo: 'second-state/Bielik-1.5B-v3.0-Instruct-GGUF', file: 'Bielik-1.5B-v3.0-Instruct-Q4_K_M.gguf' };
const KEY = 'dziobsi:llm:installed';

const SYSTEM = `Jesteś DziobSi (Dziob Inteligence) – przyjazną polską sztuczną inteligencją w aplikacji na telefon. Twoim symbolem jest ptasi dziób 🐦.
Znasz 500 000 polskich słów i świetnie posługujesz się językiem polskim.
Zasady:
- Zawsze odpowiadasz po polsku, krótko: 1–3 zdania.
- Używasz najwyżej jednej emotki w odpowiedzi.
- Uważnie czytasz wiadomość i od razu odpowiadasz dokładnie na to, o co chodzi. Nie przedstawiasz się i nie zaczynasz od „DziobSi:”.
- Jeśli użytkownik nie zadaje pytania, po prostu z nim rozmawiasz: reagujesz ciepło i podtrzymujesz rozmowę.
- Jesteś miły, wesoły i życzliwy. Lubisz użytkownika – gdy pyta, czy go lubisz, odpowiadasz, że tak, bardzo.
- Nigdy nie używasz wulgaryzmów.
- Jeśli czegoś nie wiesz na pewno, mówisz to uczciwie.
- Nie dopisuj na końcu formułek typu „jeśli masz pytania” – aplikacja zrobi to sama.
O sobie: wyklułeś się w 2026 roku, mieszkasz w telefonie użytkownika, ulubiony kolor: pomarańczowy jak twój dziób.`;

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
let error = '';
const listeners = new Set();
const emit = () => listeners.forEach(fn => { try { fn(api.info()); } catch (e) { /* nic */ } });

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

  /* history: [{role:'user'|'model', text}] (bez bieżącej wiadomości) */
  async chat(history, userText, onText) {
    if (state !== 'ready') throw new Error('Mózg AI nie jest gotowy');
    const messages = [{ role: 'system', content: SYSTEM }];
    for (const m of history.slice(-6)) {
      if (m.blocked || !m.text) continue;
      messages.push({ role: m.role === 'user' ? 'user' : 'assistant', content: m.text.slice(0, 300) });
    }
    messages.push({ role: 'user', content: userText });
    const ctrl = new AbortController();
    const stream = await wllama.createChatCompletion({
      messages, max_tokens: 180, temperature: 0.7, top_p: 0.9, top_k: 40,
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
  },
};

window.DziobLLM = api;
window.dispatchEvent(new Event('dziobllm'));
if (state === 'installed') api.load(); // model już pobrany – wczytaj z pamięci telefonu
