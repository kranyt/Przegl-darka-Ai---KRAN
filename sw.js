/* DziobSi – service worker: działanie offline */
const CACHE = 'dziobsi-v16';
const ASSETS = [
  './', 'index.html', 'style.css', 'bigdict.js', 'brain.js', 'memory.js', 'talk.js', 'code.js', 'app.js', 'llm.js', 'vendor/wllama/wllama.js', 'vendor/wllama/wllama.wasm', 'manifest.webmanifest',
  'data/slowa.txt', 'data/slownik.bin', 'icons/icon.svg', 'icons/icon-192.png', 'icons/icon-512.png',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// Nagłówki izolacji (COOP/COEP) – pozwalają mózgowi AI liczyć na wielu wątkach (szybsze odpowiedzi)
function isolate(res) {
  if (!res || res.status === 0 || res.type === 'opaque') return res;
  const h = new Headers(res.headers);
  h.set('Cross-Origin-Embedder-Policy', 'credentialless');
  h.set('Cross-Origin-Opener-Policy', 'same-origin');
  h.set('Cross-Origin-Resource-Policy', 'cross-origin');
  return new Response(res.body, { status: res.status, statusText: res.statusText, headers: h });
}

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  const big = /\.(bin|txt|wasm|png|svg)$/.test(url.pathname);
  const fromCache = () => caches.match(e.request);
  const fromNet = () => fetch(e.request).then(res => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
    return res;
  });
  // duże dane: najpierw pamięć podręczna; kod aplikacji: najpierw sieć (po aktualizacji zawsze nowy)
  e.respondWith((big ? fromCache().then(hit => hit || fromNet()) : fromNet().catch(() => fromCache())).then(isolate));
});
