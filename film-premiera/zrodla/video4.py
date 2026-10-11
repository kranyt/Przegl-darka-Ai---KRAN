"""Meme-style video #4: 'Dlaczego anarchia.gg ma tyle graczy, a my nawet filmu o premierze nie możemy zrobić?'
Self-ironic, with fully synthesized soundtrack (chiptune + meme SFX)."""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from video import (text_img, paste, glow, pad_img, clamp, lin, eo_cubic, eo_back, ei_cubic, eo_bounce,
                   tex, shade, icon, gradient, mc_panel, slot, _sq, _glow, VIGN, GRAIN, W, H)
from video2 import to_arr, to_img, draw_logo2

FPS = 30
DUR = 43.5
T_Q, T_SPLIT, T_EDIT, T_WAIT, T_WHY, T_END = 0.0, 5.5, 12.0, 19.9, 25.5, 34.0
BOOM1, BOOM2 = 1.5, 4.0
ERR_T = 15.3; TRY2_T = 17.4; SCRATCH = 19.9
THUMB_T = [21.2, 21.8, 22.4]
CHECK_T = [26.8 + 1.35 * i for i in range(5)]
HIT_T = 36.0
COUNT_T = [37.0, 37.5, 38.0, 38.5, 39.0, 39.5]
FINAL_T = 39.9
SCRATCH_DIR = os.path.join(BUILD, "..")

