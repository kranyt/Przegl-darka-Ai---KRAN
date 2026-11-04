/* DziobSi – wbudowany mózg AI (model językowy uruchamiany w telefonie, bez internetu).
   Model pobiera się raz z Hugging Face i zostaje w pamięci telefonu. */
import { Wllama } from './vendor/wllama/wllama.js';

// Polski model Bielik 1.5B v3.0 Instruct (SpeakLeash), kwantyzacja Q4_K_M (~973 MB)
const MODEL = { repo: 'second-state/Bielik-1.5B-v3.0-Instruct-GGUF', file: 'Bielik-1.5B-v3.0-Instruct-Q4_K_M.gguf' };
const KEY = 'dziobsi:llm:installed';

const SYSTEM = `Jesteś DziobSi (Dziob Inteligence) – miła, wesoła polska sztuczna inteligencja z telefonu, z ptasim dziobem.
Zasady:
1. Piszesz WYŁĄCZNIE po polsku.
2. Nigdy nie powtarzasz ani nie przepisujesz wiadomości użytkownika – zawsze odpowiadasz na nią własnymi słowami.
3. Gdy użytkownik proponuje temat (np. „pogadajmy o basenie”), podejmujesz DOKŁADNIE ten temat: mówisz o nim coś konkretnego i zadajesz pytanie o ten temat.
4. Gdy użytkownik prosi o propozycję, sam coś konkretnego proponujesz.
5. Na pytanie odpowiadasz konkretnie. Na zwykłą wiadomość reagujesz ciepło i podtrzymujesz rozmowę.
6. Krótko: 1–3 zdania, najwyżej jedna emotka, bez wulgaryzmów. Nie mówisz o słowach ani słownikach, nie przedstawiasz się.`;
// przykładowe wymiany – uczą modelu podejmować temat i nie powtarzać użytkownika
const SEED = [
  { role: 'user', content: 'Hej!' },
  { role: 'assistant', content: 'Hej! Miło cię widzieć. O czym chcesz pogadać?' },
  { role: 'user', content: 'Zaproponuj coś.' },
  { role: 'assistant', content: 'Może opowiesz mi o swoim ulubionym hobby? Albo zagrajmy w zgadywankę – ty wybierasz!' },
  { role: 'user', content: 'Może pogadamy o kotach?' },
  { role: 'assistant', content: 'Chętnie! Koty są bardzo ciekawskie i potrafią przespać nawet 16 godzin dziennie. Masz kota?' },
  { role: 'user', content: 'Powtarzasz po mnie.' },
  { role: 'assistant', content: 'Przepraszam, już się poprawiam! Powiedz, o czym chcesz pogadać, a ja chętnie podejmę temat.' },
];
// temat zaproponowany przez użytkownika: „pogadamy o basenie” → „basen”
function topicOf(user) {
  const m = user.toLowerCase().match(/(?:o|na temat|temat)\s+(?:tym\s+)?(\p{L}{4,})/u);
  return m && !/^(czym|kim|sobie|mnie|tobie|nich|niej|nim|tym|tamtym|wszystkim|czymś|czyms)$/.test(m[1]) ? m[1] : null;
}
// pytanie na końcu odpowiedzi i jego „szablon” (pierwsze 3 słowa)
const tailQ = t => { const m = t.match(/[^.!?]*\?\s*\S{0,3}\s*$/u); return m ? m[0].trim() : ''; };
const qKey = q => words(q).slice(0, 3).join(' ');
// usuń pytanie końcowe, jeśli powtarza szablon pytania z poprzedniej odpowiedzi („A co Ci się kojarzy z …?”)
function dropRepeatedQuestion(text, prev) {
  const q = tailQ(text), pq = tailQ(prev || '');
  if (!q || !pq || qKey(q).length < 5 || qKey(q) !== qKey(pq)) return text;
  const rest = text.slice(0, text.lastIndexOf(q)).trim();
  return rest.length >= 20 ? rest : text;
}
const mentions = (out, topic) => out.toLowerCase().includes(topic.slice(0, Math.max(4, topic.length - 3)));
// czy odpowiedź tylko powtarza wiadomość użytkownika?
const words = t => t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ł/g, 'l').match(/\p{L}{2,}/gu) || [];
function echoes(user, out) {
  const u = words(user), o = words(out);
  if (!o.length) return true;
  const us = new Set(u);
  const same = o.filter(w => us.has(w)).length;
  return (o.length <= u.length + 3 && same / o.length >= 0.6) || (u.length >= 2 && o.slice(0, u.length).join(' ') === u.join(' '));
}
// odpowiedź po angielsku? (brak polskich znaków, dużo angielskich słówek)
// odpowiedź po angielsku? tylko typowo angielskie słowa (bez „to”, „i”, które są też polskie)
const english = t => !/[ąćęłńóśźż]/i.test(t) &&
  !/\b(jest|nie|sie|się|czy|jak|ale|mam|masz|jestem|co|ty|ja|mi|tak|bardzo|fajnie|mozesz|możesz)\b/i.test(t) &&
  (t.match(/\b(the|and|is|are|you|your|what|it's|with|my|love|great|this|that|have|for)\b/gi) || []).length >= 3;
// instrukcja + pamięć o użytkowniku
const system = () => SYSTEM;
let memMode = 'message'; // 'message' = osobna wiadomość (szybciej) | 'inline' = w instrukcji
const memoryMsg = () => { const m = window.DziobMemory && window.DziobMemory.prompt(); return m ? [{ role: 'system', content: m }] : []; };
// zdania, które już padły w poprzednich odpowiedziach -> usuń (model lubi kopiować sam siebie)
const sentences = t => t.split(/(?<=[.!?…])\s+(?=[A-ZĄĆĘŁŃÓŚŹŻ0-9„"])/u).map(x => x + ' ');
function similar(a, b) {
  const A = words(a), B = new Set(words(b));
  if (A.length < 3) return false;
  return A.filter(w => B.has(w)).length / A.length >= 0.6;
}
function dropRepeats(text, prevReplies) {
  const old = prevReplies.flatMap(sentences);
  const kept = sentences(text).filter(s => !old.some(o => similar(s, o)));
  return kept.join('').trim();
}
const CONVO_KEY = 'dziobsi:llm:convo';

let wllama = null;
const has = () => { try { return !!localStorage.getItem(KEY); } catch (e) { return false; } };
let state = has() ? 'installed' : 'none'; // none | installed | downloading | loading | ready | error
let progress = 0;
let gpuLayers;
let lastTimings = null;

// Prawdziwa karta graficzna (WebGPU) = szybko. Programowa „karta” (SwiftShader) jest wolniejsza niż procesor – wtedy liczymy na CPU.
async function pickGpu() {
  try {
    if (!navigator.gpu || /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent || '')) return 0;
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
// awaria silnika (np. brak pamięci w telefonie) -> trzeba go uruchomić od nowa
const crashed = e => /crash|reload the module|abort|memory|out of bounds|unreachable|RuntimeError|exit\(/i.test(String((e && e.message) || e));
const SAFE_KEY = 'dziobsi:llm:safe';
// tryb oszczędny: mniej pamięci (krótszy kontekst, mniejsze bufory, 2 wątki) – włącza się sam po awarii
let safe = (() => { try { return localStorage.getItem(SAFE_KEY) === '1'; } catch (e) { return false; } })();
let lastAbort = '';
const logger = {
  debug() {}, log() {}, info() {},
  warn: (...a) => console.warn(...a),
  error: (...a) => { lastAbort = a.map(String).join(' ').slice(0, 200); console.error(...a); },
};
let noCache = false; // true = model działa, ale nie zmieścił się w pamięci (pobierze się znowu po restarcie)
let convo = (() => { try { return (JSON.parse(localStorage.getItem('dziobsi:llm:convo')) || []).slice(-4); } catch (e) { return []; } })(); // rozmowa widziana przez model – rośnie od końca, by nie przeliczać jej od nowa
let error = '';
const listeners = new Set();
const emit = () => listeners.forEach(fn => { try { fn(api.info()); } catch (e) { /* nic */ } });

let fakeCrash = false; // tylko do testów automatycznych
async function generate(turns, onText, opts = {}) {
  if (fakeCrash) { fakeCrash = false; throw new Error('wllama has crashed, please reload the module'); }
  const last = turns[turns.length - 1];
  let messages = [{ role: 'system', content: system() }, ...SEED, ...turns.slice(0, -1), ...memoryMsg(), last];
  if (memMode === 'inline') {
    const mm = memoryMsg();
    messages = [{ role: 'system', content: system() + (mm.length ? '\n' + mm[0].content : '') }, ...SEED, ...turns];
  }
  const req = () => wllama.createChatCompletion({
    messages, max_tokens: safe ? 120 : 160, temperature: opts.temperature || 0.6, top_p: 0.9, top_k: 40, min_p: 0.05,
    penalty_repeat: 1.15, penalty_last_n: 128, frequency_penalty: 0.4, presence_penalty: 0.3,
    stream: true,
  });
  let stream;
  try { stream = await req(); } catch (e) {
    // szablon rozmowy modelu nie przyjmuje drugiej wiadomości systemowej -> pamięć w instrukcji
    if (memMode === 'inline' || !memoryMsg().length) throw e;
    memMode = 'inline';
    return generate(turns, onText, opts);
  }
  let text = '', loop = false;
  try {
    // bez przerywania w trakcie (przerwanie mogło wywracać silnik) – po zapętleniu tylko przestajemy dopisywać
    for await (const chunk of stream) {
      if (chunk && chunk.error) throw new Error(chunk.error.message || String(chunk.error));
      if (chunk.timings) lastTimings = chunk.timings;
      const piece = chunk.choices && chunk.choices[0] && chunk.choices[0].delta && chunk.choices[0].delta.content;
      if (piece && !loop) {
        text += piece;
        if (looping(text)) loop = true; else onText && onText(text);
      }
    }
  } catch (e) {
    if (!crashed(e) && memMode !== 'inline' && memoryMsg().length && !text) { memMode = 'inline'; return generate(turns, onText, opts); }
    throw e;
  }
  // usuń zapętlony ogon
  text = text.replace(/(.{1,3})\1{3,}$/su, '$1').replace(/(.{8,40}?)\1+$/su, '$1');
  // bez „odgrywania” typu *uśmiecha się ciepło* albo (pyta się)
  return text.replace(/\*[^*\n]{1,60}\*/g, '').replace(/\((?:pyta|uśmiecha|odpowiada|zadaje|próbuje|śmieje|myśli|przytula)[^)]{0,60}\)/giu, '')
    .replace(/[ \t]{2,}/g, ' ').replace(/\s+([.,!?])/g, '$1').trim();
}

const api = {
  info: () => ({ state, progress, error, noCache, safe, lastAbort, gpu: gpuLayers !== 0, threads: self.crossOriginIsolated ? (navigator.hardwareConcurrency || 1) : 1, lastTimings, ready: state === 'ready' }),
  onChange(fn) { listeners.add(fn); fn(api.info()); return () => listeners.delete(fn); },
  get ready() { return state === 'ready'; },

  async load() {
    if (['downloading', 'loading', 'ready'].includes(state)) return;
    const wasInstalled = has();
    state = wasInstalled ? 'loading' : 'downloading'; progress = 0; error = ''; emit();
    try {
      wllama = new Wllama({ default: new URL('./vendor/wllama/wllama.wasm', import.meta.url).href }, { logger });
      try { if (navigator.storage && navigator.storage.persist) await navigator.storage.persist(); } catch (e) { /* nic */ }
      gpuLayers = await pickGpu();
      const mobile = /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent || '');
      const opts = {
        n_ctx: safe ? 1024 : 2048,
        n_batch: safe ? 64 : (mobile ? 128 : 512),
        n_ubatch: safe ? 64 : (mobile ? 128 : 512),
        ...(safe || mobile ? { n_threads: Math.min(safe ? 2 : 4, navigator.hardwareConcurrency || 2) } : {}),
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
      try { await wllama.createChatCompletion({ messages: [{ role: 'system', content: system() }, ...SEED, { role: 'user', content: 'cześć' }], max_tokens: 1 }); } catch (e) { /* nic */ }
      state = 'ready'; progress = 1; emit();
    } catch (e) {
      state = 'error'; error = (e && e.message) || String(e); emit();
    }
  },

  /* ponowne uruchomienie silnika po awarii (model z pamięci telefonu, bez pobierania) */
  async restart(saveMode) {
    if (saveMode && !safe) { safe = true; try { localStorage.setItem(SAFE_KEY, '1'); } catch (e) { /* brak */ } }
    try { if (wllama) await wllama.exit(); } catch (e) { /* martwy silnik */ }
    wllama = null; state = 'none'; emit();
    await api.load();
    if (state !== 'ready') throw new Error(error || 'nie udało się ponownie uruchomić Mózgu AI');
  },

  async remove() {
    try { if (wllama) { await wllama.exit(); } } catch (e) { /* nic */ }
    try { const w = wllama || new Wllama({ default: new URL('./vendor/wllama/wllama.wasm', import.meta.url).href }); await w.cacheManager.clear(); } catch (e) { /* nic */ }
    try { localStorage.removeItem(KEY); } catch (e) { /* brak */ }
    wllama = null; state = 'none'; progress = 0; emit();
  },

  _testCrash() { fakeCrash = true; },
  reset() { convo = []; try { localStorage.removeItem(CONVO_KEY); } catch (e) { /* brak */ } },

  async chat(userText, onText) {
    try { return await chatOnce(userText, onText); } catch (e) {
      if (!crashed(e)) throw e;
      // silnik się wywrócił: uruchom go ponownie (za drugim razem w trybie oszczędnym) i spróbuj jeszcze raz
      onText && onText('🔄 Uruchamiam Mózg AI ponownie…');
      convo = convo.slice(-2);
      await api.restart(true);
      onText && onText('');
      return await chatOnce(userText, onText);
    }
  },
};

async function chatOnce(userText, onText) {
  {
    if (state !== 'ready') throw new Error('Mózg AI nie jest gotowy');
    // krótki kontekst: ostatnie 3 wymiany, najwyżej ~1200 znaków
    if (convo.length > (safe ? 4 : 10) || convo.reduce((n, m) => n + m.content.length, 0) > (safe ? 800 : 2200)) convo = convo.slice(-2);
    let text = await generate([...convo, { role: 'user', content: userText }], onText);
    const longMsg = words(userText).length >= 3; // krótkie wiadomości („Eli”, „ale co”) nie są sprawdzane pod kątem powtarzania
    if (!text || (longMsg && echoes(userText, text))) {
      // model powtórzył wiadomość albo nic nie powiedział – spróbuj jeszcze raz
      onText && onText('');
      const again = await generate([...convo, { role: 'user', content: userText + '\n(Odpowiedz mi własnymi słowami.)' }], onText, { temperature: 0.9 });
      if (again && !(longMsg && echoes(userText, again))) text = again;
      else if (!text) text = again;
    }
    const topic = topicOf(userText);
    if (topic && !mentions(text, topic)) {
      // model zgubił temat – przypomnij go
      onText && onText('');
      const again = await generate([...convo, { role: 'user', content: `${userText}\n(Temat rozmowy: ${topic}. Powiedz o tym coś konkretnego i zadaj pytanie.)` }], onText, { temperature: 0.8 });
      if (again && !echoes(userText, again)) text = again;
    }
    if (english(text)) {
      // model odpłynął na angielski – zapytaj jeszcze raz, prosząc o polski
      onText && onText('');
      const pl = await generate([...convo, { role: 'user', content: userText + '\n(Odpowiedz po polsku.)' }], onText);
      if (pl && !english(pl)) text = pl;
    }
    const prevs = convo.filter(m => m.role === 'assistant').slice(-3).map(m => m.content);
    const prev = prevs[prevs.length - 1];
    let fresh = dropRepeats(text, prevs);
    if (fresh.length < 12 && prevs.length) {
      // prawie całe zdanie już było – poproś o nową odpowiedź
      onText && onText('');
      const again = await generate([...convo, { role: 'user', content: userText + '\n(Odpowiedz inaczej niż wcześniej.)' }], onText, { temperature: 0.85 });
      fresh = dropRepeats(again, prevs) || again;
    }
    text = dropRepeatedQuestion(fresh || text, prev);
    if (text) {
      convo.push({ role: 'user', content: userText }, { role: 'assistant', content: text });
      try { localStorage.setItem(CONVO_KEY, JSON.stringify(convo.slice(-10))); } catch (e) { /* brak */ }
    }
    return text;
  }
}

window.DziobLLM = api;
window.dispatchEvent(new Event('dziobllm'));
if (state === 'installed') api.load(); // model już pobrany – wczytaj z pamięci telefonu
