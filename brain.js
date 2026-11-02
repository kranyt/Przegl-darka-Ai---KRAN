/* DziobSi – własny mózg (bez wspomagania z zewnątrz) ze słownikiem 500 000 słów. */
(function () {
  'use strict';

  const ALPHABET = 'aąbcćdeęfghijklłmnńoóprsśtuwyzźżqvx';
  const VOWELS = /[aąeęioóuy]+/g;

  /* ---------- filtr wulgaryzmów ---------- */
  const BAD_CONTAINS = ['kurw', 'chuj', 'pierdol', 'pierdal', 'pierdziel', 'pizd', 'skurw', 'fuck', 'shit', 'jeb'];
  const BAD_STARTS = ['huj', 'cipa', 'cipy', 'cipk', 'cipą', 'cipie', 'cipo', 'ciota', 'cioto', 'cioty', 'dziwk', 'fiut', 'cwel', 'kutas', 'bitch'];
  const BAD_EXACT = new Set(['dupa', 'dupy', 'dupie', 'dupę', 'dupe', 'dupą', 'dupek', 'dupka', 'dupku', 'dupki', 'gówno', 'gowno', 'gówna', 'gowna',
    'gównie', 'gównem', 'sraj', 'srać', 'sracz', 'ruchać', 'ruchał', 'ruchała', 'ruchaj', 'ruchanie']);
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
    [/ość$/, 'rzeczownik oznaczający cechę (jak „radość”, „szybkość”)'],
    [/(anie|enie|cie)$/, 'rzeczownik odczasownikowy – nazwa czynności (jak „pisanie”, „myślenie”)'],
    [/(acja|izm|logia|grafia|ista|istka|ometr|ika)$/, 'rzeczownik, najpewniej wyraz zapożyczony (jak „informacja”, „biologia”)'],
    [/(ować|ywać|iwać|ać|eć|ić|yć|ąć|ść|źć|c)$/, 'czasownik w bezokoliczniku (jak „dziobać”, „robić”)'],
    [/(łem|łam|łeś|łaś|liśmy|łyśmy|liście|li|ły|ło|ła|ł)$/, 'czasownik w czasie przeszłym (jak „dziobał”, „zrobiła”)'],
    [/(iejszy|ejszy|szy)$/, 'przymiotnik w stopniu wyższym (jak „ładniejszy”)'],
    [/(owy|owa|owe|ny|na|ne|ski|ska|skie|cki|cka|ckie|czny|czna|liwy|liwa|isty|ista|asty)$/, 'przymiotnik (jak „dziobowy”, „ładny”)'],
    [/(eczek|eczka|uszek|uszka|eńko|ątko|iczek|yczek|ek|ka|ko)$/, 'rzeczownik, możliwe zdrobnienie (jak „dziobek”, „kotek”)'],
    [/(arz|acz|nik|ciel|ec|ak)$/, 'rzeczownik, możliwa nazwa osoby lub wykonawcy (jak „piekarz”, „nauczyciel”)'],
    [/(nie|wie|o)$/, 'możliwy przysłówek (jak „ładnie”, „szybko”)'],
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

    has(w) { return this.rank.has(norm(w)); },
    rankOf(w) { return this.rank.get(norm(w)) || 0; },

    search(q, mode, limit = 100) {
      q = norm(q);
      if (!q) return { total: 0, items: [] };
      if (q.includes('*') || q.includes('?')) {
        const re = new RegExp('^' + q.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*').replace(/\?/g, '.') + '$');
        return this._filter(w => re.test(w), limit);
      }
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
      return [...found].filter(x => this.rank.has(x))
        .sort((x, y) => this.rank.get(x) - this.rank.get(y))
        .slice(0, limit);
    },

    /* Analiza słowa – szczególnie takiego, którego DziobSi nie zna */
    analyze(word) {
      const w = norm(word);
      const fmt = n => n.toLocaleString('pl-PL');
      const lines = [];
      const r = this.rankOf(w);

      lines.push(r ? `🔎 **Analiza słowa „${w}”** – znam je ✅ (miejsce #${fmt(r)} z ${fmt(this.words.length)})`
                   : `🔎 **Analiza nieznanego słowa „${w}”** – nie ma go w moich ${fmt(this.words.length)} słowach, więc je rozbieram na części:`);

      // budowa
      const syl = (w.match(VOWELS) || []).length;
      const vow = (w.match(/[aąeęioóuy]/g) || []).length;
      lines.push(`• Budowa: ${pl(w.length, 'litera', 'litery', 'liter')}, ${pl(vow, 'samogłoska', 'samogłoski', 'samogłosek')}, ${pl(w.length - vow, 'spółgłoska', 'spółgłoski', 'spółgłosek')}, ok. ${pl(syl, 'sylaba', 'sylaby', 'sylab')}.`);

      // pochodzenie
      if (/[ąćęłńóśźż]/.test(w)) lines.push('• Pochodzenie: ma polskie znaki – to raczej polskie słowo.');
      else if (/[qvx]|th|sh|ee|oo|ph|ck$|w$/.test(w)) lines.push('• Pochodzenie: litery typu q/v/x/th/sh sugerują wyraz obcy (np. angielski) albo nazwę własną.');

      // część mowy
      const rule = SUFFIX_RULES.find(([re]) => re.test(w));
      if (rule) lines.push(`• Część mowy (zgaduję po końcówce „${w.match(rule[0])[0]}”): ${rule[1]}.`);

      if (/^naj.+szy$/.test(w)) lines.push('• Przedrostek „naj-” + „-szy” = stopień najwyższy przymiotnika.');

      // przedrostek + znane słowo
      for (const p of PREFIXES) {
        if (w.startsWith(p) && w.length - p.length >= 3 && this.rank.has(w.slice(p.length))) {
          const rest = w.slice(p.length);
          lines.push(p === 'nie'
            ? `• Rozkład: „nie” + „${rest}” – zaprzeczenie słowa „${rest}”.`
            : `• Rozkład: przedrostek „${p}-” + znane słowo „${rest}”.`);
          break;
        }
      }

      // słowo złożone z dwóch znanych
      if (!r) {
        for (let i = 3; i <= w.length - 3; i++) {
          const a = w.slice(0, i), b = w.slice(i);
          const ra = this.rank.get(a), rb = this.rank.get(b);
          if (ra && rb && ra < 150000 && rb < 150000) { lines.push(`• Złożenie: może to „${a}” + „${b}”.`); break; }
          // łącznik -o-/-i- jak w „słowotwórstwo”
          if (/[oi]/.test(w[i]) && i + 4 <= w.length) {
            const a2 = w.slice(0, i), b2 = w.slice(i + 1);
            if (this.rank.has(b2) && this.withPrefix(a2, 1).length && this.rank.get(b2) < 150000 && a2.length >= 3) {
              lines.push(`• Złożenie: może to rdzeń „${a2}-” + łącznik „-${w[i]}-” + „${b2}”.`); break;
            }
          }
        }
      }

      // rdzeń i rodzina wyrazów
      let family = [], stem = '';
      for (let len = w.length - 1; len >= Math.min(4, w.length - 1) && len >= 3; len--) {
        const f = this.withPrefix(w.slice(0, len), 7).filter(x => x !== w);
        if (f.length >= 2) { family = f.slice(0, 6); stem = w.slice(0, len); break; }
      }
      if (family.length) lines.push(`• Rdzeń „${stem}-” – podobne słowa, które znam: ${family.join(', ')}.`);

      // literówka?
      if (!r) {
        const s = this.suggest(w, 4);
        if (s.length) lines.push(`• Może to literówka? Pasuje: ${s.map(x => '**' + x + '**').join(', ')}.`);
      }

      // werdykt
      if (!r) {
        let v;
        if (lines.some(l => l.includes('literówka'))) v = 'najpewniej literówka albo rzadka odmiana';
        else if (family.length || lines.some(l => l.includes('Rozkład') || l.includes('Złożenie'))) v = 'wygląda na prawdziwe, rzadkie albo nowe słowo utworzone z polskich części';
        else if (lines.some(l => l.includes('obcy'))) v = 'wygląda na wyraz obcy albo nazwę własną';
        else v = 'nie przypomina niczego, co znam – może to nazwa własna, skrót albo zmyślone słowo';
        lines.push(`🐦 **Werdykt:** ${v}.`);
      }
      return lines.join('\n');
    },

    /* ---------- odpowiedzi ---------- */
    reply(msg) {
      const raw = msg.trim();
      const t = norm(raw).replace(/[?!.]+$/g, '');
      const fmt = n => n.toLocaleString('pl-PL');
      const total = fmt(this.words.length);
      let m;

      if (/^(cze[sś][cć]|hej|siema|elo|witaj|dzie[nń] dobry|dobry wiecz[oó]r|hejka|yo)(?=$|[\s,!])/.test(t))
        return `Cześć! 🐦 Jestem **DziobSi** – Dziob Inteligence. Znam **${total}** słów. Zapytaj mnie o coś albo napisz „pomoc”.`;

      if (/^(pomoc|help|co umiesz|co potrafisz)/.test(t)) return HELP(total);

      if (/(kim|czym) jeste[sś]|jak si[eę] nazywasz|twoje imi[eę]/.test(t))
        return `Jestem **DziobSi** (Dziob Inteligence) – samodzielna sztuczna inteligencja na telefon z mózgiem na **${total}** słów. Działam bez internetu i bez pomocy innych AI. Sprawdzam i analizuję słowa, szukam rymów, poprawiam literówki i liczę.`;

      if (/ile (znasz )?s[lł][oó]w|ile masz s[lł][oó]w/.test(t))
        return `Znam dokładnie **${total}** słów! 📚`;

      if (/jak si[eę] masz|co u ciebie|co tam/.test(t))
        return 'Dziobię się świetnie, dzięki! 🐦 A u Ciebie?';

      if (/co robisz/.test(t)) return 'Przeglądam swoje 500 000 słów i czekam na Twoje pytanie 🐦';

      if (/(dzi[eę]kuj[eę]|dzi[eę]ki|thx)/.test(t)) return 'Proszę bardzo! 🐦';

      if (/(opowiedz )?(dowcip|żart|zart|kawa[lł])/.test(t)) return pick(JOKES);

      if (/(kt[oó]ra (jest )?godzina|jaka godzina)/.test(t))
        return `Jest **${new Date().toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' })}**.`;
      if (/(jaki (jest )?dzi[sś] dzie[nń]|jaka (jest )?data|kt[oó]rego (jest )?dzi[sś])/.test(t))
        return `Dziś jest **${new Date().toLocaleDateString('pl-PL', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}**.`;

      if ((m = t.match(/(?:losowe|losuj|wylosuj)(?: s[lł]owo| s[lł]owa)?(?: (\d+))?/))) {
        const n = Math.min(parseInt(m[1] || '1', 10) || 1, 50);
        const ws = this.random(n);
        return n === 1 ? `Losowe słowo: **${ws[0]}** (miejsce #${fmt(this.rankOf(ws[0]))} na ${total}).`
                       : `Losowe słowa: ${ws.map(w => '**' + w + '**').join(', ')}`;
      }

      if ((m = t.match(/(?:przeanalizuj|analizuj|analiza|rozbierz|co (?:to )?(?:jest|znaczy|oznacza)) (?:s[lł]owo |s[lł]owa )?(\S+)$/)))
        return this.analyze(m[1]);

      if ((m = t.match(/rym(?:y|u)? (?:do|na) (\S+)/))) {
        const r = this.rhymes(m[1]);
        return r.length ? `Rymy do **${m[1]}**: ${r.join(', ')}` : `Nie znalazłem rymów do „${m[1]}”.`;
      }

      if ((m = t.match(/s[lł]owa (?:na|zaczynaj[aą]ce si[eę] (?:na|od)) (\S+)/))) {
        const r = this.search(m[1], 'prefix', 20);
        return r.total ? `Znam **${fmt(r.total)}** słów na „${m[1]}”, np.: ${r.items.join(', ')}` : `Nie znam słów na „${m[1]}”.`;
      }

      if ((m = t.match(/s[lł]owa (?:ko[nń]cz[aą]ce si[eę] na|z ko[nń]c[oó]wk[aą]) (\S+)/))) {
        const r = this.search(m[1], 'suffix', 20);
        return r.total ? `Znam **${fmt(r.total)}** słów kończących się na „${m[1]}”, np.: ${r.items.join(', ')}` : `Nie znam takich słów.`;
      }

      if ((m = t.match(/(?:czy (\S+) (?:jest|to) (?:s[lł]owem|s[lł]owo|poprawne)|sprawd[zź] (?:s[lł]owo )?(\S+)|znasz (?:s[lł]owo )?(\S+))/))) {
        const w = m[1] || m[2] || m[3];
        const r = this.rankOf(w);
        if (r) return `✅ Tak! „**${w}**” jest w moim słowniku – miejsce **#${fmt(r)}** z ${total} pod względem popularności.`;
        return `❌ Nie znam słowa „${w}”, ale je przeanalizowałem:\n\n` + this.analyze(w);
      }

      if ((m = t.match(/(?:policz|oblicz|ile to|ile jest)\s*(.+)/)) || /^[\d\s+\-*/().,^%x×:]+$/.test(t)) {
        const expr = (m ? m[1] : t).replace(/×|x/g, '*').replace(/:/g, '/').replace(/,/g, '.').replace(/\^/g, '**');
        if (/^[\d\s+\-*/().%]+$/.test(expr) && /\d/.test(expr)) {
          try {
            const v = Function('"use strict";return (' + expr + ')')();
            if (typeof v === 'number' && isFinite(v)) return `🧮 ${expr.replace(/\*\*/g, '^')} = **${fmt(Math.round(v * 1e10) / 1e10)}**`;
          } catch (e) { /* nie wyrażenie */ }
        }
      }

      // Zwykła wiadomość: rozumiem słowa, a nieznane – analizuję
      const tokens = raw.toLowerCase().match(/[a-ząćęłńóśźżqvx]+/g) || [];
      if (!tokens.length) return 'Hmm, nie rozumiem. 🐦 Napisz „pomoc”, żeby zobaczyć, co umiem.';
      const unknown = [...new Set(tokens.filter(w => !this.rank.has(w)))];

      if (tokens.length === 1) {
        return unknown.length ? this.analyze(tokens[0])
          : `„**${tokens[0]}**” – znam to słowo (miejsce #${fmt(this.rankOf(tokens[0]))}). Napisz „przeanalizuj ${tokens[0]}”, a rozbiorę je na części.`;
      }

      if (!unknown.length) {
        const rare = tokens.slice().sort((a, b) => this.rank.get(b) - this.rank.get(a))[0];
        return `Rozumiem wszystkie słowa Twojej wiadomości (${pl(tokens.length, 'słowo', 'słowa', 'słów')}) ✅\nNajrzadsze z nich to „**${rare}**” (miejsce #${fmt(this.rank.get(rare))} z ${total}).\n\nNapisz „pomoc”, żeby zobaczyć, w czym mogę pomóc. 🐦`;
      }

      let out = `Twoja wiadomość ma ${pl(tokens.length, 'słowo', 'słowa', 'słów')}, z czego znam ${tokens.length - unknown.length}. Nie znam: ${unknown.slice(0, 5).map(w => '„' + w + '”').join(', ')} – analizuję:`;
      for (const w of unknown.slice(0, 3)) out += '\n\n' + this.analyze(w);
      if (unknown.length > 3) out += `\n\n…i jeszcze ${unknown.length - 3} – napisz „przeanalizuj <słowo>”.`;
      return out;
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
    'Co mówi ptak, który zna 500 000 słów? Nic – bo nie może się zdecydować, którego użyć! 😄',
    'Jaki jest ulubiony przedmiot DziobSi w szkole? Ćwir-matematyka! 🧮',
    'Dlaczego wróbel nie korzysta z internetu? Bo woli ćwierkać na żywo! 🐦',
  ];

  function HELP(total) {
    return `Oto co umiem (słownik: **${total}** słów, działam w 100% sam, bez internetu):
• „sprawdź słowo dziób” – czy słowo istnieje
• „przeanalizuj dziobolot” – rozbiorę każde słowo, nawet nieznane (część mowy, rdzeń, przedrostek, złożenie, literówki)
• „rymy do kot” – rymy
• „słowa na prze” – słowa zaczynające się na…
• „słowa kończące się na ość”
• „losowe słowo” / „losuj 5”
• „policz 12*7+3” – kalkulator
• „która godzina”, „jaka data”, „opowiedz dowcip”
• dowolny tekst – nieznane słowa przeanalizuję automatycznie

🚫 Na wiadomości z wulgaryzmami nie odpowiadam.`;
  }

  window.Brain = Brain;
})();
