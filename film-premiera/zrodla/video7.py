"""Vertical viral challenge video #7: 'Tylko 1% graczy to znajdzie' - 3 find-it levels, reveal of the Dziob.6mc.PL premiere,
full info card, loop-friendly ending. Synth suspense + trap drop."""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from video import text_img, paste, glow, pad_img, clamp, lin, eo_cubic, ei_cubic, icon, tex, shade, mc_panel
from video import eo_back as _eb
from video2 import draw_logo2
def eo_back(x, s=1.9): return 0.0 if x <= 0 else _eb(x, s)

FPS = 30
W, H = 1080, 1920
DUR = 35.0
INTER = "/usr/share/fonts/opentype/inter/"
_f = {}
def F(size, bold=True):
    k = (size, bold)
    if k not in _f: _f[k] = ImageFont.truetype(INTER + ("Inter-Bold.otf" if bold else "Inter-Medium.otf"), size)
    return _f[k]
def to_arr(img): return np.asarray(img.convert("RGB")).astype(np.float32)
def to_img(a): return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

# levels: (start, timer_start, reveal)
LV = [(2.0, 3.0, 8.0), (8.8, 9.6, 14.6), (15.4, 16.2, 21.2)]
T_TWIST, T_INFO, T_CTA = 22.2, 25.4, 31.4
GX, GY, CS, COLS, ROWS = 0, 420, 120, 9, 11
ODD = [(6, 7), (2, 3), None]

# ====================================================================== AUDIO
SR = 44100
def make_audio(path):
    N = int(DUR * SR); out = np.zeros(N); rng = np.random.default_rng(21)
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
    def tick(hi=True):
        t = tt(0.05); return hp(rng.standard_normal(len(t)), 2500 if hi else 1200) * np.exp(-t * 120) + np.sin(2 * np.pi * (2200 if hi else 1600) * t) * np.exp(-t * 90) * 0.5
    def impact():
        t = tt(1.4); return np.tanh(3 * np.sin(2 * np.pi * np.cumsum(32 + 120 * np.exp(-t * 7)) / SR) * np.exp(-t * 2.3)) + lp(rng.standard_normal(len(t)), 400) * np.exp(-t * 5) * 0.4
    def ding(m=88):
        t = tt(1.0); return (np.sin(2 * np.pi * hz(m) * t) + 0.5 * np.sin(2 * np.pi * hz(m + 7) * t) + 0.3 * np.sin(2 * np.pi * hz(m + 12) * t)) * np.exp(-t * 4)
    def whoosh(d=0.45, up=True):
        n = rng.standard_normal(int(d * SR)); x = np.linspace(0, 1, len(n)); return lp(n, 3500) * (x ** 2 if up else np.sin(x * np.pi) ** 2)
    def buzzer():
        t = tt(0.5); return lp(np.sign(np.sin(2 * np.pi * 110 * t)) + np.sign(np.sin(2 * np.pi * 116 * t)), 1500) * 0.25 * np.minimum(1, (0.5 - t) / 0.05)
    def pad(ms, d):
        t = tt(d); s = 0
        for m in ms:
            for det in (-0.004, 0.004): s = s + np.sin(2 * np.pi * hz(m) * (1 + det) * t) + 0.3 * np.sin(4 * np.pi * hz(m) * (1 + det) * t)
        return s * np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.4)
    def kick():
        t = tt(0.35); return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(45 + 140 * np.exp(-t * 35)) / SR) * np.exp(-t * 8))
    def b808(m, d):
        t = tt(d); f = hz(m) * (1 + 0.5 * np.exp(-t * 30))
        return np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.minimum(1, (d - t) / 0.05) * np.exp(-t * 1.2)
    def clap():
        n = rng.standard_normal(int(0.2 * SR)); t = tt(0.2); e = sum((t >= o) * np.exp(-np.maximum(0, t - o) * 60) for o in (0, 0.012, 0.024))
        return hp(lp(n, 6000), 900) * e * 0.8
    def hat(): return hp(rng.standard_normal(int(0.05 * SR)), 7000) * np.exp(-tt(0.05) * 90)
    # hook
    add(0.0, impact(), 0.55); add(0.0, whoosh(0.6, False), 0.12)
    # suspense pad during levels + ticking during timers
    add(1.8, pad([45, 52, 57, 60], T_TWIST - 1.8), 0.035)
    for (s, ts, rv) in LV:
        add(s - 0.4, whoosh(0.4), 0.15); add(s, impact()[: int(0.7 * SR)], 0.35)
        k = 0; tq = ts
        while tq < rv - 0.05:
            add(tq, tick(k % 2 == 0), 0.35); tq += 0.5 if tq < rv - 1.5 else 0.25; k += 1
        add(rv, ding(88), 0.35); add(rv, impact()[: int(0.5 * SR)], 0.3)
    add(LV[2][2] + 0.6, buzzer(), 0.0)
    # twist: riser + drop
    add(T_TWIST - 1.0, whoosh(1.0), 0.25); add(T_TWIST, impact(), 0.7)
    # trap beat from twist to end
    roots = [45, 45, 41, 43]
    for b in range(int((DUR - T_TWIST) / 2) + 1):
        t0 = T_TWIST + b * 2.0
        if t0 > DUR - 1.0: break
        r = roots[b % 4]
        add(t0, kick(), 0.55); add(t0 + 0.75, kick(), 0.4); add(t0 + 1.25, kick(), 0.3)
        add(t0, b808(r, 0.7), 0.28); add(t0 + 0.75, b808(r, 0.45), 0.22); add(t0 + 1.25, b808(r + 3, 0.7), 0.22)
        add(t0 + 0.5, clap(), 0.32); add(t0 + 1.5, clap(), 0.32)
        for h in range(16): add(t0 + h * 0.125, hat(), 0.07 if h % 2 == 0 else 0.045)
        mel = [81, 84, 88, 86, 84, 81, 79, 76]
        for k in range(4): add(t0 + k * 0.5 + 0.25, np.sin(2 * np.pi * hz(mel[(b * 4 + k) % 8]) * tt(0.35)) * np.exp(-tt(0.35) * 9), 0.05)
    for i in range(7): add(T_INFO + 0.3 + i * 0.6, ding(93 + (i % 3) * 2)[: int(0.3 * SR)], 0.12)
    add(T_CTA - 0.4, whoosh(0.4), 0.18); add(T_CTA, impact()[: int(0.8 * SR)], 0.4)
    out *= np.clip(np.minimum(np.arange(N) / SR / 0.02, (DUR - np.arange(N) / SR) / 0.6), 0, 1)
    out = np.tanh(out * 1.15) * 0.92
    st = np.stack([out, out], 1).astype(np.float32)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", path], input=st.tobytes())

