#!/usr/bin/env python3
"""Przygotowuje dane Ziemi dla pluginu DziobEarth.

Źródła (domena publiczna / wolne licencje, pobierane z PyPI):
  * global-land-mask 1.0.0  – maska ląd/ocean 1 km (GLOBE/NOAA)
  * basemap-data 2.0.0      – etopo1.jpg (relief ETOPO1, NOAA), bmng.jpg (NASA Blue Marble),
                              rivers_i.dat (rzeki, GSHHG/WDBII)

Użycie:
  pip download --no-deps basemap-data==2.0.0 global-land-mask==1.0.0 -d /tmp/geo
  python3 dane.py /tmp/geo  ->  ../../plugin-ziemia/src/main/resources/ziemia/*.bin.gz
"""
import gzip
import io
import math
import struct
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

TU = Path(__file__).resolve().parent
OUT = TU.parent.parent / "plugin-ziemia" / "src" / "main" / "resources" / "ziemia"

# Paleta ETOPO1 (m -> RGB)
PAL = [(0, 51, 102, 0), (100, 51, 204, 102), (200, 187, 228, 146), (500, 255, 220, 185), (1000, 243, 202, 137),
       (1500, 230, 184, 88), (2000, 217, 166, 39), (2500, 168, 154, 31), (3000, 164, 144, 25), (3500, 162, 134, 19),
       (4000, 159, 123, 13), (4500, 156, 113, 7), (5000, 153, 102, 0), (5500, 162, 89, 89), (6000, 178, 118, 118),
       (6500, 183, 147, 147), (7000, 194, 176, 176), (7500, 204, 204, 204), (8000, 229, 229, 229)]
# korekta (odczyt z barwy -> prawdziwa wysokość), dopasowana do punktów kontrolnych
KOREKTA = [(0, 0), (500, 400), (1100, 800), (1500, 1100), (2500, 1700), (3000, 2200), (4000, 2900),
           (5300, 3900), (6700, 5400), (8000, 6800)]

# Klasy biomów (muszą się zgadzać z Biomy.java)
B = dict(OCEAN=1, DEEP_OCEAN=2, WARM_OCEAN=3, LUKEWARM_OCEAN=4, DEEP_LUKEWARM_OCEAN=5, COLD_OCEAN=6,
         DEEP_COLD_OCEAN=7, FROZEN_OCEAN=8, DEEP_FROZEN_OCEAN=9, PLAINS=10, SUNFLOWER_PLAINS=11, FOREST=12,
         BIRCH_FOREST=13, DARK_FOREST=14, TAIGA=15, SNOWY_TAIGA=16, SNOWY_PLAINS=17, ICE_SPIKES=18, DESERT=19,
         BADLANDS=20, SAVANNA=21, SAVANNA_PLATEAU=22, JUNGLE=23, SPARSE_JUNGLE=24, BAMBOO_JUNGLE=25, SWAMP=26,
         MANGROVE_SWAMP=27, MEADOW=28, WINDSWEPT_HILLS=29, GROVE=30, SNOWY_SLOPES=31, JAGGED_PEAKS=32,
         FROZEN_PEAKS=33, STONY_PEAKS=34, CHERRY_GROVE=35, OLD_GROWTH_SPRUCE_TAIGA=36, FLOWER_FOREST=37,
         WINDSWEPT_SAVANNA=42, ERODED_BADLANDS=43, WOODED_BADLANDS=44, LADOLOD=50)


def wczytaj_z_whl(whl, nazwa):
    with zipfile.ZipFile(whl) as z:
        return z.read(nazwa)


def blur(a, r=1):
    """Średnia ruchoma (2r+1)x(2r+1) z zawijaniem w poziomie."""
    out = np.zeros_like(a, dtype=np.float64)
    n = 0
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out += np.roll(np.pad(a, ((r, r), (0, 0)), mode="edge")[r + dy:r + dy + a.shape[0]], dx, axis=1)
            n += 1
    return out / n


def wypelnij(a, zle, iteracje=60):
    """Wypełnia piksele 'zle' średnią z sąsiadów (proste inpainting)."""
    a = a.copy()
    znane = ~zle
    a[zle] = 0
    for _ in range(iteracje):
        if znane.all():
            break
        suma = blur(np.where(znane, a, 0), 1)
        ile = blur(znane.astype(np.float64), 1)
        nowe = (~znane) & (ile > 0)
        a[nowe] = (suma[nowe] / ile[nowe]).astype(a.dtype)
        znane = znane | nowe
    return a


