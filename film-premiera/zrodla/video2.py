"""Silent premiere teaser #2 for Dziob.6mc.PL (24 December) - all-new scenes."""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from video import (text_img, paste, glow, pad_img, clamp, lin, eo_cubic, eo_back, ei_cubic, eo_bounce,
                   tex, shade, icon, gradient, tint, block_sprite, LOGO, mc_panel, slot, _sq, _glow,
                   VIGN, GRAIN, W, H)

FPS = 30
DUR = 34.0
T_LOAD, T_ISLAND, T_GIFTS, T_CAL, T_FIN = 0.0, 5.0, 11.0, 19.0, 26.0
BOUNDS = [T_ISLAND, T_GIFTS, T_CAL, T_FIN]
TR = 0.7  # transition length

# ---------------------------------------------------------------- textures
def _pal(r, cols, n=None):
    v = r.random((16, 16)) if n is None else n
    return np.array(cols)[np.minimum((v * len(cols)).astype(int), len(cols) - 1)]

def tex2(kind, seed=0):
    r = np.random.default_rng(seed + 17 * len(kind))
    snow = [(240, 246, 255), (226, 236, 250), (250, 252, 255), (214, 226, 244)]
    if kind == "snow": a = _pal(r, snow)
    elif kind == "snow_side":
        a = np.asarray(tex("dirt", seed)).copy(); s = _pal(r, snow)
        dep = 3 + (r.random(16) * 3).astype(int)
        for x in range(16): a[:dep[x], x] = s[:dep[x], x]
    elif kind == "spruce": a = _pal(r, [(38, 70, 44), (46, 84, 52), (30, 58, 36), (56, 96, 60)])
    elif kind == "spruce_snow":
        a = _pal(r, [(38, 70, 44), (46, 84, 52), (30, 58, 36)]); m = r.random((16, 16)) < 0.35
        a[m] = (235, 242, 255)
    elif kind in ("gift_r", "gift_g", "gift_b"):
        base = {"gift_r": [(200, 30, 40), (180, 24, 34), (215, 45, 55)],
                "gift_g": [(30, 140, 60), (24, 120, 50), (40, 160, 70)],
                "gift_b": [(40, 90, 210), (34, 76, 190), (55, 105, 225)]}[kind]
        a = _pal(r, base); a[:, 7:9] = (250, 210, 60); a[7:9, :] = (250, 210, 60)
    elif kind == "ice": a = _pal(r, [(140, 180, 250), (160, 200, 255), (120, 165, 240)])
    else: a = np.asarray(tex(kind, seed))
    return Image.fromarray(np.asarray(a).astype(np.uint8), "RGB")

def iso_cube(top, left, right, a, ls=0.78, rs=0.58):
    """Isometric cube sprite (2a x 2a) with textured faces."""
    S = 16 * 8
    def T(k): return tex2(k).resize((S, S), Image.NEAREST).convert("RGBA")
    out = Image.new("RGBA", (2 * a, 2 * a), (0, 0, 0, 0))
    tp = T(top).transform((2 * a, 2 * a), Image.AFFINE, (S / (2 * a), -S / a, S / 2, S / (2 * a), S / a, -S / 2), Image.NEAREST)
    lf = shade(T(left), ls).transform((2 * a, 2 * a), Image.AFFINE, (S / a, 0, 0, -S / (2 * a), S / a, -S / 2), Image.NEAREST)
    rt = shade(T(right), rs).transform((2 * a, 2 * a), Image.AFFINE, (S / a, 0, -S, S / (2 * a), S / a, -1.5 * S), Image.NEAREST)
    for f in (lf, rt, tp): out.alpha_composite(f)
    return out

A = 34
CUBE = {k: iso_cube(*v, A) for k, v in {
    "snow": ("snow", "snow_side", "snow_side"), "dirt": ("dirt", "dirt", "dirt"), "stone": ("stone", "stone", "stone"),
    "ore": ("stone", "diamond_ore", "diamond_ore"), "log": ("log", "log", "log"), "spruce": ("spruce_snow", "spruce", "spruce"),
    "gift_r": ("gift_r", "gift_r", "gift_r"), "gift_b": ("gift_b", "gift_b", "gift_b"), "ice": ("ice", "ice", "ice"),
    "gold": ("gold", "gold", "gold")}.items()}

