"""Silent premiere teaser #3 for Dziob.6mc.PL (24 December) - sleigh, portal, snow globe, slot machine, tree."""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from video import (text_img, paste, glow, pad_img, clamp, lin, eo_cubic, eo_back, ei_cubic, eo_bounce,
                   tex, shade, icon, gradient, mc_panel, _sq, _glow, VIGN, GRAIN, W, H)
from video2 import snow, to_arr, to_img, draw_logo2, star_img, tex2

FPS = 30
DUR = 36.0
T_SLEIGH, T_PORTAL, T_GLOBE, T_SLOT, T_TREE = 0.0, 6.5, 12.5, 19.5, 27.0

def pix(rows, cols, s):
    h = len(rows); w = max(len(r) for r in rows); a = np.zeros((h, w, 4), np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in cols: a[y, x] = cols[ch] + (255,)
    return Image.fromarray(a, "RGBA").resize((w * s, h * s), Image.NEAREST)

# ---------------------------------------------------------------- scene 1: sleigh writes the name
PC = {"R": (200, 30, 40), "r": (150, 20, 30), "Y": (250, 205, 60), "W": (245, 245, 250), "S": (240, 190, 160),
      "K": (30, 25, 25), "B": (120, 80, 45), "b": (90, 60, 35), "G": (40, 140, 60), "N": (220, 40, 40), "L": (170, 120, 70)}
SLEIGH = ["..........WW.........",
          ".........RRRW...GGG..",
          "........RRRRR..GYGYG.",
          ".......WSSSKW..GGGGG.",
          "..R....WWWWWW.LLLLLL.",
          ".RR...RRRRRRRRRRRRRR.",
          ".RYRRRRRRRRRRRRRRRRY.",
          "..RRRRRRRRRRRRRRRRR..",
          "...YYYYYYYYYYYYYYYY..",
          "..Y...Y.........Y...Y",
          ".YYYYYYYYYYYYYYYYYYY."]
DEER_A = ["..b.b......", "...bb......", "...BBK.....", "..BBBN.....", "BBBBBB.....", "BBBBBBBB...", ".BBBBBBBB..",
          ".B.B..B.B..", ".B.B..B.B.."]
DEER_B = ["..b.b......", "...bb......", "...BBK.....", "..BBBN.....", "BBBBBB.....", "BBBBBBBB...", ".BBBBBBBB..",
          "B...BB...B.", "B...BB...B."]
def _flip(im): return im.transpose(Image.FLIP_LEFT_RIGHT)
SLEIGH_IMG = _flip(pix(SLEIGH, PC, 13))
DEER = [_flip(pix(DEER_A, PC, 12)), _flip(pix(DEER_B, PC, 12))]

def village():
    im = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = np.random.default_rng(2)
    x = -20; wins = []
    while x < W:
        w = int(r.integers(5, 9)) * 24; h = int(r.integers(5, 9)) * 24; base = 420
        col = [(70, 50, 60), (60, 55, 80), (80, 60, 50)][int(r.integers(0, 3))]
        d.rectangle([x, base - h, x + w, base], fill=col + (255,))
        # stepped roof
        steps = w // 48
        for k in range(steps + 1):
            d.rectangle([x - 12 + k * 24, base - h - (k + 1) * 24, x + w + 12 - k * 24, base - h - k * 24], fill=(110, 40, 40, 255))
            d.rectangle([x - 12 + k * 24, base - h - (k + 1) * 24, x + w + 12 - k * 24, base - h - (k + 1) * 24 + 9], fill=(240, 245, 255, 255))
        if r.random() < 0.7:
            cx = x + w - 40; d.rectangle([cx, base - h - 90, cx + 24, base - h - 20], fill=(90, 80, 80, 255))
        for wy in range(base - h + 30, base - 30, 60):
            for wx in range(x + 24, x + w - 30, 60):
                if r.random() < 0.75: wins.append((wx, wy, r.uniform(0, 6)))
        x += w + int(r.integers(1, 4)) * 24
    d.rectangle([0, 395, W, 420], fill=(235, 240, 252, 255))
    return im, wins
VILLAGE, WINS = village()
SKY_N = gradient([(4, 6, 24), (14, 20, 60), (40, 40, 100), (80, 60, 120)])
STARS = [(float(x), float(y), int(s)) for x, y, s in zip(np.random.default_rng(1).uniform(0, W, 220), np.random.default_rng(2).uniform(0, 650, 220), np.random.default_rng(3).integers(2, 5, 220))]

def sleigh_pos(t):
    p = lin(t, 0.4, 4.6)
    x = -500 + p * (W + 1000)
    y = 300 + 60 * math.sin(p * math.pi * 2) - 80 * p
    return x, y

TITLE = text_img("DZIOB.6MC.PL", 110, (255, 230, 120), "ps", outline=6, ocol=(90, 40, 0))
TITLE_G = glow(pad_img(TITLE, 40), 22, 1.7)

def scene_sleigh(t):
    img = Image.fromarray(SKY_N.astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(img)
    for i, (x, y, s) in enumerate(STARS):
        b = int(170 + 80 * math.sin(t * 3 + i)); d.rectangle([x, y, x + s, y + s], fill=(b, b, 255, 255))
    # moon
    g = Image.new("RGBA", (600, 600), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([150, 150, 450, 450], fill=(220, 230, 255, 90))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(60)), (1250, -120))
    d.rectangle([1460, 90, 1640, 270], fill=(236, 240, 252, 255)); d.rectangle([1500, 130, 1540, 170], fill=(205, 212, 232, 255)); d.rectangle([1570, 200, 1610, 240], fill=(205, 212, 232, 255))
    img.alpha_composite(VILLAGE, (0, H - 420))
    a = to_arr(img)
    for (wx, wy, ph) in WINS:
        on = 0.75 + 0.25 * math.sin(t * 2 + ph)
        a[H - 420 + wy:H - 420 + wy + 24, wx:wx + 18] = np.array([255, 210, 110]) * on
        _glow(a, wx + 9, H - 420 + wy + 12, 30, np.array([120, 80, 20]) * on)
    # trail sparkles
    sx, sy = sleigh_pos(t)
    rr = np.random.default_rng(11)
    for k in range(70):
        dt = k * 0.03; tx, ty = sleigh_pos(t - dt)
        if t - dt < 0.4: break
        jx, jy = rr.normal(0, 14, 2)
        col = np.array([255, 230, 140]) * clamp(1 - dt / 2.1)
        _sq(a, tx - 100 + jx, ty + 40 + jy + dt * 40, 6 if k % 3 else 9, col)
    img = to_img(a)
    # name revealed behind sleigh
    reveal = sx + 60
    tx0 = W / 2 - TITLE_G.width / 2
    if reveal > tx0:
        cw = int(min(TITLE_G.width, reveal - tx0))
        if cw > 0:
            part = TITLE_G.crop((0, 0, cw, TITLE_G.height))
            img.alpha_composite(part, (int(tx0), int(480 - TITLE_G.height / 2)))
    # reindeer + sleigh
    fr = int(t * 8) % 2
    for k in range(2):
        dx = sx + 330 + k * 170; dy = sy + 30 + 8 * math.sin(t * 8 + k)
        paste(img, DEER[(fr + k) % 2], dx, dy, 1)
    ImageDraw.Draw(img).line([(sx + 120, sy + 10), (sx + 300, sy + 40)], fill=(200, 170, 110, 255), width=4)
    paste(img, SLEIGH_IMG, sx, sy, 1)
    p = lin(t, 4.6, 5.2)
    if p > 0: paste(img, text_img("zaprasza na świąteczną premierę", 46, (220, 235, 255), "px", outline=3, ocol=(10, 15, 40)), W / 2, 610 + (1 - eo_cubic(p)) * 30, p)
    a = to_arr(img); snow(a, t, 0.8)
    return to_img(a * lin(t, 0, 0.5))

# ---------------------------------------------------------------- scene 2: Christmas portal
PB = 96; PW, PH = 4, 5  # interior blocks
OBS = tex("obsidian", 3).resize((PB, PB), Image.NEAREST).convert("RGBA")
FX0 = int(W / 2 - (PW + 2) * PB / 2); FY0 = int(H / 2 - (PH + 2) * PB / 2) + 40
PY, PX = np.mgrid[0:PH * 16, 0:PW * 16].astype(np.float32)
def portal_tex(t):
    cx, cy = PW * 8, PH * 8
    ang = np.arctan2(PY - cy, PX - cx); rad = np.hypot(PX - cx, PY - cy)
    v = np.sin(ang * 3 + rad * 0.35 - t * 4) * 0.5 + np.sin(PX * 0.4 + t * 2) * 0.25 + np.sin(PY * 0.33 - t * 3) * 0.25
    v = (v + 1) / 2
    c1 = np.array([60, 140, 255]); c2 = np.array([220, 240, 255]); c3 = np.array([150, 60, 230])
    col = np.where(v[..., None] > 0.6, c1 + (c2 - c1) * ((v[..., None] - 0.6) / 0.4), c3 + (c1 - c3) * (v[..., None] / 0.6))
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).resize((PW * PB, PH * PB), Image.NEAREST).convert("RGBA")
    im.putalpha(215); return im