# ====================================================================== GRIDS
def grid_level1():
    g = tex("grass_side", 1).resize((CS, CS), Image.NEAREST).convert("RGBA")
    im = Image.new("RGBA", (COLS * CS, ROWS * CS))
    for x in range(COLS):
        for y in range(ROWS): im.alpha_composite(g, (x * CS, y * CS))
    # the odd one: a grass block with tiny bird eyes + beak (hidden Dziob)
    ox, oy = ODD[0]; px = CS // 16
    d = ImageDraw.Draw(im); bx, by = ox * CS, oy * CS
    d.rectangle([bx + 5 * px, by + 7 * px, bx + 6 * px - 1, by + 8 * px - 1], fill=(15, 15, 15, 255))
    d.rectangle([bx + 10 * px, by + 7 * px, bx + 11 * px - 1, by + 8 * px - 1], fill=(15, 15, 15, 255))
    d.rectangle([bx + 7 * px, by + 9 * px, bx + 9 * px - 1, by + 10 * px - 1], fill=(240, 150, 40, 255))
    return im
def grid_level2():
    s = tex("stone", 4).resize((CS, CS), Image.NEAREST).convert("RGBA")
    im = Image.new("RGBA", (COLS * CS, ROWS * CS))
    for x in range(COLS):
        for y in range(ROWS): im.alpha_composite(s, (x * CS, y * CS))
    ox, oy = ODD[1]
    odd = shade(tex("stone", 4).resize((CS, CS), Image.NEAREST), 1.10).convert("RGBA")  # slightly lighter stone
    im.alpha_composite(odd, (ox * CS, oy * CS))
    return im
