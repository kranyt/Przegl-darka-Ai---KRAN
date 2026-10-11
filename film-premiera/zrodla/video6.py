"""Vertical youth video #6: fake group chat 'Ekipa na święta' + Wigilia tier list + CTA. Synth jersey-club beat + chat SFX."""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from video import text_img, paste, glow, pad_img, clamp, lin, eo_cubic, eo_back, ei_cubic, icon
from video2 import draw_logo2
from video import eo_back as _eb
def eo_back(x, s=1.9): return 0.0 if x <= 0 else _eb(x, s)

FPS = 30
W, H = 1080, 1920
DUR = 34.0
INTER = "/usr/share/fonts/opentype/inter/"
_f = {}
def F(size, bold=False):
    k = (size, bold)
    if k not in _f: _f[k] = ImageFont.truetype(INTER + ("Inter-Bold.otf" if bold else "Inter-Medium.otf"), size)
    return _f[k]
def to_arr(img): return np.asarray(img.convert("RGB")).astype(np.float32)
def to_img(a): return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

T_HOOK, T_CHAT, T_TIER, T_CTA = 0.0, 2.2, 20.5, 28.0
PEOPLE = {"Kuba": (90, 160, 255), "Ola": (255, 110, 170), "Mati": (120, 220, 120), "Ty": (255, 210, 70)}
MSGS = [  # (time, who, text, big)
    (2.9, "Kuba", "ej co robimy w wigilię po kolacji?", False),
    (4.0, "Ola", "minecraft?", False),
    (5.0, "Mati", "tylko gdzie, wszędzie trzeba coś płacić", False),
    (6.3, "Ty", "dziob.6mc.pl", False),
    (7.1, "Ty", "premiera 24.12, wszyscy startują od zera", False),
    (8.4, "Kuba", "ile kosztuje?", False),
    (9.4, "Ty", "0 zł", True),
    (10.3, "Ola", "CO", True),
    (11.3, "Mati", "nawet mój młodszy brat może grać?", False),
    (12.6, "Ty", "nawet twoja babcia", False),
    (13.8, "Kuba", "dobra wbijamy", False),
    (14.6, "Ola", "WBIJAMY!!!", True),
    (15.6, "Mati", "[naklejka]", False),
    (17.0, "Kuba", "kto nie wbije ten stawia karpia", False),
]
TYPING = [(2.4, 2.9, "Kuba"), (8.0, 8.4, "Kuba"), (10.9, 11.3, "Mati"), (16.4, 17.0, "Kuba")]
TIER_ROWS = [("S", (255, 90, 90)), ("A", (255, 170, 80)), ("B", (255, 225, 90)), ("C", (150, 230, 110)), ("D", (110, 190, 255))]
TIER_ITEMS = [(4, "kłótnia przy stole", 21.6), (3, "Kevin sam w domu po raz 30.", 22.6), (2, "12 potraw", 23.6), (1, "prezenty", 24.6), (0, "PREMIERA DZIOB.6MC.PL", 25.8)]