def scene_portal(t):
    img = Image.fromarray(gradient([(6, 10, 30), (12, 24, 60), (6, 10, 30)]).astype(np.uint8)).convert("RGBA")
    lt = t - T_PORTAL
    # frame builds block by block
    frame = [(i, 0) for i in range(PW + 2)] + [(PW + 1, j) for j in range(1, PH + 2)] + [(i, PH + 1) for i in range(PW, -1, -1)] + [(0, j) for j in range(PH, 0, -1)]
    lit = lin(t, T_PORTAL + 1.9, T_PORTAL + 2.4)
    if lit > 0:
        pt = portal_tex(t)
        g = pt.filter(ImageFilter.GaussianBlur(40)); g.putalpha(int(200 * lit))
        img.alpha_composite(g, (FX0 + PB, FY0 + PB))
        pt.putalpha(int(215 * lit)); img.alpha_composite(pt, (FX0 + PB, FY0 + PB))
    for n, (i, j) in enumerate(frame):
        p = lin(t, T_PORTAL + 0.2 + n * 0.08, T_PORTAL + 0.5 + n * 0.08)
        if p <= 0: continue
        paste(img, OBS, FX0 + i * PB + PB / 2, FY0 + j * PB + PB / 2 - (1 - eo_bounce(p)) * 400, 1)
    # snowflake ornaments on frame corners when lit
    a = to_arr(img)
    if lit > 0:
        rr = np.random.default_rng(4)
        for k in range(60):
            ph = rr.uniform(0, 10); sp = rr.uniform(40, 120)
            life = ((t * 0.6 + ph) % 2.0) / 2.0
            x = W / 2 + rr.normal(0, 140); y = FY0 + PB + PH * PB * rr.uniform(0, 1) - life * sp * 2
            _sq(a, x + math.sin(t * 2 + ph) * 60 * life, y, 6, np.array([170, 210, 255]) * (1 - life) * lit)
    img = to_img(a)
    paste(img, text_img("PRZEJDŹ PRZEZ PORTAL...", 50, (200, 225, 255), "ps", outline=4, ocol=(10, 20, 60)), W / 2, 90, lin(t, T_PORTAL + 2.4, T_PORTAL + 2.9) * (1 - lin(t, T_PORTAL + 3.6, T_PORTAL + 3.9)))
    # zoom-in
    z = lin(t, T_PORTAL + 3.6, T_GLOBE)
    if z > 0:
        s = 1 + (ei_cubic(z)) * 14
        cx, cy = W / 2, FY0 + (PH + 2) * PB / 2
        bw, bh = int(W * s), int(H * s)
        big = img.resize((bw, bh), Image.BILINEAR if s < 4 else Image.NEAREST)
        left = int(cx * s - W / 2); top = int(cy * s - H / 2)
        img = big.crop((left, top, left + W, top + H))
        a = to_arr(img)
        # warp streaks
        rr = np.random.default_rng(int(t * 30))
        streak = Image.new("L", (W, H), 0); d = ImageDraw.Draw(streak)
        for k in range(int(80 * z)):
            ang = rr.uniform(0, 2 * math.pi); r0 = rr.uniform(80, 600); r1 = r0 + rr.uniform(100, 500) * z
            d.line([(W / 2 + math.cos(ang) * r0, H / 2 + math.sin(ang) * r0), (W / 2 + math.cos(ang) * r1, H / 2 + math.sin(ang) * r1)], fill=255, width=3)
        a = a + (np.asarray(streak, np.float32)[..., None] / 255) * np.array([200, 230, 255]) * z
        a = a + 255 * lin(t, T_GLOBE - 0.35, T_GLOBE)
        img = to_img(a)
    else:
        a = to_arr(img); snow(a, t, 0.5); img = to_img(a)
    return img

