/* DziobSi – logika aplikacji */
(function () {
  'use strict';

  const $ = s => document.querySelector(s);
  const store = {
    get(k, d) { try { const v = localStorage.getItem('dziobsi:' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('dziobsi:' + k, JSON.stringify(v)); } catch (e) { /* brak pamięci */ } },
  };
  const fmt = n => n.toLocaleString('pl-PL');

  const APP_VERSION = '2.0.0';
  const FOOTER = 'Jeśli masz jeszcze jakieś zapytanie, pytaj – jestem otwarty na wszystko! 🐦';
  // komendy słownikowe – zawsze obsługuje je dokładny mózg słownikowy
  const TOOL = /^(rym\S* (do|na) |policz|oblicz|kt[oó]ra (jest )?godzina|jaka (jest )?data|ile (znasz|masz) s[lł][oó]w|pomoc$)/;
  let lastSrc = '';
  let history = store.get('history', []);   // [{role:'user'|'model', text, blocked?}]
  let busy = false;

  /* ---------- zakładki ---------- */
  function showTab(name) {
    document.querySelectorAll('.tabbar button').forEach(x => x.classList.toggle('active', x.dataset.tab === name));
    document.querySelectorAll('.tab').forEach(x => x.classList.toggle('active', x.id === 'tab-' + name));
    document.body.classList.toggle('on-chat', name === 'chat');
    $('#btnNew').style.visibility = name === 'chat' ? 'visible' : 'hidden';
  }
  document.querySelectorAll('.tabbar button').forEach(b => b.addEventListener('click', () => showTab(b.dataset.tab)));
  showTab('chat');

  /* ---------- formatowanie ---------- */
  function esc(s) { return s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
  const codeStore = [];
  function md(s) {
    const blocks = [];
    s = esc(s).replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => { blocks.push({ lang, code }); return '\u0000' + (blocks.length - 1) + '\u0000'; });
    s = s.replace(/`([^`\n]+)`/g, '<code>$1</code>')
         .replace(/\*\*([^*\n]+)\*\*/g, '<b>$1</b>')
         .replace(/\n/g, '<br>');
    return s.replace(/\u0000(\d+)\u0000/g, (_, i) => {
      const b = blocks[i];
      const id = codeStore.push(b.code) - 1;
      const raw = b.code.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
      codeStore[id] = raw;
      return `<div class="codeblock"><div class="cb-bar"><span>${b.lang || 'kod'}</span>` +
        `<button data-copy="${id}">Kopiuj</button>` +
        (b.lang === 'html' ? `<button data-open="${id}">Otwórz w Code ›</button>` : '') +
        `</div><pre><code>${b.code}</code></pre></div>`;
    });
  }

  async function copyText(text, btn) {
    try { await navigator.clipboard.writeText(text); }
    catch (e) {
      const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (_) { /* brak */ } ta.remove();
    }
    if (btn) { const o = btn.textContent; btn.textContent = 'Skopiowano ✓'; setTimeout(() => { btn.textContent = o; }, 1200); }
  }

  /* ---------- czat ---------- */
  const box = $('#messages');

  const SRC = { ai: '🧠 Mózg AI', basic: '⚡ Tryb podstawowy' };
  function addBubble(role, text, blocked, src) {
    const d = document.createElement('div');
    if (role === 'user') {
      d.className = 'msg me' + (blocked ? ' blocked' : '');
      d.innerHTML = esc(text).replace(/\n/g, '<br>') + (blocked ? '<span class="note">🚫 Niecenzuralne – brak odpowiedzi</span>' : '');
    } else {
      d.className = 'msg bot';
      d.innerHTML = `<img class="av" src="icons/icon.svg" alt=""><div class="body">${md(text)}${text ? `<p class="footer">${FOOTER}</p>` : ''}${src ? `<span class="note src">${SRC[src] || ''}</span>` : ''}</div>`;
    }
    box.appendChild(d);
    box.scrollTop = box.scrollHeight;
    return d;
  }

  function greeting() {
    const h = new Date().getHours();
    return h < 5 ? 'Dobranoc' : h < 12 ? 'Dzień dobry' : h < 18 ? 'Cześć' : 'Dobry wieczór';
  }

  function renderHello() {
    const d = document.createElement('div');
    d.className = 'hello';
    d.innerHTML = `<img src="icons/icon.svg" alt=""><h1>${greeting()}! <br>W czym <em>pomóc</em>?</h1><div class="chips"></div><p class="ver">DziobSi · wersja ${APP_VERSION}</p>`;
    const chips = d.querySelector('.chips');
    ['lubisz mnie?', 'opowiedz mi coś ciekawego', 'co to jest fotosynteza?', 'zrób grę', 'rymy do kot']
      .forEach(q => { const b = document.createElement('button'); b.type = 'button'; b.className = 'chip glass'; b.textContent = q; b.onclick = () => send(q); chips.appendChild(b); });
    box.appendChild(d);
  }

  function render() {
    box.innerHTML = '';
    if (!history.length) renderHello();
    history.forEach(m => addBubble(m.role, m.text, m.blocked, m.src));
  }

  // podpowiedzi ze słownika 5 000 000 słów dla modelu (literówki w wiadomości)
  function withHints(text) {
    if (!Brain.ready) return text;
    const tokens = [...new Set(text.toLowerCase().match(/[a-ząćęłńóśźż]{3,}/g) || [])];
    const hints = [];
    for (const w of tokens) {
      if (Brain.has(w)) continue;
      const s = Brain.suggest(w, 1)[0];
      if (s) hints.push(`„${w}” = prawdopodobnie „${s}”`);
      if (hints.length >= 3) break;
    }
    return hints.length ? `${text}\n\n(Literówki: ${hints.join('; ')}. Nie wspominaj o tym w odpowiedzi.)` : text;
  }
  // korekta pisowni odpowiedzi modelu słownikiem 5 000 000 słów (np. „najfajniejssze” → „najfajniejsze”)
  function spellfix(t) {
    if (!Brain.ready) return t;
    return t.replace(/(?<![\p{L}])\p{Ll}[\p{Ll}]{4,}(?![\p{L}])/gu, w => {
      if (Brain.has(w)) return w;
      const s = Brain.suggest(w, 1)[0];
      return s && Math.abs(s.length - w.length) <= 1 ? s : w;
    });
  }
  const cleanup = t => t.replace(/^\s*\**dziob\s?si\**\s*:\s*/i, '').replace(/\s*(je[sś]li|gdyby[sś]?)\s+(masz|b[eę]dziesz mia[lł]).{0,40}pyta\S*.*$/is, '').trim();

  async function think(text, typing) {
    if (window.DziobCode && DziobCode.wants(text)) {
      const c = DziobCode.make(text);
      return `${c.title} 👇\n\`\`\`${c.lang}\n${c.code}\n\`\`\``;
    }
    const llm = window.DziobLLM;
    lastSrc = llm && llm.ready && store.get('useAI', true) ? 'ai' : 'basic';
    const lower = text.toLowerCase().trim();
    if (llm && llm.ready && store.get('useAI', true) && !TOOL.test(lower) && !/^[\d\s+\-*/().,^%x×:]+$/.test(lower)) {
      // pewne odpowiedzi o DziobSi (np. „lubisz mnie?” → „Tak, bardzo cię lubię!”) – zawsze takie same
      const sure = window.Talk && Talk.answer(text, Brain, true);
      if (sure) { await new Promise(r => setTimeout(r, 250)); return sure; }
      const body = typing.querySelector('.body');
      try {
        const out = await llm.chat(withHints(text), t => {
          body.innerHTML = md(cleanup(t)); box.scrollTop = box.scrollHeight;
        });
        const clean = spellfix(cleanup(out));
        if (clean) return clean;
      } catch (e) { console.error(e); }
    }
    await new Promise(r => setTimeout(r, 300));
    return Brain.reply(text);
  }

  async function send(text) {
    text = (text || '').trim();
    if (!text || busy) return;
    busy = true; $('#btnSend').disabled = true;
    const hello = box.querySelector('.hello'); if (hello) hello.remove();

    // Wulgaryzmy: DziobSi nie odpowiada
    if (Brain.isVulgar(text)) {
      history.push({ role: 'user', text, blocked: true });
      store.set('history', history);
      addBubble('user', text, true);
      busy = false; $('#btnSend').disabled = false;
      return;
    }

    history.push({ role: 'user', text });
    addBubble('user', text);
    const typing = addBubble('model', '');
    typing.querySelector('.body').innerHTML = '<span class="typing"><i></i><i></i><i></i></span>';

    let reply;
    try {
      if (!Brain.ready) await brainReady;
      reply = await think(text, typing);
    } catch (e) {
      reply = 'Ups: ' + e.message;
    }
    typing.remove();
    history.push({ role: 'model', text: reply, src: lastSrc });
    if (history.length > 200) history = history.slice(-200);
    store.set('history', history);
    addBubble('model', reply, false, lastSrc);
    busy = false; $('#btnSend').disabled = false;
  }

  box.addEventListener('click', e => {
    const c = e.target.closest('[data-copy]'), o = e.target.closest('[data-open]');
    if (c) copyText(codeStore[c.dataset.copy], c);
    if (o) { setEditor(codeStore[o.dataset.open], 'index.html'); showTab('code'); setView('run'); }
  });

  const input = $('#input');
  $('#chatForm').addEventListener('submit', e => { e.preventDefault(); const v = input.value; input.value = ''; autosize(); send(v); });
  input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); $('#chatForm').requestSubmit(); } });
  function autosize() { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 140) + 'px'; }
  input.addEventListener('input', autosize);

  function clearChat() { history = []; store.set('history', history); if (window.DziobLLM) DziobLLM.reset(); render(); }
  $('#btnNew').addEventListener('click', clearChat);

  /* ---------- Code ---------- */
  const editor = $('#editor'), preview = $('#preview');
  function setEditor(code, title) {
    editor.value = code; $('#codeTitle').textContent = title || 'index.html';
    store.set('code', code); store.set('codeTitle', $('#codeTitle').textContent);
  }
  function setView(v) {
    document.querySelectorAll('#codeView button').forEach(b => b.classList.toggle('active', b.dataset.v === v));
    editor.hidden = v !== 'edit'; preview.hidden = v !== 'run';
    if (v === 'run') preview.srcdoc = editor.value;
  }
  document.querySelectorAll('#codeView button').forEach(b => b.addEventListener('click', () => setView(b.dataset.v)));
  $('#btnRun').addEventListener('click', () => setView('run'));
  $('#btnCopy').addEventListener('click', e => copyText(editor.value, e.currentTarget));
  $('#btnReset').addEventListener('click', () => { setEditor('', 'index.html'); setView('edit'); });
  editor.addEventListener('input', () => store.set('code', editor.value));
  editor.addEventListener('keydown', e => {
    if (e.key === 'Tab') { e.preventDefault(); const s = editor.selectionStart; editor.setRangeText('  ', s, editor.selectionEnd, 'end'); }
  });

  function build(desc) {
    const c = DziobCode.make(desc);
    const name = c.lang === 'html' ? (c.id || 'index') + '.html' : c.lang === 'python' ? 'main.py' : 'main.js';
    setEditor(c.code, name);
    setView(c.lang === 'html' ? 'run' : 'edit');
  }
  $('#codeAsk').addEventListener('submit', e => { e.preventDefault(); const v = $('#codePrompt').value.trim(); if (v) build(v); $('#codePrompt').blur(); });
  DziobCode.templates.forEach(t => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'chip glass'; b.textContent = t.title;
    b.onclick = () => { setEditor(t.code, t.id + '.html'); setView('run'); };
    $('#codeChips').appendChild(b);
  });
  setEditor(store.get('code', DziobCode.templates[0].code), store.get('codeTitle', 'index.html'));
  setView('edit');

  /* ---------- słownik ---------- */
  let dictMode = 'prefix';
  const modeBtns = document.querySelectorAll('[data-mode]');
  function setMode(m) { dictMode = m; modeBtns.forEach(b => b.classList.toggle('active', b.dataset.mode === m)); doSearch(); }
  modeBtns.forEach(b => b.addEventListener('click', () => setMode(b.dataset.mode)));

  function showWords(list, info) {
    $('#dictInfo').textContent = info;
    $('#dictResults').innerHTML = list.map(w => { const r = Brain.rankOf(w); return `<li><span>${esc(w)}</span><small>${r ? '#' + fmt(r) : 'rzadkie'}</small></li>`; }).join('');
  }
  let searchTimer;
  function doSearch() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      if (!Brain.ready) return;
      const q = $('#dictSearch').value;
      if (!q.trim()) { showWords([], ''); return; }
      if (q.trim().length < 2 && dictMode !== 'prefix') { showWords([], 'Wpisz co najmniej 2 litery.'); return; }
      const r = Brain.search(q, dictMode, 200);
      showWords(r.items, `${fmt(r.total)} wyników${r.total > r.items.length ? ' · pokazuję ' + r.items.length : ''}`);
    }, 200);
  }
  $('#dictSearch').addEventListener('input', doSearch);
  $('#btnRandom').addEventListener('click', () => { if (Brain.ready) showWords(Brain.random(20), 'Losowe słowa'); });

  /* ---------- ustawienia ---------- */
  const themeMeta = document.querySelector('meta[name=theme-color]');
  function applyTheme(t) {
    if (t === 'auto') delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = t;
    document.querySelectorAll('#themeSeg button').forEach(b => b.classList.toggle('active', b.dataset.t === t));
    const dark = t === 'dark' || (t === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);
    themeMeta.content = dark ? '#262624' : '#f5f4ed';
  }
  document.querySelectorAll('#themeSeg button').forEach(b => b.addEventListener('click', () => { store.set('theme', b.dataset.t); applyTheme(b.dataset.t); }));
  applyTheme(store.get('theme', 'auto'));

  const glass = $('#glassToggle');
  glass.checked = store.get('glass', true);
  glass.addEventListener('change', () => { store.set('glass', glass.checked); document.documentElement.classList.toggle('no-glass', !glass.checked); });

  $('#btnClear').addEventListener('click', () => { if (confirm('Wyczyścić rozmowę?')) { clearChat(); showTab('chat'); } });

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    // service worker dodaje nagłówki izolacji – po jego starcie przeładuj raz, by AI liczyło na wielu wątkach
    const reloadOnce = () => {
      if (self.crossOriginIsolated) return;
      let tried = false; try { tried = sessionStorage.getItem('dziobsi:coi') === '1'; } catch (e) { /* brak */ }
      if (tried || (window.DziobLLM && ['downloading', 'loading'].includes(DziobLLM.info().state))) return;
      try { sessionStorage.setItem('dziobsi:coi', '1'); } catch (e) { /* brak */ }
      location.reload();
    };
    navigator.serviceWorker.addEventListener('controllerchange', reloadOnce);
    navigator.serviceWorker.register('sw.js').then(() => { if (navigator.serviceWorker.controller) reloadOnce(); }).catch(() => {});
  }

  /* ---------- mózg AI (model w telefonie) ---------- */
  const aiViews = [];
  function updateAI(info) {
    const pct = Math.round((info.progress || 0) * 100);
    const label = {
      none: 'nie pobrany', installed: 'wczytywanie…', downloading: `pobieranie ${pct}%`,
      loading: 'uruchamianie…', ready: 'gotowy ✓', error: /fetch|network/i.test(info.error) ? 'brak połączenia z internetem' : 'błąd: ' + info.error,
    }[info.state];
    $('#aiState').textContent = label;
    const btn = $('#btnAI');
    btn.hidden = !['none', 'error'].includes(info.state) && info.state !== 'ready';
    btn.textContent = info.state === 'ready' ? 'Usuń model' : info.state === 'error' ? 'Spróbuj ponownie' : 'Pobierz (~1 GB)';
    btn.classList.toggle('primary', info.state !== 'ready');
    btn.classList.toggle('danger', info.state === 'ready');
    const busyNow = ['downloading', 'loading', 'installed'].includes(info.state);
    for (const bar of document.querySelectorAll('.bar')) {
      bar.hidden = !busyNow;
      bar.classList.toggle('indeterminate', info.state !== 'downloading');
      bar.querySelector('i').style.width = (info.state === 'downloading' ? pct : 100) + '%';
    }
    // stały baner w czacie, dopóki pełny Mózg AI nie jest pobrany
    const ban = $('#aiBanner');
    let closed = false; try { closed = sessionStorage.getItem('dziobsi:banner') === '0'; } catch (e) { /* brak */ }
    const showBan = ['none', 'error', 'downloading'].includes(info.state) && !(closed && info.state !== 'downloading');
    ban.hidden = !showBan;
    document.body.classList.toggle('has-banner', showBan);
    $('#aiBannerBtn').hidden = info.state === 'downloading';
    $('#aiBannerBtn').textContent = info.state === 'error' ? 'Ponów' : 'Pobierz';
    $('#aiBannerText').innerHTML = info.state === 'downloading'
      ? `<b>Pobieranie Mózgu AI… ${pct}%</b><small>Nie zamykaj aplikacji (najlepiej Wi‑Fi).</small>`
      : info.state === 'error'
        ? `<b>Nie udało się pobrać Mózgu AI</b><small>${/fetch|network/i.test(info.error) ? 'Sprawdź internet i spróbuj ponownie.' : esc(info.error)}</small>`
        : `<b>🧠 Włącz pełny Mózg AI</b><small>Teraz działa tryb podstawowy. Mózg AI rozumie każde pytanie (~1 GB, raz).</small>`;
    for (const v of aiViews) {
      if (v.kind !== 'offer' || !v.el.isConnected) continue;
      v.el.hidden = info.state === 'ready' || info.state === 'installed' || info.state === 'loading';
      const b = v.el.querySelector('button');
      b.hidden = busyNow;
      b.textContent = info.state === 'error' ? 'Spróbuj ponownie' : 'Pobierz mózg AI';
      const sp = v.el.querySelector('span');
      if (info.state === 'error') sp.textContent = /fetch|network/i.test(info.error) ? 'Nie udało się pobrać – sprawdź internet (najlepiej Wi‑Fi) i spróbuj ponownie.' : 'Nie udało się: ' + info.error;
      else if (info.state === 'downloading') sp.textContent = `Pobieranie… ${pct}% – nie zamykaj aplikacji.`;
    }
    if (Brain.ready) status.textContent = info.state === 'downloading' ? `⬇ ${pct}%` : info.state === 'ready' ? 'AI ✓' : '';
  }
  $('#aiBannerBtn').addEventListener('click', () => window.DziobLLM && DziobLLM.load());
  $('#aiBannerClose').addEventListener('click', () => {
    try { sessionStorage.setItem('dziobsi:banner', '0'); } catch (e) { /* brak */ }
    $('#aiBanner').hidden = true; document.body.classList.remove('has-banner');
  });
  $('#appVersion').textContent = APP_VERSION;
  $('#btnAI').addEventListener('click', () => {
    const llm = window.DziobLLM; if (!llm) return;
    if (llm.ready) { if (confirm('Usunąć mózg AI z telefonu? (zwolni ~1 GB)')) llm.remove(); }
    else llm.load();
  });
  const aiToggle = $('#aiToggle');
  aiToggle.checked = store.get('useAI', true);
  aiToggle.addEventListener('change', () => store.set('useAI', aiToggle.checked));
  function hookAI() { if (window.DziobLLM && !hookAI.done) { hookAI.done = true; DziobLLM.onChange(updateAI); } }
  window.addEventListener('dziobllm', hookAI);

  /* ---------- start ---------- */
  const status = $('#status');
  render();
  hookAI();
  const brainReady = Brain.load(n => { status.textContent = Math.round(n / 5000) + '%'; })
    .then(n => {
      status.textContent = window.DziobLLM && DziobLLM.ready ? 'AI ✓' : '';
      doSearch();
      // potem wielki słownik 5 000 000 słów (spakowany, ~22 MB)
      return Brain.loadBig(p => { status.textContent = '📚 ' + Math.round(p * 100) + '%'; })
        .then(total => {
          $('#dictCount').textContent = fmt(total);
          status.textContent = window.DziobLLM && DziobLLM.ready ? 'AI ✓' : '';
          doSearch();
        })
        .catch(e => { console.error(e); status.textContent = ''; });
    })
    .catch(e => { status.textContent = '⚠️'; console.error(e); });
})();
