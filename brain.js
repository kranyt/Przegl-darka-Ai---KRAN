/* DziobSi – wbudowany (offline) mózg ze słownikiem 500 000 słów. */
(function () {
  'use strict';

  const ALPHABET = 'aąbcćdeęfghijklłmnńoóprsśtuwyzźżqvx';

  const Brain = {
    words: [],          // słowa wg częstości (indeks 0 = najczęstsze)
    rank: new Map(),    // słowo -> pozycja (1..500000)
    ready: false,

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

    /* ---------- odpowiedzi offline ---------- */
    reply(msg) {
      const raw = msg.trim();
      const t = norm(raw).replace(/[?!.]+$/g, '');
      const fmt = n => n.toLocaleString('pl-PL');
      const total = fmt(this.words.length);

      if (/^(cze[sś][cć]|hej|siema|elo|witaj|dzie[nń] dobry|dobry wiecz[oó]r|hejka|yo)(?=$|[\s,!])/.test(t))
        return `Cześć! 🐦 Jestem **DziobSi** – Dziob Inteligence. Znam **${total}** słów. Zapytaj mnie o coś albo napisz „pomoc”.`;

      if (/^(pomoc|help|co umiesz|co potrafisz)/.test(t)) return HELP(total);

      if (/(kim|czym) jeste[sś]|jak si[eę] nazywasz|twoje imi[eę]/.test(t))
        return `Jestem **DziobSi** (Dziob Inteligence) – sztuczna inteligencja na telefon z mózgiem na **${total}** słów. Offline sprawdzam słowa, rymy, poprawiam literówki i liczę. Z kluczem Gemini (w Ustawieniach) odpowiadam na każde pytanie.`;

      if (/ile (znasz )?s[lł][oó]w|ile masz s[lł][oó]w/.test(t))
        return `Znam dokładnie **${total}** słów! 📚`;

      if (/jak si[eę] masz|co u ciebie|co tam/.test(t))
        return 'Dziobię się świetnie, dzięki! 🐦 A u Ciebie?';

      if (/(dzi[eę]kuj[eę]|dzi[eę]ki|thx)/.test(t)) return 'Proszę bardzo! 🐦';

      if (/(kt[oó]ra (jest )?godzina|jaka godzina)/.test(t))
        return `Jest **${new Date().toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' })}**.`;
      if (/(jaki (jest )?dzi[sś] dzie[nń]|jaka (jest )?data|kt[oó]rego (jest )?dzi[sś])/.test(t))
        return `Dziś jest **${new Date().toLocaleDateString('pl-PL', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}**.`;

      let m;
      if ((m = t.match(/(?:losowe|losuj|wylosuj)(?: s[lł]owo| s[lł]owa)?(?: (\d+))?/))) {
        const n = Math.min(parseInt(m[1] || '1', 10) || 1, 50);
        const ws = this.random(n);
        return n === 1 ? `Losowe słowo: **${ws[0]}** (miejsce #${fmt(this.rankOf(ws[0]))} na ${total}).`
                       : `Losowe słowa: ${ws.map(w => '**' + w + '**').join(', ')}`;
      }

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
        const s = this.suggest(w);
        return `❌ Nie znam słowa „${w}”.` + (s.length ? ` Może chodziło o: ${s.map(x => '**' + x + '**').join(', ')}?` : '');
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

      // Analiza tekstu: sprawdzenie pisowni każdego słowa
      const tokens = raw.toLowerCase().match(/[a-ząćęłńóśźż]+/g) || [];
      if (!tokens.length) return 'Hmm, nie rozumiem. 🐦 Napisz „pomoc”, żeby zobaczyć, co umiem.';
      const unknown = [...new Set(tokens.filter(w => !this.rank.has(w)))];
      let out = `Przeanalizowałem Twoją wiadomość: **${tokens.length}** słów, ${tokens.length - unknown.length} znam ze słownika.`;
      if (unknown.length) {
        out += '\n\nNieznane słowa:';
        for (const w of unknown.slice(0, 5)) {
          const s = this.suggest(w, 3);
          out += `\n• „${w}”` + (s.length ? ` → może: ${s.join(', ')}` : '');
        }
      } else {
        out += ' Pisownia wygląda dobrze ✅';
      }
      out += '\n\n💡 Żeby DziobSi odpowiadał na każde pytanie jak pełne AI, dodaj klucz Gemini w ⚙️ Ustawieniach.';
      return out;
    },
  };

  function norm(s) { return String(s || '').trim().toLowerCase().replace(/^["„”'«»]+|["„”'«»,.;:!?]+$/g, ''); }

  function HELP(total) {
    return `Oto co umiem bez internetu (słownik: **${total}** słów):
• „sprawdź słowo dziób” – czy słowo istnieje
• „rymy do kot” – rymy
• „słowa na prze” – słowa zaczynające się na…
• „słowa kończące się na ość”
• „losowe słowo” / „losuj 5”
• „policz 12*7+3” – kalkulator
• „która godzina”, „jaka data”
• dowolny tekst – sprawdzę pisownię i podpowiem poprawki

🌐 Z kluczem Gemini (⚙️ Ustawienia) odpowiadam na **wszystko**.`;
  }

  window.Brain = Brain;
})();
