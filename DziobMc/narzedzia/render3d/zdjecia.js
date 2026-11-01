// Robi screeny 3D:  node zdjecia.js <three.min.js> <folder_wyjsciowy> [nazwa_sceny]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const TU = __dirname;

// --- pomocnicze do HUD (kolory Minecrafta) ---
const C = { gold: '#FFAA00', yellow: '#FFFF55', white: '#fff', gray: '#AAAAAA', dgray: '#555', aqua: '#55FFFF', red: '#FF5555',
  green: '#55FF55', lp: '#FF55FF', dred: '#AA0000', dgreen: '#00AA00', dpurple: '#AA00AA', blue: '#5555FF' };
const sp = (t, c = 'white') => `<span style="color:${C[c] || c}">${t}</span>`;
const ranga = (n, c) => sp('[', 'dgray') + sp(n, c) + sp('] ', 'dgray');
const linia = (...x) => `<div>${x.join('')}</div>`;

function bossbar(tekst, kolor, proc) {
  return `<div>${tekst}</div><div class="bar"><i style="width:${proc}%;background:${kolor}"></i><b></b></div>`;
}
const EVENT_BAR = bossbar(sp('✦ Następny event za ', 'gold') + sp('12', 'yellow') + sp('m ', 'yellow') + sp('34', 'yellow') + sp('s', 'yellow') + sp('  •  Dziob.fun', 'gray'), 'linear-gradient(#ffff70,#d8c000)', 63);
const SIDEBAR = (event = sp('wkrótce...', 'white')) => `<div id="side" class="s"><div class="t">${sp('✦ ', 'yellow')}${sp('DziobMc', 'gold')}${sp(' ✦', 'yellow')}</div>
<div></div><div><span>${sp(' ✦ ', 'gold')}${sp('Serwer: ', 'gray')}${sp('DziobMc', 'yellow')}</span></div>
<div><span>${sp(' ✦ ', 'gold')}${sp('Wersje: ', 'gray')}${sp('1.16.4+', 'white')}</span></div><div></div>
<div><span>${sp(' ● ', 'green')}${sp('Graczy łącznie')}</span>${sp('57', 'yellow')}</div>
<div><span>${sp(' ● ', 'green')}${sp('Online')}</span>${sp('12', 'yellow')}</div><div></div>
<div><span>${sp(' ★ ', 'gold')}${sp('Event: ', 'gray')}${event}</span></div>
<div>${sp(' ➤ /trigger pomoc', 'aqua')}</div><div><span>${sp(' ⛃ ', 'gold')}${sp('Monety: lista TAB', 'gray')}</span></div><div></div>
<div>${sp('    Dziob.fun', 'yellow')}</div></div>`;
const ACT = (monety, moby, pvp, seria) => `<div id="act" class="s">${sp('⛃ ', 'gold')}${sp(monety, 'yellow')}${sp('   ⚔ Moby: ', 'red')}${sp(moby)}${sp('   ☠ PvP: ', 'dred')}${sp(pvp)}${sp('   ✸ Seria: ', 'gold')}${sp(seria, 'yellow')}</div>`;
const HOTBAR = (sel = 0, items = [['⚔', '#ddd'], ['⛏', '#5ee'], ['🏹', '#b85'], ['●', '#fc3', '3'], ['■', '#a52', '16'], ['◆', '#5ee', '8'], ['', ''], ['', ''], ['', '']]) =>
  `<div id="stats" class="s"><span style="color:#e22;letter-spacing:-2px">❤❤❤❤❤❤❤❤❤❤</span><span style="color:#c84;letter-spacing:-2px">🍗🍗🍗🍗🍗🍗🍗🍗🍗🍗</span></div><div id="xp"><i></i></div>
  <div id="hot">${items.map(([g, c, n], i) => `<span class="${i === sel ? 'sel' : ''}" style="color:${c}">${g}${n ? `<em class="s">${n}</em>` : ''}</span>`).join('')}</div><div id="cross"></div>`;
const ZNAK = '<div id="znak">render 3D mapy DziobMc – bloki 1:1 z paczki (tekstury poglądowe)</div>';

