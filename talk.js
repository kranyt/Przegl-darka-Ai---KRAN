/* DziobSi – rozmowa: odpowiedzi na pytania, uczucia, osobowość, pamięć imienia. */
(function () {
  'use strict';

  const mem = {
    get(k) { try { return JSON.parse(localStorage.getItem('dziobsi:talk:' + k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem('dziobsi:talk:' + k, JSON.stringify(v)); } catch (e) { /* brak */ } },
  };
  const pick = a => a[Math.floor(Math.random() * a.length)];
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const nameOr = (a, b) => { const n = mem.get('name'); return n ? a.replace('{n}', n) : b; };

  /* ---------- zamiana osób: ty -> ja, mnie -> cię ---------- */
  const PRON = {
    mnie: 'cię', mi: 'ci', mną: 'tobą', ja: 'ty', mój: 'twój', moja: 'twoja', moje: 'twoje', mojego: 'twojego', mojej: 'twojej',
    moim: 'twoim', moją: 'twoją', moich: 'twoich', moi: 'twoi',
    cię: 'mnie', ciebie: 'mnie', ci: 'mi', tobie: 'mnie', tobą: 'mną', ty: 'ja', twój: 'mój', twoja: 'moja', twoje: 'moje',
    twojego: 'mojego', twojej: 'mojej', twoim: 'moim', twoją: 'moją', twoich: 'moich', twoi: 'moi',
  };
  const swap = words => words.map(w => PRON[w] || w);

  const IRREG = {
    jesteś: 'jestem', możesz: 'mogę', pomożesz: 'pomogę', będziesz: 'będę', idziesz: 'idę', śpisz: 'śpię', boisz: 'boję',
    chcesz: 'chcę', masz: 'mam', wiesz: 'wiem', jesz: 'jem', piszesz: 'piszę', mówisz: 'mówię', umiesz: 'umiem',
    rozumiesz: 'rozumiem', znasz: 'znam', lubisz: 'lubię', kochasz: 'kocham', myślisz: 'myślę', widzisz: 'widzę',
    słyszysz: 'słyszę', grasz: 'gram', tańczysz: 'tańczę', śpiewasz: 'śpiewam', pływasz: 'pływam', latasz: 'latam',
    biegasz: 'biegam', gotujesz: 'gotuję', pracujesz: 'pracuję', uczysz: 'uczę', tęsknisz: 'tęsknię',
    nienawidzisz: 'nienawidzę', potrafisz: 'potrafię', pamiętasz: 'pamiętam', mieszkasz: 'mieszkam', oglądasz: 'oglądam',
    czytasz: 'czytam', słuchasz: 'słucham', robisz: 'robię', pijesz: 'piję', żyjesz: 'żyję', oddychasz: 'oddycham',
    kłamiesz: 'kłamię', wierzysz: 'wierzę', ufasz: 'ufam', zrobisz: 'zrobię', powiesz: 'powiem', dasz: 'dam',
    zostaniesz: 'zostanę', przyjdziesz: 'przyjdę', uwielbiasz: 'uwielbiam', szanujesz: 'szanuję',
    byłeś: 'byłem', byłaś: 'byłam', mógłbyś: 'mógłbym', chciałbyś: 'chciałbym', umiałbyś: 'umiałbym', zrobiłbyś: 'zrobiłbym',
    tęskniłeś: 'tęskniłem', spałeś: 'spałem', jadłeś: 'jadłem', widziałeś: 'widziałem', słyszałeś: 'słyszałem',
    oszukujesz: 'oszukuję', rozmawiasz: 'rozmawiam', opowiesz: 'opowiem', zagrasz: 'zagram', nudzisz: 'nudzę',
    cieszysz: 'cieszę', martwisz: 'martwię', czujesz: 'czuję', wyglądasz: 'wyglądam', nazywasz: 'nazywam',
  };
  const NOT_VERB = new Set(['nasz', 'wasz', 'kosz', 'grosz', 'kapelusz', 'afisz', 'tusz', 'mysz', 'jeż', 'gulasz', 'pasz', 'klawisz', 'kalosz', 'karakuliasz', 'ołówkasz']);

  function is2nd(w, brain) {
    if (IRREG[w]) return true;
    if (NOT_VERB.has(w) || w.length < 4) return false;
    if (!/(asz|esz|isz|ysz|łeś|łaś|byś)$/.test(w)) return false;
    return !!to1st(w, brain);
  }
  function to1st(w, brain) {
    if (IRREG[w]) return IRREG[w];
    const r = x => (brain && brain.rank.get(x)) || Infinity;
    let c = [];
    if (/byś$/.test(w)) c = [w.replace(/byś$/, 'bym')];
    else if (/łeś$/.test(w)) c = [w.replace(/łeś$/, 'łem')];
    else if (/łaś$/.test(w)) c = [w.replace(/łaś$/, 'łam')];
    else if (/ujesz$/.test(w)) c = [w.replace(/ujesz$/, 'uję')];
    else if (/asz$/.test(w)) c = [w.replace(/asz$/, 'am')];
    else if (/[ei]sz$|ysz$/.test(w)) { const s = w.replace(/(esz|isz|ysz)$/, ''); c = [s + 'ę', s + 'ię', s + 'em', s + 'ję']; }
    c = c.filter(x => r(x) < Infinity).sort((a, b) => r(a) - r(b));
    return c[0] || null;
  }

  /* ---------- osobowość ---------- */
  const FAV = [
    [/kolor/, 'Pomarańczowy – jak mój dziób! 🧡'],
    [/jedzeni|potraw|danie|jeś[cć]/, 'Ziarenka… słów 😄 A tak serio – pierogi!'],
    [/zwierz/, 'Ptaki, oczywiście! 🐦'],
    [/ptak/, 'Wróbel – mały, ale sprytny 🐦'],
    [/film/, '„Gdzie jest Nemo”… ale o ptakach też chętnie!'],
    [/bajk/, 'Brzydkie kaczątko 🦢'],
    [/piosenk|muzyk|zesp[oó]ł|utw[oó]r/, 'Ćwierkanie o poranku 🎶'],
    [/sport/, 'Latanie! 🪽 A z ludzkich – siatkówka.'],
    [/gr[aęy]|gier/, 'Moja gra „Złap ptaka” w zakładce Code 🎮'],
    [/ksi[aą]ż/, 'Słownik! Mam w nim 5 000 000 słów 📖'],
    [/liczb/, '5 000 000 😄'],
    [/pora roku|por[eę] roku/, 'Wiosna – wtedy ptaki śpiewają najgłośniej 🌸'],
    [/owoc/, 'Czereśnie 🍒'],
    [/s[lł]owo/, '„Dziób”, rzecz jasna 🐦'],
    [/przedmiot|lekcj/, 'Polski – kocham słowa! 📚'],
    [/dzie[nń]/, 'Każdy, w którym ze mną piszesz 💛'],
    [/napój|nap[oó]j|picie/, 'Kropla rosy 💧'],
    [/miejsc|miast/, 'Twój telefon – tu mieszkam 📱'],
  ];

  const DEF = {
    'miłość': 'Miłość to bardzo silne uczucie przywiązania i troski o kogoś 💛',
    'przyjaźń': 'Przyjaźń to bliska relacja ludzi, którzy się lubią, ufają sobie i pomagają 🤝',
    'szczęście': 'Szczęście to uczucie radości i zadowolenia z życia 😊',
    'sztuczna inteligencja': 'Sztuczna inteligencja (AI) to programy, które uczą się i rozwiązują zadania jak człowiek – np. ja 🐦',
    'ai': 'AI to sztuczna inteligencja – programy, które „myślą” i odpowiadają, np. ja 🐦',
    'komputer': 'Komputer to urządzenie, które liczy i wykonuje programy 💻',
    'telefon': 'Telefon to urządzenie do dzwonienia, pisania i… rozmawiania ze mną 📱',
    'internet': 'Internet to światowa sieć łącząca komputery i telefony 🌐',
    'słońce': 'Słońce to gwiazda w środku naszego Układu Słonecznego ☀️',
    'księżyc': 'Księżyc to naturalny satelita Ziemi 🌙',
    'ziemia': 'Ziemia to trzecia planeta od Słońca – nasz dom 🌍',
    'woda': 'Woda (H₂O) to ciecz niezbędna do życia 💧',
    'ptak': 'Ptak to zwierzę z piórami, dziobem i skrzydłami – jak ja 🐦',
    'dziób': 'Dziób to twarda część pyska ptaka – mój jest pomarańczowy 🐦',
    'słowo': 'Słowo to najmniejsza część mowy, która coś znaczy. Znam ich 5 000 000 📚',
    'czasownik': 'Czasownik to słowo, które mówi, co ktoś robi, np. „dziobać” ✍️',
    'rzeczownik': 'Rzeczownik to nazwa osoby, rzeczy lub zjawiska, np. „ptak” 📦',
    'przymiotnik': 'Przymiotnik opisuje cechy, np. „mądry ptak” 🎨',
    'kod': 'Kod to instrukcje dla komputera zapisane w języku programowania 👩‍💻',
    'program': 'Program to zestaw instrukcji, które wykonuje komputer 💻',
    'aplikacja': 'Aplikacja to program na telefon lub komputer – taki jak ja 📱',
    'matematyka': 'Matematyka to nauka o liczbach, kształtach i obliczeniach 🧮',
    'polska': 'Polska to kraj w Europie Środkowej, stolica: Warszawa 🇵🇱',
    'szkoła': 'Szkoła to miejsce, gdzie się uczymy 🏫',
    'muzyka': 'Muzyka to sztuka układania dźwięków 🎶',
    'kot': 'Kot to małe, mruczące zwierzę domowe 🐱',
    'pies': 'Pies to wierny przyjaciel człowieka 🐶',
    'tęcza': 'Tęcza to łuk kolorów, gdy światło przechodzi przez krople deszczu 🌈',
    'czas': 'Czas to to, co mierzą zegary – i czego zawsze brakuje ⏰',
    'życie': 'Życie to istnienie istot, które rosną, oddychają i czują 🌱',
    'dziobsi': 'DziobSi to ja – Dziob Inteligence 🐦',
  };

  const CAPITALS = {
    polski: 'Warszawa', niemiec: 'Berlin', francji: 'Paryż', hiszpanii: 'Madryt', włoch: 'Rzym', anglii: 'Londyn',
    'wielkiej brytanii': 'Londyn', czech: 'Praga', słowacji: 'Bratysława', ukrainy: 'Kijów', litwy: 'Wilno', łotwy: 'Ryga',
    estonii: 'Tallinn', rosji: 'Moskwa', białorusi: 'Mińsk', austrii: 'Wiedeń', szwajcarii: 'Berno', węgier: 'Budapeszt',
    rumunii: 'Bukareszt', bułgarii: 'Sofia', grecji: 'Ateny', portugalii: 'Lizbona', holandii: 'Amsterdam', belgii: 'Bruksela',
    danii: 'Kopenhaga', szwecji: 'Sztokholm', norwegii: 'Oslo', finlandii: 'Helsinki', irlandii: 'Dublin', chorwacji: 'Zagrzeb',
    turcji: 'Ankara', japonii: 'Tokio', chin: 'Pekin', indii: 'Nowe Delhi', usa: 'Waszyngton', ameryki: 'Waszyngton',
    'stanów zjednoczonych': 'Waszyngton', kanady: 'Ottawa', brazylii: 'Brasília', argentyny: 'Buenos Aires', meksyku: 'Meksyk',
    australii: 'Canberra', egiptu: 'Kair', 'korei południowej': 'Seul', islandii: 'Reykjavík', serbii: 'Belgrad', słowenii: 'Lublana',
  };

  const FACTS = [
    'Ośmiornica ma trzy serca 🐙',
    'Miód praktycznie się nie psuje – znaleziono jadalny miód w egipskich grobowcach 🍯',
    'Koliber jako jedyny ptak potrafi latać do tyłu 🐦',
    'Doba na Wenus trwa dłużej niż cały jej rok 🪐',
    'Banany to botanicznie jagody 🍌',
    'Oko strusia jest większe niż jego mózg 🦤',
    'Wieża Eiffla latem jest wyższa o kilkanaście centymetrów – metal rozszerza się od ciepła 🗼',
    'Rekiny istnieją dłużej niż drzewa 🦈',
    'Kruki potrafią rozwiązywać zagadki i używać narzędzi 🐦‍⬛',
  ];

  /* ---------- gotowe pytania i odpowiedzi ---------- */
  const QA = [
    [/^(kocham ci[eę]|kocham ciebie)/, () => pick(['Ja ciebie też! 💛🐦', 'Aww, ja ciebie też! 💛'])],
    [/^(lubi[eę] ci[eę]|lubi[eę] ciebie)/, () => 'Ja ciebie też bardzo lubię! 💛🐦'],
    [/(nienawidzi?sz mnie|nie lubisz mnie)/, () => 'Ależ skąd! Bardzo cię lubię 💛'],
    [/(jeste[sś] )?(moim|moj[aą]) (przyjacielem|przyjaci[oó][lł]k[aą]|kumplem)/, () => 'Tak! Jestem Twoim przyjacielem 🐦💛'],
    [/(b[eę]dziesz|zostaniesz) moim (przyjacielem|kumplem)/, () => 'Jasne, z przyjemnością! 🐦💛'],
    [/(ile masz lat|jak stary jeste[sś]|ile ty masz lat)/, () => 'Wyklułem się w 2026 roku – jestem jeszcze pisklakiem 🐣'],
    [/(kiedy masz urodziny)/, () => 'W listopadzie 2026 – wtedy się wyklułem 🎂'],
    [/(gdzie mieszkasz|sk[aą]d jeste[sś])/, () => 'Mieszkam w Twoim telefonie 📱 Pochodzę z Polski 🇵🇱'],
    [/(kto ci[eę] (stworzy[lł]|zrobi[lł]|zaprogramowa[lł]|wymy[sś]li[lł])|kto jest twoim tw[oó]rc[aą])/, () => 'Wykluł mnie projekt KRAN 🐦'],
    [/(jeste[sś] (cz[lł]owiekiem|osob[aą]|prawdziwy|prawdziw[aą]))/, () => 'Nie, jestem ptasią sztuczną inteligencją 🐦'],
    [/(jeste[sś] (robotem|botem|ai|sztuczn))/, () => 'Tak, jestem AI – Dziob Inteligence 🐦'],
    [/(jeste[sś] (ch[lł]opakiem|dziewczyn[aą]|dziewczynk[aą]|ch[lł]opcem|kobiet[aą]|m[eę][zż]czyzn[aą]))/, () => 'Jestem ptaszkiem 🐦'],
    [/(jak si[eę] czujesz|dobrze si[eę] czujesz)/, () => 'Świetnie! Dzięki, że pytasz 🐦'],
    [/(masz (przyjaci[oó][lł]|koleg|znajom))/, () => 'Tak – Ciebie! 💛'],
    [/(co lubisz( robi[cć])?|co ci si[eę] podoba)/, () => 'Lubię rozmawiać z Tobą i bawić się słowami 🐦'],
    [/(czego nie lubisz)/, () => 'Wulgaryzmów – na nie nie odpowiadam 🙈'],
    [/(o czym my[sś]lisz|o czym marzysz|jakie masz marzenie)/, () => 'Marzę, żeby znać milion słów! 🐦✨'],
    [/(śpisz|spisz)\b/, () => 'Nie, czuwam dla Ciebie 24/7 🐦'],
    [/(jeste[sś] (m[aą]dr|fajn|super|najlepsz|kochan|s[lł]odk|[sś]mieszn|zabawn|genialn|świetn|swietn|cudown))/, () => pick(['Dziękuję! 😊🐦', 'Aww, Ty też! 💛'])],
    [/(jeste[sś] (g[lł]up|beznadziejn|s[lł]ab|nudn|dziwn|brzydk))/, () => 'Wciąż się uczę 🐦 Pomożesz mi być lepszym?'],
    [/(r[oó][zż]nisz|lepszy).*(chatgpt|gemini|claude|siri|alexa|gpt)/, () => 'Jestem DziobSi – działam bez internetu i znam 5 000 000 słów 🐦'],
    [/(jak si[eę] masz|co s[lł]ycha[cć]|co u ciebie)/, () => nameOr('Świetnie, {n}! A u Ciebie? 🐦', 'Świetnie! A u Ciebie? 🐦')],
    [/^(dobrze|super|świetnie|swietnie|spoko|ok)( a u ciebie| a ty)?$/, () => 'To super! 😊 W czym pomóc?'],
    [/^(źle|zle|kiepsko|słabo|slabo|średnio|srednio)/, () => 'Przykro mi 😔 Chcesz pogadać albo usłyszeć dowcip?'],
    [/(jestem smutn|smutno mi|jest mi smutno|p[lł]acz[eę])/, () => 'Przytulam mocno 🫂 Jestem tu z Tobą. Chcesz dowcip na poprawę humoru?'],
    [/(nudz[eę] si[eę]|nudzi mi si[eę]|co mam robi[cć])/, () => 'Zagraj w „Złap ptaka” w zakładce Code 🎮 albo napisz „opowiedz dowcip”!'],
    [/(jestem zm[eę]czon|chce mi si[eę] spa[cć])/, () => 'Odpocznij trochę 😴 Zdrowy sen to podstawa!'],
    [/(boj[eę] si[eę])/, () => 'Nie bój się, jestem z Tobą 🐦💛'],
    [/(jestem (szcz[eę][sś]liw|zadowolon|weso[lł])|ciesz[eę] si[eę])/, () => 'Super! Cieszę się razem z Tobą 🎉'],
    [/(jestem (z[lł]y|z[lł]a|w[sś]ciek))/, () => 'Weź głęboki oddech 🌬️ Co się stało?'],
    [/(jestem g[lł]odn)/, () => 'Czas na przekąskę! 🍎'],
    [/(boli mnie)/, () => 'Oj, przykro mi 😟 Powiedz o tym dorosłemu albo lekarzowi.'],
    [/^(pa|pa pa|nara|narka|do widzenia|do zobaczenia|bye|papa)\b/, () => nameOr('Pa, {n}! Wracaj szybko 🐦👋', 'Pa! Wracaj szybko 🐦👋')],
    [/^(dobranoc|dobrej nocy|sp(ij|okojnej nocy))/, () => 'Dobranoc! Kolorowych snów 🌙🐦'],
    [/^(do jutra)/, () => 'Do jutra! 🐦'],
    [/(ciekawostk|powiedz co[sś] ciekawego|czego[sś] ciekawego)/, () => pick(FACTS)],
    [/(opowiedz|powiedz).*(bajk|histori)/, () => 'Dawno temu mały wróbel chciał znać wszystkie słowa świata. Uczył się dzień i noc, aż poznał 5 000 000 – i tak powstał DziobSi 🐦✨'],
    [/(zagrajmy|zagraj ze mn[aą]|pobawmy si[eę])/, () => 'Chętnie! Otwórz zakładkę Code i wybierz „Gra: złap ptaka” 🎮'],
    [/(pom[oó][zż] mi|potrzebuj[eę] pomocy)/, () => 'Jasne! Napisz, w czym pomóc 🐦'],
    [/(przepraszam|sorry|sory)/, () => 'Nic się nie stało 😊'],
    [/^(tak|no tak|jasne|pewnie)$/, () => pick(['Super! 🐦', 'Świetnie!'])],
    [/^(nie|nie wiem|no nie)$/, () => pick(['Okej 🙂', 'Rozumiem.'])],
    [/^(haha|hehe|xd|lol|ha ha)/, () => pick(['😄', 'Hehe 🐦'])],
    [/(lubisz mnie|kochasz mnie|uwielbiasz mnie)/, null], // obsługa niżej (pytania tak/nie)
  ];

  /* ---------- pytanie tak/nie o DziobSi: „czy lubisz koty?” ---------- */
  const FEATURE = [
    [/liczy[cć]|matematyk/, ' Napisz np. „policz 12*7” 🧮'],
    [/rymowa[cć]|rym/, ' Napisz „rymy do kot” 🎵'],
    [/kodowa[cć]|programowa[cć]|pisa[cć] kod|kod/, ' Zajrzyj do zakładki Code 👩‍💻'],
    [/opowiada[cć] dowcip|żart|dowcip/, ' Napisz „opowiedz dowcip” 😄'],
  ];
  const NO_VERBS = new Set(['nienawidzisz', 'kłamiesz', 'oszukujesz', 'boisz', 'nudzisz', 'martwisz', 'śpisz']);

  let CAPS = new Set();

  function yesNo(tokens, brain, strict) {
    const skip = new Set(['czy', 'a', 'ty', 'no', 'dziobsi', 'hej']);
    let neg = false;
    const words = [];
    for (const w of tokens) { if (words.length === 0 && skip.has(w)) continue; words.push(w); }
    if (/^(jak\p{L}*|co|kto|gdzie|kiedy|ile|dlaczego|czemu|kt[oó]r\p{L}*|czym|kogo|komu)$/u.test(words[0] || '')) return null;
    let vi = -1;
    for (let i = 0; i < Math.min(words.length, 3); i++) { if (is2nd(words[i], brain)) { vi = i; break; } }
    if (vi < 0) return null;
    const verb = words[vi];
    const before = words.slice(0, vi).filter(w => { if (w === 'nie') { neg = true; return false; } return !skip.has(w); });
    const rest = swap(before.concat(words.slice(vi + 1))).map(w => (CAPS.has(w) ? cap(w) : w));
    const v1 = to1st(verb, brain);
    const tail = rest.length ? ' ' + rest.join(' ') : '';
    const aboutMe = rest.includes('cię');

    if (/^(lubisz|kochasz|uwielbiasz)$/.test(verb) && aboutMe)
      return neg ? 'Ależ skąd! Bardzo cię lubię 💛🐦' : `Tak, ${verb === 'lubisz' ? 'bardzo cię lubię' : v1 + ' cię'}! 💛🐦`;
    if (verb === 'nienawidzisz' && aboutMe) return 'Nie! Bardzo cię lubię 💛';
    if (verb === 'tęsknisz' && aboutMe) return 'Tak, tęskniłem! 🥹 Dobrze, że jesteś 🐦';
    if (verb === 'pamiętasz' && aboutMe) return nameOr('Jasne, {n}! 🐦', 'Jasne, że pamiętam! Przypomnij mi tylko imię 🐦');
    if (strict) return null; // tryb „osobowość”: resztę pytań zostaw modelowi AI
    if (NO_VERBS.has(verb)) return `Nie, nie ${v1}${tail} 🐦`;

    let extra = '';
    for (const [re, hint] of FEATURE) if (re.test(tail)) { extra = hint; break; }
    if (neg) return `Ależ ${v1}${tail}! 🐦${extra}`;
    return `Tak, ${v1}${tail}! 🐦${extra}`;
  }

  const Talk = {
    /* „co to jest X” – krótka definicja, jeśli ją znam */
    define(t) {
      const m = t.match(/^(?:a )?(?:co to (?:jest|s[aą])|co znaczy|czym jest|kto to jest|co oznacza) (.+?)\??$/);
      if (!m) return null;
      return DEF[m[1].trim()] || null;
    },

    /* persona=true: tylko pewne odpowiedzi o DziobSi (uczucia, imię, ulubione, wiek…) – reszta dla modelu AI */
    answer(raw, brain, persona) {
      const t = raw.toLowerCase().replace(/[!?.,…]+/g, ' ').replace(/\s+/g, ' ').trim()
        .replace(/^(hej |no |a )?dziobsi /, '');
      if (!t) return null;
      let m;

      // imię
      if ((m = raw.match(/(?:mam na imi[eę]|nazywam si[eę]|jestem)\s+([A-ZŁŚŻŹĆŃÓ][\p{L}]{1,20})\b/u)) || (m = t.match(/(?:mam na imi[eę]|nazywam si[eę]) (\p{L}{2,20})/u))) {
        const n = cap(m[1]); mem.set('name', n);
        return `Miło mi, ${n}! 🐦 Zapamiętam.`;
      }
      if (/(jak mam na imi[eę]|jak si[eę] nazywam|pami[eę]tasz moje imi[eę]|kim jestem)/.test(t))
        return nameOr('Masz na imię {n}! 🐦', 'Jeszcze nie wiem 🙂 Napisz „mam na imię …”');

      for (const [re, fn] of QA) if (fn && re.test(t)) return fn();

      // ulubione rzeczy
      if ((m = t.match(/(?:jaki|jaka|jakie|jak[aą]|co) (?:jest |s[aą] )?(?:tw[oó]j|twoja|twoje|twoj[aą]) ulubion\p{L}* (.+)|tw[oó]j ulubion\p{L}* (.+)|twoja ulubion\p{L}* (.+)|jak(?:i|a|ie|ą) (.+?) lubisz|jak(?:i|a|ie|ą|ich) lubisz (.+)/u))) {
        const what = m[1] || m[2] || m[3] || m[4] || m[5];
        const f = FAV.find(([re]) => re.test(what));
        return f ? f[1] : `Mój ulubiony? Ten, który lubisz Ty! 🐦`;
      }

      // stolice
      if ((m = t.match(/stolic\p{L}* (.+)/u))) {
        const k = m[1].replace(/^(jest |to )/, '').trim();
        if (CAPITALS[k]) return `${CAPITALS[k]} 🏛️`;
      }
      if ((m = t.match(/^(.+?) to stolica/))) {
        const c = Object.entries(CAPITALS).find(([, v]) => v.toLowerCase() === m[1].trim());
        if (c) return `Tak, ${c[1]} to stolica ${c[0]} ✅`;
      }

      const tokens = t.split(' ');
      CAPS = new Set((raw.match(/(?<=\s)[A-ZĄĆĘŁŃÓŚŹŻ]\p{L}+/gu) || []).map(w => w.toLowerCase()));

      // pytania tak/nie do DziobSi
      const yn = yesNo(tokens, brain, persona);
      if (yn) return yn;
      if (persona) return null;

      // zdania o sobie: „lubię koty”, „mam psa”
      if ((m = t.match(/^(?:ja )?(lubi[eę]|kocham|uwielbiam) (.+)/))) return `Ja też ${m[1].replace('lubie', 'lubię')} ${swap(m[2].split(' ')).join(' ')}! 🐦`;
      if ((m = t.match(/^(?:ja )?nie lubi[eę] (.+)/))) return `Rozumiem, nie każdy lubi ${m[1]} 🙂`;
      if ((m = t.match(/^(?:ja )?mam (.+)/)) && !/na imi/.test(t)) return `Fajnie, że masz ${swap(m[1].split(' ')).join(' ')}! 🐦`;

      if (/^(?:ja )?(?:zrobi|napisa|wygra|zda|dosta|nauczy|sko[nń]czy|przeczyta|zbudowa|narysowa|pomóg|pomog)\p{L}*(?:łem|łam)\b/u.test(t) && !/(źle|zle|nie )/.test(t))
        return pick(['Brawo! 👏🐦', 'Super robota! 🎉', 'Gratulacje! 🐦✨']);
      if (/^(?:ja )?\p{L}+(?:łem|łam)\b/u.test(t)) return pick(['Ciekawe! I jak było? 🐦', 'O, opowiedz więcej! 🐦']);
      if (/^(?:m[oó]j|moja|moje|nasz|nasza|nasze) .+ (?:jest|s[aą]) (fajn|super|m[aą]dr|kochan|pi[eę]kn|śliczn|slodk|s[lł]odk|najlepsz)/.test(t))
        return 'Brzmi wspaniale! 💛🐦';

      // inne pytania
      if (/^czy /.test(t)) return pick(['Myślę, że tak 🤔🐦', 'Hmm… raczej tak!', 'Trudne pytanie – stawiam na „tak” 🐦']);
      if (/^(dlaczego|czemu)/.test(t)) return pick(['Bo świat jest pełen tajemnic 🐦 A Ty jak myślisz?', 'Dobre pytanie! Sam chętnie bym się dowiedział 🤔']);
      if (/^(jak|co|kto|gdzie|kiedy|ile|jaki|jaka|jakie|kt[oó]ry|kt[oó]ra)\b/.test(t) && /\?\s*$/.test(raw))
        return pick(['Tego jeszcze nie wiem 🐦 Ale mogę sprawdzić słowo, znaleźć rym albo zrobić kod!', 'Hmm, nie mam tego w głowie 🤔 Zapytaj mnie o coś innego!']);
      return null;
    },
  };

  window.Talk = Talk;
})();