# ====================================================================== AUDIO
SR = 44100
BPM_BEAT = 60 / 145
def make_audio(path):
    N = int(DUR * SR); out = np.zeros(N); rng = np.random.default_rng(12)
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
        t = tt(0.25); return np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(50 + 150 * np.exp(-t * 40)) / SR) * np.exp(-t * 12))
    def clap():
        n = rng.standard_normal(int(0.18 * SR)); t = tt(0.18); e = sum((t >= o) * np.exp(-np.maximum(0, t - o) * 55) for o in (0, 0.01, 0.022))
        return hp(lp(n, 7000), 1000) * e
    def hat(): return hp(rng.standard_normal(int(0.04 * SR)), 8000) * np.exp(-tt(0.04) * 110)
    def pop(m=79):
        t = tt(0.12); f = hz(m) * (1 + 0.6 * np.exp(-t * 60))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35)
    def tap(): return hp(rng.standard_normal(int(0.02 * SR)), 3000) * np.exp(-tt(0.02) * 250)
    def whoosh(d=0.35):
        n = rng.standard_normal(int(d * SR)); return lp(n, 3500) * np.linspace(0, 1, len(n)) ** 2
    def impact():
        t = tt(1.2); return np.tanh(3 * np.sin(2 * np.pi * np.cumsum(34 + 110 * np.exp(-t * 8)) / SR) * np.exp(-t * 2.5))
    def chord(ms, d):
        t = tt(d); s = 0
        for m in ms:
            for det in (-0.006, 0.006): s = s + 2 * ((t * hz(m) * (1 + det)) % 1) - 1
        return lp(s, 2200) * np.minimum(1, t / 0.01) * np.exp(-t * 3)
    beat = BPM_BEAT; bar = beat * 4
    chords = [[69, 72, 76], [65, 69, 72], [72, 76, 79], [67, 71, 74]]
    start = T_HOOK + 0.0
    nb = int((DUR - 1.0) / bar)
    for b in range(nb + 1):
        t0 = start + b * bar
        if t0 >= DUR - 1.0: break
        quiet = T_CHAT - 0.2 < t0 < T_CHAT + 1.2  # small drop-in after hook
        # jersey club kick pattern on 8ths: x . . x . . x . | x . x . x x x .
        pat = [0, 3, 6, 8, 10, 12, 13, 14] if b % 2 else [0, 3, 6, 8, 11, 14]
        for p in pat: add(t0 + p * beat / 2, kick(), 0.45 if not quiet else 0.2)
        add(t0 + beat, clap(), 0.25); add(t0 + 3 * beat, clap(), 0.25)
        for h in range(8): add(t0 + h * beat / 2 + beat / 4, hat(), 0.05)
        ch = chords[b % 4]
        for s_ in (0, 1.5, 3):
            add(t0 + s_ * beat, chord(ch, beat * 1.2), 0.035)
        # vocal-chop-like plucks
        for k, m in enumerate([ch[2] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24]):
            add(t0 + (0.5 + k) * beat, np.sin(2 * np.pi * hz(m) * tt(0.15)) * np.exp(-tt(0.15) * 25), 0.05)
    add(0.0, impact(), 0.5)
    for k in range(14): add(0.3 + k * 0.09, tap(), 0.25)
    for (mt, who, txt, big) in MSGS:
        add(mt, pop(84 if who == "Ty" else 79), 0.35)
        if big: add(mt, impact()[: int(0.5 * SR)], 0.35)
    for (a, b_, who) in TYPING:
        k = a
        while k < b_: add(k, tap(), 0.15); k += 0.07
    add(T_TIER - 0.3, whoosh(0.4), 0.2); add(T_TIER, impact(), 0.4)
    for (row, name, it) in TIER_ITEMS:
        add(it - 0.3, whoosh(0.3), 0.18); add(it, pop(72 + (4 - row) * 3), 0.4)
    add(TIER_ITEMS[-1][2], impact(), 0.6)
    add(T_CTA - 0.35, whoosh(0.4), 0.2); add(T_CTA, impact(), 0.45)
    out *= np.clip(np.minimum(np.arange(N) / SR / 0.02, (DUR - np.arange(N) / SR) / 0.9), 0, 1)
    out = np.tanh(out * 1.15) * 0.92
    st = np.stack([out, out], 1).astype(np.float32)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", path], input=st.tobytes())

# ====================================================================== VISUALS
def bg_grad(t, c1, c2):
    yy = np.linspace(0, 1, H)[:, None, None]; xx = np.linspace(0, 1, W)[None, :, None]
    m = np.clip(yy * 0.7 + xx * 0.3 + 0.08 * math.sin(t * 0.8), 0, 1)
    a = np.array(c1, np.float32) * (1 - m) + np.array(c2, np.float32) * m
    return np.broadcast_to(a, (H, W, 3)).copy()

def avatar(name, s=64):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, s - 1, s - 1], fill=PEOPLE[name] + (255,))
    ch = name[0]; f = F(int(s * 0.5), True); w = f.getlength(ch)
    d.text((s / 2 - w / 2, s * 0.18), ch, font=f, fill=(20, 20, 30, 255)); return im