// --- gracze ---
const SKORY = [0xc8946a, 0xe0b090, 0x9a6a48, 0xd8a580];
let n = 0;
function gracz(nick, rangaN, rangaK, x, y, z, yaw, o = {}) {
  const s = SKORY[n++ % 4];
  return Object.assign({ x, y, z, yaw, skora: s, twarzKolor: '#' + s.toString(16), wlosy: o.wlosy || [0x3a2a1a, 0x8a5a2a, 0x111111, 0xd0a040][n % 4],
    koszulka: o.koszulka || [0x2aa0a0, 0xc03030, 0x3050c0, 0x40a040][n % 4], spodnie: 0x3a3a8a,
    nick: rangaN ? [{ text: '[', color: 'dark_gray' }, { text: rangaN, color: rangaK, bold: true }, { text: '] ', color: 'dark_gray' }, { text: nick, color: rangaK }] : [{ text: nick, color: 'white' }] }, o);
}
const ZELAZO = { helm: 0xd0d0d0, klata: 0xd8d8d8, spodnie: 0xc8c8c8, buty: 0xb8b8b8 };
const DIAMENT = { helm: 0x4fe3d6, klata: 0x55e8dc, spodnie: 0x45d0c4, buty: 0x3ab8ad };
const NETHERYT = { helm: 0x4d4448, klata: 0x564c50, spodnie: 0x4a4246, buty: 0x3d3639 };