# ---------------------------------------------------------------- island model
def build_island():
    r = np.random.default_rng(4); blocks = []
    N = 11; c = (N - 1) / 2
    for x in range(N):
        for y in range(N):
            d = math.hypot(x - c, y - c)
            if d > 5.3 + 0.4 * math.sin(x * 1.7 + y): continue
            top = 2 + (1 if d < 3 else 0) + (1 if d < 1.6 else 0)
            depth = int(max(1, (5.5 - d) * 1.4 + r.integers(0, 2)))
            for z in range(-depth, top + 1):
                if z == top: k = "snow"
                elif z >= top - 1: k = "dirt"
                else: k = "ore" if r.random() < 0.07 else "stone"
                blocks.append((x, y, z, k, d))
    # spruce tree at center
    cx = cy = int(c); base = 5
    for z in range(base, base + 3): blocks.append((cx, cy, z, "log", 0))
    for lvl, rad in [(base + 2, 2), (base + 3, 2), (base + 4, 1), (base + 5, 1), (base + 6, 0)]:
        for dx in range(-rad, rad + 1):
            for dy in range(-rad, rad + 1):
                if abs(dx) + abs(dy) <= rad + (0 if rad < 2 else 1) and not (dx == 0 and dy == 0 and lvl < base + 3):
                    blocks.append((cx + dx, cy + dy, lvl, "spruce", 0.5 + (lvl - base) * 0.2))
    # presents
    for (x, y, k) in [(3, 6, "gift_r"), (7, 3, "gift_b"), (6, 7, "gift_r"), (2, 4, "gift_b")]:
        topz = max(b[2] for b in blocks if b[0] == x and b[1] == y and b[3] == "snow")
        blocks.append((x, y, topz + 1, k, 7.0))
    blocks.sort(key=lambda b: (b[0] + b[1], b[2]))
    return blocks, N
ISLAND, IN = build_island()