def wrap(text, font, maxw):
    words = text.split(" "); lines = [""]
    for w in words:
        test = (lines[-1] + " " + w).strip()
        if font.getlength(test) <= maxw: lines[-1] = test
        else: lines.append(w)
    return lines

STICKER = None
def bubble(who, text, big):
    mine = who == "Ty"
    if text == "[naklejka]":
        b = icon("bird", 14); im = Image.new("RGBA", (b.width + 20, b.height + 60), (0, 0, 0, 0)); im.alpha_composite(b, (10, 50))
        if not mine: ImageDraw.Draw(im).text((14, 0), who, font=F(30, True), fill=PEOPLE[who] + (255,))
        return im, True
    font = F(96 if big else 46, True if big else False)
    lines = wrap(text, font, 620)
    lh = int(font.size * 1.25); tw = max(int(font.getlength(l)) for l in lines)
    pad = 30; bw = tw + 2 * pad; bh = lh * len(lines) + 2 * pad - int(font.size * 0.25)
    top = 0 if mine else 44
    im = Image.new("RGBA", (bw, bh + top), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if not mine: d.text((12, 0), who, font=F(30, True), fill=PEOPLE[who] + (255,))
    col = (70, 120, 255, 255) if mine else (52, 52, 66, 255)
    d.rounded_rectangle([0, top, bw - 1, top + bh - 1], radius=36, fill=col)
    for i, l in enumerate(lines): d.text((pad, top + pad - int(font.size * 0.15) + i * lh), l, font=font, fill=(255, 255, 255, 255))
    return im, mine
BUBBLES = [bubble(w, t, b) for (_, w, t, b) in MSGS]

PX0, PY0, PW, PH = 70, 250, 940, 1500
def phone_frame():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([PX0 - 24, PY0 - 24, PX0 + PW + 24, PY0 + PH + 24], radius=90, fill=(15, 15, 20, 255))
    d.rounded_rectangle([PX0, PY0, PX0 + PW, PY0 + PH], radius=70, fill=(24, 24, 32, 255))
    d.rounded_rectangle([PX0 + PW / 2 - 110, PY0 + 18, PX0 + PW / 2 + 110, PY0 + 58], radius=20, fill=(0, 0, 0, 255))
    # header
    d.rectangle([PX0, PY0 + 80, PX0 + PW, PY0 + 210], fill=(34, 34, 46, 255))
    for i, n in enumerate(["Kuba", "Ola", "Mati"]): im.alpha_composite(avatar(n, 70), (PX0 + 40 + i * 44, PY0 + 110))
    d.text((PX0 + 220, PY0 + 108), "EKIPA NA ŚWIĘTA", font=F(44, True), fill=(255, 255, 255, 255))
    d.text((PX0 + 220, PY0 + 162), "4 osoby • aktywni teraz", font=F(28), fill=(150, 220, 150, 255))
    # input bar
    d.rounded_rectangle([PX0 + 30, PY0 + PH - 120, PX0 + PW - 30, PY0 + PH - 40], radius=40, fill=(40, 40, 54, 255))
    d.text((PX0 + 70, PY0 + PH - 102), "Napisz wiadomość...", font=F(34), fill=(130, 130, 150, 255))
    return im
PHONE = phone_frame()
CHAT_TOP, CHAT_BOT = PY0 + 225, PY0 + PH - 140

def chat_layer(t):
    lay = Image.new("RGBA", (PW, CHAT_BOT - CHAT_TOP), (0, 0, 0, 0))
    shown = [i for i, m in enumerate(MSGS) if t >= m[0]]
    typing = [w for (a, b, w) in TYPING if a <= t < b]
    gap = 22
    heights = [BUBBLES[i][0].height + gap for i in shown]
    # smooth scroll: newest message height eases in
    y = lay.height - (110 if typing else 20)
    items = []
    for k in range(len(shown) - 1, -1, -1):
        i = shown[k]; bim, mine = BUBBLES[i]
        p = eo_cubic(lin(t, MSGS[i][0], MSGS[i][0] + 0.25)) if k == len(shown) - 1 else 1.0
        h = bim.height + gap
        y -= h * p
        items.append((i, y, p, mine))
        if y < -400: break
    for (i, y, p, mine) in items:
        bim = BUBBLES[i][0]
        sc = 0.6 + 0.4 * eo_back(p, 2.2)
        b2 = bim.resize((max(1, int(bim.width * sc)), max(1, int(bim.height * sc))), Image.BILINEAR) if sc < 0.999 else bim
        x = PW - 40 - b2.width if mine else 110
        if not mine and MSGS[i][2] != "[naklejka]":
            av = avatar(MSGS[i][1], 64); lay.paste(av, (30, int(y + bim.height - 64)), av)
        if MSGS[i][2] == "[naklejka]":
            b2 = b2.rotate(8 * math.sin(t * 10), resample=Image.BICUBIC, expand=True)
        lay.paste(b2, (int(x), int(y + (bim.height - b2.height))), b2)
    if typing:
        d = ImageDraw.Draw(lay); yy = lay.height - 100
        lay.alpha_composite(avatar(typing[0], 64), (30, yy + 6))
        d.rounded_rectangle([110, yy, 290, yy + 76], radius=38, fill=(52, 52, 66, 255))
        for k in range(3):
            o = abs(math.sin(t * 8 + k * 0.8)) * 10
            d.ellipse([140 + k * 44, yy + 28 - o, 162 + k * 44, yy + 50 - o], fill=(200, 200, 210, 255))
    return lay

def floaters(img, t):
    # reaction hearts after big messages
    for (mt, who, txt, big) in MSGS:
        if not big or not (mt <= t < mt + 2.0): continue
        rr = np.random.default_rng(int(mt * 10))
        for k in range(10):
            dt = t - mt - k * 0.05
            if dt < 0: continue
            x = 1030 + rr.uniform(-25, 25) + 15 * math.sin(dt * 5 + k); y = 1500 - dt * rr.uniform(400, 700)
            heart = icon("heart", 4)
            paste(img, heart, x, y, clamp(1 - dt / 1.8), scale=0.8 + 0.4 * rr.random())

def s_hook(t):
    img = to_img(bg_grad(t, (120, 40, 200), (255, 90, 140)))
    s = "POV: twoja ekipa szuka serwera na święta"
    n = int(len(s) * lin(t, 0.25, 1.5))
    f = F(84, True); lines = wrap(s, f, 920)
    d = ImageDraw.Draw(img); y = 760; shown = 0; cur = None
    for l in lines:
        k = max(0, min(len(l), n - shown)); shown += len(l) + 1
        w = f.getlength(l); part = l[:k]
        d.text((W / 2 - w / 2 + 5, y + 5), part, font=f, fill=(40, 0, 60, 255)); d.text((W / 2 - w / 2, y), part, font=f, fill=(255, 255, 255, 255))
        if k > 0 or cur is None: cur = (W / 2 - w / 2 + f.getlength(part) + 10, y)
        y += 110
    if cur and int(t * 4) % 2 == 0: d.rectangle([cur[0], cur[1] + 10, cur[0] + 12, cur[1] + 100], fill=(255, 255, 255, 255))
    return img

def s_chat(t):
    img = to_img(bg_grad(t, (30, 20, 60), (90, 30, 110)))
    p = eo_back(lin(t, T_CHAT, T_CHAT + 0.5), 1.3)
    ph = PHONE.copy(); ph.alpha_composite(chat_layer(t), (PX0, CHAT_TOP))
    # keep chat inside rounded phone area (mask header overlap)
    d = ImageDraw.Draw(ph); d.rectangle([PX0, PY0 + 80, PX0 + PW, PY0 + 210], fill=(34, 34, 46, 255))
    hdr = PHONE.crop((PX0, PY0 + 80, PX0 + PW, PY0 + 210)); ph.alpha_composite(hdr, (PX0, PY0 + 80))
    inp = PHONE.crop((PX0, CHAT_BOT, PX0 + PW, PY0 + PH)); ph.alpha_composite(inp, (PX0, CHAT_BOT))
    paste(img, ph, W / 2, H / 2 + (1 - p) * 1400 + 40, 1, rot=(1 - p) * 8, resample=Image.BICUBIC)
    floaters(img, t)
    # caption above phone
    cap = "czat ekipy w grudniu:" if t < 9.4 else ("0 zł?!" if t < 12.6 else "deal.")
    paste(img, text_img(cap, 44, (255, 255, 255), "ps", outline=4, ocol=(40, 0, 60)), W / 2, 140, lin(t, T_CHAT + 0.4, T_CHAT + 0.8))
    return img

def s_tier(t):
    img = to_img(bg_grad(t, (20, 20, 28), (40, 30, 60)))
    d = ImageDraw.Draw(img)
    paste(img, text_img("TIER LIST:", 70, (255, 255, 255), "ps", outline=5), W / 2, 170, 1)
    paste(img, text_img("plany na Wigilię", 64, (255, 220, 120), "px", outline=4), W / 2, 270, 1)
    x0, y0, rh = 40, 380, 250
    for i, (lab, col) in enumerate(TIER_ROWS):
        y = y0 + i * (rh + 14)
        d.rectangle([x0, y, x0 + 180, y + rh], fill=col + (255,))
        d.rectangle([x0 + 190, y, W - 40, y + rh], fill=(44, 44, 56, 255))
        f = F(110, True); w = f.getlength(lab); d.text((x0 + 90 - w / 2, y + rh / 2 - 70), lab, font=f, fill=(20, 20, 30, 255))
    for (row, name, it) in TIER_ITEMS:
        p = eo_back(lin(t, it - 0.25, it + 0.15), 1.8)
        if p <= 0: continue
        S = row == 0
        f = F(46 if not S else 52, True); lines = wrap(name, f, 640 if not S else 700)
        cw = int(max(f.getlength(l) for l in lines)) + 60; chh = 70 * len(lines) + 40
        card = Image.new("RGBA", (cw, chh), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, cw - 1, chh - 1], radius=24, fill=(255, 215, 60, 255) if S else (240, 240, 245, 255))
        for k, l in enumerate(lines): cd.text((30, 22 + k * 70), l, font=f, fill=(20, 20, 30, 255))
        ty = y0 + row * (rh + 14) + rh / 2
        sx, sy = W / 2, 1900
        x = sx + (x0 + 210 + cw / 2 - sx) * p; y = sy + (ty - sy) * p
        if S: card = glow(pad_img(card, 30), 22, 1.6 * (0.6 + 0.4 * math.sin(t * 8)))
        paste(img, card, x, y, 1, rot=(1 - p) * 20, resample=Image.BICUBIC)
    st = TIER_ITEMS[-1][2]
    if t > st:
        a = to_arr(img); rr = np.random.default_rng(3); dt = t - st
        cols = [(255, 90, 90), (90, 200, 255), (120, 230, 120), (255, 230, 80), (220, 120, 255)]
        for k in range(120):
            ang = rr.uniform(-math.pi, 0); v = rr.uniform(500, 1400)
            x = W / 2 + math.cos(ang) * v * dt; y = y0 + rh / 2 + math.sin(ang) * v * dt + 1100 * dt * dt
            if 0 <= x < W - 14 and 0 <= y < H - 14: a[int(y):int(y) + 14, int(x):int(x) + 14] = cols[k % 5]
        img = to_img(a)
    return img

