"""Vertical (9:16) youth/short-form video #5: 20 zł on anarchia.gg vs 0 zł on Dziob.6mc.PL. Synth trap beat + SFX."""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from video import text_img, paste, glow, pad_img, clamp, lin, eo_cubic, eo_back, ei_cubic, eo_bounce, icon, tex, mc_panel, _isext
from video2 import draw_logo2

FPS = 30
W, H = 1080, 1920
DUR = 32.0
# beat grid: 120 bpm -> 0.5 s
CUTS = [0.0, 1.5, 5.0, 8.5, 12.5, 15.5, 18.5, 22.5, 27.0, DUR]

def to_arr(img): return np.asarray(img.convert("RGB")).astype(np.float32)
def to_img(a): return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

# ====================================================================== AUDIO
SR = 44100
HITS = [0.0, 1.5, 5.0, 6.4, 8.5, 10.0, 10.75, 11.5, 15.5, 18.5, 22.5, 27.0]
def make_audio(path):
    N = int(DUR * SR); out = np.zeros(N); rng = np.random.default_rng(8)
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
        t = tt(0.35); return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(45 + 140 * np.exp(-t * 35)) / SR) * np.exp(-t * 8))
    def b808(m, d):
        t = tt(d); f = hz(m) * (1 + 0.5 * np.exp(-t * 30))
        return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.minimum(1, (d - t) / 0.05) * np.exp(-t * 1.2)
    def clap():
        n = rng.standard_normal(int(0.2 * SR)); e = np.zeros(len(n)); t = tt(0.2)
        for o in (0, 0.012, 0.024): e += (t >= o) * np.exp(-np.maximum(0, t - o) * 60)
        return hp(lp(n, 6000), 900) * e * 0.8
    def hat():
        return hp(rng.standard_normal(int(0.05 * SR)), 7000) * np.exp(-tt(0.05) * 90)
    def impact():
        t = tt(1.6); return np.tanh(3 * np.sin(2 * np.pi * np.cumsum(32 + 100 * np.exp(-t * 7)) / SR) * np.exp(-t * 2.2)) + lp(rng.standard_normal(len(t)), 500) * np.exp(-t * 6) * 0.5
    def whoosh(d=0.5, up=True):
        n = rng.standard_normal(int(d * SR)); x = np.linspace(0, 1, len(n))
        return lp(n, 3000) * ((x ** 2) if up else np.sin(x * np.pi) ** 2)
    def register():
        t = tt(1.0); bell = (np.sin(2 * np.pi * 2100 * t) + 0.6 * np.sin(2 * np.pi * 3150 * t) + 0.3 * np.sin(2 * np.pi * 5200 * t)) * np.exp(-t * 5)
        drawer = np.zeros(len(t)); k = int(0.0 * SR); drawer[:int(0.15 * SR)] = lp(rng.standard_normal(int(0.15 * SR)), 1500) * np.exp(-tt(0.15) * 20)
        return bell * 0.5 + drawer
    def vinyl_stop():
        t = tt(1.0); f = 220 * (1 - t) ** 2 + 20
        return lp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)), 900) * (1 - t) * 0.5
    def boing():
        t = tt(0.6); f = 180 + 300 * np.abs(np.sin(t * 20)) * np.exp(-t * 4)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
    def airhorn(d=0.9):
        t = tt(d); s = 0
        for f in (466, 470, 587, 591, 698):
            s = s + np.sign(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)))
        env = np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.08)
        return lp(s, 3500) * env * 0.25
    def blip(m, d=0.08):
        t = tt(d); return np.sign(np.sin(2 * np.pi * hz(m) * t)) * np.exp(-t * 30)
    # --- beat (stops for the 'prąd' twist, restarts at 15.5)
    roots = [45, 45, 41, 43]  # A A F G (808 notes)
    for b in range(int(DUR / 2)):
        t0 = b * 2.0
        if t0 + 2 > DUR - 0.5: break
        if 12.5 <= t0 < 15.5: continue
        if t0 < 1.5: continue
        r = roots[b % 4]
        add(t0, kick(), 0.6); add(t0 + 0.75, kick(), 0.45); add(t0 + 1.25, kick(), 0.35)
        add(t0, b808(r, 0.7), 0.30); add(t0 + 0.75, b808(r, 0.45), 0.25); add(t0 + 1.25, b808(r + 3 if b % 2 else r, 0.7), 0.25)
        add(t0 + 0.5, clap(), 0.35); add(t0 + 1.5, clap(), 0.35)
        for h in range(16):
            th = t0 + h * 0.125
            add(th, hat(), 0.08 if h % 2 == 0 else 0.05)
            if h in (13, 14, 15) and b % 2 == 1:
                for r2 in range(3): add(th + r2 * 0.0417, hat(), 0.05)
        # little bell melody
        mel = [81, 84, 88, 84, 81, 79, 76, 79]
        for k in range(4): add(t0 + k * 0.5 + 0.25, lp(np.sin(2 * np.pi * hz(mel[(b * 4 + k) % 8]) * tt(0.4)) * np.exp(-tt(0.4) * 9), 6000), 0.06)
    # --- SFX
    add(0.0, impact(), 0.6)
    add(0.05, whoosh(0.5, False), 0.15)
    for ht in (1.5, 8.5, 15.5, 18.5, 22.5, 27.0): add(ht - 0.45, whoosh(0.45), 0.12); add(ht, impact(), 0.35)
    add(6.4, register(), 0.45)
    for k in range(6): add(5.2 + k * 0.12, blip(90 - k * 3), 0.05)
    for ht in (10.0, 10.75, 11.5): add(ht, impact(), 0.45)
    add(12.4, vinyl_stop(), 0.55)
    for k in range(3): add(13.0 + k * 0.6, blip(64 - k * 5, 0.25) * 0.6, 0.08)  # sus 'bulb' buzz blips
    add(16.4, boing(), 0.30)
    add(20.6, airhorn(), 0.6); add(21.0, airhorn(0.5), 0.5)
    for k in range(5): add(22.8 + k * 0.7, blip(84 + k * 2), 0.06)
    add(27.3, airhorn(1.2), 0.5)
    out *= np.clip(np.minimum(np.arange(N) / SR / 0.02, (DUR - np.arange(N) / SR) / 0.8), 0, 1)
    out = np.tanh(out * 1.1) * 0.92
    st = np.stack([out, out], 1).astype(np.float32)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", path], input=st.tobytes())

