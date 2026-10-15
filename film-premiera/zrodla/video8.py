"""Vertical viral list video #8: 'Rzeczy, które w 2026 są jeszcze za darmo' - countdown #5..#1 where #1 is Dziob.6mc.PL.
Synth house beat, stamp thuds, drumroll, fireworks."""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from video import text_img, paste, glow, pad_img, clamp, lin, eo_cubic, ei_cubic, icon
from video import eo_back as _eb
from video2 import draw_logo2
def eo_back(x, s=1.9): return 0.0 if x <= 0 else _eb(x, s)

FPS = 30
W, H = 1080, 1920
DUR = 32.0
INTER = "/usr/share/fonts/opentype/inter/"
_f = {}
def F(size, bold=True):
    k = (size, bold)
    if k not in _f: _f[k] = ImageFont.truetype(INTER + ("Inter-ExtraBold.otf" if bold else "Inter-Medium.otf"), size)
    return _f[k]
def to_arr(img): return np.asarray(img.convert("RGB")).astype(np.float32)
def to_img(a): return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

# items: (start, rank, title, subtitle, stamp_text, stamp_col, bg1, bg2, kind)
ITEMS = [(2.0, 5, "Powietrze", "(na razie)", "ZA DARMO", (40, 170, 70), (120, 200, 255), (60, 120, 220), "air"),
         (5.5, 4, "Wi-Fi u babci", "hasło na lodówce", "ZA DARMO", (40, 170, 70), (255, 190, 120), (230, 110, 80), "wifi"),
         (9.0, 3, "Rady od wujka", "przy wigilijnym stole", "ZA DARMO", (40, 170, 70), (150, 220, 140), (60, 150, 90), "uncle"),
         (12.5, 2, "Darmowa dostawa", "*od 299 zł", "PRAWIE...", (210, 40, 40), (230, 230, 240), (170, 170, 190), "box")]
T_ROLL, T_ONE, T_INFO, T_CTA = 16.0, 17.8, 22.6, 28.6
STAMP_DT = 1.4
STAMPS = [s + STAMP_DT for (s, *_) in ITEMS] + [T_ONE + 1.6]