LETTERS = "ABCDEFGHIJKLMNOPRSTUWYZ"
L3_ROW, L3_COL = 6, 2  # 'DZIOB' hidden horizontally
def grid_level3():
    r = np.random.default_rng(13)
    im = Image.new("RGBA", (COLS * CS, ROWS * CS), (25, 25, 35, 255)); d = ImageDraw.Draw(im)
    grid = [[LETTERS[r.integers(0, len(LETTERS))] for _ in range(COLS)] for _ in range(ROWS)]
    # avoid accidental 'DZIOB'-like decoys; place target
    for i, ch in enumerate("DZIOB"): grid[L3_ROW][L3_COL + i] = ch
    for y in range(ROWS):
        for x in range(COLS):
            d.rectangle([x * CS + 4, y * CS + 4, x * CS + CS - 5, y * CS + CS - 5], fill=(45, 45, 60, 255))
            ch = grid[y][x]; f = F(70); w = f.getlength(ch)
            d.text((x * CS + CS / 2 - w / 2, y * CS + 18), ch, font=f, fill=(235, 235, 245, 255))
    return im
GRIDS = [grid_level1(), grid_level2(), grid_level3()]
TITLES = [("POZIOM 1", "Znajdź ukryty DZIÓB"), ("POZIOM 2", "Znajdź jaśniejszy kamień"), ("POZIOM 3", "Znajdź słowo DZIOB")]

def bg(t, c1, c2):
    yy = np.linspace(0, 1, H)[:, None, None]
    a = np.array(c1, np.float32) * (1 - yy) + np.array(c2, np.float32) * yy
    return np.broadcast_to(a, (H, W, 3)).copy()

def outlined(img, text, size, col, x, y, alpha=1.0, stroke=8, scol=(0, 0, 0)):
    f = F(size); w = f.getlength(text)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((x - w / 2, y - size * 0.6), text, font=f, fill=col + (255,), stroke_width=stroke, stroke_fill=scol + (255,))
    if alpha < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(lay)

def s_hook(t):
    img = to_img(bg(t, (20, 10, 40), (80, 20, 90)))
    # preview grid blurred in background
    g = GRIDS[0].resize((W, int(GRIDS[0].height * W / GRIDS[0].width))).filter(ImageFilter.GaussianBlur(10))
    g.putalpha(90); img.alpha_composite(g, (0, GY))
    p = eo_back(lin(t, 0.0, 0.2), 3)
    if p > 0:
        outlined(img, "TYLKO 1%", int(170 * p) + 1, (255, 230, 60), W / 2, 640)
        outlined(img, "GRACZY", int(130 * p) + 1, (255, 255, 255), W / 2, 820)
        outlined(img, "TO ZNAJDZIE", int(110 * p) + 1, (255, 255, 255), W / 2, 970)
    q = lin(t, 0.8, 1.0)
    if q > 0: outlined(img, "masz 5 sekund na poziom", 56, (150, 230, 255), W / 2, 1180, q, stroke=5)
    return img

def timer_ring(img, frac, cx, cy, r=78):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 0, 0, 170))
    col = (85, 255, 120) if frac > 0.4 else ((255, 210, 60) if frac > 0.2 else (255, 70, 70))
    d.arc([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], -90, -90 + 360 * frac, fill=col + (255,), width=16)
    sec = str(int(math.ceil(frac * 5))) if frac > 0 else "0"
    f = F(80); w = f.getlength(sec); d.text((cx - w / 2, cy - 50), sec, font=f, fill=(255, 255, 255, 255))

