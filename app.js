/* DziobSi – logika aplikacji */
(function () {
  'use strict';

  const $ = s => document.querySelector(s);
  const store = {
    get(k, d) { try { const v = localStorage.getItem('dziobsi:' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('dziobsi:' + k, JSON.stringify(v)); } catch (e) { /* brak pamięci */ } },
  };

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

  function addBubble(role, text, src, blocked) {
    const d = document.createElement('div');
    d.className = 'msg ' + (role === 'user' ? 'me' : 'bot') + (blocked ? ' blocked' : '');
    d.innerHTML = md(text) + (src ? `<span class="src">${esc(src)}</span>` : '') +
      (blocked ? '<span class="src">🚫 Niecenzuralne – DziobSi nie odpowiada</span>' : '');
    box.appendChild(d);
    box.scrollTop = box.scrollHeight;
    return d;
  }

  function welcome() {
    const d = addBubble('model', 'Cześć! 🐦 Jestem **DziobSi** – *Dziob Inteligence*.\nMam w głowie **500 000 słów**. O co chcesz zapytać?');
    const chips = document.createElement('div');
    chips.className = 'chips';
    ['pomoc', 'przeanalizuj dziobolot', 'rymy do dziób', 'losowe słowo', 'opowiedz dowcip']
      .forEach(q => { const b = document.createElement('button'); b.type = 'button'; b.textContent = q; b.onclick = () => send(q); chips.appendChild(b); });
    d.appendChild(chips);
  }

  function render() {
    box.innerHTML = '';
    welcome();
    history.forEach(m => addBubble(m.role, m.text, m.src, m.blocked));
  }

  async function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    busy = true; $('#btnSend').disabled = true;
    // Wulgaryzmy: DziobSi nie odpowiada
    if (window.Brain && Brain.isVulgar(text)) {
      history.push({ role: 'user', text, blocked: true });
      store.set('history', history);
      addBubble('user', text, null, true);
      busy = false; $('#btnSend').disabled = false;
      return;
    }

    history.push({ role: 'user', text });
    addBubble('user', text);

    const typing = addBubble('model', '');
    typing.innerHTML = '<span class="typing"><span></span><span></span><span></span></span>';

    let reply;
    try {
      if (!Brain.ready) await brainReady;
      await new Promise(r => setTimeout(r, 350)); // chwila „myślenia”
      reply = Brain.reply(text);
    } catch (e) {
      reply = 'Ups, coś poszło nie tak: ' + e.message;
    }
    const src = '🐦 DziobSi · 500 000 słów';
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
