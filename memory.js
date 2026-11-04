/* DziobSi – pamięć: fakty o użytkowniku zapamiętywane z rozmowy (zostają po zamknięciu aplikacji). */
(function () {
  'use strict';

  const KEY = 'dziobsi:memory';
  const NAME_KEY = 'dziobsi:talk:name'; // wspólne z talk.js
  const MAX = 30;
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } };
  const save = f => { try { localStorage.setItem(KEY, JSON.stringify(f)); } catch (e) { /* brak */ } };
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const clean = s => s.replace(/[.!?…]+$/, '').replace(/\s+/g, ' ').trim();
  // „lubię moją mamę” -> „lubi swoją mamę”
  const third = s => s.replace(/\b(mój|moja|moje|mojego|mojej|moim|moją|moich)\b/g, m => ({ mój: 'swój', moja: 'swoja', moje: 'swoje', mojego: 'swojego', mojej: 'swojej', moim: 'swoim', moją: 'swoją', moich: 'swoich' }[m]));
  const NOT_NAMES = /^(tu|tutaj|tam|zmęczon\p{L}*|głodn\p{L}*|smutn\p{L}*|szczęśliw\p{L}*|chor\p{L}*|w|we|na|z|ze|od|do|po|nie|już|juz|teraz|sam|sama|tak|ok)$/iu;

  let facts = load(); // [{k:'name'|'like:...', t:'tekst', ts}]

  const Mem = {
    list() { return facts.map(f => f.t); },
    name() { const f = facts.find(x => x.k === 'name'); if (f) return f.v; try { return JSON.parse(localStorage.getItem(NAME_KEY)); } catch (e) { return null; } },

    set(k, t, v) {
      const i = facts.findIndex(f => f.k === k);
      const item = { k, t, v, ts: Date.now() };
      if (i >= 0) { if (facts[i].t === t) return false; facts[i] = item; } else facts.push(item);
      if (facts.length > MAX) facts = facts.slice(-MAX);
      save(facts);
      if (k === 'name') { try { localStorage.setItem(NAME_KEY, JSON.stringify(v)); } catch (e) { /* brak */ } }
      return true;
    },
    remove(i) { facts.splice(i, 1); save(facts); },
    clear() { facts = []; save(facts); try { localStorage.removeItem(NAME_KEY); } catch (e) { /* brak */ } },

    /* Wyciąga fakty z wiadomości. prevBot = poprzednia odpowiedź DziobSi (np. pytanie o imię). Zwraca listę nowych faktów. */
    learn(text, prevBot) {
      const added = [];
      const add = (k, t, v) => { if (this.set(k, t, v)) added.push(t); };
      const raw = text.trim();
      const low = raw.toLowerCase();
      let m;

      // imię
      if ((m = raw.match(/(?:mam na imi[eę]|nazywam si[eę]|mów mi|mow mi|jestem)\s+([A-ZŁŚŻŹĆŃÓ]\p{L}{1,20})\b/u)) ||
          (m = low.match(/(?:mam na imi[eę]|nazywam si[eę]|mów mi|mow mi)\s+(\p{L}{2,20})/u))) {
        if (!NOT_NAMES.test(m[1])) add('name', `Ma na imię ${cap(m[1])}`, cap(m[1]));
      } else if (prevBot && /(jak (masz na imi[eę]|si[eę] nazywasz)|twoje imi[eę]|imi[eę]\?)/i.test(prevBot) &&
                 (m = raw.match(/^(\p{L}{2,20})[.!]?$/u)) && !NOT_NAMES.test(m[1])) {
        add('name', `Ma na imię ${cap(m[1])}`, cap(m[1]));
      }
      // wiek, miejsce
      if ((m = raw.match(/mam (\d{1,3}) (?:lat|lata|rok)/i)) && +m[1] > 0 && +m[1] <= 120) add('age', `Ma ${m[1]} lat`, m[1]);
      if ((m = raw.match(/mieszkam (?:w|we|na) ([\p{L} -]{2,30}?)(?:[.,!?]|$| i | a )/iu))) add('city', `Mieszka w ${cap(clean(m[1]))}`, m[1]);
      if ((m = low.match(/chodz[eę] do (\d+\.? ?klasy|szko[lł]y [\p{L} ]{2,25}|przedszkola|liceum|technikum)/u))) add('school', `Chodzi do ${clean(m[1])}`, m[1]);
      // upodobania
      if ((m = raw.match(/(?:^|[\s,])nie lubi[eę] ([^.,!?]{2,40})/iu))) add('dislike:' + clean(m[1]).toLowerCase(), `Nie lubi: ${third(clean(m[1]))}`);
      else if ((m = raw.match(/(?:^|[\s,])(?:bardzo |naprawd[eę] )?(lubi[eę]|kocham|uwielbiam) ([^.,!?]{2,40})/iu)) && !/^(ci[eę]|ciebie|was|dziobsi)(?![\p{L}])/iu.test(m[2])) {
        const v = m[1].toLowerCase();
        add('like:' + clean(m[2]).toLowerCase(), `${v.startsWith('lubi') ? 'Lubi' : v === 'kocham' ? 'Kocha' : 'Uwielbia'}: ${third(clean(m[2]))}`);
      }
      if ((m = raw.match(/(?:m[oó]j|moja|moje) ulubion\p{L}* (\p{L}+) to ([^.,!?]{2,30})/iu))) add('fav:' + m[1].toLowerCase(), `Ulubion${/a$/i.test(m[1]) ? 'a' : /e$/i.test(m[1]) ? 'e' : 'y'} ${m[1].toLowerCase()}: ${clean(m[2])}`);
      // zwierzęta i rodzina
      if ((m = raw.match(/mam (psa|kota|chomika|kr[oó]lika|rybki|papug[eę]|[zż][oó][lł]wia|śwink[eę] morsk[aą]|brata|siostr[eę]|dw[oó]ch braci|dwie siostry)(?:,?\s+(?:o imieniu|imieniem|kt[oó]r\p{L}+ (?:ma na imi[eę]|nazywa si[eę]))\s+(\p{L}+)|\s+([A-ZŁŚŻŹĆŃÓ]\p{L}+))?/iu))) {
        const who = m[1].toLowerCase(), nm = m[2] ? cap(m[2]) : m[3];
        add('has:' + who, nm ? (m[2] ? `Ma ${who} o imieniu ${nm}` : `Ma ${who}: ${nm}`) : `Ma ${who}`);
      }
      // jawna prośba
      if (!added.length && (m = raw.match(/^zapami[eę]taj(?:\s*[,:]?\s*(?:[zż]e|to))?[,:]?\s+(.{3,100})$/iu))) add('note:' + clean(m[1]).toLowerCase(), `Prosił(a), by zapamiętać: „${clean(m[1])}”`);
      return added;
    },

    /* tekst do instrukcji modelu */
    prompt() {
      if (!facts.length) return '';
      return 'Co pamiętasz o użytkowniku (używaj naturalnie, nie wyliczaj tego bez potrzeby): ' + facts.map(f => f.t).join('; ') + '.';
    },
  };

  window.DziobMemory = Mem;
})();
