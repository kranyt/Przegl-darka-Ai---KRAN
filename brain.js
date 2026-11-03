/* DziobSi – własny mózg ze słownikiem 5 000 000 słów
   (500 000 najczęstszych z rankingiem w pamięci + pełne 5 mln w spakowanym BigDict). */
(function () {
  'use strict';

  const ALPHABET = 'aąbcćdeęfghijklłmnńoóprsśtuwyzźżqvx';
  const VOWELS = /[aąeęioóuy]+/g;

  /* ---------- filtr wulgaryzmów ---------- */
  const BAD_CONTAINS = ['kurw', 'chuj', 'pierdol', 'pierdal', 'pierdziel', 'pizd', 'skurw', 'fuck', 'shit', 'jeb', 'nigger', 'nigga', 'motherf', 'cocksuck'];
  const BAD_STARTS = ['huj', 'cipa', 'cipy', 'cipk', 'cipą', 'cipie', 'cipo', 'ciota', 'cioto', 'cioty', 'dziwk', 'fiut', 'cwel', 'kutas', 'bitch', 'asshole', 'cunt', 'faggot', 'whore', 'dickhead', 'wanker'];
  const BAD_EXACT = new Set(['dupa', 'dupy', 'dupie', 'dupę', 'dupe', 'dupą', 'dupek', 'dupka', 'dupku', 'dupki', 'gówno', 'gowno', 'gówna', 'gowna',
    'gównie', 'gównem', 'sraj', 'srać', 'sracz', 'ruchać', 'ruchał', 'ruchała', 'ruchaj', 'ruchanie',
    'dick', 'dicks', 'cock', 'cocks', 'pussy', 'slut', 'sluts', 'twat', 'wank', 'tits', 'fag', 'fags']);
  const LEET = { '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '@': 'a', '$': 's', '!': 'i' };
  const FOLD = { 'ą': 'a', 'ć': 'c', 'ę': 'e', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z' };

  function badWord(w) {
    return BAD_EXACT.has(w) || BAD_STARTS.some(s => w.startsWith(s)) || BAD_CONTAINS.some(s => w.includes(s));
  }
  function isVulgar(text) {
    const tokens = String(text).toLowerCase().split(/\s+/);
    for (let t of tokens) {
      t = t.replace(/[0-9@$!]/g, c => LEET[c] || c).replace(/[^a-ząćęłńóśźż]/g, '');   // k.u.r.w.a, k*u*r*w*a, 4 -> a
      if (!t) continue;
      const squeezed = t.replace(/(.)\1+/g, '$1');                                       // kuuurwaaa -> kurwa
      const folded = squeezed.replace(/[ąćęńóśźż]/g, c => FOLD[c]);
      const foldedU = squeezed.replace(/ó/g, 'u').replace(/[ąćęńśźż]/g, c => FOLD[c]); // kórwa, chój
      if ([t, squeezed, folded, foldedU].some(badWord)) return true;
    }
    return false;
  }

  /* ---------- analiza słowa ---------- */
  const PREFIXES = ['współ', 'przeciw', 'anty', 'super', 'mega', 'ultra', 'przed', 'prze', 'przy', 'naj', 'nad', 'pod', 'roz', 'bez', 'nie',
    'wy', 'za', 'na', 'po', 'od', 'do', 'ob', 'pra', 'wz', 'ws', 'u', 's', 'z', 'w', 'o'];
  const SUFFIX_RULES = [
    [/ość$/, 'rzeczownik (cecha)'],
    [/(anie|enie|cie)$/, 'rzeczownik (czynność)'],
    [/(acja|izm|logia|grafia|ista|istka|ometr|ika)$/, 'rzeczownik'],
    [/(ować|ywać|iwać|ać|eć|ić|yć|ąć|ść|źć)$/, 'czasownik'],
    [/(łem|łam|łeś|łaś|liśmy|łyśmy|liście|li|ły|ło|ła|ł)$/, 'czasownik (czas przeszły)'],
    [/(iejszy|ejszy|szy)$/, 'przymiotnik (stopień wyższy)'],
    [/(owy|owa|owe|ny|na|ne|ski|ska|skie|cki|cka|ckie|czny|czna|liwy|liwa|isty|asty)$/, 'przymiotnik'],
    [/(eczek|eczka|uszek|uszka|eńko|ątko|iczek|yczek|ek|ka|ko)$/, 'rzeczownik (zdrobnienie)'],
    [/(arz|acz|nik|ciel|ec|ak)$/, 'rzeczownik (osoba lub rzecz)'],
    [/(nie|wie)$/, 'przysłówek'],
  ];

  const Brain = {
    words: [],          // słowa wg częstości (indeks 0 = najczęstsze)
    rank: new Map(),    // słowo -> pozycja (1..500000)
    sorted: null,       // słowa alfabetycznie (do szybkiego szukania rdzeni)
    ready: false,
    isVulgar,

    async load(onProgress) {
      const res = await fetch('data/slowa.txt');
      if (!res.ok) throw new Error('Nie udało się wczytać słownika (' + res.status + ')');
      const text = await res.text();
      const words = text.split('\n').filter(Boolean);
      const rank = new Map();
      const CHUNK = 50000;
      for (let i = 0; i < words.length; i++) {
        rank.set(words[i], i + 1);
        if (i % CHUNK === 0) {
          onProgress && onProgress(i);
          await new Promise(r => setTimeout(r, 0)); // nie blokuj UI
        }
      }
      this.words = words;
      this.rank = rank;
      this.ready = true;
      onProgress && onProgress(words.length);
      return words.length;
    },

    big() { const b = (typeof window !== 'undefined' ? window : globalThis).BigDict; return b && b.ready ? b : null; },
    /* liczba wszystkich znanych słów (5 000 000 po wczytaniu wielkiego słownika) */
    total() { const b = this.big(); return b ? b.count : this.words.length; },
    _has(w) { if (this.rank.has(w)) return true; const b = this.big(); return !!(b && b.has(w)); },
    has(w) { return this._has(norm(w)); },
    async loadBig(onProgress) {
      const b = (typeof window !== 'undefined' ? window : globalThis).BigDict;
      if (!b) return 0;
      return b.load('data/slownik.bin', onProgress);
    },
    rankOf(w) { return this.rank.get(norm(w)) || 0; },

    /* wyniki z 5 mln: najpierw popularne (wg rankingu), potem rzadkie alfabetycznie */
    search(q, mode, limit = 100) {
      const r = this._search(q, mode, this.big() ? 5000 : limit);
      if (!this.big()) return r;
      const R = w => this.rank.get(w) || 1e9;
      r.items = r.items.map((w, i) => [w, R(w), i]).sort((a, b) => a[1] - b[1] || a[2] - b[2]).slice(0, limit).map(x => x[0]);
      return r;
    },

    _search(q, mode, limit = 100) {
      q = norm(q);
      if (!q) return { total: 0, items: [] };
      const big = this.big();
      if (q.includes('*') || q.includes('?')) {
        const re = new RegExp('^' + q.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*').replace(/\?/g, '.') + '$');
        if (big) return big.pattern(re, q.split(/[*?]/)[0], limit);
        return this._filter(w => re.test(w), limit);
      }
      if (big) return mode === 'suffix' || mode === 'contains' ? big.scan(mode, q, limit) : big.prefix(q, limit);
      if (mode === 'suffix') return this._filter(w => w.endsWith(q), limit);
      if (mode === 'contains') return this._filter(w => w.includes(q), limit);
      return this._filter(w => w.startsWith(q), limit);
    },

    _filter(fn, limit) {
      const items = [];
      let total = 0;
      for (const w of this.words) {
        if (fn(w)) { total++; if (items.length < limit) items.push(w); }
      }
      return { total, items };
    },

    /* słowa zaczynające się od prefiksu – przez wyszukiwanie binarne */
    withPrefix(p, limit = 6) {
      if (!this.sorted) this.sorted = this.words.slice().sort();
      const a = this.sorted;
      let lo = 0, hi = a.length;
      while (lo < hi) { const mid = (lo + hi) >> 1; if (a[mid] < p) lo = mid + 1; else hi = mid; }
      const out = [];
      for (let i = lo; i < a.length && a[i].startsWith(p); i++) out.push(a[i]);
      return out.sort((x, y) => this.rank.get(x) - this.rank.get(y)).slice(0, limit);
    },

    random(n = 1) {
      const out = [];
      for (let i = 0; i < n; i++) out.push(this.words[Math.floor(Math.random() * this.words.length)]);
      return out;
    },

    rhymes(w, limit = 15) {
      w = norm(w);
      const end = w.slice(-Math.min(3, Math.max(2, w.length - 1)));
      return this._filter(x => x !== w && x.endsWith(end) && x.length > 2, limit).items;
    },

    /* „cos” → „coś”, „gadac” → „gadać”: wariant z polskimi znakami, jeśli jest dużo popularniejszy */
    fixDiacritics(w) {
      const lw = w.toLowerCase();
      if (/[ąćęłńóśźż]/.test(lw) || lw.length < 2 || lw.length > 20) return w;
      const MAP = { a: 'aą', c: 'cć', e: 'eę', l: 'lł', n: 'nń', o: 'oó', s: 'sś', z: 'zźż' };
      let vars = [''];
      for (const ch of lw) {
        const opts = MAP[ch] || ch;
        const next = [];
        for (const v of vars) for (const o of opts) next.push(v + o);
        vars = next;
        if (vars.length > 4096) return w;
      }
      const own = this.rank.get(lw) || 1e9;
      let best = null, br = own;
      for (const v of vars) { const r = this.rank.get(v); if (r && r < br) { best = v; br = r; } }
      if (!best || best === lw || br * 5 > own) return w;
      return w[0] === w[0].toUpperCase() && w[0] !== w[0].toLowerCase() ? best[0].toUpperCase() + best.slice(1) : best;
    },
    fixText(t) { return this.ready ? t.replace(/\p{L}+/gu, x => this.fixDiacritics(x)) : t; },

    suggest(w, limit = 5) {
      w = norm(w);
      const found = new Set();
      for (let i = 0; i <= w.length; i++) {
        const a = w.slice(0, i), b = w.slice(i);
        if (b) found.add(a + b.slice(1));                                   // usunięcie
        if (b.length > 1) found.add(a + b[1] + b[0] + b.slice(2));          // zamiana
        for (const c of ALPHABET) {
          if (b) found.add(a + c + b.slice(1));                             // podmiana
          found.add(a + c + b);                                             // wstawienie
        }
      }
      found.delete(w);
      const R = x => this.rank.get(x) || 1e9;
      return [...found].filter(x => this._has(x))
        .sort((x, y) => R(x) - R(y))
        .slice(0, limit);
    },

    /* Krótka analiza słowa – zawsze coś powie, nigdy „nie znam” */
    analyze(word, detailed) {
      const w = norm(word);
      const r = this.rankOf(w);
      const known = !!r || this._has(w);
      const rule = SUFFIX_RULES.find(([re]) => re.test(w));
      let pos = rule ? rule[1] : '';
      let parts = '';

      for (const p of PREFIXES) {
        if (w.startsWith(p) && w.length - p.length >= 3 && this.rank.has(w.slice(p.length))) {
          parts = p === 'nie' ? `zaprzeczenie „${w.slice(3)}”` : `${p}- + ${w.slice(p.length)}`;
          break;
        }
      }
      if (!parts && !known) {
        for (let i = 3; i <= w.length - 3 && !parts; i++) {
          const a = w.slice(0, i), b = w.slice(i);
          const ra = this.rank.get(a), rb = this.rank.get(b);
          if (ra && rb && ra < 150000 && rb < 150000) parts = `${a} + ${b}`;
          else if (/[oi]/.test(w[i]) && i + 4 <= w.length && this.rank.has(w.slice(i + 1)) && this.rank.get(w.slice(i + 1)) < 150000 && this.withPrefix(a, 1).length) {
            parts = `${a}-${w[i]}-${w.slice(i + 1)}`; pos = 'słowo złożone';
          }
        }
      }

      let family = [];
      for (let len = w.length - 1; len >= 3 && len >= Math.min(4, w.length - 1); len--) {
        const f = this.withPrefix(w.slice(0, len), 5).filter(x => x !== w);
        if (f.length >= 2) { family = f.slice(0, 3); break; }
      }

      const typo = !known && !parts ? this.suggest(w, 1)[0] : null;
      let out = `**${w}**`;
      if (typo) out += ` – pewnie chodzi o **${typo}**.`;
      else if (pos || parts) out += ` – ${pos || 'słowo'}${parts ? ': ' + parts : ''}.`;
      else if (/[qvx]|th|sh|ee|oo|ph/.test(w)) out += ' – wyraz obcy albo nazwa własna.';
      else out += ` – ${known ? 'słowo' : 'rzadkie słowo, może nazwa własna'}.`;
      if (family.length && !typo) out += ` Podobne: ${family.join(', ')}.`;
      if (detailed) {
        const syl = (w.match(VOWELS) || []).length;
        out += ` (${pl(w.length, 'litera', 'litery', 'liter')}, ${pl(syl, 'sylaba', 'sylaby', 'sylab')}${r ? ', #' + r.toLocaleString('pl-PL') : known ? ', rzadkie – ze słownika 5 mln' : ''})`;
      }
      return out;
    },

    /* ---------- odpowiedzi (krótkie) ---------- */
    reply(msg) {
      const raw = msg.trim();
      const t = norm(raw).replace(/[?!.]+$/g, '');
      const fmt = n => n.toLocaleString('pl-PL');
      let m;

      if (/^(cze[sś][cć]|hej|siema|elo|witaj|dzie[nń] dobry|dobry wiecz[oó]r|hejka|yo)(?=$|[\s,!])/.test(t))
        return pick(['Cześć! 🐦 W czym pomóc?', 'Hej! Co dziś robimy?', 'Siema! 🐦']);

      if (/^(pomoc|help|co umiesz|co potrafisz)/.test(t)) return HELP;

      if (/(kim|czym) jeste[sś]|jak si[eę] nazywasz|twoje imi[eę]/.test(t))
        return 'Jestem **DziobSi** – Dziob Inteligence, Twój ptasi asystent AI 🐦';

      if (/ile (znasz )?s[lł][oó]w|ile masz s[lł][oó]w/.test(t)) return `${fmt(this.total())} słów! 📚`;
      if (/jak si[eę] masz|co u ciebie|co tam/.test(t)) return 'Świetnie, dzięki! A u Ciebie?';
      if (/co robisz/.test(t)) return 'Czekam na Twoje pytanie 🐦';
      if (/(dzi[eę]kuj[eę]|dzi[eę]ki|thx)/.test(t)) return 'Proszę! 🐦';
      if (/^(ok|okej|spoko|dobrze|super|fajnie|git|xd|haha)\b/.test(t)) return pick(['👍', 'Spoko! 🐦', 'Super!']);
      if (/(opowiedz )?(dowcip|żart|zart|kawa[lł])/.test(t)) return pick(JOKES);

      if (/(kt[oó]ra (jest )?godzina|jaka godzina)/.test(t))
        return `${new Date().toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' })} 🕐`;
      if (/(jaki (jest )?dzi[sś] dzie[nń]|jaka (jest )?data|kt[oó]rego (jest )?dzi[sś])/.test(t))
        return new Date().toLocaleDateString('pl-PL', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) + ' 📅';

      if (window.Talk) { const d = window.Talk.define(t); if (d) return d; }

      if ((m = t.match(/rym(?:y|u)? (?:do|na) (\S+)/))) {
        const r = this.rhymes(m[1], 8);
        return r.length ? `Rymy do „${m[1]}”: ${r.join(', ')} 🎵` : 'Trudny rym! Spróbuj innego słowa.';
      }

      if ((m = t.match(/(?:policz|oblicz|ile to|ile jest)\s*(.+)/)) || /^[\d\s+\-*/().,^%x×:]+$/.test(t)) {
        const expr = (m ? m[1] : t).replace(/×|x/g, '*').replace(/:/g, '/').replace(/,/g, '.').replace(/\^/g, '**');
        if (/^[\d\s+\-*/().%]+$/.test(expr) && /\d/.test(expr)) {
          try {
            const v = Function('"use strict";return (' + expr + ')')();
            if (typeof v === 'number' && isFinite(v)) return `To jest **${fmt(Math.round(v * 1e10) / 1e10)}** 🧮`;
          } catch (e) { /* nie wyrażenie */ }
        }
      }

      if (window.Talk) { const ans = window.Talk.answer(raw, this); if (ans) return ans; }

      // zwykła rozmowa (bez mózgu AI): reaguj na temat wiadomości
      for (const [re, answers] of TOPICS) if (re.test(t)) return pick(answers);
      const aiMissing = !(window.DziobLLM && window.DziobLLM.ready);
      if (/\?\s*$/.test(raw) || /^(jak|co|kto|gdzie|kiedy|dlaczego|czemu|ile|czy|jaki|jaka|jakie|kt[oó]r)/.test(t)) {
        return aiMissing
          ? 'Na takie pytania odpowiada pełny Mózg AI 🧠 Pobierz go raz w Ustawieniach (~1 GB) – potem zrozumiem każde pytanie, także bez internetu.'
          : pick(['Hmm, nie jestem tego pewien 🤔 Możesz zapytać inaczej?', 'Dobre pytanie! Opowiedz mi więcej, to spróbuję pomóc 🐦']);
      }
      return pick(['Opowiedz mi więcej! 🐦', 'Ciekawe! I co było dalej?', 'Rozumiem. A jak się z tym czujesz?', 'Brzmi ciekawie! Mów dalej 🐦']);
    },
  };

  function norm(s) { return String(s || '').trim().toLowerCase().replace(/^["„”'«»]+|["„”'«»,.;:!?]+$/g, ''); }

  // odmiana: pl(3,'słowo','słowa','słów') -> '3 słowa'
  function pl(n, one, few, many) {
    const d = n % 10, dd = n % 100;
    const f = n === 1 ? one : (d >= 2 && d <= 4 && (dd < 12 || dd > 14) ? few : many);
    return n.toLocaleString('pl-PL') + ' ' + f;
  }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }

  const JOKES = [
    'Dlaczego DziobSi nigdy się nie gubi? Bo zawsze ma dziób na właściwym kierunku! 🐦',
    'Co mówi ptak, który zna 5 000 000 słów? Nic – bo nie może się zdecydować, którego użyć! 😄',
    'Jaki jest ulubiony przedmiot DziobSi w szkole? Ćwir-matematyka! 🧮',
    'Dlaczego wróbel nie korzysta z internetu? Bo woli ćwierkać na żywo! 🐦',
  ];

  const HELP = `**W czym pomogę:**
• po prostu ze mną pogadaj 🐦
• zadaj dowolne pytanie (pełny Mózg AI – Ustawienia)
• rymy do …
• policz 2+2
• napisz kod … / zrób grę
• opowiedz dowcip`;

  // tematy rozmowy dla trybu podstawowego
  const TOPICS = [
    [/szko[lł]|lekcj|nauczyciel|klas[aeięy]|sprawdzian|kartk[oó]wk/, ['Szkoła potrafi zmęczyć! 📚 Jaki przedmiot lubisz najbardziej?', 'Jak tam w szkole? Coś ciekawego się dziś wydarzyło?']],
    [/\bgr[aęy]\b|gram |gra[lł]|minecraft|fortnite|roblox|konsol|playstation|xbox/, ['Lubisz grać? 🎮 W co grasz najczęściej?', 'Gry są super! U mnie w zakładce Code jest „Złap ptaka” 🐦']],
    [/\bpies|psa\b|psem|piesek|kot\b|kota\b|kotek|zwierz/, ['Uwielbiam zwierzaki! 🐾 Jak się nazywa?', 'Zwierzęta są najlepsze! Masz jakieś w domu?']],
    [/jedzeni|jem\b|zjad|obiad|[sś]niadani|kolacj|pizz|głodn|glodn/, ['Mniam! 😋 Co najbardziej lubisz jeść?', 'Smacznego! 🍽️ Sam gotowałeś?']],
    [/pogod|deszcz|śnieg|snieg|słońc|slonc|zimno|ciepło|cieplo/, ['Pogoda potrafi zaskoczyć! ☀️🌧️ Lubisz taką aurę?', 'Mam nadzieję, że jest przyjemnie! Wolisz słońce czy deszcz?']],
    [/film|serial|netflix|bajk|kino/, ['Oglądanie to świetny relaks! 🎬 Co ostatnio widziałeś?', 'Lubię dobre historie! Jaki jest Twój ulubiony film?']],
    [/muzyk|piosenk|śpiew|spiew|słucham|slucham|rap|rock/, ['Muzyka poprawia humor! 🎶 Czego słuchasz?', 'Ja lubię ćwierkanie o poranku 🐦 A Ty jaką muzykę?']],
    [/pi[lł]k|sport|trening|biega|rower|basen|p[lł]ywa/, ['Ruch to zdrowie! 💪 Często trenujesz?', 'Super! Jaki sport lubisz najbardziej?']],
    [/mam[aey]\b|tat[aey]\b|brat|siostr|rodzin|babci|dziadk/, ['Rodzina jest ważna 💛 Opowiesz mi coś o nich?', 'Fajnie! Spędzacie razem czas?']],
    [/prac[aęy]|szef|biur/, ['Praca bywa męcząca – pamiętaj o przerwach ☕', 'Jak Ci dziś minęła praca?']],
  ];

  window.Brain = Brain;
})();