# ====================================================================== AUDIO
SR = 44100
def make_audio(path):
    N = int(DUR * SR); out = np.zeros(N); rng = np.random.default_rng(3)
    def add(t0, sig, g=1.0):
        i = int(t0 * SR)
        if i >= N or i + len(sig) <= 0: return
        j = min(N, i + len(sig)); out[i:j] += g * sig[:j - i]
    def tt(d): return np.arange(int(d * SR)) / SR
    def hz(m): return 440 * 2 ** ((m - 69) / 12)
    def lp(x, fc):
        X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X /= np.sqrt(1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
    def sq(f, d, duty=0.5):
        t = tt(d); return np.where((t * f) % 1 < duty, 1.0, -1.0)
    def boom():
        t = tt(2.2); f = 38 + 140 * np.exp(-t * 9)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
        return np.tanh(s * 3) * 0.9 + lp(rng.standard_normal(len(t)), 300) * np.exp(-t * 4) * 0.4
    def click():
        t = tt(0.03); return rng.standard_normal(len(t)) * np.exp(-t * 300) * 0.6
    def ding(m=88):
        t = tt(0.8); return (np.sin(2 * np.pi * hz(m) * t) + 0.4 * np.sin(2 * np.pi * hz(m + 12) * t)) * np.exp(-t * 6)
    def whoosh(d=0.45):
        n = rng.standard_normal(int(d * SR)); return lp(n, 2500) * np.sin(np.linspace(0, np.pi, len(n))) ** 2
    def scratch():
        t = tt(0.5); f = 300 + 1500 * np.abs(np.sin(t * 2 * np.pi * 3.2))
        return lp(rng.standard_normal(len(t)), 4000) * 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3)
    def err_beep():
        a = sq(hz(69), 0.18, 0.5) * np.exp(-tt(0.18) * 6); b = sq(hz(64), 0.3, 0.5) * np.exp(-tt(0.3) * 5)
        return np.concatenate([lp(a, 2500), np.zeros(int(0.05 * SR)), lp(b, 2500)]) * 0.35
    def trombone():
        parts = []
        for m, d, vib in [(67, 0.45, 0), (66, 0.45, 0), (65, 0.45, 0), (64, 1.4, 1)]:
            t = tt(d); f = hz(m - 12) * (1 + vib * 0.03 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / 0.3, 0, 1))
            ph = 2 * np.pi * np.cumsum(f) / SR
            s = sum(np.sin(k * ph) / k ** 1.1 for k in range(1, 9))
            env = np.minimum(1, t / 0.04) * np.minimum(1, (d - t) / 0.08)
            parts.append(lp(s, 1800) * env)
        return np.concatenate(parts) * 0.28
    # --- scene 1: drone + typing + booms
    t = tt(5.5); drone = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 82.4 * t)) * np.minimum(1, t / 1.0) * np.minimum(1, (5.5 - t) / 0.4)
    add(0, drone, 0.10)
    for k in range(20): add(0.2 + k * 0.06, click(), 0.35)
    for k in range(30): add(2.4 + k * 0.05, click(), 0.35)
    add(BOOM1, boom(), 0.55); add(BOOM2, boom(), 0.75)
    # --- scene 2: crowd (left) vs crickets (right)
    d = T_EDIT - T_SPLIT; t = tt(d)
    crowd = lp(rng.standard_normal(len(t)), 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * t) * np.sin(2 * np.pi * 0.7 * t))
    add(T_SPLIT, crowd * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.3), 0.08)
    for k in range(30):  # little jump pops
        add(T_SPLIT + rng.uniform(0, d - 0.2), sq(hz(rng.integers(72, 90)), 0.05, 0.25) * np.exp(-tt(0.05) * 40), 0.04)
    for k in range(int(d / 0.55)):  # crickets
        c = np.sin(2 * np.pi * 4600 * tt(0.12)) * (np.sin(2 * np.pi * 30 * tt(0.12)) > 0) * np.exp(-tt(0.12) * 8)
        add(T_SPLIT + 0.3 + k * 0.55, c, 0.06)
    add(7.0, lp(rng.standard_normal(int(3 * SR)), 600) * np.sin(np.linspace(0, np.pi, int(3 * SR))), 0.12)  # wind for tumbleweed
    for ct in (7.6, 9.0, 10.4): add(ct, ding(84) * 0.5, 0.2)  # chat pings
    # --- scene 3: lounge marimba until scratch
    bar = 1.6
    prog = [[60, 64, 67], [57, 60, 64], [62, 65, 69], [55, 59, 62]]
    tt0 = T_EDIT
    k = 0
    while tt0 < SCRATCH:
        ch = prog[(k // 8) % 4]; m = ch[[0, 1, 2, 1, 0, 2, 1, 2][k % 8]] + 12
        s = np.sin(2 * np.pi * hz(m) * tt(0.4)) * np.exp(-tt(0.4) * 9) + 0.3 * np.sin(2 * np.pi * hz(m) * 4 * tt(0.4)) * np.exp(-tt(0.4) * 30)
        if not (ERR_T <= tt0 < ERR_T + 2.3): add(tt0, s, 0.10)
        tt0 += 0.2; k += 1
    for k in range(10): add(T_EDIT + 0.6 + k * 0.08, click(), 0.25)  # typing title
    add(ERR_T, err_beep(), 1.0); add(ERR_T + 0.6, trombone(), 1.0)
    add(TRY2_T, whoosh(), 0.2)
    for k in range(6): add(TRY2_T + 0.4 + k * 0.25, sq(hz(84 + (k % 3) * 4), 0.1, 0.5) * np.exp(-tt(0.1) * 20) * 0.3, 0.25)  # cheesy sparkle
    add(SCRATCH, scratch(), 0.8)
    # --- scene 4: dings for thumbnails
    for i, tt1 in enumerate(THUMB_T): add(tt1, whoosh(0.3), 0.15); add(tt1 + 0.15, ding(84 + i * 4), 0.25)
    add(24.3, boom()[: int(0.8 * SR)], 0.3)
    # --- scene 5/6: chiptune
    beat = 0.4; start = T_WHY
    chords = [60, 55, 57, 53]
    mel = [[72, 76, 79, 76, 81, 79, 76, 74], [71, 74, 79, 74, 83, 81, 79, 74], [72, 76, 81, 76, 84, 83, 81, 76], [72, 77, 81, 77, 84, 81, 79, 77]]
    endm = DUR - 1.2
    nb = int((endm - start) / (beat * 4))
    for b in range(nb + 1):
        t0 = start + b * beat * 4; c = chords[b % 4]
        for e in range(8):
            te = t0 + e * 0.2
            if te >= endm: break
            add(te, lp(sq(hz(c - 24), 0.18, 0.5), 1200) * np.exp(-tt(0.18) * 6), 0.10)  # bass
            if not (HIT_T - 0.4 <= te < HIT_T):
                add(te, lp(sq(hz(mel[b % 4][e]), 0.19, 0.25), 5000) * np.exp(-tt(0.19) * 5), 0.055)  # lead
        for q in range(4):
            tq = t0 + q * beat
            if tq >= endm: break
            kt = tt(0.3); kick = np.sin(2 * np.pi * np.cumsum(50 + 110 * np.exp(-kt * 30)) / SR) * np.exp(-kt * 9)
            add(tq, kick, 0.45)
            if q % 2 == 1: add(tq, lp(rng.standard_normal(int(0.15 * SR)), 5000) * np.exp(-tt(0.15) * 20), 0.18)
            add(tq + 0.2, np.diff(rng.standard_normal(int(0.04 * SR)), prepend=0) * np.exp(-tt(0.04) * 80), 0.06)
    for ct in CHECK_T: add(ct, ding(91), 0.22)
    add(T_END, whoosh(0.6), 0.2); add(HIT_T, boom(), 0.5)
    for i, ct in enumerate(COUNT_T):
        for j, m in enumerate([72, 76, 79, 84]): add(ct + j * 0.04, lp(sq(hz(m + i * 2), 0.08, 0.5), 5000) * np.exp(-tt(0.08) * 20), 0.10)
    add(FINAL_T, boom(), 0.5)
    for j, m in enumerate([60, 64, 67, 72, 76, 79, 84]): add(FINAL_T + j * 0.05, lp(sq(hz(m), 0.6, 0.5), 4000) * np.exp(-tt(0.6) * 4), 0.06)
    out *= np.clip(np.minimum(np.arange(N) / SR / 0.05, (DUR - np.arange(N) / SR) / 1.0), 0, 1)
    out = np.tanh(out * 1.2) * 0.9
    st = np.stack([out, out], 1).astype(np.float32)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", path], input=st.tobytes())

# ====================================================================== VISUALS
def typed_lines(img, lines, t, t0, t1, size, col, cy, gap=1.5, outline=4, ocol=(0, 0, 0), fam="ps"):
    total = sum(len(l) for l in lines); n = int(total * lin(t, t0, t1)); y = cy - (len(lines) - 1) * size * gap / 2
    for l in lines:
        k = max(0, min(len(l), n)); n -= len(l)
        full = text_img(l, size, col, fam, outline=outline, ocol=ocol)
        if k: paste(img, text_img(l[:k], size, col, fam, outline=outline, ocol=ocol), W / 2 - full.width / 2, y, anchor="l")
        y += size * gap

def scene_q(t):
    a = np.zeros((H, W, 3), np.float32)
    yy, xx = np.ogrid[0:H, 0:W]; r = np.sqrt((xx - W / 2) ** 2 + (yy - H / 2) ** 2) / 1100
    red = 0.25 * lin(t, BOOM2, BOOM2 + 0.2)
    a += (np.clip(1 - r, 0, 1) ** 2)[..., None] * np.array([40 + 120 * red, 20, 30])
    img = to_img(a)
    typed_lines(img, ["DLACZEGO ANARCHIA.GG", "MA TYLE GRACZY..."], t, 0.2, 1.4, 76, (255, 255, 255), 330, outline=5)
    typed_lines(img, ["...A MY NAWET FILMU", "O PREMIERZE NIE MOŻEMY ZROBIĆ?"], t, 2.4, 3.9, 56, (255, 210, 80), 700, outline=4, ocol=(60, 20, 0))
    # punch zoom on booms
    z = 1 + 0.06 * math.exp(-max(0, t - BOOM1) * 6) * (t >= BOOM1) + 0.10 * math.exp(-max(0, t - BOOM2) * 5) * (t >= BOOM2) + 0.02 * lin(t, BOOM2, 5.5)
    if z > 1.001:
        big = img.resize((int(W * z), int(H * z)), Image.BILINEAR); l = (big.width - W) // 2; tp = (big.height - H) // 2
        img = big.crop((l, tp, l + W, tp + H))
    return img

# ---- pixel players
def player(seed, bird=False, s=6):
    r = np.random.default_rng(seed)
    skin = [(236, 188, 150), (198, 140, 100), (140, 95, 65)][int(r.integers(0, 3))]
    shirt = tuple(int(c) for c in r.integers(40, 230, 3)); pants = tuple(int(c) for c in r.integers(20, 120, 3))
    hair = tuple(int(c) for c in r.integers(20, 120, 3))
    a = np.zeros((32, 16, 4), np.uint8)
    a[0:8, 4:12] = skin + (255,); a[0:2, 4:12] = hair + (255,); a[3:5, 5:7] = (255, 255, 255, 255); a[3:5, 9:11] = (255, 255, 255, 255)
    a[4, 6] = a[4, 10] = (40, 40, 80, 255)
    a[8:20, 4:12] = shirt + (255,); a[8:20, 0:4] = shirt + (255,); a[8:20, 12:16] = shirt + (255,)
    a[18:20, 0:4] = skin + (255,); a[18:20, 12:16] = skin + (255,)
    a[20:32, 4:12] = pants + (255,); a[30:32, 4:12] = (50, 50, 50, 255)
    im = Image.fromarray(a, "RGBA").resize((16 * s, 32 * s), Image.NEAREST)
    if bird:
        im.paste((0, 0, 0, 0), (0, 0, 16 * s, 8 * s))
        head = icon("bird", 1).crop((2, 1, 16, 14)).resize((int(9.5 * s), int(9 * s)), Image.NEAREST)
        im.alpha_composite(head, (int(3 * s), 0))
    return im
CROWD = [(player(i, s=4), float(x), float(y), float(ph)) for i, (x, y, ph) in enumerate(zip(np.random.default_rng(5).uniform(40, 900, 46), np.random.default_rng(6).uniform(620, 900, 46), np.random.default_rng(7).uniform(0, 6, 46)))]
CROWD.sort(key=lambda c: c[2])
ME = player(99, bird=True, s=6)
CHAT_L = ["siema", "gg", "ktoś na pvp?", "kupię diamenty", "lol", "jest event?", "xD", "gdzie spawn?", "elo", "gg wp",
          "kto handluje", "tpa?", "nice", "siemka", "hej", "dawaj", "ok", "gg ez"]
NICKS = ["Kacper", "Ola", "Bartek", "Zuza", "Mati", "Kuba", "Nina", "Szymon", "Lena", "Olek"]
def tumble(s=7):
    rows = ["..BBBB..", ".B.B.BB.", "B.BB.B.B", "BB.B.BB.", "B.B.B..B", ".BB.BB.B", "..BBBB.."]
    a = np.zeros((7, 8, 4), np.uint8)
    for y, rw in enumerate(rows):
        for x, ch in enumerate(rw):
            if ch == "B": a[y, x] = (150, 110, 60, 255)
    return Image.fromarray(a, "RGBA").resize((8 * s * 2, 7 * s * 2), Image.NEAREST)
TUMBLE = tumble()

def half_bg(w, sky, grass_y=900):
    im = Image.fromarray(gradient(sky, H, w).astype(np.uint8)).convert("RGBA")
    g = tex("grass_side", 1).resize((60, 60), Image.NEAREST).convert("RGBA"); d = tex("dirt", 1).resize((60, 60), Image.NEAREST).convert("RGBA")
    for x in range(0, w, 60):
        im.alpha_composite(g, (x, grass_y))
        for y in range(grass_y + 60, H, 60): im.alpha_composite(d, (x, y))
    return im
LEFT_BG = half_bg(955, [(90, 150, 240), (160, 200, 255)])
RIGHT_BG = half_bg(955, [(110, 120, 140), (170, 175, 185)])

def chat(lines, w, h=None):
    im = Image.new("RGBA", (w, 52 * len(lines) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = 6
    for nm, nc, msg in lines:
        d.rectangle([0, y - 4, w, y + 46], fill=(0, 0, 0, 120))
        a = text_img(f"<{nm}> ", 30, nc, "px"); im.alpha_composite(a, (10, y)); im.alpha_composite(text_img(msg, 30, (255, 255, 255), "px"), (10 + a.width, y))
        y += 52
    return im

def scene_split(t):
    lt = t - T_SPLIT
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    L = LEFT_BG.copy()
    for (sp, x, y, ph) in CROWD:
        j = abs(math.sin(t * 5 + ph)) * 40
        L.alpha_composite(sp, (int(x + 20 * math.sin(t * 0.8 + ph)), int(y - j - sp.height + 120)))
    k = int(lt * 7)
    lines = [(NICKS[(k + i) % 10], (85, 255, 255) if (k + i) % 3 else (255, 170, 0), CHAT_L[(k * 3 + i * 5) % len(CHAT_L)]) for i in range(5)]
    L.alpha_composite(chat(lines, 520), (20, 330))
    L.alpha_composite(text_img("ANARCHIA.GG", 60, (255, 255, 255), "ps", outline=4, ocol=(20, 40, 90)), (60, 60))
    L.alpha_composite(text_img("graczy: MNÓSTWO", 40, (85, 255, 85), "px", outline=3, ocol=(0, 40, 0)), (64, 170))
    Rr = RIGHT_BG.copy()
    Rr.alpha_composite(ME, (int(955 / 2 - ME.width / 2), 900 - ME.height + 20))
    tp = lin(t, 7.0, 10.0)
    if 0 < tp < 1:
        tw = TUMBLE.rotate(-tp * 900, resample=Image.NEAREST, expand=True)
        Rr.alpha_composite(tw, (int(-150 + tp * 1250), int(900 - tw.height + 10 - abs(math.sin(tp * 12)) * 40)))
    mine = [("Ty", (255, 85, 255), "halo?"), ("Ty", (255, 85, 255), "jest ktoś?"), ("Ty", (255, 85, 255), "...")]
    shown = [m for m, ct in zip(mine, (7.6, 9.0, 10.4)) if t >= ct]
    if shown: Rr.alpha_composite(chat(shown, 420), (20, 330))
    Rr.alpha_composite(text_img("DZIOB.6MC.PL", 60, (255, 255, 255), "ps", outline=4, ocol=(40, 40, 40)), (60, 60))
    Rr.alpha_composite(text_img("graczy: 1 (to ty)", 40, (255, 120, 120), "px", outline=3, ocol=(50, 0, 0)), (64, 170))
    sl = eo_cubic(lin(t, T_SPLIT, T_SPLIT + 0.5))
    img.alpha_composite(L, (int(-955 + 955 * sl), 0)); img.alpha_composite(Rr, (int(W - 955 * sl), 0))
    ImageDraw.Draw(img).rectangle([955, 0, 964, H], fill=(255, 255, 255, 255))
    p = lin(t, 11.0, 11.3)
    if p > 0:
        paste(img, glow(pad_img(text_img("HMMM...", 120, (255, 255, 255), "ps", outline=8), 30), 18), W / 2, H / 2, p, scale=0.6 + 0.4 * eo_back(p))
    return img

# ---- editor scene
EDIT_BG = gradient([(28, 30, 38), (18, 20, 26)])
def ugly_slide(t):
    im = Image.new("RGBA", (880, 495), (255, 255, 255, 255))
    txt = text_img("PREMIERA!!!", 80, (255, 0, 200), "pxr", shadow=False)
    cols = [(255, 0, 0), (255, 140, 0), (240, 220, 0), (0, 200, 0), (0, 120, 255), (160, 0, 255)]
    a = np.asarray(txt).copy(); hgt = a.shape[0]
    for k in range(6): a[k * hgt // 6:(k + 1) * hgt // 6, :, :3] = np.where(a[k * hgt // 6:(k + 1) * hgt // 6, :, 3:4] > 0, cols[k], a[k * hgt // 6:(k + 1) * hgt // 6, :, :3])
    txt = Image.fromarray(a, "RGBA")
    paste(im, txt, 440, 240, 1, rot=math.sin(t * 6) * 15, scale=1 + 0.15 * math.sin(t * 9), resample=Image.BICUBIC)
    for k in range(5):
        paste(im, text_img("*", 60, cols[k], "ps", shadow=False), 100 + k * 170, 420 + 20 * math.sin(t * 7 + k), 1)
    paste(im, text_img("serwer dziob czy coś", 30, (0, 0, 0), "pxr", shadow=False), 440, 360, 1)
    return im

def scene_edit(t):
    img = Image.fromarray(EDIT_BG.astype(np.uint8)).convert("RGBA")
    try2 = t >= TRY2_T
    title = "PRÓBA NR 2" if try2 else "PRÓBA NR 1: ROBIMY FILM O PREMIERZE"
    paste(img, text_img(title, 44, (255, 220, 80), "ps", outline=3, ocol=(50, 30, 0)), W / 2, 80, 1)
    win = mc_panel(1500, 820, dark=True); img.alpha_composite(win, (210, 150))
    d = ImageDraw.Draw(img)
    d.rectangle([520, 200, 1400, 695], fill=(0, 0, 0, 255))
    if try2 and t > TRY2_T + 0.5:
        img.alpha_composite(ugly_slide(t), (520, 200))
    elif not try2:
        paste(img, text_img("[ podgląd ]", 30, (90, 90, 90), "px"), 960, 450, 1)
    # timeline
    rr = np.random.default_rng(1)
    for tr in range(3):
        y = 740 + tr * 50; x = 260
        while x < 1650:
            w = int(rr.integers(60, 260)); c = [(80, 160, 255), (120, 220, 120), (255, 170, 60)][tr]
            d.rectangle([x, y, x + w - 6, y + 38], fill=c + (255,)); x += w
    ph = 260 + ((t - T_EDIT) * 160) % 1390; d.rectangle([ph, 730, ph + 4, 900], fill=(255, 60, 60, 255))
    # render bar
    if not try2:
        p = 0.99 * eo_cubic(lin(t, 12.8, 15.0))
        pct = f"{int(p * 100)}%" if t < 15.0 else ("99%" if int(t * 6) % 2 else "99,9%")
    else:
        p = lin(t, TRY2_T, TRY2_T + 0.5); pct = f"{int(p * 100)}%"
    d.rectangle([260, 920, 1660, 950], fill=(60, 60, 60, 255)); d.rectangle([260, 920, 260 + 1400 * p, 950], fill=(85, 255, 85, 255))
    paste(img, text_img("Renderowanie... " + pct, 30, (255, 255, 255), "px"), 960, 990, 1)
    if ERR_T <= t < TRY2_T:
        pe = eo_back(lin(t, ERR_T, ERR_T + 0.25), 2.5)
        dlg = mc_panel(820, 330); dd = ImageDraw.Draw(dlg)
        dd.rectangle([6, 6, 813, 64], fill=(200, 40, 40, 255))
        dlg.alpha_composite(text_img("BŁĄD", 36, (255, 255, 255), "ps"), (30, 16))
        dlg.alpha_composite(text_img("Komputer się poddał.", 46, (40, 40, 40), "px", shadow=False), (60, 110))
        dlg.alpha_composite(text_img("(nie zapisano zmian)", 32, (110, 110, 110), "pxr", shadow=False), (60, 178))
        btn = mc_panel(200, 70); btn.alpha_composite(text_img("OK", 34, (40, 40, 40), "ps", shadow=False), (70, 18))
        dlg.alpha_composite(btn, (310, 238))
        paste(img, dlg, W / 2, 480, 1, scale=max(0.05, pe))
        # cursor moving to OK and clicking
        cp = eo_cubic(lin(t, ERR_T + 0.8, ERR_T + 1.6))
        cx = 1500 + (960 - 1500) * cp; cy = 900 + (690 - 900) * cp
        cur = ["X.......", "XX......", "XWX.....", "XWWX....", "XWWWX...", "XWWWWX..", "XWWXXXX.", "XX......", "X......."]
        a = np.zeros((9, 8, 4), np.uint8)
        for y, rw in enumerate(cur):
            for x, ch in enumerate(rw):
                if ch == "X": a[y, x] = (0, 0, 0, 255)
                if ch == "W": a[y, x] = (255, 255, 255, 255)
        img.alpha_composite(Image.fromarray(a, "RGBA").resize((40, 45), Image.NEAREST), (int(cx), int(cy)))
    return img

# ---- "but wait" scene
THUMBS = []
for i in range(3):
    im = Image.open(os.path.join(SCRATCH_DIR, "thumbs", f"t{i + 1}.png")).convert("RGBA").resize((480, 270), Image.BILINEAR)
    fr = Image.new("RGBA", (500, 340), (255, 255, 255, 255)); fr.alpha_composite(im, (10, 10))
    lb = text_img(f"FILM #{i + 1}", 30, (30, 30, 30), "ps", shadow=False); fr.alpha_composite(lb, (250 - lb.width // 2, 292))
    THUMBS.append(fr)

def scene_wait(t):
    if t < 21.0:
        base = scene_edit(SCRATCH - 0.01)
        g = to_arr(base); g = g.mean(2, keepdims=True).repeat(3, 2) * 0.5; img = to_img(g)
    else:
        img = Image.fromarray(gradient([(20, 40, 70), (40, 80, 120), (20, 40, 70)]).astype(np.uint8)).convert("RGBA")
        a = to_arr(img); yy, xx = np.mgrid[0:H:4, 0:W:4]
        a += ((((xx // 60 + yy // 60) % 2) * 10).astype(np.float32).repeat(4, 0).repeat(4, 1)[:H, :W, None]); img = to_img(a)
    p = lin(t, SCRATCH + 0.05, SCRATCH + 0.3)
    if t < 21.0:
        paste(img, glow(pad_img(text_img("ALE CHWILA...", 110, (255, 255, 255), "ps", outline=7), 30), 16), W / 2, H / 2, p, scale=0.8 + 0.2 * eo_back(p))
    else:
        paste(img, text_img("ZROBILIŚMY JUŻ 3 FILMY O PREMIERZE!", 52, (255, 255, 255), "ps", outline=4, ocol=(10, 20, 50)), W / 2, 150, lin(t, 21.0, 21.3))
        for i, tt1 in enumerate(THUMB_T):
            pp = eo_back(lin(t, tt1, tt1 + 0.45), 1.6)
            if pp <= 0: continue
            x = 360 + i * 600; y = 560 + (1 - pp) * 700
            paste(img, THUMBS[i], x, y, 1, rot=(-6, 3, -3)[i] + (1 - pp) * 30, resample=Image.BICUBIC)
        q = lin(t, 24.3, 24.5)
        if q > 0:
            paste(img, text_img("(ten jest czwarty)", 44, (255, 220, 80), "px", outline=3, ocol=(50, 30, 0)), W / 2, 930, q, scale=0.7 + 0.3 * eo_back(q))
    return img

# ---- why scene
ITEMS = ["Świeży start – wszyscy zaczynają od zera", "Każdy gracz się liczy (dosłownie, liczymy)",
         "Admin osobiście powie ci 'siema!'", "Wbijesz do pierwszej setki graczy", "Premiera w Wigilię – 24 grudnia"]
def checkbox(on):
    im = slot(70)
    if on:
        d = ImageDraw.Draw(im); pts = [(14, 36), (28, 52), (56, 16)]
        d.line(pts, fill=(40, 200, 60, 255), width=12)
    return im
CB = [checkbox(False), checkbox(True)]
def scene_why(t):
    a = np.zeros((H, W, 3), np.float32)
    small_y, small_x = np.mgrid[0:H // 8, 0:W // 8]
    hue = ((small_x + small_y + t * 12) // 10) % 4
    pal = np.array([(40, 30, 90), (50, 36, 110), (36, 26, 80), (46, 34, 100)], np.float32)
    a = pal[hue.astype(int)].repeat(8, 0).repeat(8, 1)
    img = to_img(a)
    paste(img, text_img("DLACZEGO WARTO WBIĆ NA DZIOB.6MC.PL?", 50, (255, 230, 90), "ps", outline=4, ocol=(60, 20, 0)), W / 2, 110, lin(t, T_WHY, T_WHY + 0.3), scale=0.9 + 0.1 * eo_back(lin(t, T_WHY, T_WHY + 0.3)))
    for i, ct in enumerate(CHECK_T):
        p = eo_back(lin(t, ct - 0.35, ct), 1.4)
        if p <= 0: continue
        y = 260 + i * 145; x = 230 + (1 - p) * -900
        paste(img, CB[1 if t >= ct else 0], x, y, 1)
        paste(img, text_img(ITEMS[i], 50, (255, 255, 255), "px", outline=3, ocol=(20, 10, 40)), x + 70, y, 1, anchor="l")
    # bouncing bird mascot in corner
    b = icon("bird", 10); paste(img, b, W - 170, 900 - abs(math.sin(t * 2 * math.pi / 0.8)) * 50, 1)
    return img

# ---- ending
def scene_end(t):
    img = Image.fromarray(gradient([(10, 14, 40), (30, 30, 90), (60, 40, 120)]).astype(np.uint8)).convert("RGBA")
    if t < HIT_T:
        p = lin(t, T_END + 0.1, T_END + 0.6)
        paste(img, text_img("KAŻDY WIELKI SERWER", 64, (255, 255, 255), "ps", outline=4), W / 2, 450, p)
        paste(img, text_img("ZACZYNAŁ OD ZERA.", 64, (255, 255, 255), "ps", outline=4), W / 2, 560, lin(t, T_END + 0.6, T_END + 1.1))
        return img
    if t < FINAL_T:
        paste(img, text_img("TERAZ NASZA KOLEJ.", 72, (255, 220, 70), "ps", outline=5, ocol=(60, 20, 0)), W / 2, 150, 1, scale=1 + 0.3 * math.exp(-(t - HIT_T) * 8))
        vals = ["1", "2", "5", "20", "100", "???"]; hs = [20, 40, 90, 200, 380, 520]
        d = ImageDraw.Draw(img)
        d.line([(300, 900), (1620, 900)], fill=(255, 255, 255, 255), width=6)
        for i, ct in enumerate(COUNT_T):
            p = eo_back(lin(t, ct, ct + 0.3), 1.6)
            if p <= 0: continue
            x = 360 + i * 210; hh = hs[i] * p
            col = (85, 255, 85) if i < 5 else (255, 220, 70)
            d.rectangle([x, 900 - hh, x + 150, 897], fill=col + (255,))
            d.rectangle([x, 900 - hh, x + 150, 900 - hh + 14], fill=(255, 255, 255, 180))
            paste(img, text_img(vals[i], 44, (255, 255, 255), "ps", outline=3), x + 75, 900 - hh - 50, min(1, p))
        paste(img, text_img("GRACZE", 34, (200, 200, 255), "px"), 960, 960, 1)
        return img
    lg = draw_logo2(t, FINAL_T)
    paste(img, lg, W / 2, 280, 1)
    p = eo_back(lin(t, FINAL_T + 0.6, FINAL_T + 1.0))
    if p > 0: paste(img, glow(pad_img(text_img("IP: DZIOB.6MC.PL", 80, (255, 255, 255), "ps", outline=5, ocol=(30, 10, 70)), 30), 18), W / 2, 540, 1, scale=max(.05, p))
    p2 = lin(t, FINAL_T + 1.1, FINAL_T + 1.5)
    if p2 > 0: paste(img, text_img("PREMIERA 24.12", 60, (255, 220, 70), "ps", outline=4, ocol=(60, 20, 0)), W / 2, 690, p2)
    p3 = lin(t, FINAL_T + 1.7, FINAL_T + 2.1)
    if p3 > 0: paste(img, text_img("BĄDŹ JEDNYM Z PIERWSZYCH!", 54, (85, 255, 85), "ps", outline=4, ocol=(0, 40, 0)), W / 2, 830, p3, scale=1 + 0.04 * math.sin(t * 7))
    return img

SCENES = [(T_Q, scene_q), (T_SPLIT, scene_split), (T_EDIT, scene_edit), (T_WAIT, scene_wait), (T_WHY, scene_why), (T_END, scene_end)]

def shake(t):
    s = 14 * math.exp(-max(0, t - BOOM1) * 7) * (t >= BOOM1) + 26 * math.exp(-max(0, t - BOOM2) * 5) * (t >= BOOM2)
    s += 18 * math.exp(-max(0, t - HIT_T) * 6) * (t >= HIT_T) + 14 * math.exp(-max(0, t - FINAL_T) * 6) * (t >= FINAL_T)
    s += 10 * math.exp(-max(0, t - ERR_T) * 6) * (t >= ERR_T) * (t < TRY2_T)
    return s

def render(fi):
    t = fi / FPS
    si = max(i for i, (s, _) in enumerate(SCENES) if s <= t)
    img = SCENES[si][1](t)
    # quick slide transitions (except into the scratch freeze)
    for k in (1, 2, 4, 5):
        b = SCENES[k][0]
        if b <= t < b + 0.3:
            p = eo_cubic((t - b) / 0.3)
            old = SCENES[k - 1][1](b - 0.001)
            canvas = Image.new("RGBA", (W, H)); canvas.alpha_composite(old, (int(-W * p), 0)); canvas.alpha_composite(img, (int(W * (1 - p)), 0)); img = canvas
    s = shake(t)
    if s > 0.5:
        rr = np.random.default_rng(fi); dx, dy = rr.uniform(-s, s, 2)
        img = img.transform((W, H), Image.AFFINE, (1 / 1.05, 0, -dx + W * 0.0238, 0, 1 / 1.05, -dy + H * 0.0238), Image.BILINEAR)
    a = np.asarray(img.convert("RGB")).astype(np.float32) * VIGN + GRAIN[fi % 6] * 0.5
    a *= clamp((DUR - t) / 0.8)
    return np.clip(a, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    from multiprocessing import Pool
    out = sys.argv[1]
    if len(sys.argv) > 4:
        start, end = float(sys.argv[2]), float(sys.argv[3])
        for f in range(int(round(start * FPS)), int(round(end * FPS)), max(1, int(float(sys.argv[4]) * FPS))):
            Image.frombytes("RGB", (W, H), render(f)).save(f"{out}/s4_{f / FPS:05.2f}.jpg", quality=85)
        sys.exit()
    wav = os.path.join(BUILD, "mix4.wav"); make_audio(wav)
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    with Pool(4) as p:
        for i, b in enumerate(p.imap(render, range(int(DUR * FPS)), chunksize=4)):
            ff.stdin.write(b)
            if i % 150 == 0: print("frame", i, flush=True)
    ff.stdin.close(); ff.wait()