def draw_island(img, t, t0, cx, cy, scale=1.0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for (x, y, z, k, d) in ISLAND:
        delay = t0 + d * 0.16 + (0.0 if k not in ("spruce", "log") else 1.2) + (z + 6) * 0.03 + (0.6 if k.startswith("gift") else 0)
        p = lin(t, delay, delay + 0.6)
        if p <= 0: continue
        off = (1 - eo_back(p, 1.5)) * 260 if k != "spruce" else 0
        sx = cx + (x - y) * A - A; sy = cy + (x + y) * A / 2 - z * A + off
        if k == "spruce":
            sp = eo_back(p, 2.5)
            if sp < 0.05: continue
            cube = CUBE[k].resize((max(1, int(2 * A * sp)), max(1, int(2 * A * sp))), Image.NEAREST)
            layer.alpha_composite(cube, (int(sx + A - cube.width / 2), int(sy + A - cube.height / 2)))
        else:
            if p < 1:
                cube = CUBE[k].copy(); cube.putalpha(cube.getchannel("A").point(lambda v: int(v * min(1, p * 3))))
                layer.alpha_composite(cube, (int(sx), int(sy)))
            else:
                layer.alpha_composite(CUBE[k], (int(sx), int(sy)))
    if scale != 1.0:
        layer = layer.resize((int(W * scale), int(H * scale)), Image.NEAREST)
        img.alpha_composite(layer, (int(W / 2 - layer.width / 2), int(H / 2 - layer.height / 2)))
    else:
        img.alpha_composite(layer)
    return cx, cy - 5.5 * A - 26  # star position above tree top

STAR = ["......Y......", ".....YYY.....", "....YYYYY....", "YYYYYYYYYYYYY", ".YYYYYYYYYYY.", "..YYYYYYYYY..",
        "...YYYYYYY...", "..YYYY.YYYY..", ".YYY.....YYY.", "YY.........YY"]
def star_img(s):
    a = np.zeros((len(STAR), 13, 4), np.uint8)
    for y, row in enumerate(STAR):
        for x, ch in enumerate(row):
            if ch == "Y": a[y, x] = (255, 225, 70, 255)
    return Image.fromarray(a, "RGBA").resize((13 * s, len(STAR) * s), Image.NEAREST)
STAR_IMG = glow(pad_img(star_img(6), 40), 20, 2.2)

# ---------------------------------------------------------------- common bits
SNOW_R = np.random.default_rng(5); NS = 320
SNOWP = (SNOW_R.uniform(0, W, NS), SNOW_R.uniform(0, H, NS), SNOW_R.uniform(30, 120, NS), SNOW_R.integers(3, 10, NS), SNOW_R.uniform(0, 6.3, NS))
def snow(arr, t, a=1.0, wind=20):
    xs, ys, sp, sz, ph = SNOWP
    for i in range(NS):
        y = (ys[i] + t * sp[i]) % (H + 40) - 20; x = (xs[i] + 35 * math.sin(t * 0.7 + ph[i]) + t * wind) % W
        s = int(sz[i]); y0, x0 = max(0, int(y)), int(x)
        arr[y0:y0 + s, x0:x0 + s] = arr[y0:y0 + s, x0:x0 + s] * (1 - 0.85 * a) + 250 * 0.85 * a

def to_arr(img): return np.asarray(img.convert("RGB")).astype(np.float32)
def to_img(arr): return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

def typed(img, s, t, t0, t1, size, col, cx, cy, fam="ps", cursor=True, outline=3, ocol=(0, 0, 0)):
    n = int(len(s) * lin(t, t0, t1))
    if t < t0: return
    full = text_img(s, size, col, fam, outline=outline, ocol=ocol)
    x0 = cx - full.width / 2
    if n: paste(img, text_img(s[:n], size, col, fam, outline=outline, ocol=ocol), x0, cy, anchor="l")
    if cursor and (n < len(s) or int(t * 3) % 2 == 0):
        w = text_img(s[:n], size, col, fam, outline=outline, ocol=ocol).width if n else 0
        ImageDraw.Draw(img).rectangle([x0 + w + 6, cy - size / 2, x0 + w + 6 + size * 0.6, cy + size / 2], fill=col + (255,))

# ---------------------------------------------------------------- scene 1: loading world
DIRT_BG = None
def dirt_bg():
    t1 = tex("dirt", 1).resize((128, 128), Image.NEAREST); bg = Image.new("RGB", (W + 128, H + 128))
    for x in range(0, W + 128, 128):
        for y in range(0, H + 128, 128): bg.paste(t1, (x, y))
    return shade(bg, 0.32).convert("RGBA")
DIRT_BG = dirt_bg()
TIPS = ["Generowanie terenu...", "Sypanie śniegu...", "Ubieranie choinki...", "Pakowanie prezentów..."]

def scene_load(t):
    off = int(t * 30) % 128
    img = DIRT_BG.crop((off, off, off + W, off + H))
    p = eo_cubic(lin(t, 0.6, 4.4))
    paste(img, text_img("Ładowanie świata", 56, (255, 255, 255), "ps", outline=3), W / 2, 380, lin(t, 0.2, 0.6))
    tip = TIPS[min(3, int(lin(t, 0.6, 4.4) * 4))]
    paste(img, text_img(tip, 34, (200, 200, 200), "px"), W / 2, 470, lin(t, 0.4, 0.8))
    d = ImageDraw.Draw(img); bw, bh = 900, 30; x0, y0 = W / 2 - bw / 2, 560
    d.rectangle([x0 - 6, y0 - 6, x0 + bw + 6, y0 + bh + 6], fill=(30, 30, 30, 255))
    d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(80, 80, 80, 255))
    d.rectangle([x0, y0, x0 + bw * p, y0 + bh], fill=(128, 255, 128, 255))
    d.rectangle([x0, y0, x0 + bw * p, y0 + 8], fill=(190, 255, 190, 255))
    paste(img, text_img(f"{int(p * 100)}%", 32, (255, 255, 255), "ps"), W / 2, 650, lin(t, 0.6, 0.9))
    # walking presents ticker under bar
    for i in range(4):
        x = x0 + bw * p - 40 - i * 70
        if x > x0: paste(img, icon("chest", 3), x, y0 - 50 - 6 * abs(math.sin(t * 8 + i)), 1)
    paste(img, text_img("DZIOB.6MC.PL", 30, (255, 220, 120), "ps"), W / 2, 960, lin(t, 1.0, 1.6))
    a = to_arr(img)
    snow(a, t, 0.5 * lin(t, 1.5, 3.0))
    return to_img(a * lin(t, 0, 0.5))