# ====================================================================== AUDIO
SR = 44100
def make_audio(path):
    N = int(DUR * SR); out = np.zeros(N); rng = np.random.default_rng(31)
    def add(t0, sig, g=1.0):
        i = int(t0 * SR)
        if i >= N: return
        j = min(N, i + len(sig)); out[i:j] += g * sig[:j - i]
    def tt(d): return np.arange(int(d * SR)) / SR
    def hz(m): return 440 * 2 ** ((m - 69) / 12)
    def lp(x, fc):
        X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X /= np.sqrt(1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
    def hp(x, fc):
        X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / np.sqrt(1 + (fc / np.maximum(f, 1)) ** 4); return np.fft.irfft(X, len(x))
    def kick():
        t = tt(0.3); return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(48 + 130 * np.exp(-t * 30)) / SR) * np.exp(-t * 9))
    def hat(o=False):
        d = 0.18 if o else 0.05; return hp(rng.standard_normal(int(d * SR)), 7500) * np.exp(-tt(d) * (18 if o else 90))
    def clap():
        n = rng.standard_normal(int(0.2 * SR)); t = tt(0.2); e = sum((t >= o) * np.exp(-np.maximum(0, t - o) * 55) for o in (0, 0.012, 0.024))
        return hp(lp(n, 6500), 900) * e
    def stamp():
        t = tt(0.5); return np.tanh(3 * np.sin(2 * np.pi * np.cumsum(60 + 90 * np.exp(-t * 25)) / SR) * np.exp(-t * 10)) + lp(rng.standard_normal(len(t)), 1500) * np.exp(-t * 25) * 0.6
    def whoosh(d=0.4):
        n = rng.standard_normal(int(d * SR)); return lp(n, 3500) * np.linspace(0, 1, len(n)) ** 2
    def impact():
        t = tt(1.5); return np.tanh(3 * np.sin(2 * np.pi * np.cumsum(32 + 120 * np.exp(-t * 7)) / SR) * np.exp(-t * 2.2))
    def sad():
        out_ = []
        for m in (64, 61):
            t = tt(0.35); s = sum(np.sin(2 * np.pi * hz(m) * k * t) / k for k in range(1, 6)); out_.append(lp(s, 2000) * np.exp(-t * 4))
        return np.concatenate(out_) * 0.4
    def cheer(d=2.5):
        n = rng.standard_normal(int(d * SR)); t = tt(d)
        mod = 0.7 + 0.3 * np.sin(2 * np.pi * 7 * t) * np.sin(2 * np.pi * 3.3 * t)
        return hp(lp(n, 3500), 400) * mod * np.minimum(1, t / 0.15) * np.exp(-t * 0.9)
    def airhorn(d=0.9):
        t = tt(d); s = sum(np.sign(np.sin(2 * np.pi * f * t + rng.uniform(0, 6))) for f in (466, 470, 587, 591, 698))
        return lp(s, 3500) * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.08) * 0.25
    def pluck(m, d=0.25):
        t = tt(d); return lp(2 * ((t * hz(m)) % 1) - 1, 3000) * np.exp(-t * 14)
    beat = 60 / 124
    chords = [[57, 60, 64], [53, 57, 60], [60, 64, 67], [55, 59, 62]]
    k = 0; t0 = 0.0
    while t0 < DUR - 1.0:
        in_roll = T_ROLL <= t0 < T_ONE
        if not in_roll:
            add(t0, kick(), 0.5)
            add(t0 + beat / 2, hat(True), 0.06)
            if k % 2 == 1: add(t0, clap(), 0.25)
            for h in (0.25, 0.75): add(t0 + beat * h, hat(), 0.05)
            ch = chords[(k // 4) % 4]
            add(t0, lp(np.sin(2 * np.pi * hz(ch[0] - 24) * tt(beat * 0.9)) * np.exp(-tt(beat * 0.9) * 3), 400), 0.35)
            for j, m in enumerate(ch): add(t0 + beat * 0.5 + j * 0.0, pluck(m + 12), 0.035)
        t0 += beat; k += 1
    add(0.0, impact(), 0.5)
    for (s, *_), st in zip(ITEMS, STAMPS):
        add(s - 0.4, whoosh(), 0.15); add(s, impact()[: int(0.5 * SR)], 0.3)
        add(st, stamp(), 0.7)
    add(STAMPS[3] + 0.15, sad(), 0.6)
    # drumroll
    t = T_ROLL
    while t < T_ONE - 0.05:
        n = rng.standard_normal(int(0.05 * SR)); add(t, hp(lp(n, 5000), 600) * np.exp(-tt(0.05) * 40), 0.12 + 0.25 * (t - T_ROLL) / (T_ONE - T_ROLL)); t += 0.045
    add(T_ONE, impact(), 0.8); add(T_ONE, cheer(3.0), 0.5); add(STAMPS[4], stamp(), 0.8); add(STAMPS[4] + 0.1, airhorn(), 0.6)
    for k in range(6): add(T_ONE + 0.6 + k * 0.5, lp(rng.standard_normal(int(0.4 * SR)), 2500) * np.exp(-tt(0.4) * 9), 0.12)  # firework pops
    add(T_INFO - 0.4, whoosh(), 0.15)
    for i in range(6): add(T_INFO + 0.4 + i * 0.55, pluck(84 + i * 2, 0.2), 0.12)
    add(T_CTA - 0.4, whoosh(), 0.15); add(T_CTA, impact()[: int(0.7 * SR)], 0.4)
    out *= np.clip(np.minimum(np.arange(N) / SR / 0.02, (DUR - np.arange(N) / SR) / 0.8), 0, 1)
    out = np.tanh(out * 1.15) * 0.92
    st = np.stack([out, out], 1).astype(np.float32)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", path], input=st.tobytes())

# ====================================================================== VISUALS
def bg(c1, c2, t):
    yy = np.linspace(0, 1, H)[:, None, None]
    a = np.array(c1, np.float32) * (1 - yy) + np.array(c2, np.float32) * yy
    a = np.broadcast_to(a, (H, W, 3)).copy()
    # soft dot pattern
    ys, xs = np.mgrid[0:H // 8, 0:W // 8]
    dots = ((((xs + int(t * 6)) % 10) < 1) & ((ys % 10) < 1)).astype(np.float32).repeat(8, 0).repeat(8, 1)[..., None] * 25
    return a + dots

def outlined(img, text, size, col, x, y, alpha=1.0, stroke=10, scol=(0, 0, 0), rot=0):
    f = F(size); w = f.getlength(text)
    lay = Image.new("RGBA", (int(w + 4 * stroke + 20), int(size * 1.6 + 4 * stroke)), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((2 * stroke + 10, 2 * stroke), text, font=f, fill=col + (255,), stroke_width=stroke, stroke_fill=scol + (255,))
    paste(img, lay, x, y, alpha, rot=rot, resample=Image.BICUBIC)

def stamp_img(text, col):
    f = F(96); w = f.getlength(text); im = Image.new("RGBA", (int(w + 100), 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, im.width - 7, 193], radius=26, fill=(255, 255, 255, 235), outline=col + (255,), width=14)
    d.text((50, 30), text, font=f, fill=col + (255,))
    a = np.asarray(im).copy(); r = np.random.default_rng(len(text))
    a[..., 3] = (a[..., 3] * (r.random(a.shape[:2]) > 0.12)).astype(np.uint8)  # grungy ink
    return Image.fromarray(a, "RGBA")
STAMP_IMGS = [stamp_img(it[4], it[5]) for it in ITEMS] + [stamp_img("ZA DARMO", (230, 170, 20))]

def art(kind, t):
    im = Image.new("RGBA", (800, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == "air":
        for i in range(3):
            y = 200 + i * 130; pts = [(80 + x, y + 30 * math.sin(x / 60 + t * 3 + i)) for x in range(0, 560, 10)]
            d.line(pts, fill=(255, 255, 255, 255), width=22, joint="curve")
            ex, ey = pts[-1]; d.ellipse([ex - 40, ey - 70, ex + 30, ey], outline=(255, 255, 255, 255), width=20)
    elif kind == "wifi":
        cx, cy = 400, 470
        for i, r in enumerate((90, 190, 290)):
            on = (int(t * 4) % 4) > i
            d.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=(255, 255, 255, 255 if on else 90), width=48)
        d.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], fill=(255, 255, 255, 255))
        note = Image.new("RGBA", (330, 200), (255, 240, 120, 255)); nd = ImageDraw.Draw(note)
        nd.text((24, 24), "hasło:", font=F(40, False), fill=(60, 60, 60, 255)); nd.text((24, 90), "babcia123", font=F(56), fill=(30, 30, 30, 255))
        im.alpha_composite(note.rotate(-8, expand=True, resample=Image.BICUBIC), (440, 400))
    elif kind == "uncle":
        d.ellipse([250, 260, 550, 560], fill=(240, 200, 160, 255))
        d.ellipse([320, 360, 350, 390], fill=(30, 30, 30, 255)); d.ellipse([450, 360, 480, 390], fill=(30, 30, 30, 255))
        d.rounded_rectangle([320, 430, 480, 470], radius=20, fill=(90, 60, 40, 255))  # moustache
        m = abs(math.sin(t * 10)) * 30; d.ellipse([370, 480, 430, 500 + m], fill=(120, 30, 30, 255))
        d.rounded_rectangle([60, 20, 740, 220], radius=40, fill=(255, 255, 255, 255)); d.polygon([(330, 210), (390, 210), (360, 290)], fill=(255, 255, 255, 255))
        d.text((110, 60), "a za moich", font=F(56), fill=(30, 30, 30, 255)); d.text((110, 130), "czasów...", font=F(56), fill=(30, 30, 30, 255))
    elif kind == "box":
        d.polygon([(150, 260), (650, 260), (650, 600), (150, 600)], fill=(190, 140, 80, 255))
        d.polygon([(150, 260), (400, 160), (900 - 250, 260)], fill=(215, 165, 100, 255))
        d.rectangle([370, 260, 430, 600], fill=(230, 210, 150, 255))
        lab = Image.new("RGBA", (300, 140), (255, 255, 255, 255)); ld = ImageDraw.Draw(lab)
        ld.text((20, 10), "0 zł*", font=F(80), fill=(20, 140, 50, 255))
        im.alpha_composite(lab, (180, 400))
        d.text((470, 520), "*od 299 zł", font=F(44), fill=(200, 30, 30, 255))
    return im

def s_hook(t):
    img = to_img(bg((255, 80, 80), (130, 20, 120), t))
    p = eo_back(lin(t, 0.0, 0.25), 2.5)
    if p > 0:
        sc = max(0.05, p)
        for i, (l, c, sz) in enumerate([("RZECZY,", (255, 255, 255), 120), ("KTÓRE W 2026", (255, 255, 255), 110), ("SĄ JESZCZE", (255, 255, 255), 110), ("ZA DARMO", (255, 230, 60), 150)]):
            outlined(img, l, int(sz * sc) + 1, c, W / 2, 560 + i * 170)
    q = lin(t, 0.9, 1.1)
    if q > 0: outlined(img, "(nr 1 cię zaskoczy)", 60, (255, 255, 255), W / 2, 1330, q, stroke=6)
    return img

def s_item(t, i):
    s, rank, title, sub, stx, stc, c1, c2, kind = ITEMS[i]
    img = to_img(bg(c1, c2, t))
    p = eo_back(lin(t, s, s + 0.25), 3)
    outlined(img, f"#{rank}", int(220 * max(p, 0.01)) + 1, (255, 255, 255), W / 2, 260, 1, stroke=14)
    q = eo_back(lin(t, s + 0.2, s + 0.45), 2)
    if q > 0:
        outlined(img, title, int(92 * q) + 1, (255, 255, 255), W / 2, 520)
        outlined(img, sub, 60, (255, 255, 255), W / 2, 650, min(1, q), stroke=6)
    a = art(kind, t); r = eo_back(lin(t, s + 0.35, s + 0.7), 1.5)
    if r > 0: paste(img, a, W / 2, 1150 + (1 - r) * 800, 1)
    st = STAMPS[i]
    sp = lin(t, st - 0.15, st)
    if sp > 0:
        sc = 2.4 - 1.4 * ei_cubic(sp)
        paste(img, STAMP_IMGS[i], W / 2, 1650, min(1, sp * 2), scale=sc, rot=-12, resample=Image.BICUBIC)
    return img

def s_roll(t):
    img = to_img(bg((30, 20, 50), (10, 5, 20), t))
    sh = 8 * math.sin(t * 60) * lin(t, T_ROLL, T_ONE)
    outlined(img, "a numer 1...", 110, (255, 255, 255), W / 2 + sh, 860, lin(t, T_ROLL, T_ROLL + 0.2))
    outlined(img, "?", 300, (255, 230, 60), W / 2 - sh, 1150, lin(t, T_ROLL + 0.3, T_ROLL + 0.5), stroke=14)
    return img

FW = []
_r = np.random.default_rng(5)
for k in range(10): FW.append((T_ONE + 0.3 + k * 0.42, _r.uniform(150, 930), _r.uniform(250, 900), k % 5))
FCOL = [(255, 80, 80), (255, 220, 60), (90, 220, 255), (120, 255, 120), (230, 110, 255)]
def s_one(t):
    img = to_img(bg((70, 20, 110), (25, 10, 50), t))
    a = to_arr(img); yy, xx = np.ogrid[0:H, 0:W]
    ang = np.arctan2(yy - 900, xx - W / 2) + t * 0.7
    a += ((np.sin(ang * 14) > 0.4) * 1.0)[..., None] * np.array([60, 40, 0])
    for (ft, x, y, c) in FW:
        dt = t - ft
        if 0 <= dt < 1.6:
            for j in range(36):
                an = j / 36 * 2 * math.pi; v = 380 * (1 - math.exp(-dt * 3)) / 1
                px, py = x + math.cos(an) * v, y + math.sin(an) * v + 120 * dt * dt
                if 0 <= px < W - 12 and 0 <= py < H - 12: a[int(py):int(py) + 12, int(px):int(px) + 12] = np.array(FCOL[c]) * (1 - dt / 1.6) + a[int(py):int(py) + 12, int(px):int(px) + 12] * (dt / 1.6)
    img = to_img(a)
    p = eo_back(lin(t, T_ONE, T_ONE + 0.3), 3)
    outlined(img, "#1", int(240 * max(p, 0.01)) + 1, (255, 255, 255), W / 2, 230, 1, stroke=14)
    lg = draw_logo2(t, T_ONE + 0.1)
    gl = glow(pad_img(lg, 40), 26, 1.4)
    paste(img, gl, W / 2, 560, 1, scale=0.68)
    q = eo_back(lin(t, T_ONE + 0.7, T_ONE + 1.0), 2)
    if q > 0:
        outlined(img, "DZIOB.6MC.PL", int(96 * q) + 1, (255, 255, 255), W / 2, 820)
        outlined(img, "serwer Minecraft", 64, (255, 255, 255), W / 2, 950, min(1, q), stroke=7)
        outlined(img, "premiera 24.12", 64, (255, 255, 255), W / 2, 1040, min(1, q), stroke=7)
    paste(img, icon("bird", 14), W / 2, 1350 - abs(math.sin(t * math.pi * 2)) * 60, lin(t, T_ONE + 0.4, T_ONE + 0.7), rot=10 * math.sin(t * 6), resample=Image.NEAREST)
    st = STAMPS[4]; sp = lin(t, st - 0.15, st)
    if sp > 0: paste(img, STAMP_IMGS[4], W / 2, 1660, min(1, sp * 2), scale=2.4 - 1.4 * ei_cubic(sp), rot=-10, resample=Image.BICUBIC)
    return img

INFO = [("SERWER", "Dziob.6mc.PL"), ("IP", "dziob.6mc.pl"), ("PREMIERA", "24 grudnia 2026 (Wigilia)"), ("CENA", "0 zł – serio za darmo"),
        ("START", "wszyscy od zera"), ("GRA", "Minecraft")]
def s_info(t):
    img = to_img(bg((25, 25, 45), (60, 30, 90), t))
    outlined(img, "WSZYSTKO, CO", 84, (255, 230, 60), W / 2, 170, lin(t, T_INFO, T_INFO + 0.2))
    outlined(img, "MUSISZ WIEDZIEĆ", 84, (255, 230, 60), W / 2, 280, lin(t, T_INFO + 0.1, T_INFO + 0.3))
    for i, (k, v) in enumerate(INFO):
        rt = T_INFO + 0.4 + i * 0.55
        p = eo_back(lin(t, rt, rt + 0.3), 1.5)
        if p <= 0: continue
        row = Image.new("RGBA", (980, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
        d.rounded_rectangle([0, 0, 979, 189], radius=36, fill=(255, 255, 255, 30), outline=(255, 255, 255, 130), width=4)
        d.text((40, 22), k, font=F(36, False), fill=(150, 200, 255, 255)); d.text((40, 74), v, font=F(66), fill=(255, 255, 255, 255))
        paste(img, row, W / 2 + (1 - p) * 1200, 480 + i * 215, 1)
    return img

def s_cta(t):
    img = to_img(bg((255, 80, 80), (130, 20, 120), t))
    p = eo_back(lin(t, T_CTA, T_CTA + 0.25), 2.5)
    if p > 0:
        outlined(img, "CO JESZCZE JEST", int(96 * p) + 1, (255, 255, 255), W / 2, 480)
        outlined(img, "ZA DARMO?", int(140 * p) + 1, (255, 230, 60), W / 2, 640)
    q = lin(t, T_CTA + 0.6, T_CTA + 0.9)
    if q > 0:
        outlined(img, "pisz w komentarzu", 68, (255, 255, 255), W / 2, 850, q, stroke=7)
        # bouncing arrow
        ay = 1000 + abs(math.sin(t * 6)) * 30; d = ImageDraw.Draw(img)
        d.polygon([(W / 2 - 60, ay), (W / 2 + 60, ay), (W / 2, ay + 80)], fill=(255, 255, 255, int(255 * q)))
    r = lin(t, T_CTA + 1.2, T_CTA + 1.5)
    if r > 0:
        box = Image.new("RGBA", (960, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
        d.rounded_rectangle([0, 0, 959, 199], radius=50, fill=(0, 0, 0, 170), outline=(255, 255, 255, 230), width=6)
        tx = "IP: dziob.6mc.pl"; f = F(72); w = f.getlength(tx); d.text((480 - w / 2, 48), tx, font=f, fill=(255, 255, 255, 255))
        paste(img, box, W / 2, 1260, r)
        outlined(img, "premiera 24.12 • 0 zł", 60, (255, 230, 60), W / 2, 1440, r, stroke=6)
    paste(img, icon("bird", 10), W / 2, 1680 - abs(math.sin(t * math.pi * 2.4)) * 50, lin(t, T_CTA + 0.3, T_CTA + 0.6))
    return img

SCENES = [(0.0, s_hook)] + [(it[0], (lambda i: (lambda t: s_item(t, i)))(i)) for i, it in enumerate(ITEMS)] + [(T_ROLL, s_roll), (T_ONE, s_one), (T_INFO, s_info), (T_CTA, s_cta)]
GRAIN = [np.random.default_rng(i).normal(0, 3.5, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1) for i in range(4)]
PUNCH = [s for s, _ in SCENES] + STAMPS

def render(fi):
    t = fi / FPS
    si = max(i for i, (s, _) in enumerate(SCENES) if s <= t)
    img = SCENES[si][1](t)
    z = 1.0 + sum(0.05 * math.exp(-max(0, t - h) * 9) for h in PUNCH if t >= h)
    if z > 1.002:
        big = img.resize((int(W * z), int(H * z)), Image.BILINEAR); l = (big.width - W) // 2; tp = (big.height - H) // 2
        img = big.crop((l, tp, l + W, tp + H))
    sh = sum(18 * math.exp(-max(0, t - st) * 12) for st in STAMPS if t >= st)
    if sh > 0.5:
        rr = np.random.default_rng(fi); dx, dy = rr.uniform(-sh, sh, 2)
        img = img.transform((W, H), Image.AFFINE, (1 / 1.04, 0, -dx + W * 0.0192, 0, 1 / 1.04, -dy + H * 0.0192), Image.BILINEAR)
    d = ImageDraw.Draw(img); d.rectangle([0, 0, W, 12], fill=(0, 0, 0, 120)); d.rectangle([0, 0, W * t / DUR, 12], fill=(255, 255, 255, 230))
    fl = max([clamp(1 - (t - c) / 0.12) for c in [s for s, _ in SCENES[1:]] if t >= c] + [0])
    a = to_arr(img) + GRAIN[fi % 4]
    a = a + (255 - a) * fl * 0.55
    a *= clamp((DUR - t) / 0.5)
    return np.clip(a, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    from multiprocessing import Pool
    out = sys.argv[1]
    if len(sys.argv) > 4:
        s, e = float(sys.argv[2]), float(sys.argv[3])
        for f in range(int(round(s * FPS)), int(round(e * FPS)), max(1, int(float(sys.argv[4]) * FPS))):
            Image.frombytes("RGB", (W, H), render(f)).save(f"{out}/s8_{f / FPS:05.2f}.jpg", quality=85)
        sys.exit()
    wav = os.path.join(BUILD, "mix8.wav"); make_audio(wav)
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    with Pool(4) as p:
        for i, b in enumerate(p.imap(render, range(int(DUR * FPS)), chunksize=4)):
            ff.stdin.write(b)
            if i % 150 == 0: print("frame", i, flush=True)
    ff.stdin.close(); ff.wait()