def s_level(t, i):
    s, ts, rv = LV[i]
    img = to_img(bg(t, [(30, 60, 30), (40, 40, 50), (20, 20, 40)][i], (10, 10, 15)))
    lab, task = TITLES[i]
    p = eo_back(lin(t, s, s + 0.25), 2.2)
    outlined(img, lab, 64, (255, 230, 60), W / 2, 130, 1)
    if p > 0: outlined(img, task, 62, (255, 255, 255), W / 2, 240, 1, stroke=6)
    gp = eo_cubic(lin(t, s + 0.1, s + 0.6))
    g = GRIDS[i]
    if t >= rv:
        # dim everything except the target
        g = g.copy(); a = to_arr(g) * (1 - 0.6 * lin(t, rv, rv + 0.25)); g = to_img(a)
        if i < 2:
            ox, oy = ODD[i]; g.alpha_composite(GRIDS[i].crop((ox * CS, oy * CS, ox * CS + CS, oy * CS + CS)), (ox * CS, oy * CS))
        else:
            g.alpha_composite(GRIDS[i].crop((L3_COL * CS, L3_ROW * CS, (L3_COL + 5) * CS, L3_ROW * CS + CS)), (L3_COL * CS, L3_ROW * CS))
    img.alpha_composite(g, (GX, int(GY + (1 - gp) * 1500)))
    if ts <= t < rv:
        timer_ring(img, clamp(1 - (t - ts) / (rv - ts)), W - 110, 1700 + 90)
        if rv - t < 1.6: outlined(img, "...", 80, (255, 255, 255), W / 2, 1790, 1)
    if t >= rv:
        rp = eo_back(lin(t, rv, rv + 0.3), 2.0)
        d = ImageDraw.Draw(img)
        if i < 2:
            ox, oy = ODD[i]; cx = GX + ox * CS + CS / 2; cy = GY + oy * CS + CS / 2; r = 95 * max(rp, 0.05) + 6 * math.sin(t * 10)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 50, 50, 255), width=12)
            outlined(img, "TU!", 90, (255, 60, 60), cx + (220 if ox < 5 else -220), cy - 120, min(1, rp * 2), stroke=8, scol=(255, 255, 255))
        else:
            x0 = GX + L3_COL * CS; y0 = GY + L3_ROW * CS
            d.rounded_rectangle([x0 - 6, y0 - 6, x0 + 5 * CS + 6, y0 + CS + 6], radius=30, outline=(255, 50, 50, 255), width=12)
            outlined(img, "DZIOB!", 100, (255, 230, 60), W / 2, y0 - 120, min(1, rp * 2), stroke=8)
        msg = ["Znalazłeś? Pisz w komentarzu", "Dalej! Teraz trudniej...", "Wiesz już, co to znaczy?"][i]
        outlined(img, msg, 50, (255, 255, 255), W / 2, 1790, lin(t, rv + 0.2, rv + 0.4), stroke=5)
    return img

def s_twist(t):
    img = to_img(bg(t, (255, 60, 90), (120, 20, 160)))
    a = to_arr(img); yy, xx = np.ogrid[0:H, 0:W]
    ang = np.arctan2(yy - 700, xx - W / 2) + t * 0.8
    a += ((np.sin(ang * 12) > 0.5) * 25)[..., None]; img = to_img(a)
    lg = draw_logo2(t, T_TWIST); paste(img, lg, W / 2, 560, 1, scale=0.66)
    p = eo_back(lin(t, T_TWIST + 0.5, T_TWIST + 0.8), 2.2)
    if p > 0:
        outlined(img, "PREMIERA", int(120 * p) + 1, (255, 255, 255), W / 2, 900)
        outlined(img, "24 GRUDNIA", int(140 * p) + 1, (255, 230, 60), W / 2, 1080)
    q = lin(t, T_TWIST + 1.4, T_TWIST + 1.7)
    if q > 0: outlined(img, "w Wigilię wbijamy wszyscy", 60, (255, 255, 255), W / 2, 1290, q, stroke=6)
    return img

INFO = [("SERWER", "Dziob.6mc.PL"), ("IP", "dziob.6mc.pl"), ("PREMIERA", "24 grudnia 2026 (Wigilia)"), ("CENA", "0 zł – za darmo"),
        ("START", "wszyscy od zera"), ("GRA", "Minecraft")]
