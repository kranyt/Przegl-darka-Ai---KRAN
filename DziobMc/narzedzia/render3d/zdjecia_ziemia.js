// Screeny mapy Ziemi (Earth SMP):  node zdjecia_ziemia.js <three.min.js> <folder> [scena]
// Dane scen: ziemia_<nazwa>.json z plugin-ziemia/test/TestZiemi (prawdziwy kod generatora).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const TU = __dirname;

const C = { gold: '#FFAA00', yellow: '#FFFF55', white: '#fff', gray: '#AAAAAA', dgray: '#555', aqua: '#55FFFF', red: '#FF5555',
  green: '#55FF55', lp: '#FF55FF', dred: '#AA0000', dgreen: '#00AA00', blue: '#5555FF', dblue: '#0000AA' };
const sp = (t, c = 'white') => `<span style="color:${C[c] || c}">${t}</span>`;
const tag = (n, c) => sp('[', 'dgray') + sp(n, c) + sp('] ', 'dgray');
const linia = (...x) => `<div>${x.join('')}</div>`;
const bossbar = (tekst, kolor, proc) => `<div>${tekst}</div><div class="bar"><i style="width:${proc}%;background:${kolor}"></i><b></b></div>`;
const EVENT = bossbar(sp('✦ Następny event za ', 'gold') + sp('8m 02s', 'yellow') + sp('  •  Dziob.fun', 'gray'), 'linear-gradient(#ffff70,#d8c000)', 40);
const RANKING = `<div id="side" class="s"><div class="t">${sp('✪ ', 'aqua')}${sp('Potęga państw', 'gold')}</div>
  ${[['POL', 'Polska', 'red', 2140], ['GER', 'Niemcy', 'dgray', 1610], ['USA', 'USA', 'blue', 1290], ['JPN', 'Japonia', 'white', 980],
     ['FRA', 'Francja', 'blue', 760], ['ITA', 'Włochy', 'green', 540], ['BRA', 'Brazylia', 'green', 330]]
    .map(([k, n, c, v]) => `<div><span>${sp(k + ' ', 'dgray')}${sp(n, c)}</span>${sp(v, 'red')}</div>`).join('')}</div>`;
const SIDE = `<div id="side" class="s"><div class="t">${sp('✦ ', 'yellow')}${sp('DziobMc', 'gold')}${sp(' ✦', 'yellow')}</div>
  <div></div><div><span>${sp(' ✦ ', 'gold')}${sp('Serwer: ', 'gray')}${sp('DziobMc', 'yellow')}</span></div>
  <div><span>${sp(' ✦ ', 'gold')}${sp('Wersje: ', 'gray')}${sp('1.16.4+', 'white')}</span></div><div></div>
  <div><span>${sp(' ● ', 'green')}${sp('Graczy łącznie')}</span>${sp('214', 'yellow')}</div>
  <div><span>${sp(' ● ', 'green')}${sp('Online')}</span>${sp('48', 'yellow')}</div><div></div>
  <div><span>${sp(' ★ ', 'gold')}${sp('Event: ', 'gray')}${sp('wkrótce...')}</span></div>
  <div>${sp(' ➤ /trigger pomoc', 'aqua')}</div><div><span>${sp(' ⛃ ', 'gold')}${sp('Monety: lista TAB', 'gray')}</span></div><div></div>
  <div>${sp('    Dziob.fun', 'yellow')}</div></div>`;
const ACT = `<div id="act" class="s">${sp('⛃ ', 'gold')}${sp('2480', 'yellow')}${sp('   ⚔ Moby: ', 'red')}${sp('64')}${sp('   ☠ PvP: ', 'dred')}${sp('9')}${sp('   ✸ Seria: ', 'gold')}${sp('1', 'yellow')}</div>`;
const HOT = (sel = 0) => `<div id="stats" class="s"><span style="color:#e22;letter-spacing:-2px">❤❤❤❤❤❤❤❤❤❤</span><span style="color:#c84;letter-spacing:-2px">🍗🍗🍗🍗🍗🍗🍗🍗🍗🍗</span></div><div id="xp"><i></i></div>
  <div id="hot">${[['⚔', '#5ee'], ['⛏', '#5ee'], ['🪓', '#ddd'], ['■', '#a52', '64'], ['●', '#fc3', '12'], ['🧭', '#f55'], ['🗺', '#eda'], ['', ''], ['', '']]
    .map(([g, c, n], i) => `<span class="${i === sel ? 'sel' : ''}" style="color:${c}">${g}${n ? `<em class="s">${n}</em>` : ''}</span>`).join('')}</div><div id="cross"></div>`;
