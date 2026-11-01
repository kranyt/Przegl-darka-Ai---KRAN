/* DziobMc – render 3D w stylu Minecrafta (three.js, tekstury proceduralne 16x16).
   Wejście: window.SCENA = {typy, bloki, encje}; wywołanie: window.renderuj(konfig) */
(function () {
  const T = THREE;
  const KOL = {
    grass_block: [95, 159, 53], dirt: [134, 96, 67], stone: [125, 125, 125], andesite: [136, 136, 137],
    cobblestone: [115, 115, 115], mossy_cobblestone: [100, 120, 90], tuff: [108, 109, 102], moss_block: [89, 109, 45],
    coal_ore: [125, 125, 125], iron_ore: [125, 125, 125], gold_ore: [125, 125, 125], nether_gold_ore: [111, 54, 52],
    amethyst_block: [133, 97, 191], smooth_quartz: [236, 230, 223], polished_deepslate: [72, 72, 73],
    gold_block: [246, 208, 61], orange_glazed_terracotta: [225, 120, 40], yellow_concrete: [240, 175, 21],
    polished_blackstone_bricks: [48, 42, 49], gilded_blackstone: [60, 45, 40], quartz_bricks: [234, 229, 221],
    chiseled_quartz_block: [231, 226, 218], prismarine_bricks: [99, 171, 158], iron_block: [220, 220, 220],
    water: [50, 95, 220], beacon: [130, 230, 225], orange_stained_glass: [230, 130, 40], obsidian: [20, 18, 30],
    crying_obsidian: [40, 12, 70], polished_blackstone: [53, 48, 56], red_nether_bricks: [69, 7, 9],
    chiseled_polished_blackstone: [55, 50, 60], blackstone: [42, 36, 41], basalt: [80, 80, 85], netherrack: [111, 54, 52],
    magma_block: [70, 30, 20], crimson_nylium: [130, 30, 30], shroomlight: [240, 145, 70],
    light_blue_concrete: [36, 137, 199], sea_lantern: [172, 199, 190], emerald_block: [42, 203, 87],
    red_concrete: [142, 32, 32], orange_concrete: [224, 97, 0], lime_concrete: [94, 168, 24], blue_concrete: [44, 46, 143],
    purple_concrete: [100, 31, 156], magenta_concrete: [169, 48, 159], pink_concrete: [213, 101, 142],
    cherry_leaves: [236, 160, 196], oak_leaves: [58, 120, 36], cherry_log: [55, 32, 42], oak_log: [104, 83, 50],
    stone_bricks: [122, 121, 122], chiseled_stone_bricks: [118, 118, 118], mossy_stone_bricks: [112, 120, 100],
    smooth_sandstone: [223, 214, 170], sandstone: [216, 203, 155], chiseled_sandstone: [216, 203, 155],
    cut_red_sandstone: [189, 101, 31], red_sandstone: [184, 99, 31], chiseled_red_sandstone: [183, 96, 27],
    smooth_red_sandstone: [184, 100, 33], terracotta: [152, 94, 67], red_terracotta: [143, 61, 46],
    orange_terracotta: [161, 83, 37], yellow_terracotta: [186, 133, 35], hay_block: [180, 145, 30], red_banner: [160, 39, 34],
    sand: [219, 207, 163], red_sand: [190, 102, 33], gravel: [131, 127, 126], clay: [160, 166, 179], snow_block: [249, 254, 254],
    packed_ice: [141, 180, 250], blue_ice: [116, 167, 253], ice: [145, 183, 253], podzol: [91, 63, 24], coarse_dirt: [119, 85, 59],
    mud: [60, 57, 60], calcite: [223, 224, 220], deepslate: [80, 80, 82], bedrock: [85, 85, 85],
    white_terracotta: [209, 178, 161], light_gray_terracotta: [135, 107, 98], brown_terracotta: [77, 51, 35],
    spruce_log: [58, 37, 16], spruce_leaves: [60, 95, 60], birch_log: [216, 215, 210], birch_leaves: [110, 150, 70],
    jungle_log: [85, 67, 25], jungle_leaves: [48, 140, 20], acacia_log: [103, 96, 86], acacia_leaves: [110, 140, 30],
    dark_oak_log: [60, 46, 26], dark_oak_leaves: [40, 95, 25], mangrove_log: [84, 66, 36], mangrove_leaves: [80, 130, 40],
    lantern: [255, 205, 110], soul_lantern: [110, 235, 240], chain: [60, 62, 70], soul_campfire: [80, 70, 60],
  };
  const ROSLINY = { short_grass: [100, 165, 55], poppy: [210, 30, 30], dandelion: [250, 225, 40], cornflower: [70, 100, 230],
    oxeye_daisy: [245, 245, 235], azure_bluet: [225, 235, 245], allium: [185, 100, 225], lily_of_the_valley: [252, 252, 252],
    fire: [255, 150, 30], amethyst_cluster: [190, 140, 240] };

  function R(seed) { let s = seed >>> 0 || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
  function hs(str) { let h = 2166136261; for (const c of str) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; }
  const cl = v => Math.max(0, Math.min(255, v | 0));
  const mul = (c, f) => [cl(c[0] * f), cl(c[1] * f), cl(c[2] * f)];

  function bazaNazwy(n) {
    n = n.split('[')[0];
    if (n.endsWith('_slab')) { const b = n.slice(0, -5); return KOL[b + 's'] ? b + 's' : b; }
    if (n.endsWith('_wall')) { const b = n.slice(0, -5); return KOL[b + 's'] ? b + 's' : b; }
    return n;
  }

  // ------------------------------------------------------------------ tekstury
  const cacheTex = {};
  function tex(nazwa, kind) {
    const key = nazwa + ':' + kind;
    if (cacheTex[key]) return cacheTex[key];
    const c = document.createElement('canvas'); c.width = c.height = 16;
    const g = c.getContext('2d');
    const r = R(hs(key));
    const p = (x, y, col, a = 1) => { g.fillStyle = `rgba(${col[0]},${col[1]},${col[2]},${a})`; g.fillRect(x, y, 1, 1); };
    const n = nazwa;
    const base = KOL[n] || ROSLINY[n] || [200, 0, 200];
    const szum = (b, amp = 0.12) => { for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) p(x, y, mul(b, 1 - amp + r() * amp * 2)); };
    if (ROSLINY[n]) {
      g.clearRect(0, 0, 16, 16);
      if (n === 'short_grass') { for (let i = 0; i < 9; i++) { const x = 1 + (r() * 14) | 0, h = 6 + (r() * 9) | 0; for (let y = 16 - h; y < 16; y++) p(x, y, mul(base, 0.8 + r() * 0.4)); } }
      else if (n === 'fire') { for (let x = 0; x < 16; x++) { const h = 6 + (r() * 10) | 0; for (let y = 16 - h; y < 16; y++) p(x, y, y < 16 - h + 3 ? [255, 230, 80] : base, 0.95); } }
      else if (n === 'amethyst_cluster') { for (let i = 0; i < 4; i++) { const x = 3 + i * 3; for (let y = 4 + (i % 2) * 3; y < 16; y++) p(x, y, mul(base, 0.8 + r() * .4)), p(x + 1, y, mul(base, 1.1)); } }
      else { for (let y = 7; y < 16; y++) p(7, y, [60, 130, 40]), p(8, y, [50, 115, 35]); p(6, 11, [60, 130, 40]); p(9, 12, [60, 130, 40]);
        for (const [dx, dy] of [[0, -1], [-1, 0], [1, 0], [0, 1], [0, 0], [-1, -1], [1, -1], [-1, 1], [1, 1]]) p(7 + dx + (dx > 0), 5 + dy, dx === 0 && dy === 0 ? [250, 220, 60] : mul(base, 0.9 + r() * .2)); }
    } else if (n === 'grass_block') {
      if (kind === 'top') szum(base, 0.15);
      else { szum(KOL.dirt, 0.15); if (kind === 'side') for (let x = 0; x < 16; x++) { const h = 3 + (r() < .4 ? 1 : 0); for (let y = 0; y < h; y++) p(x, y, mul(base, 0.85 + r() * .3)); } }
    } else if (n.endsWith('_log')) {
      if (kind === 'side') { for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) p(x, y, mul(base, (x % 4 === 0 ? 0.75 : 1) * (0.9 + r() * .2))); }
      else { const inner = n.startsWith('cherry') ? [190, 110, 120] : [180, 145, 90]; for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) { const d = Math.max(Math.abs(x - 7.5), Math.abs(y - 7.5)); p(x, y, d > 6.5 ? base : mul(inner, (Math.floor(d) % 2 ? 0.85 : 1) * (0.95 + r() * .1))); } }
    } else if (n.endsWith('_leaves')) {
      g.clearRect(0, 0, 16, 16); for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) if (r() > 0.18) p(x, y, mul(base, 0.75 + r() * 0.45));
    } else if (n.includes('ore')) {
      szum(KOL.stone, 0.15); const oc = n.startsWith('coal') ? [30, 30, 30] : n.startsWith('iron') ? [216, 175, 147] : [250, 220, 60];
      for (let i = 0; i < 6; i++) { const x = (r() * 14) | 0, y = (r() * 14) | 0; p(x, y, oc); p(x + 1, y, mul(oc, .85)); p(x, y + 1, mul(oc, .8)); }
    } else if (n === 'water') {
      for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) p(x, y, mul(base, 0.85 + 0.25 * Math.sin((x + y * 0.5) * 0.9 + r())), 0.78);
    } else if (n.includes('glass') || n === 'beacon') {
      g.clearRect(0, 0, 16, 16);
      for (let i = 0; i < 16; i++) { p(i, 0, base); p(i, 15, base); p(0, i, base); p(15, i, base); }
      if (n === 'beacon') { g.fillStyle = 'rgb(120,240,235)'; g.fillRect(3, 3, 10, 10); g.fillStyle = 'rgb(220,255,255)'; g.fillRect(5, 5, 6, 6); }
      else { g.fillStyle = `rgba(${base},0.35)`; g.fillRect(1, 1, 14, 14); p(3, 3, [255, 255, 255]); p(4, 4, [255, 255, 255]); }
    } else if (/bricks$/.test(n) || n === 'prismarine_bricks') {
      const big = n.startsWith('stone') || n.startsWith('mossy_stone') || n.startsWith('polished_blackstone') || n === 'quartz_bricks';
      szum(base, 0.1);
      const zap = mul(base, 0.62);
      if (big) { for (let x = 0; x < 16; x++) { p(x, 7, zap); p(x, 15, zap); } for (let y = 0; y < 8; y++) p(15, y, zap); for (let y = 8; y < 16; y++) p(7, y, zap); }
      else { for (let y = 3; y < 16; y += 4) for (let x = 0; x < 16; x++) p(x, y, zap); for (let y = 0; y < 16; y++) p(((y >> 2) % 2) ? 3 : 11, y, zap); }
      if (n.startsWith('mossy')) for (let i = 0; i < 30; i++) p((r() * 16) | 0, (r() * 16) | 0, [80, 110, 50]);
    } else if (n.includes('sandstone')) {
      if (kind === 'side' && !n.startsWith('smooth') && !n.startsWith('chiseled')) { szum(base, 0.06); for (let x = 0; x < 16; x++) { p(x, 0, mul(base, 1.08)); p(x, 1, mul(base, 1.05)); p(x, 12, mul(base, .88)); p(x, 13, mul(base, .92)); } if (n.startsWith('cut')) for (let y = 0; y < 16; y++) p(15, y, mul(base, .85)); }
      else szum(base, 0.05);
      if (n.startsWith('chiseled')) { g.strokeStyle = `rgb(${mul(base, .75)})`; g.strokeRect(2.5, 2.5, 11, 11); g.strokeRect(5.5, 5.5, 5, 5); }
    } else if (n.startsWith('chiseled')) {
      szum(base, 0.06); g.strokeStyle = `rgb(${mul(base, .7)})`; g.strokeRect(1.5, 1.5, 13, 13); g.strokeRect(4.5, 4.5, 7, 7);
    } else if (['gold_block', 'iron_block', 'emerald_block', 'sea_lantern', 'shroomlight'].includes(n)) {
      szum(base, 0.05); for (let i = 0; i < 16; i++) { p(i, 0, mul(base, 1.15)); p(0, i, mul(base, 1.15)); p(i, 15, mul(base, .75)); p(15, i, mul(base, .75)); }
      if (n === 'emerald_block') for (let i = 3; i < 13; i += 3) for (let j = 3; j < 13; j += 3) p(i, j, mul(base, 1.3));
    } else if (n.includes('concrete')) { szum(base, 0.03);
    } else if (n.includes('glazed')) {
      for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) { const d = (x + y) % 8; p(x, y, d < 2 ? [250, 240, 220] : d < 4 ? [200, 90, 20] : base); }
    } else if (n === 'hay_block') {
      if (kind === 'top') szum(base, .15); else { for (let y = 0; y < 16; y++) for (let x = 0; x < 16; x++) p(x, y, mul(base, (x % 3 ? 1 : .8) * (.9 + r() * .2))); for (const yy of [4, 11]) for (let x = 0; x < 16; x++) p(x, yy, [110, 80, 20]); }
    } else if (n === 'crying_obsidian' || n === 'obsidian') {
      szum(base, 0.3); for (let i = 0; i < 12; i++) p((r() * 16) | 0, (r() * 16) | 0, n === 'crying_obsidian' ? [170, 60, 255] : [70, 50, 110]);
    } else if (n === 'magma_block') {
      szum(base, .2); for (let i = 0; i < 40; i++) p((r() * 16) | 0, (r() * 16) | 0, [255, 120 + r() * 80, 20]);
    } else if (n === 'gilded_blackstone') {
      szum(base, .25); for (let i = 0; i < 18; i++) p((r() * 16) | 0, (r() * 16) | 0, [240, 180, 40]);
    } else if (n.startsWith('polished') || n.startsWith('smooth')) {
      szum(base, 0.05); for (let i = 0; i < 16; i++) { p(i, 0, mul(base, .88)); p(0, i, mul(base, .88)); p(i, 15, mul(base, .82)); p(15, i, mul(base, .82)); }
    } else if (n === 'red_banner') { szum(base, .05); g.fillStyle = 'rgb(250,200,40)'; g.fillRect(5, 4, 6, 6); }
    else szum(base, n === 'stone' || n === 'cobblestone' || n === 'andesite' || n === 'tuff' ? 0.18 : 0.12);
    const t = new T.CanvasTexture(c); t.magFilter = T.NearestFilter; t.minFilter = T.NearestFilter; t.colorSpace = T.SRGBColorSpace;
    cacheTex[key] = t; return t;
  }

  const cacheMat = {};
  function mat(nazwa, kind) {
    const key = nazwa + ':' + kind;
    if (cacheMat[key]) return cacheMat[key];
    const przezr = nazwa === 'water' || nazwa.includes('glass') || nazwa === 'beacon';
    const alfa = ROSLINY[nazwa] || nazwa.endsWith('_leaves');
    const m = new T.MeshBasicMaterial({ map: tex(nazwa, kind), vertexColors: true, side: T.DoubleSide,
      transparent: przezr, alphaTest: alfa ? 0.5 : 0, depthWrite: !przezr });
    cacheMat[key] = m; return m;
  }

  // ------------------------------------------------------------------ geometria bloków
  const FACES = [
    { n: [0, 1, 0], c: [[0, 1, 1], [1, 1, 1], [1, 1, 0], [0, 1, 0]], s: 1.0, k: 'top' },
    { n: [0, -1, 0], c: [[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1]], s: 0.5, k: 'bottom' },
    { n: [1, 0, 0], c: [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]], s: 0.6, k: 'side' },
    { n: [-1, 0, 0], c: [[0, 0, 0], [0, 0, 1], [0, 1, 1], [0, 1, 0]], s: 0.6, k: 'side' },
    { n: [0, 0, 1], c: [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]], s: 0.8, k: 'side' },
    { n: [0, 0, -1], c: [[1, 0, 0], [0, 0, 0], [0, 1, 0], [1, 1, 0]], s: 0.8, k: 'side' },
  ];
  const UV = [[0, 0], [1, 0], [1, 1], [0, 1]];
  const AO = [0.5, 0.68, 0.84, 1.0];

  function budujSwiat(scene) {
    const S = window.SCENA, typy = S.typy;
    const swiat = new Map();
    const K = (x, y, z) => (x + 512) * 1048576 + (y + 64) * 1024 + (z + 512);
    for (const [x, y, z, i] of S.bloki) swiat.set(K(x, y, z), typy[i]);
    const NIEPELNE = n => { const b = n.split('[')[0]; return ROSLINY[b] || b.endsWith('_slab') || b.endsWith('_wall') || b.endsWith('_leaves') ||
      b === 'water' || b.includes('glass') || b.includes('lantern') || b === 'chain' || b.includes('campfire') || b === 'red_banner' || b === 'beacon'; };
    const pelny = (x, y, z) => { const b = swiat.get(K(x, y, z)); return b !== undefined && !NIEPELNE(b); };
    const jest = (x, y, z) => swiat.has(K(x, y, z));
    const bufs = {};
    const buf = (nazwa, kind) => { const k = nazwa + ':' + kind; return bufs[k] || (bufs[k] = { nazwa, kind, pos: [], uv: [], col: [], idx: [] }); };
    function quad(b, pts, uvs, cols) {
      const o = b.pos.length / 3;
      for (let i = 0; i < 4; i++) { b.pos.push(...pts[i]); b.uv.push(...uvs[i]); b.col.push(cols[i], cols[i], cols[i]); }
      if (cols[0] + cols[2] < cols[1] + cols[3]) b.idx.push(o + 1, o + 2, o + 3, o + 1, o + 3, o + 0);
      else b.idx.push(o, o + 1, o + 2, o, o + 2, o + 3);
    }
    function box(nazwa, x0, y0, z0, x1, y1, z1, jasn = 1, tylkoGora = false) {
      for (const f of FACES) {
        if (tylkoGora && f.k !== 'top') continue;
        const pts = f.c.map(c => [c[0] ? x1 : x0, c[1] ? y1 : y0, c[2] ? z1 : z0]);
        const uvs = f.c.map((c, i) => {
          if (f.k !== 'side') return [c[0] ? (x1 % 1 || 1) : x0 % 1, c[2] ? (z1 % 1 || 1) : z0 % 1];
          const u = f.n[0] !== 0 ? (c[2] ? (z1 % 1 || 1) : z0 % 1) : (c[0] ? (x1 % 1 || 1) : x0 % 1);
          return [u, c[1] ? (y1 % 1 || 1) : y0 % 1];
        });
        quad(buf(nazwa, f.k), pts, uvs, [f.s * jasn, f.s * jasn, f.s * jasn, f.s * jasn]);
      }
    }
    function krzyz(nazwa, x, y, z, h = 1, w = 0.45) {
      const b = buf(nazwa, 'side');
      for (const [dx, dz] of [[1, 1], [1, -1]]) {
        const pts = [[x + .5 - w * dx, y, z + .5 - w * dz], [x + .5 + w * dx, y, z + .5 + w * dz], [x + .5 + w * dx, y + h, z + .5 + w * dz], [x + .5 - w * dx, y + h, z + .5 - w * dz]];
        quad(b, pts, UV, [1, 1, 1, 1]);
      }
    }
    for (const [x, y, z, ti] of S.bloki) {
      const pelna = typy[ti], n = pelna.split('[')[0];
      if (ROSLINY[n]) { krzyz(n, x, y, z, n === 'short_grass' ? .8 : n === 'fire' ? 1.2 : .85); continue; }
      if (n.endsWith('_slab')) { const gora = pelna.includes('top'); box(bazaNazwy(n), x, y + (gora ? .5 : 0), z, x + 1, y + (gora ? 1 : .5), z + 1); continue; }
      if (n.endsWith('_wall')) {
        const bn = bazaNazwy(n); box(bn, x + .25, y, z + .25, x + .75, y + 1, z + .75);
        const sc = (xx, zz) => { const b = swiat.get(K(xx, y, zz)); return b && (b.endsWith('_wall') || !NIEPELNE(b)); };
        if (sc(x + 1, z)) box(bn, x + .75, y, z + .31, x + 1, y + .81, z + .69);
        if (sc(x - 1, z)) box(bn, x, y, z + .31, x + .25, y + .81, z + .69);
        if (sc(x, z + 1)) box(bn, x + .31, y, z + .75, x + .69, y + .81, z + 1);
        if (sc(x, z - 1)) box(bn, x + .31, y, z, x + .69, y + .81, z + .25);
        continue;
      }
      if (n.includes('lantern') && n !== 'sea_lantern') {
        const wis = pelna.includes('hanging'); const y0 = wis ? y + .1 : y;
        box(n, x + .31, y0, z + .31, x + .69, y0 + .5, z + .69, 1.25); if (wis) box('chain', x + .45, y + .6, z + .45, x + .55, y + 1, z + .55);
        swiatla.push([x + .5, y0 + .25, z + .5, n === 'lantern' ? 0xffb050 : 0x60e8f0]); continue;
      }
      if (n === 'chain') { box('chain', x + .44, y, z + .44, x + .56, y + 1, z + .56); continue; }
      if (n.includes('campfire')) { box('oak_log', x, y, z + .2, x + 1, y + .25, z + .45); box('oak_log', x + .2, y, z, x + .45, y + .25, z + 1); krzyz('fire', x, y + .2, z, .8); swiatla.push([x + .5, y + .6, z + .5, 0x60e8f0]); continue; }
      if (n === 'red_banner') { box(n, x + .05, y - .9, z + .45, x + .95, y + 1, z + .52); continue; }
      if (n === 'water') { if (!jest(x, y + 1, z)) box('water', x, y, z, x + 1, y + .875, z + 1, 1, true); continue; }
      if (n.includes('glass') || n === 'beacon') { box(n, x, y, z, x + 1, y + 1, z + 1, n === 'beacon' ? 1.2 : 1); continue; }
      const liscie = n.endsWith('_leaves');
      const jasn = ['sea_lantern', 'shroomlight', 'magma_block'].includes(n) ? 1.25 : 1;
      for (const f of FACES) {
        const [nx, ny, nz] = f.n;
        if (liscie ? jest(x + nx, y + ny, z + nz) && swiat.get(K(x + nx, y + ny, z + nz)).endsWith('_leaves') : pelny(x + nx, y + ny, z + nz)) continue;
        const pts = [], cols = [];
        for (const c of f.c) {
          pts.push([x + c[0], y + c[1], z + c[2]]);
          const osie = [0, 1, 2].filter(a => f.n[a] === 0);
          const d = osie.map(a => c[a] ? 1 : -1);
          const b0 = [x + nx, y + ny, z + nz];
          const s1 = [...b0]; s1[osie[0]] += d[0];
          const s2 = [...b0]; s2[osie[1]] += d[1];
          const cc = [...b0]; cc[osie[0]] += d[0]; cc[osie[1]] += d[1];
          const o1 = pelny(...s1) ? 1 : 0, o2 = pelny(...s2) ? 1 : 0, o3 = pelny(...cc) ? 1 : 0;
          const lvl = (o1 && o2) ? 0 : 3 - (o1 + o2 + o3);
          cols.push(f.s * AO[lvl] * jasn);
        }
        quad(buf(n, f.k), pts, UV, cols);
      }
    }
    for (const k in bufs) {
      const b = bufs[k];
      const geo = new T.BufferGeometry();
      geo.setAttribute('position', new T.Float32BufferAttribute(b.pos, 3));
      geo.setAttribute('uv', new T.Float32BufferAttribute(b.uv, 2));
      geo.setAttribute('color', new T.Float32BufferAttribute(b.col, 3));
      geo.setIndex(b.idx);
      const kind = b.nazwa === 'grass_block' || b.nazwa.endsWith('_log') || b.nazwa.includes('sandstone') || b.nazwa === 'hay_block' ? b.kind : 'side';
      const m = new T.Mesh(geo, mat(b.nazwa, kind === 'bottom' && b.nazwa === 'grass_block' ? 'bottom' : kind));
      if (b.nazwa === 'water' || b.nazwa.includes('glass')) m.renderOrder = 2;
      scene.add(m);
    }
  }
  const swiatla = [];

  // ------------------------------------------------------------------ tekst (hologramy, nicki)
  const MC = { gold: '#FFAA00', yellow: '#FFFF55', white: '#FFFFFF', gray: '#AAAAAA', aqua: '#55FFFF', red: '#FF5555',
    green: '#55FF55', light_purple: '#FF55FF', dark_gray: '#555555', dark_red: '#AA0000', blue: '#5555FF', dark_purple: '#AA00AA',
    dark_green: '#00AA00', dark_aqua: '#00AAAA', black: '#000' };
  function napis(segmenty, { tlo = null, wys = 0.3 } = {}) {
    const linie = [[]];
    for (const s of segmenty) s.text.split('\n').forEach((t, i) => { if (i) linie.push([]); if (t) linie[linie.length - 1].push({ t, c: MC[s.color] || '#fff', b: s.bold }); });
    const F = 48, c = document.createElement('canvas'), g = c.getContext('2d');
    const font = b => `${b ? 'bold ' : ''}${F}px "DejaVu Sans Mono", monospace`;
    let W = 0; for (const l of linie) { let w = 0; for (const s of l) { g.font = font(s.b); w += g.measureText(s.t).width; } W = Math.max(W, w); }
    c.width = Math.ceil(W + 24); c.height = Math.ceil(linie.length * F * 1.15 + 12);
    if (tlo) { g.fillStyle = tlo; g.fillRect(0, 0, c.width, c.height); }
    linie.forEach((l, i) => {
      let w = 0; for (const s of l) { g.font = font(s.b); w += g.measureText(s.t).width; }
      let x = (c.width - w) / 2; const y = 6 + F * 0.95 + i * F * 1.15;
      for (const s of l) { g.font = font(s.b); g.fillStyle = 'rgba(40,40,40,0.9)'; g.fillText(s.t, x + 4, y + 4); g.fillStyle = s.c; g.fillText(s.t, x, y); x += g.measureText(s.t).width; }
    });
    const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; t.minFilter = T.LinearFilter;
    const sp = new T.Sprite(new T.SpriteMaterial({ map: t, transparent: true, depthWrite: false }));
    const h = linie.length * wys * 1.15; sp.scale.set(h * c.width / c.height, h, 1); sp.center.set(0.5, 0);
    sp.renderOrder = 5; return sp;
  }

  // ------------------------------------------------------------------ modele postaci
  function skora(kolor, oczy = true, extra = null) {
    const c = document.createElement('canvas'); c.width = c.height = 8; const g = c.getContext('2d');
    g.fillStyle = kolor; g.fillRect(0, 0, 8, 8);
    if (oczy) { g.fillStyle = '#fff'; g.fillRect(1, 4, 2, 1); g.fillRect(5, 4, 2, 1); g.fillStyle = '#2a2a7a'; g.fillRect(2, 4, 1, 1); g.fillRect(5, 4, 1, 1); g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(3, 6, 2, 1); }
    if (extra) extra(g);
    const t = new T.CanvasTexture(c); t.magFilter = T.NearestFilter; t.colorSpace = T.SRGBColorSpace; return t;
  }
  const lam = (col, map) => new T.MeshLambertMaterial({ color: col, map: map || null });
  function kloc(w, h, d, m, x, y, z) { const me = new T.Mesh(new T.BoxGeometry(w, h, d), m); me.position.set(x, y, z); return me; }
  function postac(o) {
    const g = new T.Group();
    const s = o.skala || 1;
    const glowaMat = [lam(o.skora), lam(o.skora), lam(o.wlosy || o.skora), lam(o.skora), lam(0xffffff, skora(o.twarzKolor || '#c8946a', true, o.twarz)), lam(o.wlosy || o.skora)];
    if (o.helm) for (const i of [0, 1, 2, 3, 5]) glowaMat[i] = lam(o.helm);
    const glowa = new T.Mesh(new T.BoxGeometry(.5, .5, .5), glowaMat); glowa.position.set(0, 1.75, 0); glowa.rotation.y = o.glowaYaw || 0; g.add(glowa);
    if (o.helm) { const h = kloc(.56, .2, .56, lam(o.helm), 0, 1.92, 0); g.add(h); }
    if (o.korona) for (const [dx, dz] of [[-.22, -.22], [.22, -.22], [-.22, .22], [.22, .22], [0, -.25], [0, .25], [-.25, 0], [.25, 0]]) g.add(kloc(.1, .18, .1, lam(0xffd02a), dx, 2.15, dz));
    g.add(kloc(.5, .75, .25, lam(o.klata || o.koszulka), 0, 1.125, 0));
    const reka = (strona, kat) => { const p = new T.Group(); p.position.set(strona * .375, 1.5, 0); const r = kloc(.25, .75, .25, lam(o.klata || o.koszulka), 0, -.375, 0); p.add(r);
      const dlon = kloc(.24, .2, .24, lam(o.skora), 0, -.66, 0); p.add(dlon); p.rotation.x = kat; g.add(p); return p; };
    const rp = reka(1, o.rekaP ?? -0.3), rl = reka(-1, o.rekaL ?? 0.3);
    if (o.bron) { const b = new T.Group(); b.position.set(0, -.75, -.05); const ost = kloc(.07, .95, .14, lam(o.bron), 0, .2, -.35); ost.rotation.x = Math.PI / 2.4; b.add(ost); b.add(kloc(.3, .07, .07, lam(0x5a4020), 0, -.02, -.12)); rp.add(b); }
    const noga = (strona, kat) => { const p = new T.Group(); p.position.set(strona * .125, .75, 0); p.add(kloc(.25, .75, .25, lam(o.spodnie), 0, -.375, 0)); p.add(kloc(.26, .2, .26, lam(o.buty || 0x3b3b3b), 0, -.65, 0)); p.rotation.x = kat; g.add(p); };
    noga(1, o.nogaP ?? 0.25); noga(-1, o.nogaL ?? -0.25);
    g.scale.setScalar(s); g.position.set(o.x, o.y, o.z); g.rotation.y = -(o.yaw || 0) * Math.PI / 180;
    if (o.nick) { const n = napis(o.nick, { tlo: 'rgba(0,0,0,0.3)', wys: .25 }); n.position.set(o.x, o.y + 2.15 * s + .15, o.z); g.userData.nick = n; }
    return g;
  }
  function wiesniak(o) {
    const sz = { librarian: 0xf5f5f5, armorer: 0x3c3c3c, cleric: 0x7b2b8f, cartographer: 0xe0e0e0 }[o.prof] || 0x6a4a30;
    const pas = { librarian: 0xb22222, armorer: 0x222222, cleric: 0xffd040, cartographer: 0x2050c0 }[o.prof] || 0x333;
    const g = new T.Group();
    const twarz = skora('#bd8b72', false, gg => { gg.fillStyle = '#2b6b2b'; gg.fillRect(1, 3, 2, 1); gg.fillRect(5, 3, 2, 1); gg.fillStyle = '#4a2a1a'; gg.fillRect(1, 1, 6, 1); gg.fillStyle = '#a06a55'; gg.fillRect(3, 4, 2, 3); });
    const glowa = new T.Mesh(new T.BoxGeometry(.5, .62, .5), [lam(0xbd8b72), lam(0xbd8b72), lam(0x6a4a30), lam(0xbd8b72), lam(0xffffff, twarz), lam(0xbd8b72)]);
    glowa.position.set(0, 1.62, 0); g.add(glowa); g.add(kloc(.12, .25, .12, lam(0xa06a55), 0, 1.5, .3));
    g.add(kloc(.5, .75, .38, lam(sz), 0, 1.0, 0)); g.add(kloc(.52, .12, .4, lam(pas), 0, .9, 0));
    g.add(kloc(.5, .62, .38, lam(sz), 0, .31, 0)); g.add(kloc(.62, .25, .25, lam(0xbd8b72), 0, 1.05, .25));
    g.position.set(o.x, o.y, o.z); g.rotation.y = -o.yaw * Math.PI / 180; return g;
  }

  // ------------------------------------------------------------------ scena
  window.renderuj = function (K) {
    const W = K.w || 1600, H = K.h || 900;
    const renderer = new T.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setSize(W, H); renderer.setPixelRatio(1); renderer.outputColorSpace = T.SRGBColorSpace;
    document.getElementById('gl').appendChild(renderer.domElement);
    const scene = new T.Scene();
    const horyzont = new T.Color(K.mgla || 0xbfdcff);
    scene.background = horyzont; scene.fog = new T.Fog(horyzont, K.mglaOd || 70, K.mglaDo || 320);
    // niebo gradient
    const sky = new T.Mesh(new T.SphereGeometry(900, 32, 16), new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false,
      uniforms: { top: { value: new T.Color(K.niebo || 0x5f9dee) }, bot: { value: horyzont } },
      vertexShader: 'varying vec3 p; void main(){p=normalize(position);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
      fragmentShader: 'uniform vec3 top; uniform vec3 bot; varying vec3 p; void main(){float t=clamp(p.y*2.2+0.1,0.,1.);gl_FragColor=vec4(mix(bot,top,t),1.);}' }));
    scene.add(sky);
    // słońce
    const slonce = new T.Mesh(new T.PlaneGeometry(60, 60), new T.MeshBasicMaterial({ color: 0xfff6c0, fog: false })); slonce.position.set(-300, 420, -500); slonce.lookAt(0, 150, 0); scene.add(slonce);
    // świat w dole
    const gc = document.createElement('canvas'); gc.width = gc.height = 256; const gg = gc.getContext('2d'); const rr = R(77);
    for (let y = 0; y < 256; y += 4) for (let x = 0; x < 256; x += 4) { const v = rr(); gg.fillStyle = v < .06 ? '#3d6fd0' : v < .25 ? '#3f7d2a' : `rgb(${85 + rr() * 25 | 0},${145 + rr() * 30 | 0},${50 + rr() * 15 | 0})`; gg.fillRect(x, y, 4, 4); }
    const gt = new T.CanvasTexture(gc); gt.wrapS = gt.wrapT = T.RepeatWrapping; gt.repeat.set(40, 40); gt.magFilter = T.NearestFilter; gt.colorSpace = T.SRGBColorSpace;
    const ziemia = new T.Mesh(new T.PlaneGeometry(6000, 6000), new T.MeshBasicMaterial({ map: gt })); ziemia.rotation.x = -Math.PI / 2; ziemia.position.y = 66; if (!K.bezZiemi) scene.add(ziemia);
    if (K.morze) { const m = new T.Mesh(new T.PlaneGeometry(6000, 6000), new T.MeshBasicMaterial({ color: 0x2f5fd0 })); m.rotation.x = -Math.PI / 2; m.position.y = K.morze; scene.add(m); }
    // chmury
    const cm = new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .85 }); const rc = R(9);
    for (let i = 0; i < (K.bezChmur ? 0 : 160); i++) { const w = 8 + rc() * 24, d = 8 + rc() * 24; const c = new T.Mesh(new T.BoxGeometry(w, 2, d), cm); c.position.set(-500 + rc() * 1000, 232, -500 + rc() * 1000); scene.add(c); }
    scene.add(new T.AmbientLight(0xffffff, 1.6)); const dl = new T.DirectionalLight(0xffffff, 1.4); dl.position.set(-3, 8, 4); scene.add(dl);
    budujSwiat(scene);
    // poświata latarni
    for (const [x, y, z, col] of swiatla) { const sp = new T.Sprite(new T.SpriteMaterial({ color: col, transparent: true, opacity: .35, blending: T.AdditiveBlending, depthWrite: false, map: glowTex() })); sp.position.set(x, y, z); sp.scale.set(2.2, 2.2, 1); scene.add(sp); }
    // promień beacona
    const beam = new T.Mesh(new T.BoxGeometry(.38, 260, .38), new T.MeshBasicMaterial({ color: 0xffa030, transparent: true, opacity: .75, blending: T.AdditiveBlending, depthWrite: false, fog: false }));
    beam.position.set(.5, 152 + 130, .5); if (!K.bezBeacona) scene.add(beam);
    const beam2 = new T.Mesh(new T.BoxGeometry(.75, 260, .75), new T.MeshBasicMaterial({ color: 0xff8a20, transparent: true, opacity: .2, blending: T.AdditiveBlending, depthWrite: false, fog: false }));
    beam2.position.copy(beam.position); if (!K.bezBeacona) scene.add(beam2);
    // encje z mapy
    for (const e of window.SCENA.encje) {
      if (e.typ === 'villager') scene.add(wiesniak(e));
      if (e.typ === 'text_display') { const n = napis(e.tekst, { wys: 0.25 * e.skala }); n.position.set(e.x, e.y, e.z); scene.add(n); }
    }
    // postacie scenki
    for (const p of K.postacie || []) { const g = postac(p); scene.add(g); if (g.userData.nick) scene.add(g.userData.nick); }
    for (const c of K.czasteczki || []) { const sp = new T.Sprite(new T.SpriteMaterial({ color: c.kolor, transparent: true, opacity: c.op || .9, blending: T.AdditiveBlending, depthWrite: false, map: glowTex() })); sp.position.set(c.x, c.y, c.z); sp.scale.set(c.r || .4, c.r || .4, 1); scene.add(sp); }
    const cam = new T.PerspectiveCamera(K.fov || 70, W / H, 0.05, 2000);
    cam.position.set(...K.kamera); cam.lookAt(new T.Vector3(...K.cel));
    renderer.render(scene, cam);
    return true;
  };
  let _glow = null;
  function glowTex() { if (_glow) return _glow; const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d');
    const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
    _glow = new T.CanvasTexture(c); return _glow; }
})();
