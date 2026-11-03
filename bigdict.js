/* DziobSi – wielki słownik 5 000 000 słów (data/slownik.bin).
   Format: słowa posortowane bajtowo (UTF-8), kodowanie przedrostkowe w blokach po B słów.
   W pamięci zostaje spakowany (~22 MB) – sprawdzenie słowa to wyszukiwanie binarne + rozpakowanie jednego bloku. */
(function () {
  'use strict';

  const enc = new TextEncoder();
  const dec = new TextDecoder();

  const BigDict = {
    ready: false,
    count: 0,

    async load(url, onProgress) {
      const res = await fetch(url);
      if (!res.ok) throw new Error('Nie udało się wczytać słownika 5 mln (' + res.status + ')');
      let buf;
      const total = +res.headers.get('content-length') || 0;
      if (res.body && total && onProgress) {
        const out = new Uint8Array(total); let got = 0;
        const reader = res.body.getReader();
        for (;;) {
          const { done, value } = await reader.read();
          if (done) break;
          out.set(value, got); got += value.length; onProgress(got / total);
        }
        buf = out.buffer;
      } else {
        buf = await res.arrayBuffer();
      }
      this.init(buf);
      return this.count;
    },

    init(buf) {
      const h = new DataView(buf, 0, 20);
      const magic = String.fromCharCode(h.getUint8(0), h.getUint8(1), h.getUint8(2), h.getUint8(3));
      if (magic !== 'DZSL') throw new Error('Zły format słownika');
      this.count = h.getUint32(8, true);
      this.B = h.getUint32(12, true);
      this.nBlocks = h.getUint32(16, true);
      this.offs = new Uint32Array(buf, 20, this.nBlocks);
      this.data = new Uint8Array(buf, 20 + 4 * this.nBlocks);
      this.buf = new Uint8Array(256);
      this.ready = true;
    },

    /* porównanie bajtów: zapytanie q z pierwszym słowem bloku */
    _cmpHead(q, block) {
      const d = this.data, o = this.offs[block], len = d[o];
      const n = Math.min(len, q.length);
      for (let i = 0; i < n; i++) {
        const a = q[i], b = d[o + 1 + i];
        if (a !== b) return a - b;
      }
      return q.length - len;
    },

    /* ostatni blok, którego pierwsze słowo <= q */
    _block(q) {
      let lo = 0, hi = this.nBlocks - 1;
      while (lo < hi) {
        const mid = (lo + hi + 1) >> 1;
        if (this._cmpHead(q, mid) >= 0) lo = mid; else hi = mid - 1;
      }
      return lo;
    },

    /* przechodzi słowa od bloku `block`; fn(buf, len) zwraca false, by przerwać */
    _walk(block, fn) {
      const d = this.data, buf = this.buf, B = this.B;
      for (let b = block; b < this.nBlocks; b++) {
        let p = this.offs[b], len = 0;
        const end = b + 1 < this.nBlocks ? this.offs[b + 1] : d.length;
        for (let j = 0; j < B && p < end; j++) {
          if (j === 0) { len = d[p++]; buf.set(d.subarray(p, p + len), 0); p += len; }
          else { const k = d[p++], s = d[p++]; buf.set(d.subarray(p, p + s), k); p += s; len = k + s; }
          if (fn(buf, len) === false) return;
        }
      }
    },

    has(word) {
      if (!this.ready || !word) return false;
      const q = enc.encode(word);
      if (q.length > 255) return false;
      let found = false;
      const b = this._block(q);
      let left = this.B;
      this._walk(b, (buf, len) => {
        if (len === q.length) {
          let eq = true;
          for (let i = 0; i < len; i++) if (buf[i] !== q[i]) { eq = false; break; }
          if (eq) { found = true; return false; }
        }
        return --left > 0;
      });
      return found;
    },

    /* słowa zaczynające się od prefiksu (alfabetycznie) */
    prefix(p, limit = 200) {
      const items = []; let total = 0;
      if (!this.ready) return { total, items };
      const q = enc.encode(p);
      this._walk(this._block(q), (buf, len) => {
        let cmp = 0;
        for (let i = 0; i < q.length; i++) {
          if (i >= len) { cmp = -1; break; }
          if (buf[i] !== q[i]) { cmp = buf[i] - q[i]; break; }
        }
        if (cmp < 0) return true;          // jeszcze przed prefiksem
        if (cmp > 0) return false;         // już za prefiksem – koniec
        total++;
        if (items.length < limit) items.push(dec.decode(buf.subarray(0, len)));
        return true;
      });
      return { total, items };
    },

    /* pełny przegląd (końcówka / zawiera) – porównanie na bajtach, dekodowane tylko trafienia */
    scan(mode, s, limit = 200) {
      const items = []; let total = 0;
      if (!this.ready) return { total, items };
      const q = enc.encode(s), n = q.length;
      const match = mode === 'suffix'
        ? (buf, len) => { if (len < n) return false; for (let i = 0; i < n; i++) if (buf[len - n + i] !== q[i]) return false; return true; }
        : (buf, len) => {
          outer: for (let st = 0; st + n <= len; st++) {
            for (let i = 0; i < n; i++) if (buf[st + i] !== q[i]) continue outer;
            return true;
          }
          return false;
        };
      this._walk(0, (buf, len) => {
        if (match(buf, len)) { total++; if (items.length < limit) items.push(dec.decode(buf.subarray(0, len))); }
        return true;
      });
      return { total, items };
    },

    /* wzorzec z * i ? – przegląd zawężony stałym początkiem wzorca */
    pattern(re, literalPrefix, limit = 200) {
      const items = []; let total = 0;
      if (!this.ready) return { total, items };
      const q = enc.encode(literalPrefix);
      this._walk(literalPrefix ? this._block(q) : 0, (buf, len) => {
        if (literalPrefix) {
          for (let i = 0; i < q.length; i++) {
            if (i >= len || buf[i] < q[i]) return true;
            if (buf[i] > q[i]) return false;
          }
        }
        const w = dec.decode(buf.subarray(0, len));
        if (re.test(w)) { total++; if (items.length < limit) items.push(w); }
        return true;
      });
      return { total, items };
    },
  };

  (typeof window !== 'undefined' ? window : globalThis).BigDict = BigDict;
})();