const GDZIE = (lat, ns, lon, ew, stol, kraj, kc, odl) => linia(sp('━━━━━━━━━━━ ✪ GDZIE JESTEM ✪ ━━━━━━━━━━━', 'aqua')) + linia(sp(' Szerokość: ', 'gray'), sp(lat), sp('° ' + ns, 'yellow')) +
  linia(sp(' Długość:    ', 'gray'), sp(lon), sp('° ' + ew, 'yellow')) + linia(sp(' Najbliższa stolica: ', 'gray'), sp(stol, kc), sp(' (', 'gray'), sp(kraj, kc), sp(') ~', 'gray'), sp(odl), sp(' kratek', 'gray'));
const ZNAK = '<div id="znak">render 3D terenu z generatora DziobEarth (skala 1:2000) • drzewa przybliżone, w grze stawia je Minecraft</div>';

let n = 0;
function gracz(nick, rN, rK, kN, kK, x, y, z, yaw, o = {}) {
  const sk = [0xc8946a, 0xe0b090, 0x9a6a48, 0xd8a580][n++ % 4];
  return Object.assign({ x, y, z, yaw, skora: sk, twarzKolor: '#' + sk.toString(16), wlosy: [0x3a2a1a, 0x8a5a2a, 0x111111][n % 3],
    koszulka: [0x2aa0a0, 0xc03030, 0x3050c0][n % 3], spodnie: 0x3a3a8a,
    nick: [{ text: '[', color: 'dark_gray' }, { text: rN, color: rK, bold: true }, { text: '] ', color: 'dark_gray' },
      { text: '[', color: 'dark_gray' }, { text: kN, color: kK, bold: true }, { text: '] ', color: 'dark_gray' }, { text: nick, color: rK }] }, o);
}
const ZEL = { helm: 0xd0d0d0, klata: 0xd8d8d8, spodnie: 0xc8c8c8, buty: 0xb8b8b8 };
const DIA = { helm: 0x4fe3d6, klata: 0x55e8dc, spodnie: 0x45d0c4, buty: 0x3ab8ad };