# ---------------------------------------------------------------- scene 2: floating island
SKY2 = gradient([(8, 14, 40), (20, 40, 90), (60, 90, 150), (120, 150, 200)])
STARS2 = [(np.random.default_rng(i).uniform(0, W), np.random.default_rng(i + 999).uniform(0, H * 0.6)) for i in range(150)]
def scene_island(t):
    img = Image.fromarray(SKY2.astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(img)
    for i, (x, y) in enumerate(STARS2):
        b = int(160 + 90 * math.sin(t * 3 + i)); d.rectangle([x, y, x + 3, y + 3], fill=(b, b, 255, 255))
    bob = math.sin(t * 1.3) * 12
    zoom = 1.3 + 0.12 * eo_cubic(lin(t, T_ISLAND, T_GIFTS))
    sx, sy = draw_island(img, t, T_ISLAND + 0.1, W / 2, 500 + bob, zoom)
    sp = lin(t, T_ISLAND + 3.4, T_ISLAND + 3.9)
    if sp > 0:
        paste(img, STAR_IMG, W / 2, H / 2 + (sy - H / 2) * zoom, 1, scale=eo_back(sp, 3) * (1 + 0.06 * math.sin(t * 6)))
    typed(img, "DZIOB.6MC.PL", t, T_ISLAND + 2.2, T_ISLAND + 3.4, 76, (255, 255, 255), W / 2, 110, outline=5, ocol=(20, 30, 80))
    pa = lin(t, T_ISLAND + 3.8, T_ISLAND + 4.3)
    if pa > 0: paste(img, text_img("Świąteczna premiera serwera Minecraft", 40, (190, 225, 255), "px", outline=3, ocol=(10, 20, 50)), W / 2, 1000 - (1 - eo_cubic(pa)) * 30, pa)
    a = to_arr(img); snow(a, t, 1.0)
    return to_img(a)

# ---------------------------------------------------------------- scene 3: gifts
GA = 95
GIFT_CUBES = [iso_cube(k, k, k, GA) for k in ("gift_r", "gift_g", "gift_b", "gift_r")]
def lid(k):
    c = iso_cube(k, k, k, GA); return c.crop((0, 0, 2 * GA, int(GA * 1.25)))
LIDS = [lid(k) for k in ("gift_r", "gift_g", "gift_b", "gift_r")]
FEATS = [("pickaxe", "NOWY ŚWIAT", "Świeża mapa"), ("sword", "PRZYGODA", "Odkrywaj i buduj"),
         ("chest", "EVENTY", "Konkursy i nagrody"), ("heart", "SPOŁECZNOŚĆ", "Graj ze znajomymi")]
GIFT_T = [T_GIFTS + 0.9 + 1.6 * i for i in range(4)]
def feat_label(i):
    ic, t1, t2 = FEATS[i]; w, h = 400, 300; im = mc_panel(w, h)
    sl = slot(130); sl.alpha_composite(icon(ic, 7), (9, 9)); im.alpha_composite(sl, (w // 2 - 65, 22))
    tt = text_img(t1, 40, (63, 63, 63), "px", shadow=False); im.alpha_composite(tt, (w // 2 - tt.width // 2, 170))
    t3 = text_img(t2, 30, (95, 95, 95), "pxr", shadow=False); im.alpha_composite(t3, (w // 2 - t3.width // 2, 228))
    return im
LABELS = [feat_label(i) for i in range(4)]
SKY3 = gradient([(70, 20, 30), (120, 30, 45), (60, 15, 30)])

def scene_gifts(t):
    img = Image.fromarray(SKY3.astype(np.uint8)).convert("RGBA")
    # diagonal candy stripes
    a = to_arr(img); yy, xx = np.mgrid[0:H:4, 0:W:4]
    stripes = ((((xx + yy + t * 120) // 90) % 2) * 14).astype(np.float32).repeat(4, 0).repeat(4, 1)[:H, :W, None]
    a = a + stripes
    # floor
    a[850:, :] = a[850:, :] * 0.12 + np.array([235, 240, 252]) * 0.88
    img = to_img(a)
    paste(img, text_img("CO ZNAJDZIESZ POD CHOINKĄ?", 52, (255, 255, 255), "ps", outline=4, ocol=(80, 10, 20)), W / 2, 110, lin(t, T_GIFTS + 0.1, T_GIFTS + 0.6), scale=0.9 + 0.1 * eo_back(lin(t, T_GIFTS + 0.1, T_GIFTS + 0.6)))
    addl = np.zeros((H, W, 3), np.float32); late = []
    for i, gt in enumerate(GIFT_T):
        gx = 270 + i * 460; gy = 760
        pin = lin(t, gt - 0.8, gt - 0.3)
        if pin <= 0: continue
        drop = (1 - eo_bounce(pin)) * -900
        wob = math.sin((t - gt) * 30) * 6 * (1 - lin(t, gt - 0.2, gt)) if t > gt - 0.3 else 0
        paste(img, GIFT_CUBES[i], gx + wob, gy + drop, 1)
        po = lin(t, gt, gt + 0.7)
        if po < 1:
            lx = gx + po * 140 * (1 if i % 2 else -1); ly = gy - GA * 0.38 + drop - eo_cubic(po) * 420 + 600 * po * po
            paste(img, LIDS[i], lx, ly, 1 - lin(po, 0.6, 1), rot=po * 160 * (1 if i % 2 else -1), resample=Image.NEAREST)
        if t >= gt:
            dt = t - gt
            # light beam
            beam = clamp(1 - dt / 1.2)
            if beam > 0:
                x0 = int(gx - 70); x1 = int(gx + 70)
                g = np.linspace(0, 1, gy - 60)[:, None, None]
                addl[0:gy - 60, x0:x1] += g * np.array([255, 230, 150]) * 0.5 * beam
            rr = np.random.default_rng(i)
            for k in range(40):  # confetti
                ang = rr.uniform(-math.pi * 0.9, -math.pi * 0.1); v = rr.uniform(300, 750)
                x = gx + math.cos(ang) * v * dt; y = gy - 60 + math.sin(ang) * v * dt + 500 * dt * dt
                col = np.array([(255, 80, 80), (255, 220, 60), (90, 220, 255), (120, 255, 120)][k % 4]) * clamp(1 - dt / 1.6)
                _sq(addl, x, y, 10 if k % 3 else 6, col)
            lp = eo_back(lin(t, gt + 0.15, gt + 0.65), 1.6)
            late.append((LABELS[i], gx, gy - 330 + (1 - lp) * 150, min(1, lin(t, gt + 0.15, gt + 0.4)), lp))
    a = to_arr(img) + addl
    img = to_img(a)
    for (lb, x, y, al, lp) in late: paste(img, lb, x, y, al, scale=max(0.05, lp), resample=Image.NEAREST)
    a = to_arr(img); snow(a, t, 0.6, wind=-15)
    return to_img(a)

# ---------------------------------------------------------------- scene 4: advent calendar
CW, CH, GAP = 196, 150, 18; COLS, ROWS = 6, 4
GX0 = W / 2 - (COLS * CW + (COLS - 1) * GAP) / 2; GY0 = 250
PLANK = tex("plank", 2).resize((CW, CH), Image.NEAREST).convert("RGBA")
def door(n, gold=False):
    im = PLANK.copy() if not gold else tex("gold", 1).resize((CW, CH), Image.NEAREST).convert("RGBA")
    d = ImageDraw.Draw(im); d.rectangle([0, 0, CW - 1, CH - 1], outline=(60, 40, 20, 255), width=6)
    num = text_img(str(n), 52, (255, 255, 255) if not gold else (120, 60, 0), "ps", outline=3, ocol=(70, 40, 10) if not gold else (255, 250, 200))
    im.alpha_composite(num, (CW // 2 - num.width // 2, CH // 2 - num.height // 2))
    d.rectangle([CW - 28, CH // 2 - 8, CW - 18, CH // 2 + 8], fill=(240, 200, 60, 255))
    return im
DOORS = [door(i + 1, gold=(i == 23)) for i in range(24)]
INSIDE_ICONS = ["chest", "heart", "sword", "pickaxe", "bird"]
def inside(i):
    im = Image.new("RGBA", (CW, CH), (25, 20, 45, 255))
    ic = icon(INSIDE_ICONS[i % 5], 6); im.alpha_composite(ic, (CW // 2 - 48, CH // 2 - 48)); return im
INSIDES = [inside(i) for i in range(24)]
OPEN_T = [T_CAL + 0.8 + i * 0.13 for i in range(23)]
Z24 = T_CAL + 4.5
SKY4 = gradient([(14, 30, 24), (24, 60, 40), (14, 30, 24)])

def scene_cal(t):
    img = Image.fromarray(SKY4.astype(np.uint8)).convert("RGBA")
    zp = eo_cubic(lin(t, Z24, Z24 + 0.9))
    paste(img, text_img("KALENDARZ ADWENTOWY", 56, (255, 255, 255), "ps", outline=4, ocol=(10, 50, 20)), W / 2, 150, lin(t, T_CAL + 0.1, T_CAL + 0.5) * (1 - zp))
    board = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i in range(24):
        c, r = i % COLS, i // COLS; x = GX0 + c * (CW + GAP); y = GY0 + r * (CH + GAP)
        pin = eo_back(lin(t, T_CAL + i * 0.03, T_CAL + i * 0.03 + 0.4))
        if pin <= 0: continue
        board.alpha_composite(INSIDES[i] if i < 23 else DOORS[i], (int(x), int(y)))
        if i < 23:
            op = eo_cubic(lin(t, OPEN_T[i], OPEN_T[i] + 0.35))
            w = int(CW * (1 - op * 0.88))
            if w > 2:
                dsp = DOORS[i].resize((w, CH), Image.NEAREST)
                dsp = shade(dsp, 1 - 0.4 * op)
                board.alpha_composite(dsp, (int(x), int(y)))
        else:
            if t > OPEN_T[-1]:
                sh = math.sin(t * 50) * 6 * lin(t, OPEN_T[-1] + 0.3, Z24)
                g = glow(pad_img(DOORS[23], 30), 20, 2.0 * (0.5 + 0.5 * math.sin(t * 8)))
                board.alpha_composite(g, (int(x - 30 + sh), int(y - 30)))
    if zp > 0:
        # zoom into door 24
        i = 23; c, r = i % COLS, i // COLS
        dx = GX0 + c * (CW + GAP) + CW / 2; dy = GY0 + r * (CH + GAP) + CH / 2
        s = 1 + zp * 9
        bw, bh = int(W * s), int(H * s)
        big = board.resize((bw, bh), Image.NEAREST)
        ox = int(W / 2 - dx * s * (zp) - W / 2 * (1 - zp) * s + W / 2 * (1 - zp))
        cx = dx + (W / 2 - dx) * 0  # keep math simple: interpolate focus point
        fx = dx * zp + W / 2 * (1 - zp); fy = dy * zp + H / 2 * (1 - zp)
        left = int(fx * s - W / 2); top = int(fy * s - H / 2)
        img.alpha_composite(big.crop((left, top, left + W, top + H)))
    else:
        img.alpha_composite(board)
    # reveal
    rp = lin(t, Z24 + 0.8, Z24 + 1.3)
    if rp > 0:
        wht = Image.new("RGBA", (W, H), (255, 245, 210, int(255 * (1 - lin(t, Z24 + 1.0, Z24 + 1.6)) * min(1, rp * 3))))
        bg = Image.fromarray(gradient([(90, 10, 20), (170, 30, 40), (90, 10, 20)]).astype(np.uint8)).convert("RGBA")
        bg.putalpha(int(255 * rp)); img.alpha_composite(bg)
        add_a = np.zeros((H, W, 3), np.float32)
        rr = np.random.default_rng(3)
        for k in range(60):
            ang = rr.uniform(0, 2 * math.pi); v = rr.uniform(200, 900); dt = t - Z24 - 0.8
            _sq(add_a, W / 2 + math.cos(ang) * v * dt, H / 2 + math.sin(ang) * v * dt + 200 * dt * dt, 12, np.array([255, 220, 80]) * clamp(1 - dt / 1.6))
        img = to_img(to_arr(img) + add_a)
        p1 = eo_back(lin(t, Z24 + 1.0, Z24 + 1.5), 2.0)
        big = glow(pad_img(text_img("24 GRUDNIA", 150, (255, 225, 70), "ps", outline=8, ocol=(90, 20, 0)), 40), 26, 1.8)
        paste(img, big, W / 2, 470, 1, scale=max(0.05, p1) * (1 + 0.025 * math.sin(t * 6)))
        p2 = lin(t, Z24 + 1.5, Z24 + 2.0)
        if p2 > 0: paste(img, text_img("WIGILIA  •  PREMIERA SERWERA", 50, (255, 255, 255), "ps", outline=4, ocol=(60, 0, 10)), W / 2, 680 + (1 - eo_cubic(p2)) * 40, p2)
        img.alpha_composite(wht)
    a = to_arr(img); snow(a, t, 0.7)
    return to_img(a)

# ---------------------------------------------------------------- scene 5: aurora finale
AY, AX = np.mgrid[0:135, 0:240].astype(np.float32)
def aurora(t):
    base = gradient([(4, 6, 22), (10, 18, 48), (20, 30, 70)], 135, 240).astype(np.float32)
    out = base.copy()
    for k, (col, sp, off) in enumerate([((40, 255, 160), 0.35, 0), ((90, 160, 255), 0.25, 2.0), ((200, 90, 255), 0.18, 4.0)]):
        cy = 40 + k * 10 + 10 * np.sin(AX / 30 + t * sp * 3 + off) + 6 * np.sin(AX / 11 - t * sp * 5)
        band = np.exp(-((AY - cy) / (7 + 3 * np.sin(AX / 17 + t))) ** 2)
        curtain = np.clip((AY < cy) * np.exp(-(cy - AY) / 18), 0, 1)
        inten = (0.55 + 0.45 * np.sin(AX / 9 + t * 2 + off)) * (0.8 - 0.2 * k)
        out += (band * 0.9 + curtain * 0.5)[..., None] * np.array(col) * inten[..., None] * 0.55
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    return im.convert("RGBA")

HILLS = None
def make_hills():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); B = 40
    r = np.random.default_rng(8)
    for layer, (base, col) in enumerate([(820, (150, 175, 215)), (900, (215, 228, 248))]):
        for i in range(W // B + 1):
            h = base + int(40 * math.sin(i / 5 + layer * 2) + 25 * math.sin(i / 2.3 + layer)) // B * B
            d.rectangle([i * B, h, (i + 1) * B - 1, H], fill=col + (255,))
            if layer == 0 and r.random() < 0.12:  # little spruces
                for j, w in enumerate([3, 3, 2, 1]):
                    d.rectangle([i * B - (w - 1) * 12, h - (j + 1) * 34, i * B + B - 1 + (w - 1) * 12, h - j * 34], fill=(30, 60, 50, 255))
    return im
HILLS = make_hills()

LOGO2 = []
_LS = 30; _LD = 10
_SPR2 = {"snow": block_sprite("stone", "stone", _LS, _LD)}
def _logo_sprites():
    # snowy gold blocks: gold front, white top
    g = block_sprite("gold", "gold", _LS, _LD)
    a = np.asarray(g).copy(); a[:_LD + 6, :, :3] = np.maximum(a[:_LD + 6, :, :3], 235); return Image.fromarray(a, "RGBA"), g
SNOWGOLD, GOLD = _logo_sprites()
lh, lw = LOGO.shape
for y in range(lh - 1, -1, -1):
    for x in range(lw):
        if LOGO[y, x]:
            d = math.hypot(x - lw / 2, (y - lh / 2) * 2)
            LOGO2.append((x, y, d, (y == 0 or not LOGO[y - 1, x])))
def draw_logo2(t, t0):
    im = Image.new("RGBA", (lw * _LS + _LD + 20, lh * _LS + _LD + 20), (0, 0, 0, 0))
    for (x, y, d, top) in LOGO2:
        p = lin(t, t0 + d * 0.035, t0 + d * 0.035 + 0.35)
        if p <= 0: continue
        sp = SNOWGOLD if top else GOLD
        s = eo_back(p, 2.6)
        if s < 0.99:
            spr = sp.resize((max(1, int(sp.width * s)), max(1, int(sp.height * s))), Image.NEAREST)
            im.alpha_composite(spr, (int(x * _LS + 10 + sp.width / 2 - spr.width / 2), int(y * _LS + 10 + sp.height / 2 - spr.height / 2)))
        else:
            im.alpha_composite(sp, (x * _LS + 10, y * _LS + 10))
    return im

def chat_box(t, t0):
    lines = [("<Mikołaj> ", (255, 85, 85), "Ho ho ho! Widzimy się 24 grudnia!"),
             ("<Mikołaj> ", (255, 85, 85), "IP: dziob.6mc.pl")]
    im = Image.new("RGBA", (1100, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = 10
    for i, (nm, nc, msg) in enumerate(lines):
        ts = t0 + i * 1.3
        if t < ts: continue
        d.rectangle([0, y - 6, 1100, y + 52], fill=(0, 0, 0, 130))
        a = text_img(nm, 34, nc, "px"); im.alpha_composite(a, (12, y))
        n = int(len(msg) * lin(t, ts, ts + 0.9))
        if n: im.alpha_composite(text_img(msg[:n], 34, (255, 255, 255), "px"), (12 + a.width, y))
        y += 64
    return im

LIGHT_COLS = [(255, 60, 60), (60, 255, 90), (255, 220, 60), (80, 160, 255)]
def lights(arr, t):
    n = 26
    for i in range(n + 1):
        x = i * W / n; sag = 40 * math.sin((x / (W / n)) % 1 * math.pi)
    for i in range(n * 3):
        u = i / (n * 3); x = u * W; seg = (u * n) % 1
        y = 20 + 46 * math.sin(seg * math.pi)
        _sq(arr, x, y, 4, np.array([30, 40, 30]))
    for i in range(n):
        x = (i + 0.5) * W / n; y = 20 + 46 + 14
        col = np.array(LIGHT_COLS[i % 4]); on = 0.35 + 0.65 * (math.sin(t * 5 + i * 1.3) > 0)
        _glow(arr, x, y, 34, col * 0.6 * on)
        _sq(arr, x, y, 14, col * on)

def scene_final(t):
    img = aurora(t)
    img.alpha_composite(HILLS)
    lg = draw_logo2(t, T_FIN + 0.3)
    bob = math.sin(t * 1.5) * 8
    gl = lg.filter(ImageFilter.GaussianBlur(20)); gl.putalpha(gl.getchannel("A").point(lambda v: int(v * 0.9 * lin(t, T_FIN + 1.2, T_FIN + 1.8))))
    gc = Image.new("RGBA", gl.size, (255, 210, 90, 0)); gc.putalpha(gl.getchannel("A"))
    paste(img, gc, W / 2, 300 + bob); paste(img, lg, W / 2, 300 + bob)
    p = eo_back(lin(t, T_FIN + 1.6, T_FIN + 2.1))
    if p > 0: paste(img, glow(pad_img(text_img(".6MC.PL", 70, (120, 235, 255), "ps", outline=4, ocol=(10, 30, 60)), 30), 16), W / 2, 520 + bob, min(1, p), scale=max(.05, p))
    p2 = lin(t, T_FIN + 2.3, T_FIN + 2.8)
    if p2 > 0:
        badge = mc_panel(1000, 130, dark=True)
        tt = text_img("PREMIERA 24.12", 56, (255, 225, 70), "ps", outline=3, ocol=(60, 20, 0)); badge.alpha_composite(tt, (500 - tt.width // 2, 65 - tt.height // 2))
        paste(img, badge, W / 2, 660, p2, scale=0.8 + 0.2 * eo_back(p2))
    cb = chat_box(t, T_FIN + 3.2)
    img.alpha_composite(cb, (40, 790))
    p3 = lin(t, T_FIN + 5.6, T_FIN + 6.0)
    if p3 > 0:
        sp = text_img("Wesołych Świąt!", 54, (255, 255, 0), "px", outline=3, ocol=(60, 60, 0))
        paste(img, sp, W - 330, 880, 1, scale=max(.05, eo_back(p3)) * (1 + 0.08 * abs(math.sin(t * 6))), rot=14, resample=Image.BICUBIC)
    a = to_arr(img); lights(a, t); snow(a, t, 1.0)
    return to_img(a * clamp((DUR - t) / 1.0))

# ---------------------------------------------------------------- transitions / render
SCENES = [(T_LOAD, scene_load), (T_ISLAND, scene_island), (T_GIFTS, scene_gifts), (T_CAL, scene_cal), (T_FIN, scene_final)]
def scene_at(t):
    return max(i for i, (s, _) in enumerate(SCENES) if s <= t)

CELL = 90
def block_wipe_mask(p, kind):
    """Squares grow along a diagonal wave (kind alternates direction)."""
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    nx, ny = W // CELL + 1, H // CELL + 1; maxd = nx + ny
    for i in range(nx):
        for j in range(ny):
            dd = (i + j) if kind % 2 == 0 else (nx - i + j)
            q = clamp(p * 2.2 - dd / maxd * 1.2)
            if q <= 0: continue
            s = CELL * q / 2; cx, cy = i * CELL + CELL / 2, j * CELL + CELL / 2
            d.rectangle([cx - s - 1, cy - s - 1, cx + s + 1, cy + s + 1], fill=255)
    return m

def render(fi):
    t = fi / FPS
    si = scene_at(t)
    img = SCENES[si][1](t)
    for k, b in enumerate(BOUNDS):
        if b - TR / 2 <= t < b + TR / 2:
            p = (t - (b - TR / 2)) / TR
            old = SCENES[k][1](t) if t >= b else img
            new = SCENES[k + 1][1](t) if t < b else img
            img = old.copy(); img.paste(new, (0, 0), block_wipe_mask(p, k))
    if si >= 1 and t < DUR - 1.2:
        paste(img, text_img("DZIOB.6MC.PL • 24.12", 22, (255, 255, 255), "ps"), W - 40, H - 40, 0.7, anchor="r")
    a = np.asarray(img.convert("RGB")).astype(np.float32) * VIGN + GRAIN[fi % 6] * 0.6
    return np.clip(a, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    from multiprocessing import Pool
    out = sys.argv[1]
    start = float(sys.argv[2]) if len(sys.argv) > 2 else 0; end = float(sys.argv[3]) if len(sys.argv) > 3 else DUR
    frames = range(int(start * FPS), int(end * FPS))
    if len(sys.argv) > 4:
        for f in frames[::max(1, int(float(sys.argv[4]) * FPS))]:
            Image.frombytes("RGB", (W, H), render(f)).save(f"{out}/s2_{f / FPS:05.2f}.jpg", quality=85)
        sys.exit()
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    with Pool(4) as p:
        for i, b in enumerate(p.imap(render, frames, chunksize=4)):
            ff.stdin.write(b)
            if i % 150 == 0: print("frame", i, flush=True)
    ff.stdin.close(); ff.wait()