const SCENY = {
  '1-spawn': {
    kamera: [0.5, 152.62, 18.5], cel: [0.5, 154.6, 0], fov: 75,
    postacie: [gracz('Kuba_PL', 'MVP', 'gold', 4.5, 151, 9.5, 160, { ...DIAMENT }), gracz('Ola_Gamer', 'LEGENDA', 'light_purple', -5.5, 151, 7.5, 200),
      gracz('Tomek2010', 'VIP', 'yellow', -2.5, 151, -8.5, 20, { ...ZELAZO }), gracz('nowy_gracz', 'GRACZ', 'gray', -7.5, 151, -2.5, 120)],
    hud: `<div id="boss" class="s">${EVENT_BAR}</div>${SIDEBAR()}
      <div id="chat" class="s">${linia(sp('✦ ', 'gold'), sp('nowy_gracz', 'yellow'), sp(' dołączył pierwszy raz! ', 'white'), sp('(gracz #57)', 'gray'))}
      ${linia(sp('➤ Dostajesz ', 'green'), sp('100 monet', 'gold'), sp(' i zestaw startowy na dobry początek!', 'green'))}
      ${linia(ranga('MVP', 'gold'), sp('Kuba_PL', 'gold'), sp(': siema! kto idzie na arenę PvP?'))}
      ${linia(ranga('LEGENDA', 'lp'), sp('Ola_Gamer', 'lp'), sp(': ja! zaraz event z bossem'))}</div>
      ${ACT('1250', '37', '12', '0')}${HOTBAR()}`,
  },
  '2-sklep': {
    kamera: [7.8, 152.62, -3.2], cel: [10.5, 152.9, -10.5], fov: 70,
    postacie: [],
    hud: `<div id="boss" class="s">${EVENT_BAR}</div>${SIDEBAR()}
      <div id="chat" class="s">${linia(sp('━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'gold'))}${linia(sp('        ✦ ', 'yellow'), sp('DziobMc', 'gold'), sp(' » ', 'dgray'), sp('SKLEP', 'yellow'))}${linia(sp('━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'gold'))}
      ${linia(sp(' Twoje monety: ', 'gray'), sp('1250', 'gold'), sp(' ⛃', 'gold'))}
      ${[['Diamenty x8', 150, 'aqua'], ['Złote jabłka x5', 100, 'gold'], ['Perły Endu x16', 120, '#00AAAA'], ['Butelki XP x64', 200, 'green'], ['Totem Nieśmiertelności', 400, 'yellow'],
        ['Skrzynia Szczęścia', 250, 'lp'], ['Miecz Dzioba', 1500, 'gold'], ['Kilof Dzioba', 1800, 'gold'], ['Elytra + 32 fajerwerki', 2500, 'dpurple']]
        .map(([a, b, c]) => linia(sp(' ➤ ', 'dgray'), sp('[KUP]', 'green'), sp(' ' + a + ' ', c), sp('» ' + b + ' ⛃', 'gold'))).join('')}</div>
      ${ACT('1250', '37', '12', '0')}${HOTBAR()}`,
  },
  '3-arena-pvp': {
    kamera: [6.5, 152.62, 61.5], cel: [-1.5, 152.2, 76], fov: 74,
    postacie: [
      gracz('Kuba_PL', 'MVP', 'gold', -1.5, 151, 68.5, 200, { ...DIAMENT, bron: 0x5ee8e0, rekaP: -1.6, nogaP: .5, nogaL: -.5 }),
      gracz('Zosia', 'MOD', 'green', 1.2, 151, 70.3, 20, { ...ZELAZO, bron: 0xe0e0e0, rekaP: -1.1 }),
      gracz('KrafciakTV', 'YT', 'white', 6.5, 151, 77.5, 230, { ...NETHERYT, bron: 0x4d4448, rekaP: -1.4, nogaP: -.4, nogaL: .4 }),
      gracz('Tomek2010', 'VIP', 'yellow', 9.0, 151, 73.0, 60, { ...ZELAZO, bron: 0xe0e0e0, rekaP: -.4 }),
      gracz('Bartek', 'GRACZ', 'gray', -7.5, 151, 79.5, 140, { bron: 0x9a7a4a, rekaP: -1.2 }),
      gracz('Antek', 'HELPER', 'aqua', -5, 151, 85, 180, { ...DIAMENT, bron: 0x5ee8e0, rekaP: -.9, nogaP: .4, nogaL: -.4 }),
    ],
    czasteczki: [{ x: 0, y: 152.6, z: 69.4, kolor: 0xff3030, r: .35 }, { x: .3, y: 152.9, z: 69.6, kolor: 0xff5050, r: .25 }, { x: 7.8, y: 152.8, z: 75.2, kolor: 0xffffff, r: .5 }],
    hud: `<div id="boss" class="s">${bossbar(sp('★ EVENT: ', 'white') + sp('Bitwa PvP', 'dred') + sp('  •  zostało ', 'gray') + sp('3m 41s'), 'linear-gradient(#ff6060,#c00000)', 74)}</div>${SIDEBAR(sp('Bitwa PvP', 'dred'))}
      <div id="chat" class="s">${linia(sp('⚔ Strefa PvP! ', 'red'), sp('Kit PvP: ', 'gray'), sp('[ODBIERZ]', 'green'), sp('  •  25 monet za kill, serie 3/5/10!', 'gray'))}
      ${linia(sp('Bartek', 'gray'), sp(' został zabity przez ', 'white'), ranga('MVP', 'gold'), sp('Kuba_PL', 'gold'))}
      ${linia(sp('⚔ Zabójstwo gracza! ', 'red'), sp('Seria: ', 'gray'), sp('3', 'yellow'))}
      ${linia(sp('  + ', 'gold'), sp('150', 'gold'), sp(' monet ⛃', 'yellow'))}
      ${linia(sp('⚔ ', 'red'), ranga('MVP', 'gold'), sp('Kuba_PL', 'gold'), sp(' ma serię ', 'gold'), sp('3 zabójstw', 'red'), sp('!', 'gold'))}</div>
      ${ACT('1400', '37', '15', '3')}${HOTBAR(0, [['⚔', '#5ee'], ['🏹', '#b85'], ['●', '#fc3', '2'], ['▼', '#ccc', '14'], ['■', '#a52', '16'], ['', ''], ['', ''], ['', ''], ['', '']])}`,
  },
  '4-boss': {
    kamera: [4.5, 153.6, -57.5], cel: [0, 154.5, -75], fov: 74,
    postacie: [
      Object.assign({ x: 0.5, y: 151, z: -74.5, yaw: 10, skala: 2.5, skora: 0xb59a6a, twarzKolor: '#b59a6a', koszulka: 0x8a7a50, spodnie: 0x6a5a3a,
        helm: 0xffcf30, klata: 0xffd84a, buty: 0xe8b828, korona: true, bron: 0x4d4448, rekaP: -1.3, rekaL: -.5, nogaP: .3, nogaL: -.3,
        twarz: g => { g.fillStyle = '#300'; g.fillRect(1, 4, 2, 1); g.fillRect(5, 4, 2, 1); g.fillStyle = '#f00'; g.fillRect(2, 4, 1, 1); g.fillRect(5, 4, 1, 1); },
        nick: [{ text: '♛ Król Dziobów ♛', color: 'gold', bold: true }] }),
      Object.assign({ x: -5.5, y: 151, z: -69.5, yaw: 150, skora: 0x5a9a4a, twarzKolor: '#5a9a4a', koszulka: 0x2a8a9a, spodnie: 0x3a3a8a, ...ZELAZO, helm: 0xffcf30, bron: 0xe0e0e0, rekaP: -1.5, rekaL: -1.5,
        twarz: g => { g.fillStyle = '#000'; g.fillRect(1, 4, 2, 1); g.fillRect(5, 4, 2, 1); } }),
      Object.assign({ x: 6.5, y: 151, z: -69, yaw: 210, skora: 0x5a9a4a, twarzKolor: '#5a9a4a', koszulka: 0x2a8a9a, spodnie: 0x3a3a8a, ...ZELAZO, helm: 0xffcf30, bron: 0xe0e0e0, rekaP: -1.5, rekaL: -1.5,
        twarz: g => { g.fillStyle = '#000'; g.fillRect(1, 4, 2, 1); g.fillRect(5, 4, 2, 1); } }),
      gracz('Zosia', 'MOD', 'green', -2.5, 151, -65.5, 190, { ...DIAMENT, bron: 0x5ee8e0, rekaP: -1.6 }),
      gracz('Marek', 'ADMIN', 'red', 7.5, 151, -67.5, 135, { ...NETHERYT, bron: 0x4d4448, rekaP: -1.2, nogaP: .4, nogaL: -.4 }),
    ],
    czasteczki: Array.from({ length: 26 }, (_, i) => ({ x: .5 + Math.cos(i) * (2 + (i % 3)), y: 151.2 + (i % 4) * .2, z: -74.5 + Math.sin(i) * (2 + (i % 3)), kolor: 0x40e0f0, r: .35 })),
    hud: `<div id="boss" class="s">${bossbar(sp('★ EVENT: ', 'white') + sp('Król Dziobów', 'gold') + sp('  •  zostało ', 'gray') + sp('7m 12s'), 'linear-gradient(#ffff70,#d8c000)', 72)}
      ${bossbar(sp('♛ Król Dziobów ♛', 'gold'), 'linear-gradient(#ff5050,#b00000)', 54)}</div>${SIDEBAR(sp('Król Dziobów', 'gold'))}
      <div id="chat" class="s">${linia(sp('♛ Król Dziobów ', 'gold'), sp('pojawił się na arenie! ', 'red'), sp('[WALCZ]', 'green'))}
      ${linia(sp('♛ Król Dziobów: ', 'gold'), sp('Słudzy, do mnie!', 'red'))}
      ${linia(sp('⚔ Pokonano: ', 'gray'), sp('⚔ Dziobak Wojownik', 'gold'))}${linia(sp('  + ', 'gold'), sp('15', 'gold'), sp(' monet ⛃', 'yellow'))}
      ${linia(sp('♛ Król Dziobów: ', 'gold'), sp('CZUJCIE MOJĄ MOC!', 'red'))}</div>
      ${ACT('1265', '38', '12', '0')}${HOTBAR(0, [['⚔', '#ffd84a'], ['🏹', '#b85'], ['●', '#fc3', '5'], ['▼', '#ccc', '32'], ['■', '#a52', '12'], ['', ''], ['', ''], ['', ''], ['', '']])}`,
  },
  '5-z-lotu-ptaka': {
    kamera: [62, 196, 92], cel: [-6, 146, -12], fov: 60, mglaOd: 200, mglaDo: 700, postacie: [], hud: '',
  },
  '6-parkour': {
    kamera: [-22.5, 152.62, 3.5], cel: [-60, 154, -1], fov: 72,
    postacie: [gracz('Ola_Gamer', 'LEGENDA', 'light_purple', -40.5, 151, 1.5, 90, { nogaP: .7, nogaL: -.7, rekaP: .8, rekaL: -.8 })],
    hud: `<div id="boss" class="s">${EVENT_BAR}</div>${SIDEBAR()}
      <div id="chat" class="s">${linia(sp('✔ ', 'green'), ranga('VIP', 'yellow'), sp('Tomek2010', 'yellow'), sp(' ukończył parkour na spawnie!', 'green'))}</div>
      ${ACT('1250', '37', '12', '0')}${HOTBAR(6)}`,
  },
};