def szum(shape, skala, seed):
    """Gładki losowy szum o zadanej skali (w pikselach), wartości ~[-1,1]."""
    rng = np.random.default_rng(seed)
    h, w = shape[0] // skala + 2, shape[1] // skala + 2
    m = rng.uniform(-1, 1, (h, w)).astype(np.float32)
    big = np.asarray(Image.fromarray(m, mode="F").resize((w * skala, h * skala), Image.BICUBIC))
    return big[:shape[0], :shape[1]]


def odleglosc(maska, maks):
    """Przybliżona odległość (w pikselach) od krawędzi maski – iteracyjna erozja."""
    d = np.zeros(maska.shape, np.float32)
    cur = maska.copy()
    for i in range(1, maks + 1):
        er = cur.copy()
        for sh in [(1, 0), (-1, 0), (1, 1), (-1, 1)]:
            er &= np.roll(cur, sh[0], axis=sh[1])
        d[cur & ~er] = i
        cur = er
        if not cur.any():
            break
    d[cur] = maks
    return d


def main(geo):
    geo = Path(geo)
    whl_glm = next(geo.glob("global_land_mask-*.whl"))
    whl_bd = next(geo.glob("basemap_data-*.whl"))
    OUT.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------- maska lądu 2 km
    npz = np.load(io.BytesIO(wczytaj_z_whl(whl_glm, "global_land_mask/globe_combined_mask_compressed.npz")))
    m1 = ~npz["mask"]                                 # w pliku True = ocean, odwracamy
    lad2 = m1.reshape(10800, 2, 21600, 2).mean(axis=(1, 3)) >= 0.5
    ls = np.frombuffer(gzip.decompress(wczytaj_z_whl(whl_bd, "mpl_toolkits/basemap_data/lsmask_1.25min_i.bin")), np.uint8)
    ls = ls.reshape(8640, 17280)[::-1]                # w pliku od bieguna płd.
    iy = (np.arange(10800) * 8640 // 10800)
    ix = (np.arange(21600) * 17280 // 21600)
    jez2 = (ls[iy][:, ix] == 2) & lad2
    print("ląd 2 km:", lad2.shape, f"{lad2.mean() * 100:.1f}% lądu, jeziora: {int(jez2.sum())} px")

    # ---------------------------------------------------------------- relief / wysokości 5400x2700
    ety = np.asarray(Image.open(io.BytesIO(wczytaj_z_whl(whl_bd, "mpl_toolkits/basemap_data/etopo1.jpg"))).convert("RGB")).astype(np.float32)
    H, W = ety.shape[:2]
    lad5 = lad2.reshape(2700, 4, 5400, 4).mean(axis=(1, 3))      # udział lądu w pikselu 5400
    gest = []
    for (e1, *c1), (e2, *c2) in zip(PAL, PAL[1:]):
        for tt in np.linspace(0, 1, int((e2 - e1) / 25), endpoint=False):
            gest.append((e1 + (e2 - e1) * tt, *[a + (b - a) * tt for a, b in zip(c1, c2)]))
    G = np.array(gest, np.float32)
    Gc = G[:, 1:] / (G[:, 1:].sum(1, keepdims=True) + 1e-6)
    Gl = G[:, 1:].max(1)
    # tablica: kolor skwantowany do 5 bitów/kanał -> wysokość
    q = np.arange(32) * 8 + 4.0
    kq = np.stack(np.meshgrid(q, q, q, indexing="ij"), -1).reshape(-1, 3)
    c = kq / (kq.sum(-1, keepdims=True) + 1e-6)
    d = ((c[:, None, :] - Gc[None]) ** 2).sum(-1) + 0.0000012 * (kq.max(-1)[:, None] - Gl[None]) ** 2
    lut = G[d.argmin(-1), 0].astype(np.float32)
    qi = (ety.astype(np.int32) >> 3)
    elev = lut[(qi[..., 0] << 10) | (qi[..., 1] << 5) | qi[..., 2]]
    ke, kr = zip(*KOREKTA)
    elev = np.interp(elev, ke, kr).astype(np.float32)
    jez5 = jez2.reshape(2700, 4, 5400, 4).mean(axis=(1, 3)) > 0.25
    niebieski = (ety[..., 2] > ety[..., 0] + 25) & (ety[..., 2] >= ety[..., 1])
    zle = (niebieski | jez5) & (lad5 >= 0.5)
    elev = wypelnij(elev, zle)
    elev = blur(blur(elev, 2), 2)

    # piksele przy oceanie mieszają kolor morza z lądem -> fałszywe "szczyty"; ograniczamy
    ladp0 = lad5 >= 0.5
    do_morza = odleglosc(ladp0, 8)
    limit = 250 + 380 * do_morza
    elev = np.where(ladp0 & (do_morza < 8), np.minimum(elev, limit), elev).astype(np.float32)
    lat5 = 90 - (np.arange(H) + 0.5) * 180 / H
    LAT = np.repeat(lat5[:, None], W, 1)
    jasn = ety.max(-1)
    sat = ety.max(-1) - ety.min(-1)
    lod = (jasn > 205) & (sat < 22) & (np.abs(LAT) > 58)
    lod = blur(lod.astype(np.float32), 1) > 0.5
    ladp = lad5 >= 0.5
    lod &= ladp
    dl = odleglosc(lod, 80)
    elev[lod] = np.minimum(3100, 120 + dl[lod] * 55)

    # głębokość oceanu z jasności błękitu
    L = (ety[..., 0] + ety[..., 1]) / 2
    glab = np.interp(L, [0, 60, 85, 130, 175, 200, 255], [9000, 5000, 4000, 1500, 200, 60, 20])
    glab = blur(glab, 1)
    do_brzegu = odleglosc(~ladp, 6)
    glab = np.minimum(glab, 40 + do_brzegu * 600)
    wys = np.where(ladp, np.maximum(np.round(elev / 10) * 10, 1), -np.round(glab / 50) * 50).astype(np.int16)

    # ---------------------------------------------------------------- biomy (zdjęcie NASA + szerokość + wysokość)
    bm = np.asarray(Image.open(io.BytesIO(wczytaj_z_whl(whl_bd, "mpl_toolkits/basemap_data/bmng.jpg"))).convert("RGB")).astype(np.float32)
    bm = np.stack([blur(bm[..., i], 1) for i in range(3)], -1)
    r, g, b = bm[..., 0], bm[..., 1], bm[..., 2]
    zielen = g - (r + b) / 2          # >0 roślinność
    jas = (r + g + b) / 3
    czerw = r - g                     # >0 czerwone pustynie
    alat = np.abs(LAT)
    lon5 = -180 + (np.arange(W) + 0.5) * 360 / W
    LON = np.repeat(lon5[None, :], H, 0)
    biom = np.zeros((H, W), np.uint8)

    n1 = szum((H, W), 40, 1) * 4          # rozmycie granic szerokości (stopnie)
    n2 = szum((H, W), 12, 2)              # łaty biomów
    alat = alat + n1
    lasy = (zielen > 3) & (jas < 34 + n2 * 4)
    gr = g / (r + 1)
    czerwona = (gr < 0.68) & (jas > 45) & ~lasy
    pustynia = (jas > 112) & (zielen < 9.5) & ~czerwona
    step = (zielen < 9.5) & ~pustynia & ~czerwona & ~lasy
    trawy = ~lasy & ~pustynia & ~czerwona & ~step
    sr = blur(elev, 2)
    rug = np.sqrt(np.maximum(blur(elev ** 2, 2) - sr ** 2, 0))   # poszarpanie terenu

    def ustaw(maska, nazwa):
        biom[maska & (biom == 0) & ladp] = B[nazwa]

    ustaw(lod, "LADOLOD")
    e = elev
    ustaw((e > 3800) & (rug > 550), "JAGGED_PEAKS")
    ustaw((e > 3000) & (rug > 380) & (alat > 28), "FROZEN_PEAKS")
    ustaw((e > 2800) & (rug > 380), "STONY_PEAKS")
    ustaw((e > 3000) & (alat > 26), "SNOWY_PLAINS")
    ustaw(e > 3000, "WINDSWEPT_HILLS")
    ustaw((e > 2200) & (rug > 250) & (alat > 35), "SNOWY_SLOPES")
    ustaw((e > 2000) & (rug > 200) & lasy, "GROVE")
    ustaw((e > 2000) & (rug > 200), "WINDSWEPT_HILLS")
    ustaw((LAT > 30) & (LAT < 42) & (LON > 129) & (LON < 146) & (lasy | trawy), "CHERRY_GROVE")
    ustaw((alat > 66) & (lasy | trawy) & (n2 > -0.2), "SNOWY_TAIGA")
    ustaw(alat > 64, "SNOWY_PLAINS")
    ustaw((alat > 57) & (lasy | trawy) & (n2 > 0.45), "OLD_GROWTH_SPRUCE_TAIGA")
    ustaw((alat > 55) & (lasy | trawy), "TAIGA")
    ustaw(alat > 55, "SNOWY_PLAINS")
    ustaw((e > 1400) & trawy & (alat < 50), "MEADOW")
    ustaw(czerwona & (n2 > 0.55), "ERODED_BADLANDS")
    ustaw(czerwona & (n2 < -0.5), "WOODED_BADLANDS")
    ustaw(czerwona, "BADLANDS")
    ustaw(pustynia, "DESERT")
    ustaw((alat < 11) & lasy & (n2 > 0.55), "BAMBOO_JUNGLE")
    ustaw((alat < 11) & lasy, "JUNGLE")
    ustaw((alat < 24) & lasy, "SPARSE_JUNGLE")
    ustaw((alat < 32) & step & (e > 900), "SAVANNA_PLATEAU")
    ustaw((alat < 32) & step, "SAVANNA")
    ustaw((alat < 32) & trawy & (n2 > 0.55), "SUNFLOWER_PLAINS")
    ustaw((alat < 32) & trawy & (zielen < 13), "SAVANNA")
    ustaw((alat < 32) & lasy, "SPARSE_JUNGLE")
    ustaw(lasy & (n2 > 0.5) & (alat < 50), "DARK_FOREST")
    ustaw(lasy & (n2 < -0.45), "BIRCH_FOREST")
    ustaw(lasy & (n2 > 0.3) & (n2 < 0.42), "FLOWER_FOREST")
    ustaw(lasy, "FOREST")
    ustaw(step & (e > 1200), "WINDSWEPT_SAVANNA")
    ustaw(trawy & (n2 > 0.6), "SUNFLOWER_PLAINS")
    ustaw(trawy & (n2 < -0.6) & (alat > 40), "TAIGA")
    ustaw(ladp, "PLAINS")
    # bagna: płasko, nisko i zielono przy wybrzeżach
    przy_brz = odleglosc(ladp, 3) <= 2
    tropik = alat < 22
    biom[ladp & przy_brz & tropik & lasy & (e < 60)] = B["MANGROVE_SWAMP"]
    biom[ladp & (e < 40) & lasy & (alat > 25) & (alat < 40) & przy_brz] = B["SWAMP"]
    biom[jez5 & ladp] = 38                  # jeziora -> RIVER (woda słodka)
    # oceany
    oc = ~ladp
    gleb = glab > 1200
    for nazwa, war in [("FROZEN_OCEAN", alat > 63), ("COLD_OCEAN", alat > 45), ("OCEAN", alat > 30),
                       ("LUKEWARM_OCEAN", alat > 18), ("WARM_OCEAN", alat >= 0)]:
        sel = oc & war & (biom == 0)
        gl = {"FROZEN_OCEAN": "DEEP_FROZEN_OCEAN", "COLD_OCEAN": "DEEP_COLD_OCEAN", "OCEAN": "DEEP_OCEAN",
              "LUKEWARM_OCEAN": "DEEP_LUKEWARM_OCEAN", "WARM_OCEAN": "WARM_OCEAN"}[nazwa]
        biom[sel & gleb] = B[gl]
        biom[sel & ~gleb] = B[nazwa]

    # ---------------------------------------------------------------- rzeki (2 km)
    meta = wczytaj_z_whl(whl_bd, "mpl_toolkits/basemap_data/riversmeta_i.dat").decode().split("\n")
    dane = wczytaj_z_whl(whl_bd, "mpl_toolkits/basemap_data/rivers_i.dat")
    rzeki = np.zeros(lad2.shape, bool)
    n_odc = 0
    for ln in meta:
        p = ln.split()
        if len(p) < 7:
            continue
        npts, off, cnt = int(p[2]), int(p[5]), int(p[6])
        if npts < 10:
            continue
        grub = 2 if npts >= 60 else 1
        xy = np.frombuffer(dane[off:off + cnt], "<f4").reshape(-1, 2)
        lo, la = xy[:, 0], xy[:, 1]
        px = (lo + 180) / 360 * 21600
        py = (90 - la) / 180 * 10800
        for i in range(len(px) - 1):
            k = int(max(abs(px[i + 1] - px[i]), abs(py[i + 1] - py[i])) * 2) + 1
            if k > 400:
                continue
            xs = np.linspace(px[i], px[i + 1], k).astype(int) % 21600
            ys = np.clip(np.linspace(py[i], py[i + 1], k).astype(int), 0, 10799)
            rzeki[ys, xs] = True
            if grub == 2:
                rzeki[np.clip(ys + 1, 0, 10799), xs] = True
                rzeki[ys, (xs + 1) % 21600] = True
        n_odc += 1
    rzeki &= lad2
    print("rzeki: odcinków", n_odc, "pikseli", int(rzeki.sum()))

    # ---------------------------------------------------------------- zapis
    def zapisz(nazwa, bajty):
        p = OUT / nazwa
        with gzip.open(p, "wb", compresslevel=9) as f:
            f.write(bajty)
        print(f"{nazwa}: {p.stat().st_size / 1e6:.2f} MB")

    zapisz("lad.bin.gz", struct.pack(">ii", 21600, 10800) + np.packbits(lad2, axis=1).tobytes())
    zapisz("jeziora.bin.gz", struct.pack(">ii", 21600, 10800) + np.packbits(jez2, axis=1).tobytes())
    zapisz("rzeki.bin.gz", struct.pack(">ii", 21600, 10800) + np.packbits(rzeki, axis=1).tobytes())
    zapisz("wys.bin.gz", struct.pack(">ii", W, H) + wys.astype(">i2").tobytes())
    zapisz("biom.bin.gz", struct.pack(">ii", W, H) + biom.tobytes())

    # podgląd
    kol = np.zeros((H, W, 3), np.uint8)
    paleta = {B["LADOLOD"]: (240, 245, 255), B["DESERT"]: (230, 210, 150), B["BADLANDS"]: (200, 110, 60),
              B["ERODED_BADLANDS"]: (190, 100, 60), B["WOODED_BADLANDS"]: (170, 120, 60), B["SAVANNA"]: (190, 180, 90),
              B["SAVANNA_PLATEAU"]: (170, 160, 80), B["WINDSWEPT_SAVANNA"]: (160, 150, 90), B["JUNGLE"]: (30, 120, 20),
              B["BAMBOO_JUNGLE"]: (60, 140, 30), B["SPARSE_JUNGLE"]: (70, 150, 40), B["FOREST"]: (50, 120, 50),
              B["DARK_FOREST"]: (30, 80, 30), B["BIRCH_FOREST"]: (90, 150, 80), B["FLOWER_FOREST"]: (100, 160, 70),
              B["TAIGA"]: (40, 90, 70), B["OLD_GROWTH_SPRUCE_TAIGA"]: (50, 80, 60), B["SNOWY_TAIGA"]: (180, 200, 200),
              B["SNOWY_PLAINS"]: (220, 230, 235), B["PLAINS"]: (120, 180, 80), B["SUNFLOWER_PLAINS"]: (140, 190, 70),
              B["MEADOW"]: (130, 200, 110), B["CHERRY_GROVE"]: (240, 160, 200), B["SWAMP"]: (70, 90, 50),
              B["MANGROVE_SWAMP"]: (60, 100, 50), B["WINDSWEPT_HILLS"]: (120, 130, 120), B["GROVE"]: (150, 180, 170),
              B["SNOWY_SLOPES"]: (210, 220, 230), B["JAGGED_PEAKS"]: (250, 250, 255), B["FROZEN_PEAKS"]: (235, 240, 250),
              B["STONY_PEAKS"]: (140, 140, 140)}
    for k, v in paleta.items():
        kol[biom == k] = v
    gl = np.clip(-wys.astype(np.float32) / 6000, 0, 1)
    for i, (a, bb) in enumerate([(70, 10), (130, 30), (220, 110)]):
        kol[..., i] = np.where(ladp, kol[..., i], (a * (1 - gl) + bb * gl).astype(np.uint8))
    rz5 = rzeki.reshape(2700, 4, 5400, 4).any(axis=(1, 3))
    kol[rz5] = (60, 120, 230)
    Image.fromarray(kol).save(TU / "podglad_biomy.png")
    w = np.clip(wys.astype(np.float32), -6000, 6000)
    img = np.where(w > 0, 60 + w / 6000 * 195, 0).astype(np.uint8)
    Image.fromarray(img).save(TU / "podglad_wysokosci.png")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/geo")
