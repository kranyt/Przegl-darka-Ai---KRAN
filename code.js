/* DziobSi Code – własne szablony i fragmenty kodu (bez internetu, bez innych AI). */
(function () {
  'use strict';

  const BASE_CSS = `body{font-family:system-ui,sans-serif;margin:0;min-height:100vh;display:grid;place-items:center;background:#f5f4ed;color:#141413}
button{font:inherit;border:0;border-radius:12px;padding:10px 16px;background:#c96442;color:#fff;cursor:pointer}
.card{background:#fff;border-radius:20px;padding:24px;box-shadow:0 8px 30px rgba(0,0,0,.08);min-width:260px;text-align:center}`;

  const page = (title, css, body, js) => `<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<style>
${BASE_CSS}
${css}
</style>
</head>
<body>
${body}
<script>
${js}
</script>
</body>
</html>`;

  const TEMPLATES = [
    {
      id: 'hello', title: 'Witaj, świecie', keys: /witaj|hello|pierwsz|prost/,
      code: page('Witaj', 'h1{font-family:Georgia,serif}', '<div class="card">\n  <h1>Witaj! 🐦</h1>\n  <p>Strona zrobiona w DziobSi Code.</p>\n  <button onclick="hej()">Kliknij</button>\n</div>',
        "function hej() {\n  alert('Cześć od DziobSi!');\n}"),
    },
    {
      id: 'licznik', title: 'Licznik kliknięć', keys: /licznik|klik|przycisk|zlicz/,
      code: page('Licznik', '#n{font-size:64px;margin:12px 0;font-weight:700}', '<div class="card">\n  <h2>Licznik</h2>\n  <div id="n">0</div>\n  <button id="minus">−</button>\n  <button id="plus">+</button>\n</div>',
        "let n = 0;\nconst out = document.getElementById('n');\ndocument.getElementById('plus').onclick = () => out.textContent = ++n;\ndocument.getElementById('minus').onclick = () => out.textContent = --n;"),
    },
    {
      id: 'todo', title: 'Lista zadań', keys: /zada[nń]|todo|to-do|lista|list[eę]/,
      code: page('Lista zadań', 'ul{list-style:none;padding:0;text-align:left}li{padding:8px;border-bottom:1px solid #eee;cursor:pointer}li.done{text-decoration:line-through;opacity:.5}input{padding:10px;border-radius:12px;border:1px solid #ddd;font:inherit}',
        '<div class="card">\n  <h2>Lista zadań</h2>\n  <input id="txt" placeholder="Nowe zadanie">\n  <button id="add">Dodaj</button>\n  <ul id="list"></ul>\n</div>',
        "const list = document.getElementById('list');\nconst txt = document.getElementById('txt');\ndocument.getElementById('add').onclick = () => {\n  if (!txt.value.trim()) return;\n  const li = document.createElement('li');\n  li.textContent = txt.value;\n  li.onclick = () => li.classList.toggle('done');\n  list.appendChild(li);\n  txt.value = '';\n};"),
    },
    {
      id: 'kalkulator', title: 'Kalkulator', keys: /kalkulator|licz(?!nik)|matemat|dodaw/,
      code: page('Kalkulator', '#ekran{font-size:28px;padding:12px;background:#f0eee6;border-radius:12px;text-align:right;margin-bottom:12px;min-height:40px}.k{display:grid;grid-template-columns:repeat(4,56px);gap:8px}.k button{padding:14px 0}',
        '<div class="card">\n  <div id="ekran"></div>\n  <div class="k" id="k"></div>\n</div>',
        "const ekran = document.getElementById('ekran');\nconst klawisze = '789/456*123-0.=+C'.split('');\nfor (const z of klawisze) {\n  const b = document.createElement('button');\n  b.textContent = z;\n  b.onclick = () => {\n    if (z === 'C') ekran.textContent = '';\n    else if (z === '=') {\n      try { ekran.textContent = Function('return ' + ekran.textContent)(); }\n      catch (e) { ekran.textContent = 'Błąd'; }\n    } else ekran.textContent += z;\n  };\n  document.getElementById('k').appendChild(b);\n}"),
    },
    {
      id: 'zegar', title: 'Zegar', keys: /zegar|godzin|czas|data/,
      code: page('Zegar', '#z{font-size:56px;font-weight:700;font-variant-numeric:tabular-nums}#d{opacity:.6}', '<div class="card">\n  <div id="z"></div>\n  <div id="d"></div>\n</div>',
        "function tik() {\n  const t = new Date();\n  document.getElementById('z').textContent = t.toLocaleTimeString('pl-PL');\n  document.getElementById('d').textContent = t.toLocaleDateString('pl-PL', { weekday: 'long', day: 'numeric', month: 'long' });\n}\ntik();\nsetInterval(tik, 1000);"),
    },
    {
      id: 'gra', title: 'Gra: złap ptaka', keys: /gr[aęy]|gier|zabaw/,
      code: page('Złap ptaka', '#pole{position:relative;width:300px;height:300px;background:#f0eee6;border-radius:16px;overflow:hidden}#ptak{position:absolute;font-size:40px;cursor:pointer;user-select:none;transition:.15s}',
        '<div class="card">\n  <h2>Złap ptaka! <span id="pkt">0</span> pkt</h2>\n  <p>Czas: <b id="czas">20</b> s</p>\n  <div id="pole"><div id="ptak">🐦</div></div>\n</div>',
        "let pkt = 0, czas = 20;\nconst ptak = document.getElementById('ptak');\nfunction skok() {\n  ptak.style.left = Math.random() * 250 + 'px';\n  ptak.style.top = Math.random() * 250 + 'px';\n}\nptak.onclick = () => {\n  if (czas <= 0) return;\n  document.getElementById('pkt').textContent = ++pkt;\n  skok();\n};\nconst timer = setInterval(() => {\n  document.getElementById('czas').textContent = --czas;\n  if (czas <= 0) { clearInterval(timer); alert('Koniec! Wynik: ' + pkt); }\n}, 1000);\nskok();"),
    },
    {
      id: 'strona', title: 'Strona wizytówka', keys: /stron|wizyt[oó]wk|portfolio|witryn/,
      code: page('Moja strona', 'body{display:block}header{padding:60px 24px;text-align:center;background:linear-gradient(135deg,#d97757,#c96442);color:#fff}h1{font-family:Georgia,serif;font-size:40px;margin:0}section{max-width:600px;margin:24px auto;padding:0 16px}',
        '<header>\n  <h1>Moja strona</h1>\n  <p>Zrobione w DziobSi Code 🐦</p>\n</header>\n<section>\n  <h2>O mnie</h2>\n  <p>Tu napisz coś o sobie.</p>\n  <button onclick="alert(\'Dzięki za wizytę!\')">Kontakt</button>\n</section>', ''),
    },
    {
      id: 'animacja', title: 'Animacja kolorów', keys: /animac|kolor|t[eę]cz|gradient|efekt/,
      code: page('Animacja', 'body{background:linear-gradient(-45deg,#d97757,#e8c4a0,#9b87f5,#6cc4b8);background-size:400% 400%;animation:fala 8s ease infinite}@keyframes fala{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}h1{color:#fff;font-size:48px;font-family:Georgia,serif;text-shadow:0 4px 20px rgba(0,0,0,.2)}',
        '<h1>DziobSi 🐦</h1>', ''),
    },
  ];

  const SNIPPETS = {
    python: [
      { keys: /p[eę]tl|for|powt/, title: 'Pętla', code: "for i in range(1, 6):\n    print('Dziób nr', i)" },
      { keys: /silni/, title: 'Silnia', code: "def silnia(n):\n    return 1 if n <= 1 else n * silnia(n - 1)\n\nprint(silnia(5))  # 120" },
      { keys: /fibonac/, title: 'Fibonacci', code: "a, b = 0, 1\nfor _ in range(10):\n    print(a)\n    a, b = b, a + b" },
      { keys: /sort/, title: 'Sortowanie', code: "liczby = [5, 2, 9, 1]\nprint(sorted(liczby))  # [1, 2, 5, 9]" },
      { keys: /losow|random/, title: 'Losowa liczba', code: "import random\nprint(random.randint(1, 100))" },
      { keys: /funkcj|def/, title: 'Funkcja', code: "def przywitaj(imie):\n    return f'Cześć, {imie}!'\n\nprint(przywitaj('DziobSi'))" },
      { keys: /warun|if|je[sś]li/, title: 'Warunek', code: "wiek = 15\nif wiek >= 18:\n    print('Dorosły')\nelse:\n    print('Niepełnoletni')" },
      { keys: /list|tablic/, title: 'Lista', code: "ptaki = ['wróbel', 'sikorka', 'dzięcioł']\nfor p in ptaki:\n    print(p)" },
      { keys: /.*/, title: 'Witaj, świecie', code: "print('Cześć od DziobSi! 🐦')" },
    ],
    javascript: [
      { keys: /p[eę]tl|for|powt/, title: 'Pętla', code: "for (let i = 1; i <= 5; i++) {\n  console.log('Dziób nr', i);\n}" },
      { keys: /silni/, title: 'Silnia', code: "const silnia = n => n <= 1 ? 1 : n * silnia(n - 1);\nconsole.log(silnia(5)); // 120" },
      { keys: /fibonac/, title: 'Fibonacci', code: "let a = 0, b = 1;\nfor (let i = 0; i < 10; i++) {\n  console.log(a);\n  [a, b] = [b, a + b];\n}" },
      { keys: /sort/, title: 'Sortowanie', code: "const liczby = [5, 2, 9, 1];\nconsole.log(liczby.sort((a, b) => a - b)); // [1, 2, 5, 9]" },
      { keys: /losow|random/, title: 'Losowa liczba', code: "console.log(Math.floor(Math.random() * 100) + 1);" },
      { keys: /funkcj/, title: 'Funkcja', code: "function przywitaj(imie) {\n  return `Cześć, ${imie}!`;\n}\nconsole.log(przywitaj('DziobSi'));" },
      { keys: /warun|if|je[sś]li/, title: 'Warunek', code: "const wiek = 15;\nconsole.log(wiek >= 18 ? 'Dorosły' : 'Niepełnoletni');" },
      { keys: /list|tablic/, title: 'Tablica', code: "const ptaki = ['wróbel', 'sikorka', 'dzięcioł'];\nptaki.forEach(p => console.log(p));" },
      { keys: /.*/, title: 'Witaj, świecie', code: "console.log('Cześć od DziobSi! 🐦');" },
    ],
  };

  // granice słów działające z polskimi literami
  const W = (body) => new RegExp('(?<![\\p{L}])(?:' + body + ')(?![\\p{L}])', 'u');
  const CODE_WORD = W('kod|kodu|kodem|code|program\\p{L}*|skrypt\\p{L}*|html|css|javascript|js|python\\p{L}*|py|funkcj\\p{L}*|p[eę]tl\\p{L}*|zaprogramuj');
  const MAKE = W('zr[oó]b|napisz|stw[oó]rz|zbuduj|daj|poka[zż]');
  const THING = W('stron\\p{L}*|aplikacj\\p{L}*|gr[eęay]|kalkulator|licznik|zegar|animacj\\p{L}*|list[eęa] zada[nń]');

  const DziobCode = {
    templates: TEMPLATES,

    /* Czy wiadomość w czacie prosi o kod? */
    wants(text) {
      const t = text.toLowerCase();
      if (CODE_WORD.test(t)) return true;
      return MAKE.test(t) && THING.test(t);
    },

    /* Dobierz kod do opisu: { lang, title, code } */
    make(text) {
      const t = text.toLowerCase();
      const lang = /python|pythonie|\bpy\b/.test(t) ? 'python' : (/javascript|\bjs\b/.test(t) && !/stron|html/.test(t) ? 'javascript' : null);
      if (lang) {
        const s = SNIPPETS[lang].find(x => x.keys.test(t));
        return { lang, title: s.title, code: s.code };
      }
      const tpl = TEMPLATES.find(x => x.id !== 'hello' && x.keys.test(t));
      if (tpl) return { lang: 'html', title: tpl.title, code: tpl.code, id: tpl.id };
      const js = SNIPPETS.javascript.find(x => x.keys.source !== '.*' && x.keys.test(t));
      if (js) return { lang: 'javascript', title: js.title, code: js.code };
      return { lang: 'html', title: TEMPLATES[0].title, code: TEMPLATES[0].code, id: 'hello' };
    },
  };

  window.DziobCode = DziobCode;
})();