// kamera/cel względem wysokości środka sceny
const SCENY = {
  '7-ziemia-alpy': { dane: 'alpy', kamera: [-95, 30, 70], cel: [10, 5, -20], fov: 70, postacie: [], wys: 'abs',
    hud: `<div id="boss" class="s">${EVENT}</div>${RANKING}<div id="chat" class="s">${GDZIE('45.98', 'N', '7.70', 'E', 'Berno', 'Szwajcaria', 'red', '1430')}
      ${linia(tag('MVP', 'gold'), tag('CHE', 'red'), sp('Heidi_Alps', 'gold'), sp(': zbudujmy schronisko pod Matterhornem!'))}</div>${ACT}${HOT(6)}` },
  '8-ziemia-polska': { dane: 'polska', kamera: [-60, 22, 75], cel: [15, 0, -25], fov: 72,
    postacie: [], hud: `<div id="boss" class="s">${EVENT}</div>${SIDE}<div id="chat" class="s">
      ${linia(sp('♛ ', 'gold'), tag('VIP', 'yellow'), tag('POL', 'red'), sp('Kuba_PL', 'yellow'), sp(' zakłada państwo ', 'yellow'), sp('Polska', 'red'), sp(' i zostaje jego ', 'yellow'), sp('WŁADCĄ', 'gold'), sp('!', 'yellow'))}
      ${linia(sp('✪ ', 'aqua'), tag('GRACZ', 'gray'), tag('POL', 'red'), sp('Ola_W', 'gray'), sp(' dołączył do państwa ', 'gray'), sp('Polska', 'red'), sp('!', 'gray'))}
      ${GDZIE('52.23', 'N', '21.02', 'E', 'Warszawa', 'Polska', 'red', '20')}</div>${ACT}${HOT(0)}` },
  '9-ziemia-norwegia': { dane: 'norwegia', morze: 61.9, mglaDo: 260, kamera: [95, 85, 95], cel: [-30, -10, -30], fov: 70, postacie: [],
    hud: `<div id="boss" class="s">${EVENT}</div>${RANKING}<div id="chat" class="s">${GDZIE('61.15', 'N', '6.40', 'E', 'Oslo', 'Norwegia', 'dred', '4880')}</div>${ACT}${HOT(6)}` },
  '10-ziemia-nil': { dane: 'nil', kamera: [-70, 25, 60], cel: [10, 0, -10], fov: 72, postacie: [],
    hud: `<div id="boss" class="s">${bossbar(sp('★ EVENT: ', 'white') + sp('Krwawy Księżyc', 'dred') + sp('  •  zostało ', 'gray') + sp('3m 10s'), 'linear-gradient(#ff6060,#c00000)', 63)}</div>${SIDE}<div id="chat" class="s">
      ${linia(sp('⚔ ', 'dred'), sp('Egipt', 'gold'), sp(' wypowiada wojnę państwu ', 'gray'), sp('Arabia Saudyjska', 'dgreen'), sp('! 30 minut, do 15 punktów.', 'gray'))}
      ${linia(sp('⚔ +1 punkt wojenny! Wynik: ', 'gold'), sp('4', 'green'), sp(' : ', 'gray'), sp('2', 'red'))}
      ${GDZIE('25.70', 'N', '32.62', 'E', 'Kair', 'Egipt', 'gold', '2950')}</div>${ACT}${HOT(0)}` },
  '11-ziemia-himalaje': { dane: 'himalaje', bezChmur: true, kamera: [-95, 5, 90], cel: [10, 15, -10], fov: 70, postacie: [],
    hud: `<div id="boss" class="s">${EVENT}</div>${RANKING}<div id="chat" class="s">${GDZIE('27.99', 'N', '86.93', 'E', 'Nowe Delhi', 'Indie', 'gold', '5230')}
      ${linia(tag('LEGENDA', 'lp'), tag('IND', 'gold'), sp('Raj_Climber', 'lp'), sp(': stoję na Evereście! Y=' + 'najwyżej na serwerze'))}</div>${ACT}${HOT(6)}` },
  '12-ziemia-japonia': { dane: 'japonia', morze: 61.9, mglaDo: 230, kamera: [70, 35, 95], cel: [-10, 15, 0], fov: 72, postacie: [],
    hud: `<div id="boss" class="s">${EVENT}</div>${RANKING}<div id="chat" class="s">${GDZIE('35.36', 'N', '138.73', 'E', 'Tokio', 'Japonia', 'white', '2160')}
      ${linia(tag('MVP', 'gold'), tag('JPN', 'white'), sp('Sakura_san', 'gold'), sp(': wiśnie pod Fuji, zapraszam!'))}</div>${ACT}${HOT(0)}` },
};

(async () => {
  const [threePath, outDir, tylko] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  for (const [nazwa, K] of Object.entries(SCENY)) {
    if (tylko && nazwa !== tylko) continue;
    const dane = JSON.parse(fs.readFileSync(path.join(TU, `ziemia_${K.dane}.json`), 'utf8'));
    const h0 = dane.srodek[1];
    const kam = [K.kamera[0], h0 + K.kamera[1], K.kamera[2]], cel = [K.cel[0], h0 + K.cel[1], K.cel[2]];
    const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
    p.on('pageerror', e => console.log('BŁĄD', e.message));
    await p.goto('file://' + path.join(TU, 'strona.html'));
    await p.addScriptTag({ path: threePath });
    await p.evaluate(s => { window.SCENA = s; }, dane);
    await p.addScriptTag({ path: path.join(TU, 'render3d.js') });
    await p.evaluate(k => window.renderuj(k), { kamera: kam, cel, fov: K.fov, postacie: K.postacie, bezZiemi: true, bezBeacona: true,
      bezChmur: !!K.bezChmur, morze: K.morze, mglaOd: K.mglaOd || 70, mglaDo: K.mglaDo || 200 });
    await p.evaluate(h => { document.getElementById('hud').innerHTML = h; }, K.hud + ZNAK);
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(outDir, nazwa + '.png') });
    console.log('zapisano', nazwa);
    await p.close();
  }
  await b.close();
})();