def s_cta(t):
    img = to_img(bg_grad(t, (60, 20, 120), (255, 80, 120)))
    a = to_arr(img); rr = np.random.default_rng(9)
    for k in range(70):
        x = rr.uniform(0, W); y = (rr.uniform(0, H) + t * rr.uniform(60, 160)) % H
        a[int(y):int(y) + 8, int(x):int(x) + 8] = 255
    img = to_img(a)
    lg = draw_logo2(t, T_CTA); paste(img, lg, W / 2, 330, 1, scale=0.62)
    p = eo_back(lin(t, T_CTA + 0.5, T_CTA + 0.8), 2.0)
    if p > 0: paste(img, glow(pad_img(text_img("24.12", 150, (255, 235, 90), "ps", outline=8, ocol=(80, 20, 40)), 30), 22), W / 2, 640, 1, scale=max(.05, p) * (1 + 0.04 * math.sin(t * 7)))
    q = eo_back(lin(t, T_CTA + 1.0, T_CTA + 1.3))
    if q > 0:
        box = Image.new("RGBA", (960, 190), (0, 0, 0, 170)); bd = ImageDraw.Draw(box); bd.rounded_rectangle([0, 0, 959, 189], radius=40, outline=(255, 255, 255, 230), width=6)
        tx = text_img("IP: dziob.6mc.pl", 52, (255, 255, 255), "ps", outline=0); box.alpha_composite(tx, (480 - tx.width // 2, 95 - tx.height // 2))
        paste(img, box, W / 2, 880, 1, scale=max(.05, q))
    r = lin(t, T_CTA + 1.6, T_CTA + 2.0)
    if r > 0:
        f = F(70, True); d = ImageDraw.Draw(img)
        for k, l in enumerate(["oznacz ekipę,", "z którą wbijasz"]):
            w = f.getlength(l); y = 1100 + k * 95 + (1 - eo_cubic(r)) * 40
            d.text((W / 2 - w / 2 + 5, y + 5), l, font=f, fill=(40, 0, 60, int(255 * r))); d.text((W / 2 - w / 2, y), l, font=f, fill=(255, 255, 255, int(255 * r)))
    s = lin(t, T_CTA + 2.4, T_CTA + 2.8)
    if s > 0: paste(img, text_img("Minecraft • 0 zł • start od zera", 44, (255, 240, 200), "px", outline=3, ocol=(60, 0, 40)), W / 2, 1390, s)
    paste(img, icon("bird", 10), W / 2, 1640 - abs(math.sin(t * math.pi * 2.4)) * 60, lin(t, T_CTA + 0.2, T_CTA + 0.5), rot=8 * math.sin(t * 5), resample=Image.NEAREST)
    return img

SCENES = [(T_HOOK, s_hook), (T_CHAT, s_chat), (T_TIER, s_tier), (T_CTA, s_cta)]
GRAIN = [np.random.default_rng(i).normal(0, 3.5, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1) for i in range(4)]
PUNCH = [0.0, T_CHAT, T_TIER, TIER_ITEMS[-1][2], T_CTA] + [m[0] for m in MSGS if m[3]]

def render(fi):
    t = fi / FPS
    si = max(i for i, (s, _) in enumerate(SCENES) if s <= t)
    img = SCENES[si][1](t)
    z = 1.0 + sum(0.05 * math.exp(-max(0, t - h) * 9) for h in PUNCH if t >= h)
    if z > 1.002:
        big = img.resize((int(W * z), int(H * z)), Image.BILINEAR); l = (big.width - W) // 2; tp = (big.height - H) // 2
        img = big.crop((l, tp, l + W, tp + H))
    fl = max([clamp(1 - (t - c) / 0.12) for c in (T_CHAT, T_TIER, T_CTA) if t >= c] + [0])
    a = to_arr(img) + GRAIN[fi % 4]
    a = a + (255 - a) * fl * 0.6
    a *= clamp((DUR - t) / 0.6)
    return np.clip(a, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    from multiprocessing import Pool
    out = sys.argv[1]
    if len(sys.argv) > 4:
        s, e = float(sys.argv[2]), float(sys.argv[3])
        for f in range(int(round(s * FPS)), int(round(e * FPS)), max(1, int(float(sys.argv[4]) * FPS))):
            Image.frombytes("RGB", (W, H), render(f)).save(f"{out}/s6_{f / FPS:05.2f}.jpg", quality=85)
        sys.exit()
    wav = os.path.join(BUILD, "mix6.wav"); make_audio(wav)
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    with Pool(4) as p:
        for i, b in enumerate(p.imap(render, range(int(DUR * FPS)), chunksize=4)):
            ff.stdin.write(b)
            if i % 150 == 0: print("frame", i, flush=True)
    ff.stdin.close(); ff.wait()
