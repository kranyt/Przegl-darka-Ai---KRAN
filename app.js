/* DziobSi – logika aplikacji */
(function () {
  'use strict';

  const $ = s => document.querySelector(s);
  const store = {
    get(k, d) { try { const v = localStorage.getItem('dziobsi:' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('dziobsi:' + k, JSON.stringify(v)); } catch (e) { /* brak pamięci */ } },
  };

  const SYSTEM_PROMPT =
    'Jesteś DziobSi (Dziob Inteligence) – przyjazny, pomocny asystent AI w aplikacji na telefon. ' +
    'Twoim symbolem jest ptasi dziób 🐦. Odpowiadasz domyślnie po polsku, zwięźle i konkretnie. ' +
    'Masz wbudowany słownik 500 000 polskich słów.';

  let history = store.get('history', []);   // [{role:'user'|'model', text, src}]
  let busy = false;

  /* ---------- zakładki ---------- */
  document.querySelectorAll('.tabs button').forEach(b => b.addEventListener('click', () => {
    document.querySelectorAll('.tabs button').forEach(x => x.classList.toggle('active', x === b));
    document.querySelectorAll('.tab').forEach(x => x.classList.toggle('active', x.id === 'tab-' + b.dataset.tab));
  }));

  /* ---------- formatowanie ---------- */
  function esc(s) { return s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
  function md(s) {
    const blocks = [];
    s = esc(s).replace(/```(\w*)\n?([\s\S]*?)```/g, (_, l, code) => { blocks.push(code); return '\u0000' + (blocks.length - 1) + '\u0000'; });
    s = s.replace(/`([^`\n]+)`/g, '<code>$1</code>')
         .replace(/\*\*([^*\n]+)\*\*/g, '<b>$1</b>')
         .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<i>$2</i>')
         .replace(/^#{1,6}\s*(.+)$/gm, '<b>$1</b>')
         .replace(/^\s*[-*]\s+/gm, '• ')
         .replace(/\n/g, '<br>');
    return s.replace(/\u0000(\d+)\u0000/g, (_, i) => '<pre><code>' + blocks[i] + '</code></pre>');
  }

  /* ---------- czat ---------- */
  const box = $('#messages');

  function addBubble(role, text, src) {
    const d = document.createElement('div');
    d.className = 'msg ' + (role === 'user' ? 'me' : 'bot');
    d.innerHTML = md(text) + (src ? `<span class="src">${esc(src)}</span>` : '');
    box.appendChild(d);
    box.scrollTop = box.scrollHeight;
    return d;
  }

  function welcome() {
    const d = addBubble('model', 'Cześć! 🐦 Jestem **DziobSi** – *Dziob Inteligence*.\nMam w głowie **500 000 słów**. O co chcesz zapytać?');
    const chips = document.createElement('div');
    chips.className = 'chips';
    ['pomoc', 'losowe słowo', 'rymy do dziób', 'sprawdź słowo inteligencja', 'policz 123*45']
      .forEach(q => { const b = document.createElement('button'); b.type = 'button'; b.textContent = q; b.onclick = () => send(q); chips.appendChild(b); });
    d.appendChild(chips);
  }

  function render() {
    box.innerHTML = '';
    welcome();
    history.forEach(m => addBubble(m.role, m.text, m.src));
  }

  async function askGemini(key, model) {
    const contents = history.slice(-20).map(m => ({ role: m.role, parts: [{ text: m.text }] }));
    const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
      body: JSON.stringify({ systemInstruction: { parts: [{ text: SYSTEM_PROMPT }] }, contents }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error((data.error && data.error.message) || ('HTTP ' + res.status));
    const parts = data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts;
    const text = (parts || []).map(p => p.text || '').join('').trim();
    if (!text) throw new Error('Pusta odpowiedź modelu');
    return text;
  }

  async function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    busy = true; $('#btnSend').disabled = true;
    history.push({ role: 'user', text });
    addBubble('user', text);

    const typing = addBubble('model', '');
    typing.innerHTML = '<span class="typing"><span></span><span></span><span></span></span>';

    const key = store.get('apiKey', '');
    const useOnline = store.get('useOnline', true);
    let reply, src;
    try {
      if (key && useOnline && navigator.onLine !== false) {
        try {
          reply = await askGemini(key, store.get('model', '') || 'gemini-2.5-flash');
          src = '🌐 DziobSi Online';
        } catch (e) {
          reply = Brain.reply(text) + `\n\n⚠️ AI online niedostępne: ${e.message}`;
          src = '🐦 DziobSi Offline';
        }
      } else {
        if (!Brain.ready) await brainReady;
        reply = Brain.reply(text);
        src = '🐦 DziobSi Offline · 500 000 słów';
      }
    } catch (e) {
      reply = 'Ups, coś poszło nie tak: ' + e.message;
    }
    typing.remove();
    history.push({ role: 'model', text: reply, src });
    if (history.length > 200) history = history.slice(-200);
    store.set('history', history);
    addBubble('model', reply, src);
    busy = false; $('#btnSend').disabled = false;
  }

  const input = $('#input');
  $('#chatForm').addEventListener('submit', e => { e.preventDefault(); const v = input.value; input.value = ''; autosize(); send(v); });
  input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); $('#chatForm').requestSubmit(); } });
  function autosize() { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 120) + 'px'; }
  input.addEventListener('input', autosize);

  /* ---------- słownik ---------- */
  let dictMode = 'prefix';
  const modeBtns = document.querySelectorAll('[data-mode]');
  function setMode(m) { dictMode = m; modeBtns.forEach(b => b.classList.toggle('active', b.dataset.mode === m)); doSearch(); }
  modeBtns.forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));

  function showWords(list, info) {
    $('#dictInfo').textContent = info;
    $('#dictResults').innerHTML = list.map(w => `<li><span>${esc(w)}</span><small>#${Brain.rankOf(w).toLocaleString('pl-PL')}</small></li>`).join('');
  }
  let searchTimer;
  function doSearch() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      if (!Brain.ready) { $('#dictInfo').textContent = 'Słownik jeszcze się ładuje…'; return; }
      const q = $('#dictSearch').value;
      if (!q.trim()) { showWords([], ''); return; }
      const r = Brain.search(q, dictMode, 200);
      const exact = Brain.has(q) ? `✅ „${q.trim()}” jest w słowniku. ` : '';
      showWords(r.items, `${exact}Znaleziono ${r.total.toLocaleString('pl-PL')} słów${r.total > r.items.length ? ' (pokazuję ' + r.items.length + ')' : ''}.`);
    }, 200);
  }
  $('#dictSearch').addEventListener('input', doSearch);
  $('#btnRandom').addEventListener('click', () => { if (Brain.ready) showWords(Brain.random(20), '20 losowych słów:'); });
  setMode('prefix');

  /* ---------- ustawienia ---------- */
  $('#apiKey').value = store.get('apiKey', '');
  $('#model').value = store.get('model', '');
  $('#useOnline').checked = store.get('useOnline', true);
  $('#btnSave').addEventListener('click', () => {
    store.set('apiKey', $('#apiKey').value.trim());
    store.set('model', $('#model').value.trim());
    store.set('useOnline', $('#useOnline').checked);
    $('#saveInfo').textContent = '✅ Zapisano.';
    setTimeout(() => { $('#saveInfo').textContent = ''; }, 2000);
  });
  $('#btnClear').addEventListener('click', () => {
    if (!confirm('Wyczyścić całą rozmowę?')) return;
    history = []; store.set('history', history); render();
  });

  /* ---------- instalacja (PWA) ---------- */
  let deferredPrompt;
  window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); deferredPrompt = e; $('#btnInstall').hidden = false; });
  $('#btnInstall').addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt(); await deferredPrompt.userChoice; deferredPrompt = null; $('#btnInstall').hidden = true;
  });
  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }

  /* ---------- start ---------- */
  render();
  const status = $('#status');
  const brainReady = Brain.load(n => { status.textContent = `Ładowanie mózgu… (${n.toLocaleString('pl-PL')} / 500 000 słów)`; })
    .then(n => {
      status.textContent = `Dziob Inteligence · ${n.toLocaleString('pl-PL')} słów`;
      $('#dictCount').textContent = n.toLocaleString('pl-PL');
      doSearch();
    })
    .catch(e => { status.textContent = 'Błąd słownika: ' + e.message; });
})();