def s_info(t):
    img = to_img(bg(t, (15, 15, 30), (40, 20, 70)))
    outlined(img, "WSZYSTKO, CO", 76, (255, 230, 60), W / 2, 170, lin(t, T_INFO, T_INFO + 0.2))
    outlined(img, "MUSISZ WIEDZIEĆ", 76, (255, 230, 60), W / 2, 270, lin(t, T_INFO + 0.1, T_INFO + 0.3))
    for i, (k, v) in enumerate(INFO):
        rt = T_INFO + 0.3 + i * 0.6
        p = eo_back(lin(t, rt, rt + 0.3), 1.5)
        if p <= 0: continue
        row = Image.new("RGBA", (980, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
        d.rounded_rectangle([0, 0, 979, 189], radius=36, fill=(255, 255, 255, 28), outline=(255, 255, 255, 120), width=4)
        d.text((40, 24), k, font=F(36), fill=(150, 200, 255, 255))
        d.text((40, 78), v, font=F(68), fill=(255, 255, 255, 255))
        paste(img, row, W / 2 + (1 - p) * 1200, 470 + i * 215, 1)
    return img

def s_cta(t):
    img = to_img(bg(t, (20, 10, 40), (80, 20, 90)))
    g = GRIDS[0].resize((W, int(GRIDS[0].height * W / GRIDS[0].width))).filter(ImageFilter.GaussianBlur(10)); g.putalpha(90); img.alpha_composite(g, (0, GY))
    p = eo_back(lin(t, T_CTA, T_CTA + 0.25), 2.5)
    if p > 0:
        outlined(img, "W ILU SEKUNDACH", int(96 * p) + 1, (255, 255, 255), W / 2, 520)
        outlined(img, "ZNALAZŁEŚ?", int(130 * p) + 1, (255, 230, 60), W / 2, 680)
    q = lin(t, T_CTA + 0.7, T_CTA + 1.0)
    if q > 0:
        outlined(img, "napisz w komentarzu", 64, (150, 230, 255), W / 2, 900, q, stroke=6)
        outlined(img, "i wyślij ziomkowi", 64, (150, 230, 255), W / 2, 990, q, stroke=6)
    r = lin(t, T_CTA + 1.4, T_CTA + 1.7)
    if r > 0:
        box = Image.new("RGBA", (960, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(box)
        d.rounded_rectangle([0, 0, 959, 199], radius=50, fill=(0, 0, 0, 180), outline=(255, 255, 255, 230), width=6)
        tx = "IP: dziob.6mc.pl"; f = F(72); w = f.getlength(tx); d.text((480 - w / 2, 50), tx, font=f, fill=(255, 255, 255, 255))
        paste(img, box, W / 2, 1240, r)
        outlined(img, "premiera 24.12 • 0 zł", 60, (255, 230, 60), W / 2, 1420, r, stroke=6)
    paste(img, icon("bird", 10), W / 2, 1680 - abs(math.sin(t * math.pi * 2.4)) * 50, lin(t, T_CTA + 0.3, T_CTA + 0.6))
    return img

SCENES = [(0.0, s_hook), (LV[0][0], lambda t: s_level(t, 0)), (LV[1][0], lambda t: s_level(t, 1)), (LV[2][0], lambda t: s_level(t, 2)),
          (T_TWIST, s_twist), (T_INFO, s_info), (T_CTA, s_cta)]
GRAIN = [np.random.default_rng(i).normal(0, 3.5, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1) for i in range(4)]
PUNCH = [0.0, T_TWIST, T_CTA] + [l[0] for l in LV] + [l[2] for l in LV]

def render(fi):
    t = fi / FPS
    si = max(i for i, (s, _) in enumerate(SCENES) if s <= t)
    img = SCENES[si][1](t)
    z = 1.0 + sum(0.05 * math.exp(-max(0, t - h) * 9) for h in PUNCH if t >= h)
    if z > 1.002:
        big = img.resize((int(W * z), int(H * z)), Image.BILINEAR); l = (big.width - W) // 2; tp = (big.height - H) // 2
        img = big.crop((l, tp, l + W, tp + H))
    # progress bar
    d = ImageDraw.Draw(img); d.rectangle([0, 0, W, 12], fill=(0, 0, 0, 120)); d.rectangle([0, 0, W * t / DUR, 12], fill=(255, 255, 255, 230))
    fl = max([clamp(1 - (t - c) / 0.12) for c in [s for s, _ in SCENES[1:]] if t >= c] + [0])
    a = to_arr(img) + GRAIN[fi % 4]
    a = a + (255 - a) * fl * 0.55
    return np.clip(a, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    from multiprocessing import Pool
    out = sys.argv[1]
    if len(sys.argv) > 4:
        s, e = float(sys.argv[2]), float(sys.argv[3])
        for f in range(int(round(s * FPS)), int(round(e * FPS)), max(1, int(float(sys.argv[4]) * FPS))):
            Image.frombytes("RGB", (W, H), render(f)).save(f"{out}/s7_{f / FPS:05.2f}.jpg", quality=85)
        sys.exit()
    wav = os.path.join(BUILD, "mix7.wav"); make_audio(wav)
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    with Pool(4) as p:
        for i, b in enumerate(p.imap(render, range(int(DUR * FPS)), chunksize=4)):
            ff.stdin.write(b)
            if i % 150 == 0: print("frame", i, flush=True)
    ff.stdin.close(); ff.wait()