# ---------------------------------------------------------------- scene 3: snow globe
GR = 330; GCX, GCY = W // 2, 440
def globe_inside(t, shake_amt):
    im = Image.new("RGBA", (2 * GR, 2 * GR), (0, 0, 0, 0))
    bg = Image.fromarray(gradient([(20, 40, 100), (60, 100, 170), (150, 190, 235)], 2 * GR, 2 * GR).astype(np.uint8)).convert("RGBA")
    im.alpha_composite(bg)
    lg = draw_logo2(99, 0)  # settled logo
    lg = lg.resize((int(lg.width * 0.5), int(lg.height * 0.5)), Image.NEAREST)
    im.alpha_composite(lg, (GR - lg.width // 2, GR - 40 - lg.height // 2))
    d = ImageDraw.Draw(im)
    # snowy ground + mini trees inside
    for i in range(0, 2 * GR, 30):
        h = GR + 150 + int(18 * math.sin(i / 50)) // 15 * 15
        d.rectangle([i, h, i + 29, 2 * GR], fill=(235, 242, 255, 255))
    for tx in (GR - 220, GR + 170):
        for j, w in enumerate([5, 4, 3, 2, 1]):
            d.rectangle([tx - w * 9, GR + 140 - j * 26 - 26, tx + w * 9, GR + 140 - j * 26], fill=(30, 90, 55, 255))
    a = to_arr(im)
    rr = np.random.default_rng(9); n = 180
    for k in range(n):
        ph = rr.uniform(0, 6.28); r = rr.uniform(0, GR * 0.95); sp = rr.uniform(0.5, 1.5)
        swirl = shake_amt * 3.0
        ang = ph + swirl * sp + t * 0.2 * sp
        x = GR + math.cos(ang) * r * 0.9
        fall = (t * 25 * sp + ph * 50) % (2 * GR)
        y = (GR + math.sin(ang) * r * 0.9) * min(1, shake_amt * 2) + fall * (1 - min(1, shake_amt * 2))
        _sq(a, x, y, 7 if k % 3 else 5, np.array([255, 255, 255]) * 0.85)
    im = to_img(a)
    m = Image.new("L", (2 * GR, 2 * GR), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * GR - 1, 2 * GR - 1], fill=255)
    im.putalpha(m)
    # glass rim + highlight
    hl = Image.new("RGBA", (2 * GR, 2 * GR), (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
    hd.ellipse([0, 0, 2 * GR - 1, 2 * GR - 1], outline=(220, 240, 255, 200), width=10)
    hd.arc([60, 50, 2 * GR - 60, 2 * GR - 60], 200, 250, fill=(255, 255, 255, 170), width=26)
    im.alpha_composite(hl)
    return im

def base_img():
    w, h = 640, 190; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pl = tex("plank", 4).resize((w, h), Image.NEAREST).convert("RGBA")
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).polygon([(70, 0), (w - 70, 0), (w, h), (0, h)], fill=255)
    im.paste(pl, (0, 0), m)
    d.rectangle([150, 70, w - 150, 150], fill=(235, 190, 60, 255), outline=(140, 90, 20, 255), width=5)
    tt = text_img("24.12", 46, (110, 60, 10), "ps", shadow=False); im.alpha_composite(tt, (w // 2 - tt.width // 2, 110 - tt.height // 2))
    return im
BASE = base_img()
ROOM = gradient([(40, 12, 16), (70, 20, 26), (30, 10, 14)])
BOKEH = [(float(x), float(y), float(r), c) for x, y, r, c in zip(np.random.default_rng(6).uniform(0, W, 30), np.random.default_rng(7).uniform(0, H, 30), np.random.default_rng(8).uniform(30, 90, 30), np.random.default_rng(9).integers(0, 4, 30))]
BCOL = [(255, 200, 90), (255, 80, 80), (90, 220, 120), (120, 170, 255)]

def scene_globe(t):
    img = Image.fromarray(ROOM.astype(np.uint8)).convert("RGBA")
    bk = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bk)
    for i, (x, y, r, c) in enumerate(BOKEH):
        a = int(60 + 40 * math.sin(t * 1.5 + i)); bd.ellipse([x - r, y - r, x + r, y + r], fill=BCOL[c] + (a,))
    img.alpha_composite(bk.filter(ImageFilter.GaussianBlur(14)))
    lt = t - T_GLOBE
    shake = lin(t, T_GLOBE + 1.6, T_GLOBE + 1.8) * (1 - lin(t, T_GLOBE + 3.0, T_GLOBE + 3.3))
    rot = math.sin(t * 28) * 7 * shake
    swirl = clamp(lin(t, T_GLOBE + 1.6, T_GLOBE + 2.2) * (1 - lin(t, T_GLOBE + 3.2, T_GLOBE + 6.0)))
    drop = (1 - eo_bounce(lin(t, T_GLOBE + 0.1, T_GLOBE + 1.0))) * -900
    gl = globe_inside(t, swirl)
    grp = Image.new("RGBA", (2 * GR + 40, 2 * GR + 200), (0, 0, 0, 0))
    grp.alpha_composite(BASE.resize((560, 170)), (GR + 20 - 280, 2 * GR - 30))
    grp.alpha_composite(gl, (20, 0))
    paste(img, grp, GCX, GCY + 90 + drop, 1, rot=rot, resample=Image.BICUBIC)
    p = lin(t, T_GLOBE + 1.0, T_GLOBE + 1.5)
    paste(img, text_img("WSTRZĄŚNIJ ŚWIĄTEM!", 50, (255, 235, 200), "ps", outline=4, ocol=(60, 10, 10)), W / 2, 70, p * (1 - lin(t, T_GLOBE + 3.4, T_GLOBE + 3.8)))
    p2 = lin(t, T_GLOBE + 3.8, T_GLOBE + 4.3)
    if p2 > 0:
        paste(img, text_img("Świąteczna premiera serwera", 50, (255, 235, 200), "px", outline=3, ocol=(60, 10, 10)), W / 2, 70 + (1 - eo_cubic(p2)) * -30, p2)
    a = to_arr(img)
    return to_img(a)

# ---------------------------------------------------------------- scene 4: slot machine draws the date
DIG = [text_img(str(d), 150, (40, 20, 10), "ps", shadow=False) for d in range(10)]
RW, RH, CELLH = 190, 250, 230
def reel_strip():
    im = Image.new("RGBA", (RW, CELLH * 10), (245, 240, 225, 255))
    for d in range(10):
        im.alpha_composite(DIG[d], (RW // 2 - DIG[d].width // 2, d * CELLH + CELLH // 2 - DIG[d].height // 2))
    return im
STRIP = reel_strip()
TARGETS = [2, 4, 1, 2]
STOPS = [T_SLOT + 2.4 + 0.7 * i for i in range(4)]
def reel(t, i):
    out = Image.new("RGBA", (RW, RH), (245, 240, 225, 255))
    start = T_SLOT + 0.8
    stop = STOPS[i]
    speed = 2600.0
    target_off = TARGETS[i] * CELLH - (RH - CELLH) / 2
    if t < start: off = target_off * 0 + 3 * CELLH
    elif t < stop - 0.5:
        off = (t - start) * speed
    else:
        # decelerate to target with bounce
        p = lin(t, stop - 0.5, stop + 0.15)
        base_off = (stop - 0.5 - start) * speed
        full = CELLH * 10
        end = math.ceil((base_off + 400) / full) * full + target_off
        off = base_off + (end - base_off) * eo_back(p, 1.3)
    off = off % (CELLH * 10)
    strip2 = Image.new("RGBA", (RW, CELLH * 20)); strip2.paste(STRIP, (0, 0)); strip2.paste(STRIP, (0, CELLH * 10))
    win = strip2.crop((0, int(off), RW, int(off) + RH))
    moving = start <= t < stop - 0.1
    if moving:
        win = win.filter(ImageFilter.BoxBlur(0)).resize((RW, RH // 8)).resize((RW, RH), Image.BILINEAR)
    out.alpha_composite(win)
    sh = Image.new("RGBA", (RW, RH), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    for k in range(40):
        a = int(110 * (1 - k / 40)); d.line([(0, k), (RW, k)], fill=(0, 0, 0, a)); d.line([(0, RH - 1 - k), (RW, RH - 1 - k)], fill=(0, 0, 0, a))
    out.alpha_composite(sh)
    return out

def machine():
    w, h = 1200, 560; im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gold = tex("gold", 2).resize((64, 64), Image.NEAREST).convert("RGBA")
    for x in range(0, w, 64):
        for y in range(0, h, 64): im.alpha_composite(gold, (x, y))
    d = ImageDraw.Draw(im)
    d.rectangle([40, 120, w - 40, h - 40], fill=(40, 10, 10, 255))
    d.rectangle([0, 0, w - 1, h - 1], outline=(130, 80, 10, 255), width=10)
    return im
MACHINE = machine()
REEL_X = [W / 2 - 480, W / 2 - 230, W / 2 + 120, W / 2 + 370]
LAMP = [(255, 60, 60), (255, 220, 60), (60, 255, 120), (80, 160, 255)]

def scene_slot(t):
    img = Image.fromarray(gradient([(20, 6, 30), (50, 12, 60), (20, 6, 30)]).astype(np.uint8)).convert("RGBA")
    a = to_arr(img)
    # rotating spotlight wedges
    yy, xx = np.ogrid[0:H:4, 0:W:4]
    ang = np.arctan2(yy - H / 2, xx - W / 2) + t * 0.6
    wedge = ((np.sin(ang * 10) > 0.6) * 18).astype(np.float32).repeat(4, 0).repeat(4, 1)[:H, :W, None]
    img = to_img(a + wedge)
    enter = eo_back(lin(t, T_SLOT + 0.1, T_SLOT + 0.7), 1.3)
    my = 560 + (1 - enter) * 900
    paste(img, MACHINE, W / 2, my, 1)
    paste(img, text_img("LOSUJEMY DATĘ PREMIERY...", 46, (255, 240, 200), "ps", outline=4, ocol=(60, 10, 40)), W / 2, 150, lin(t, T_SLOT + 0.5, T_SLOT + 0.9))
    for i in range(4):
        r = reel(t, i)
        paste(img, r, REEL_X[i] + RW / 2, my + 40, 1)
        if t >= STOPS[i] + 0.1:
            fl = clamp(1 - (t - STOPS[i] - 0.1) / 0.5)
            if fl > 0:
                ov = Image.new("RGBA", (RW, RH), (255, 255, 200, int(150 * fl))); paste(img, ov, REEL_X[i] + RW / 2, my + 40, 1)
    # dot between day and month
    d = ImageDraw.Draw(img); d.rectangle([W / 2 - 10 + 50 - 50, my + 120, W / 2 + 26 - 50 + 50 - 26 + 10, my + 156], fill=(255, 220, 60, 255))
    a = to_arr(img)
    # lamps on top of the machine
    win = t > STOPS[-1] + 0.2
    for k in range(14):
        x = W / 2 - 560 + k * 86; y = my - 240
        on = (int(t * (10 if win else 3)) + k) % 2 == 0
        c = np.array(LAMP[k % 4]) * (1 if on else 0.25)
        _sq(a, x, y, 26, c); _glow(a, x, y, 50, c * 0.5)
    if win:
        dt = t - STOPS[-1] - 0.2
        rr = np.random.default_rng(12)
        for k in range(80):
            ang = rr.uniform(-math.pi, 0); v = rr.uniform(400, 1100)
            x = W / 2 + math.cos(ang) * v * dt; y = my + math.sin(ang) * v * dt + 900 * dt * dt
            _sq(a, x, y, 16, np.array([255, 205, 50]) * clamp(1 - dt / 2.5))
            _sq(a, x - 3, y - 3, 6, np.array([255, 255, 200]) * clamp(1 - dt / 2.5))
    img = to_img(a)
    if win:
        p = eo_back(lin(t, STOPS[-1] + 0.3, STOPS[-1] + 0.8), 2.2)
        jp = glow(pad_img(text_img("JACKPOT! PREMIERA 24 GRUDNIA", 50, (255, 235, 80), "ps", outline=5, ocol=(90, 20, 0)), 30), 20, 1.8)
        paste(img, jp, W / 2, 990, 1, scale=max(0.05, p) * (1 + 0.03 * math.sin(t * 9)))
    return img

# ---------------------------------------------------------------- scene 5: decorating the tree
TB = 46
TREE_ROWS = [1, 3, 3, 5, 5, 7, 7, 9, 9, 11, 11, 13, 13, 15]
SPR = tex2("spruce", 1).resize((TB, TB), Image.NEAREST).convert("RGBA")
SPRS = tex2("spruce_snow", 2).resize((TB, TB), Image.NEAREST).convert("RGBA")
LOG = tex("log", 1).resize((TB, TB), Image.NEAREST).convert("RGBA")
def tree_img():
    w = 15 * TB; h = (len(TREE_ROWS) + 3) * TB; im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for j, n in enumerate(TREE_ROWS):
        x0 = (15 - n) // 2
        for i in range(n): im.alpha_composite(SPRS if (j + i) % 3 == 0 else SPR, ((x0 + i) * TB, j * TB))
    for j in range(3): im.alpha_composite(LOG, (7 * TB, (len(TREE_ROWS) + j) * TB))
    return im
TREE = tree_img()
_rr = np.random.default_rng(21); ORN = []
for j, n in enumerate(TREE_ROWS[1:], 1):
    for i in range(n):
        if _rr.random() < 0.28:
            ORN.append((((15 - n) // 2 + i) * TB + TB / 2, j * TB + TB / 2, int(_rr.integers(0, 4)), float(_rr.uniform(0, 1))))
ORN.sort(key=lambda o: o[3])
OCOL = [(230, 40, 50), (250, 205, 60), (70, 140, 255), (200, 80, 255)]
def ornament(c, s=26):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([4, 4, s - 5, s - 5], fill=OCOL[c] + (255,)); d.rectangle([0, 8, s - 1, s - 9], fill=OCOL[c] + (255,)); d.rectangle([8, 0, s - 9, s - 1], fill=OCOL[c] + (255,))
    d.rectangle([7, 6, 12, 11], fill=(255, 255, 255, 220)); return im
ORN_IMG = [ornament(c) for c in range(4)]
STAR = glow(pad_img(star_img(7), 40), 22, 2.2)
GROUND = gradient([(20, 24, 50), (40, 50, 90), (70, 80, 130)])

def scene_tree(t):
    img = Image.fromarray(GROUND.astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(img)
    for i in range(0, W, 40):
        h = 900 + int(20 * math.sin(i / 120)) // 20 * 20
        d.rectangle([i, h, i + 39, H], fill=(230, 238, 252, 255))
    lt = t - T_TREE
    slide = eo_cubic(lin(t, T_TREE + 4.2, T_TREE + 5.0))
    tx = W / 2 - slide * 480
    grow = eo_back(lin(t, T_TREE + 0.2, T_TREE + 0.9), 1.6)
    tree = TREE.copy()
    for k, (ox, oy, c, ord_) in enumerate(ORN):
        tt = T_TREE + 1.0 + ord_ * 2.0
        p = eo_back(lin(t, tt, tt + 0.25), 3)
        if p > 0:
            o = ORN_IMG[c].resize((max(1, int(26 * p)), max(1, int(26 * p))), Image.NEAREST)
            tree.alpha_composite(o, (int(ox - o.width / 2), int(oy - o.height / 2)))
    th = int(TREE.height * max(0.02, grow))
    tr = tree.resize((TREE.width, th), Image.NEAREST)
    img.alpha_composite(tr, (int(tx - TREE.width / 2), int(910 - th)))
    a = to_arr(img)
    # garland lights blinking
    if t > T_TREE + 2.8:
        for j in range(2, len(TREE_ROWS), 2):
            n = TREE_ROWS[j]
            for i in range(n + 1):
                x = tx - TREE.width / 2 + ((15 - n) / 2 + i) * TB; y = 910 - TREE.height + j * TB + (i % 2) * 10
                on = (int(t * 4) + i + j) % 3 != 0
                c = np.array(LAMP_C[(i + j) % 4]) * (1 if on else 0.3)
                _sq(a, x, y, 10, c); _glow(a, x, y, 22, c * 0.5)
    img = to_img(a)
    sp = lin(t, T_TREE + 3.0, T_TREE + 3.6)
    if sp > 0:
        paste(img, STAR, tx, 910 - TREE.height - 30 - (1 - eo_bounce(sp)) * 500, 1, scale=1 + 0.06 * math.sin(t * 5))
    # right-side text column
    if slide > 0:
        cx = 1270
        lg = draw_logo2(99, 0); lg = lg.resize((int(lg.width * 0.62), int(lg.height * 0.62)), Image.NEAREST)
        paste(img, lg, cx + 120, 260, slide)
        items = [("PREMIERA", 60, (255, 255, 255)), ("24 GRUDNIA", 76, (255, 220, 70)), ("WIGILIA 2026", 46, (190, 225, 255))]
        y = 470
        for k, (s, sz, col) in enumerate(items):
            p = eo_back(lin(t, T_TREE + 5.0 + k * 0.35, T_TREE + 5.5 + k * 0.35))
            if p > 0: paste(img, text_img(s, sz, col, "ps", outline=4, ocol=(20, 20, 50)), cx + 120 + (1 - p) * 300, y, min(1, p))
            y += sz + 50
        p = lin(t, T_TREE + 6.4, T_TREE + 6.9)
        if p > 0:
            paste(img, text_img("Wesołych Świąt!", 54, (255, 255, 0), "px", outline=3, ocol=(60, 60, 0)), cx + 120, 830, p, scale=1 + 0.06 * abs(math.sin(t * 5)))
    a = to_arr(img); snow(a, t, 0.9)
    return to_img(a * clamp((DUR - t) / 1.0))
LAMP_C = [(255, 60, 60), (255, 220, 60), (60, 255, 120), (80, 160, 255)]

# ---------------------------------------------------------------- transitions / render
SCENES = [(T_SLEIGH, scene_sleigh), (T_PORTAL, scene_portal), (T_GLOBE, scene_globe), (T_SLOT, scene_slot), (T_TREE, scene_tree)]
# transition kinds: circle iris at sleigh->portal, globe->slot, slot->tree; portal->globe uses the white warp
IRIS = [T_PORTAL, T_SLOT, T_TREE]; TR = 0.8
def iris_mask(p):
    q = 24; w, h = W // q + 1, H // q + 1
    yy, xx = np.mgrid[0:h, 0:w]; d = np.hypot(xx - w / 2, yy - h / 2) / math.hypot(w / 2, h / 2)
    m = (d < eo_cubic(p) * 1.05).astype(np.uint8) * 255
    return Image.fromarray(m, "L").resize((w * q, h * q), Image.NEAREST).crop((0, 0, W, H))

def render(fi):
    t = fi / FPS
    si = max(i for i, (s, _) in enumerate(SCENES) if s <= t)
    img = SCENES[si][1](t)
    if T_GLOBE <= t < T_GLOBE + 0.5:  # fade out of white
        a = to_arr(img); a = a + 255 * (1 - lin(t, T_GLOBE, T_GLOBE + 0.5)); img = to_img(a)
    for b in IRIS:
        if b - TR / 2 <= t < b + TR / 2:
            k = [s for s, _ in SCENES].index(b)
            p = (t - (b - TR / 2)) / TR
            old = SCENES[k - 1][1](t) if t >= b else img
            new = SCENES[k][1](t) if t < b else img
            m = iris_mask(p)
            ring = m.filter(ImageFilter.MaxFilter(25))
            img = old.copy()
            img.paste(Image.new("RGBA", (W, H), (255, 240, 200, 255)), (0, 0), ring)
            img.paste(new, (0, 0), m)
    if t > 1.0 and t < DUR - 1.3:
        paste(img, text_img("DZIOB.6MC.PL • 24.12", 22, (255, 255, 255), "ps"), W - 40, H - 40, 0.7, anchor="r")
    a = np.asarray(img.convert("RGB")).astype(np.float32) * VIGN + GRAIN[fi % 6] * 0.6
    return np.clip(a, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    from multiprocessing import Pool
    out = sys.argv[1]
    start = float(sys.argv[2]) if len(sys.argv) > 2 else 0; end = float(sys.argv[3]) if len(sys.argv) > 3 else DUR
    frames = range(int(round(start * FPS)), int(round(end * FPS)))
    if len(sys.argv) > 4:
        for f in frames[::max(1, int(float(sys.argv[4]) * FPS))]:
            Image.frombytes("RGB", (W, H), render(f)).save(f"{out}/s3_{f / FPS:05.2f}.jpg", quality=85)
        sys.exit()
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    with Pool(4) as p:
        for i, b in enumerate(p.imap(render, frames, chunksize=4)):
            ff.stdin.write(b)
            if i % 150 == 0: print("frame", i, flush=True)
    ff.stdin.close(); ff.wait()