# ====================================================================== VISUAL HELPERS
def stripes(c1, c2, t, speed=60, band=70):
    yy, xx = np.mgrid[0:H // 4, 0:W // 4]
    m = (((xx * 4 + yy * 4 + t * speed) // band) % 2).astype(np.float32)[..., None]
    a = np.array(c1, np.float32) * (1 - m) + np.array(c2, np.float32) * m
    return a.repeat(4, 0).repeat(4, 1)

def radial(c1, c2):
    yy, xx = np.ogrid[0:H, 0:W]; r = np.clip(np.sqrt((xx - W / 2) ** 2 + (yy - H / 2) ** 2) / 1100, 0, 1)[..., None]
    return np.array(c1, np.float32) * (1 - r) + np.array(c2, np.float32) * r

def words(img, t, t0, items, y, size, per=0.18, maxw=980, gap=1.35, fam="ps", outline=6):
    """TikTok-style captions: words pop one by one. items: list of (word, color)."""
    imgs = [text_img(w, size, c, fam, outline=outline, ocol=(0, 0, 0)) for w, c in items]
    sp = size * 0.45; lines = [[]]; lw = 0
    for i, im in enumerate(imgs):
        if lines[-1] and lw + sp + im.width > maxw: lines.append([]); lw = 0
        lines[-1].append(i); lw += (sp if lw else 0) + im.width
    yy = y - (len(lines) - 1) * size * gap / 2
    for ln in lines:
        tw = sum(imgs[i].width for i in ln) + sp * (len(ln) - 1); x = W / 2 - tw / 2
        for i in ln:
            p = lin(t, t0 + i * per, t0 + i * per + 0.12)
            if p > 0:
                paste(img, imgs[i], x + imgs[i].width / 2, yy, 1, scale=max(0.05, eo_back(p, 3.0)))
            x += imgs[i].width + sp
        yy += size * gap

def pixmap(rows, cols, s):
    h = len(rows); w = max(len(r) for r in rows); a = np.zeros((h, w, 4), np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in cols: a[y, x] = cols[ch] + (255,)
    return Image.fromarray(a, "RGBA").resize((w * s, h * s), Image.NEAREST)

C = {"K": (20, 20, 20), "W": (255, 255, 255), "Y": (255, 220, 50), "y": (220, 170, 20), "O": (255, 150, 40), "B": (130, 80, 40),
     "b": (90, 55, 25), "G": (60, 190, 60), "g": (30, 130, 40), "R": (230, 50, 50), "P": (150, 90, 200), "p": (110, 60, 160),
     "S": (190, 190, 200), "M": (160, 90, 50), "L": (255, 250, 200)}
EYES = pixmap([".KKKK....KKKK.", "KWWWWK..KWWWWK", "KWWKKK..KWWKKK", "KWWKKK..KWWKKK", "KWWWWK..KWWWWK", ".KKKK....KKKK."], C, 26)
BULB = pixmap(["...KKKKK...", "..KYYYYYK..", ".KYYLLYYYK.", ".KYLLYYYYK.", ".KYYYYYYYK.", ".KYYYYYYYK.", "..KYYYYYK..", "...KYYYK...",
               "...KSSSK...", "...KSSSK...", "...KSSSK...", "....KKK...."], C, 22)
KEBAB = pixmap(["....BBBBBB....", "...BMMMMMMB...", "..BGMRMGMRMB..", "..BMGMMRMGMB..", ".BRMMGRMMGRMB.", ".BMGRMMGMRMMB.",
                ".BBBBBBBBBBBB.", "..BBBBBBBBBB..", "....KWWWWK....", "....KWWWWK....", "....KKKKKK...."], C, 24)
TROPHY = pixmap(["KKKKKKKKKKKK", "KYYYYYYYYYYK", "YKYYYYYYYYKY", "YKYYLYYYYYKY", ".KYYLYYYYYK.", "..KYYYYYYK..", "...KYYYYK...",
                 "....KyyK....", "....KyyK....", "...KyyyyK...", "..KKKKKKKK.."], C, 26)
COIN = pixmap(["..KKKK..", ".KYYYYK.", "KYYLYYyK", "KYLYYYyK", "KYYYYYyK", "KYYYYyyK", ".KyyyyK.", "..KKKK.."], C, 12)

def banknote(s=1.0):
    w, h = int(560 * s), int(280 * s); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=(160, 110, 200, 255), outline=(60, 30, 90, 255), width=10)
    d.rectangle([24, 24, w - 25, h - 25], outline=(210, 180, 240, 255), width=6)
    d.ellipse([w * 0.6, h * 0.2, w * 0.85, h * 0.8], fill=(200, 170, 230, 255))
    t = text_img("20", int(110 * s), (255, 255, 255), "ps", outline=5, ocol=(60, 30, 90)); im.alpha_composite(t, (int(40 * s), h // 2 - t.height // 2))
    z = text_img("ZŁ", int(44 * s), (60, 30, 90), "ps", shadow=False); im.alpha_composite(z, (int(w * 0.66), h // 2 - z.height // 2))
    return im
NOTE = banknote()

def progress_bar(img, t):
    d = ImageDraw.Draw(img); d.rectangle([0, 0, W, 14], fill=(0, 0, 0, 120)); d.rectangle([0, 0, W * t / DUR, 14], fill=(255, 255, 255, 230))

def footnote(img, t):
    if 5.0 <= t < 22.5:
        paste(img, text_img("*kwota wg ekipy Dziob.6mc.PL (10.2026)", 26, (255, 255, 255), "pxr", outline=2, ocol=(0, 0, 0)), W / 2, H - 70, 0.85)

def mc_money(val, col):
    im = Image.new("RGBA", (760, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 759, 199], fill=(0, 0, 0, 170), outline=(255, 255, 255, 200), width=5)
    im.alpha_composite(text_img("Twoje saldo:", 34, (200, 200, 200), "px"), (30, 22))
    v = text_img(val, 84, col, "ps", outline=4); im.alpha_composite(v, (30, 80))
    return im

# ====================================================================== SCENES
def s_hook(t):
    a = radial((255, 60, 60), (90, 0, 20)); img = to_img(a)
    p = eo_back(lin(t, 0.0, 0.18), 3)
    paste(img, glow(pad_img(text_img("CZEKAJ.", 128, (255, 255, 255), "ps", outline=10), 30), 20), W / 2, 760, 1, scale=max(0.05, p) * (1 + 0.03 * math.sin(t * 30)))
    q = eo_back(lin(t, 0.45, 0.6), 3)
    if q > 0: paste(img, EYES, W / 2, 1060 + 10 * math.sin(t * 12), 1, scale=max(.05, q))
    words(img, t, 0.75, [("TO", (255, 255, 255)), ("CIĘ", (255, 255, 255)), ("ZASKOCZY", (255, 230, 60))], 1300, 74, per=0.15)
    return img

def s_q(t):
    img = to_img(stripes((50, 40, 120), (70, 55, 150), t))
    words(img, t, 1.6, [("ŻEBY", (255, 255, 255)), ("MIEĆ", (255, 255, 255)), ("CHOCIAŻ", (255, 255, 255)), ("1000$", (85, 255, 85)),
                       ("NA", (255, 255, 255)), ("ANARCHIA.GG...", (255, 120, 120))], 520, 64, per=0.22)
    p = eo_back(lin(t, 3.1, 3.4))
    if p > 0:
        val = "$0" if t < 4.2 else "$0 ..."
        paste(img, mc_money(val, (255, 90, 90)), W / 2, 1200, 1, scale=max(.05, p))
    q = lin(t, 4.0, 4.3)
    if q > 0: paste(img, text_img(":(", 120, (255, 255, 255), "ps", outline=6), W / 2, 1500, q, rot=-90 * 0, scale=1)
    return img

def s_pay(t):
    img = to_img(stripes((200, 40, 60), (230, 60, 80), t))
    words(img, t, 5.05, [("MUSISZ", (255, 255, 255)), ("WYDAĆ", (255, 255, 255)), ("20 ZŁ*", (255, 230, 60))], 380, 96, per=0.25)
    # banknote flies out of wallet
    p = lin(t, 5.9, 6.9)
    if p > 0:
        x = W / 2 + 300 * p; y = 1000 - 500 * eo_cubic(p) + 50 * math.sin(p * 9)
        paste(img, NOTE, x, y, 1 - lin(p, 0.8, 1), rot=p * 40, resample=Image.BICUBIC)
    # wallet
    wl = Image.new("RGBA", (420, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(wl)
    d.rectangle([0, 40, 419, 299], fill=(110, 70, 40, 255), outline=(50, 30, 15, 255), width=10)
    d.rectangle([260, 120, 419, 220], fill=(140, 95, 55, 255), outline=(50, 30, 15, 255), width=8); d.rectangle([300, 155, 330, 185], fill=(240, 200, 60, 255))
    paste(img, wl, W / 2, 1200, 1, scale=1 - 0.08 * lin(t, 6.4, 6.6) + 0.08 * lin(t, 6.6, 6.9))
    q = eo_back(lin(t, 6.4, 6.7), 2.5)
    if q > 0:
        paste(img, mc_money("$1000", (85, 255, 85)), W / 2, 1560, 1, scale=max(.05, q))
        paste(img, text_img("-20 ZŁ", 80, (255, 255, 255), "ps", outline=5, ocol=(120, 0, 0)), W / 2 + 260, 1400 - 80 * lin(t, 6.4, 8.4), 1 - lin(t, 7.6, 8.4))
    return img

def s_zero(t):
    img = to_img(stripes((30, 150, 70), (40, 175, 85), t))
    # coins raining... staying in wallet
    rr = np.random.default_rng(3)
    for k in range(14):
        x = rr.uniform(80, W - 80); sp = rr.uniform(500, 900); ph = rr.uniform(0, 3)
        y = ((t - 8.5) * sp + ph * 400) % (H + 200) - 100
        if t > 9.0: paste(img, COIN, x, y, 0.9)
    words(img, t, 8.55, [("A", (255, 255, 255)), ("NA", (255, 255, 255)), ("DZIOB.6MC.PL?", (255, 230, 60))], 330, 68, per=0.2)
    big = [("0 ZŁ.", 10.0), ("ZERO.", 10.75), ("NIC.", 11.5)]
    for i, (w, bt) in enumerate(big):
        p = eo_back(lin(t, bt, bt + 0.15), 3)
        if p > 0:
            paste(img, glow(pad_img(text_img(w, 150, (255, 255, 255), "ps", outline=9, ocol=(0, 60, 20)), 30), 18), W / 2, 760 + i * 260, 1, scale=max(.05, p) * (1 + 0.15 * math.exp(-(t - bt) * 10)))
    paste(img, text_img("nawet grosza", 54, (255, 255, 255), "px", outline=3), W / 2, 1560, lin(t, 11.8, 12.1))
    return img

def s_power(t):
    flick = 0.55 + 0.45 * (math.sin(t * 37) > -0.3) * (0.7 + 0.3 * math.sin(t * 13))
    img = to_img(radial((60 * flick, 50 * flick, 20 * flick), (8, 8, 12)))
    words(img, t, 12.6, [("no", (220, 220, 220)), ("dobra...", (220, 220, 220))], 330, 70, per=0.25, fam="px")
    words(img, t, 13.3, [("musisz", (255, 255, 255)), ("opłacić", (255, 255, 255)), ("PRĄD", (255, 230, 60))], 500, 84, per=0.25)
    p = eo_back(lin(t, 13.6, 13.9))
    if p > 0:
        g = glow(pad_img(BULB, 60), 40, 1.2 * flick)
        paste(img, g, W / 2, 1050, 1, scale=max(.05, p))
    q = eo_back(lin(t, 14.4, 14.7))
    if q > 0:
        bill = mc_panel(700, 260); bill.alpha_composite(text_img("RACHUNEK ZA PRĄD", 40, (60, 60, 60), "ps", shadow=False), (40, 40))
        bill.alpha_composite(text_img("płatne: rodzice :)", 40, (110, 110, 110), "px", shadow=False), (40, 140))
        paste(img, bill, W / 2, 1560, 1, scale=max(.05, q), rot=-4, resample=Image.BICUBIC)
    return img

def s_also(t):
    img = to_img(stripes((40, 40, 50), (55, 55, 70), t, speed=20))
    words(img, t, 15.55, [("ALE", (255, 255, 255)), ("NA", (255, 255, 255)), ("ANARCHIA.GG", (255, 120, 120)), ("TEŻ", (255, 230, 60)), ("MUSISZ.", (255, 230, 60))], 380, 74, per=0.2)
    # shrug guy: two bulbs (both pay electricity) 1:1
    p = eo_back(lin(t, 16.4, 16.7), 2.5)
    if p > 0:
        paste(img, BULB, W / 2 - 230, 1050, 1, scale=max(.05, p) * 0.8)
        paste(img, BULB, W / 2 + 230, 1050, 1, scale=max(.05, p) * 0.8)
        paste(img, text_img("=", 140, (255, 255, 255), "ps", outline=6), W / 2, 1050, 1, scale=max(.05, p))
    q = eo_back(lin(t, 17.2, 17.5), 3)
    if q > 0: paste(img, text_img("PRĄD: 1 : 1", 72, (255, 255, 255), "ps", outline=6), W / 2, 1450, 1, scale=max(.05, q))
    return img

def s_math(t):
    img = to_img(stripes((240, 180, 30), (255, 200, 50), t))
    words(img, t, 18.55, [("CZYLI", (20, 20, 20))], 230, 70, per=0.1, outline=0)
    rows = [("ANARCHIA.GG", "20 ZŁ + PRĄD", (200, 30, 30), 19.0), ("DZIOB.6MC.PL", "0 ZŁ + PRĄD", (20, 130, 40), 19.6)]
    for i, (n, v, c, rt) in enumerate(rows):
        p = eo_back(lin(t, rt, rt + 0.3), 1.6)
        if p <= 0: continue
        card = Image.new("RGBA", (940, 230), (255, 255, 255, 235)); d = ImageDraw.Draw(card); d.rectangle([0, 0, 939, 229], outline=(20, 20, 20, 255), width=8)
        card.alpha_composite(text_img(n, 52, c, "ps", shadow=False), (40, 35)); card.alpha_composite(text_img(v, 64, (20, 20, 20), "ps", shadow=False), (40, 120))
        paste(img, card, W / 2 + (1 - p) * -1100, 480 + i * 290, 1)
    q = eo_back(lin(t, 20.6, 20.9), 2.5)
    if q > 0:
        paste(img, glow(pad_img(TROPHY, 40), 30, 1.5), W / 2, 1180, 1, scale=max(.05, q) * (1 + 0.05 * math.sin(t * 8)))
        paste(img, text_img("DZIOB WYGRYWA", 64, (255, 255, 255), "ps", outline=6, ocol=(20, 90, 30)), W / 2, 1450, 1, scale=max(.05, q))
        paste(img, text_img("O 20 ZŁ", 64, (255, 255, 255), "ps", outline=6, ocol=(20, 90, 30)), W / 2, 1570, 1, scale=max(.05, q))
    r = lin(t, 21.3, 21.6)
    if r > 0:
        paste(img, KEBAB, W / 2 + 330, 1720, r, scale=0.6, rot=12, resample=Image.NEAREST)
        paste(img, text_img("20 zł = 1 kebab ;)", 64, (20, 20, 20), "px", shadow=False), W / 2 - 120, 1730, r)
    # confetti
    if t > 20.6:
        a = to_arr(img); rr = np.random.default_rng(7); dt = t - 20.6
        cols = [(255, 60, 60), (60, 200, 255), (80, 220, 80), (255, 255, 255), (200, 80, 255)]
        for k in range(110):
            x = rr.uniform(0, W) + 40 * math.sin(dt * 3 + k); y = -50 + dt * rr.uniform(350, 800) + rr.uniform(-300, 0)
            if 0 <= y < H - 14 and 0 <= x < W - 14: a[int(y):int(y) + 14, int(x):int(x) + 14] = cols[k % 5]
        img = to_img(a)
    return img

INFO = [("SERWER", "Dziob.6mc.PL"), ("IP", "dziob.6mc.pl"), ("PREMIERA", "24 grudnia (Wigilia)"), ("CENA", "0 zł"), ("START", "wszyscy od zera"), ("GRA", "Minecraft")]
def s_info(t):
    img = to_img(stripes((15, 15, 30), (25, 25, 50), t, speed=30))
    paste(img, text_img("WSZYSTKO CO MUSISZ", 58, (255, 230, 60), "ps", outline=4), W / 2, 230, lin(t, 22.5, 22.7))
    paste(img, text_img("WIEDZIEĆ:", 58, (255, 230, 60), "ps", outline=4), W / 2, 320, lin(t, 22.6, 22.8))
    for i, (k, v) in enumerate(INFO):
        rt = 22.8 + i * 0.6
        p = eo_back(lin(t, rt, rt + 0.3), 1.5)
        if p <= 0: continue
        row = Image.new("RGBA", (980, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
        d.rectangle([0, 0, 979, 169], fill=(255, 255, 255, 30), outline=(255, 255, 255, 120), width=4)
        row.alpha_composite(text_img(k, 34, (150, 200, 255), "ps", shadow=False), (30, 22))
        row.alpha_composite(text_img(v, 60, (255, 255, 255), "px", outline=2), (30, 72))
        paste(img, row, W / 2 + (1 - p) * 1200, 520 + i * 200, 1)
    return img

def s_cta(t):
    img = to_img(radial((90, 40, 160), (15, 5, 40)))
    a = to_arr(img); rr = np.random.default_rng(4)
    for k in range(60):
        x = rr.uniform(0, W); y = (rr.uniform(0, H) + t * rr.uniform(40, 140)) % H
        a[int(y):int(y) + 8, int(x):int(x) + 8] = 255
    img = to_img(a)
    lg = draw_logo2(t, 27.0); paste(img, lg, W / 2, 360, 1, scale=0.62)
    p = eo_back(lin(t, 27.6, 27.9), 2.2)
    if p > 0: paste(img, glow(pad_img(text_img("WBIJAJ 24.12", 74, (255, 230, 60), "ps", outline=6, ocol=(70, 20, 0)), 30), 20), W / 2, 660, 1, scale=max(.05, p) * (1 + 0.04 * math.sin(t * 7)))
    q = eo_back(lin(t, 28.2, 28.5))
    if q > 0:
        box = Image.new("RGBA", (960, 200), (0, 0, 0, 180)); d = ImageDraw.Draw(box); d.rectangle([0, 0, 959, 199], outline=(255, 255, 255, 220), width=6)
        tt_ = text_img("IP: dziob.6mc.pl", 50, (255, 255, 255), "ps", outline=0); box.alpha_composite(tt_, (480 - tt_.width // 2, 100 - tt_.height // 2))
        paste(img, box, W / 2, 900, 1, scale=max(.05, q))
    words(img, t, 29.0, [("WYŚLIJ", (255, 255, 255)), ("TO", (255, 255, 255)), ("ZIOMKOWI,", (255, 255, 255)), ("KTÓRY", (255, 255, 255)),
                         ("WYDAJE", (255, 255, 255)), ("KASĘ", (255, 120, 120)), ("NA", (255, 255, 255)), ("SERWERY", (255, 120, 120))], 1300, 62, per=0.14)
    r = lin(t, 30.4, 30.7)
    if r > 0: paste(img, text_img("Minecraft • 0 zł • Premiera w Wigilię", 40, (200, 220, 255), "px", outline=2), W / 2, 1640, r)
    b = icon("bird", 9); paste(img, b, W / 2, 1800 - abs(math.sin(t * math.pi * 2)) * 40, lin(t, 27.2, 27.5))
    return img

SCENES = [s_hook, s_q, s_pay, s_zero, s_power, s_also, s_math, s_info, s_cta]

def zoom_punch(t):
    z = 1.0
    for h in HITS: z += 0.07 * math.exp(-max(0, t - h) * 9) * (t >= h)
    return z

GRAIN = [np.random.default_rng(i).normal(0, 4, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1) for i in range(4)]
def render(fi):
    t = fi / FPS
    si = max(i for i, c in enumerate(CUTS[:-1]) if c <= t)
    img = SCENES[si](t)
    z = zoom_punch(t)
    if z > 1.002:
        big = img.resize((int(W * z), int(H * z)), Image.BILINEAR); l = (big.width - W) // 2; tp = (big.height - H) // 2
        img = big.crop((l, tp, l + W, tp + H))
    # white flash on cuts
    fl = max([clamp(1 - (t - c) / 0.12) for c in CUTS[1:-1] if t >= c] + [0])
    progress_bar(img, t); footnote(img, t)
    a = to_arr(img) + GRAIN[fi % 4]
    a = a + (255 - a) * fl * 0.6
    a *= clamp((DUR - t) / 0.5)
    return np.clip(a, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    from multiprocessing import Pool
    out = sys.argv[1]
    if len(sys.argv) > 4:
        s, e = float(sys.argv[2]), float(sys.argv[3])
        for f in range(int(round(s * FPS)), int(round(e * FPS)), max(1, int(float(sys.argv[4]) * FPS))):
            Image.frombytes("RGB", (W, H), render(f)).save(f"{out}/s5_{f / FPS:05.2f}.jpg", quality=85)
        sys.exit()
    wav = os.path.join(BUILD, "mix5.wav"); make_audio(wav)
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    with Pool(4) as p:
        for i, b in enumerate(p.imap(render, range(int(DUR * FPS)), chunksize=4)):
            ff.stdin.write(b)
            if i % 150 == 0: print("frame", i, flush=True)
    ff.stdin.close(); ff.wait()