(async () => {
  const [threePath, outDir, tylko] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const scena = JSON.parse(fs.readFileSync(path.join(TU, 'scena.json'), 'utf8'));
  for (const [nazwa, K] of Object.entries(SCENY)) {
    if (tylko && nazwa !== tylko) continue;
    const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
    p.on('pageerror', e => console.log('BŁĄD', e.message));
    await p.goto('file://' + path.join(TU, 'strona.html'));
    await p.addScriptTag({ path: threePath });
    await p.evaluate(s => { window.SCENA = s; }, scena);
    await p.addScriptTag({ path: path.join(TU, 'render3d.js') });
    // funkcje (np. twarz) nie przechodzą przez evaluate – przekazujemy jako tekst
    const kod = 'window.renderuj(' + serial(K) + ')';
    await p.evaluate(kod);
    await p.evaluate(h => { document.getElementById('hud').innerHTML = h; }, (K.hud || '') + ZNAK);
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(outDir, nazwa + '.png') });
    console.log('zapisano', nazwa);
    await p.close();
  }
  await b.close();
})();

function serial(o) {
  if (typeof o === 'function') return o.toString();
  if (Array.isArray(o)) return '[' + o.map(serial).join(',') + ']';
  if (o && typeof o === 'object') return '{' + Object.entries(o).filter(([k]) => k !== 'hud').map(([k, v]) => JSON.stringify(k) + ':' + serial(v)).join(',') + '}';
  return JSON.stringify(o);
}
