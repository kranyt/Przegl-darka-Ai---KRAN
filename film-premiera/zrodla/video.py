import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from cfg import *

FONTS = os.path.join(BUILD, "..", "fonts")
R = np.random.default_rng(42)

# ---------------------------------------------------------------- fonts / text
_fc = {}
def _font(fam, size, ext):
    files = {"ps": "press-start-2p-latin%s-400-normal.woff",
             "px": "pixelify-sans-latin%s-700-normal.woff",
             "pxr": "pixelify-sans-latin%s-400-normal.woff",
             "sk": "silkscreen-latin%s-400-normal.woff"}
    k = (fam, size, ext)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FONTS, files[fam] % ("-ext" if ext else "")), size)
    return _fc[k]

def _isext(ch): return 0x100 <= ord(ch) <= 0x24F

_tc = {}
def text_img(txt, size, color=(255, 255, 255), fam="ps", shadow=True, outline=0, ocol=(0, 0, 0)):
    """Pixel text as RGBA image with Minecraft-like drop shadow."""
    key = (txt, size, color, fam, shadow, outline, ocol)
    if key in _tc: return _tc[key]
    widths = [_font(fam, size, _isext(c)).getlength(c) for c in txt]
    w = int(sum(widths)) + size; h = int(size * 1.6)
    sh = max(2, size // 8) if shadow else 0
    pad = outline + sh + 4
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    def draw_all(dx, dy, col):
        x = pad + dx
        for c, cw in zip(txt, widths):
            d.text((x, pad + dy), c, font=_font(fam, size, _isext(c)), fill=col)
            x += cw
    if outline:
        for ox in range(-outline, outline + 1, max(1, outline // 2)):
            for oy in range(-outline, outline + 1, max(1, outline // 2)):
                draw_all(ox + sh, oy + sh, ocol + (255,))
                draw_all(ox, oy, ocol + (255,))
    if shadow:
        sc = tuple(int(c * 0.25) for c in color)
        draw_all(sh, sh, sc + (255,))
    draw_all(0, 0, color + (255,))
    im = im.crop(im.getbbox())
    _tc[key] = im
    return im

def paste(dst, src, cx, cy, alpha=1.0, scale=1.0, anchor="c", rot=0.0, resample=Image.NEAREST):
    if alpha <= 0.003 or scale <= 0.01: return
    if scale != 1.0:
        src = src.resize((max(1, int(src.width * scale)), max(1, int(src.height * scale))), resample)
    if rot:
        src = src.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1.0:
        a = src.getchannel("A").point(lambda v: int(v * alpha))
        src = src.copy(); src.putalpha(a)
    if anchor == "c": x, y = int(cx - src.width / 2), int(cy - src.height / 2)
    elif anchor == "l": x, y = int(cx), int(cy - src.height / 2)
    else: x, y = int(cx - src.width), int(cy - src.height / 2)
    dst.alpha_composite(src, (x, y)) if dst.mode == "RGBA" else dst.paste(src, (x, y), src)

def glow(img, radius=18, strength=1.6):
    g = img.filter(ImageFilter.GaussianBlur(radius))
    a = g.getchannel("A").point(lambda v: min(255, int(v * strength)))
    g.putalpha(a)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(img)
    return out

def pad_img(img, p):
    o = Image.new("RGBA", (img.width + 2 * p, img.height + 2 * p), (0, 0, 0, 0)); o.paste(img, (p, p)); return o

# ---------------------------------------------------------------- easing
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def lin(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def eo_cubic(x): return 1 - (1 - x) ** 3
def eo_back(x, s=1.9): x -= 1; return 1 + x * x * ((s + 1) * x + s)
def ei_cubic(x): return x ** 3
def eo_bounce(x):
    n, d = 7.5625, 2.75
    if x < 1 / d: return n * x * x
    if x < 2 / d: x -= 1.5 / d; return n * x * x + .75
    if x < 2.5 / d: x -= 2.25 / d; return n * x * x + .9375
    x -= 2.625 / d; return n * x * x + .984375

# ---------------------------------------------------------------- textures 16x16
def tex(kind, seed=0):
    r = np.random.default_rng(seed + hash(kind) % 1000)
    n = r.random((16, 16))
    def pal(cols, v): return np.array(cols)[np.minimum((v * len(cols)).astype(int), len(cols) - 1)]
    if kind == "dirt": a = pal([(121, 85, 58), (134, 96, 67), (150, 108, 74), (96, 67, 45)], n)
    elif kind == "stone": a = pal([(116, 116, 116), (127, 127, 127), (137, 137, 137), (104, 104, 104)], n)
    elif kind == "grass_top": a = pal([(89, 140, 50), (101, 160, 58), (113, 170, 64), (80, 125, 45)], n)
    elif kind == "grass_side":
        a = pal([(121, 85, 58), (134, 96, 67), (150, 108, 74), (96, 67, 45)], n)
        g = pal([(89, 140, 50), (101, 160, 58), (113, 170, 64), (80, 125, 45)], n)
        depth = 3 + (r.random(16) * 2.5).astype(int)
        for x in range(16): a[:depth[x], x] = g[:depth[x], x]
    elif kind == "gold":
        a = pal([(248, 211, 64), (255, 236, 92), (235, 190, 40), (252, 222, 75)], n)
        a[0, :] = a[:, 0] = (255, 251, 180); a[15, :] = a[:, 15] = (196, 140, 20)
        for i in range(3, 13): a[i, 16 - i] = (255, 248, 160)
    elif kind == "diamond_ore":
        a = pal([(116, 116, 116), (127, 127, 127), (137, 137, 137), (104, 104, 104)], n)
        for _ in range(5):
            x, y = r.integers(1, 14, 2); a[y:y + 2, x:x + 2] = (92, 219, 213); a[y, x] = (210, 255, 250)
    elif kind == "log":
        a = pal([(102, 80, 48), (88, 68, 40), (110, 86, 52)], n)
        for x in range(0, 16, 3): a[:, x] = (76, 58, 34)
    elif kind == "leaves":
        a = pal([(48, 110, 28), (58, 128, 34), (40, 92, 22), (66, 140, 40)], n)
    elif kind == "plank":
        a = pal([(162, 130, 78), (172, 140, 86), (150, 120, 70)], n)
        for y in (3, 7, 11, 15): a[y, :] = (110, 86, 50)
    elif kind == "tnt":
        a = pal([(219, 68, 38), (196, 52, 30), (230, 90, 50)], n)
        for x in range(0, 16, 4): a[:, x] = (160, 40, 25)
        a[5:11, :] = (230, 230, 230)
        T = ["XXX.X..X.XXX", ".X..XX.X..X.", ".X..X.XX..X.", ".X..X..X..X."]
        for yy, row in enumerate(T):
            for xx, ch in enumerate(row):
                if ch == "X": a[6 + yy, 2 + xx] = (30, 30, 30)
    elif kind == "tnt_top":
        a = pal([(219, 68, 38), (196, 52, 30)], n); a[6:10, 6:10] = (60, 60, 60); a[7:9, 7:9] = (230, 200, 120)
    elif kind == "obsidian":
        a = pal([(20, 18, 30), (32, 24, 50), (45, 32, 70), (15, 12, 22)], n)
    else:
        a = np.full((16, 16, 3), 200)
    return Image.fromarray(a.astype(np.uint8), "RGB")

def tex_s(kind, s, seed=0): return tex(kind, seed).resize((s, s), Image.NEAREST)

def shade(im, f):
    return Image.fromarray(np.clip(np.asarray(im).astype(np.float32) * f, 0, 255).astype(np.uint8), im.mode)

def block_sprite(front, top, s, d):
    """Extruded block: front face + top + right side (viewed from up-right)."""
    im = Image.new("RGBA", (s + d, s + d), (0, 0, 0, 0))
    ft = tex_s(front, s).convert("RGBA"); tp = tex_s(top, s).convert("RGBA")
    # top face (parallelogram) via affine
    topf = shade(tp, 1.15).transform((s + d, d), Image.AFFINE, (1, 1, -d, 0, s / d, 0), Image.NEAREST)
    side = shade(ft, 0.6).transform((d, s + d), Image.AFFINE, (d / d * 1, 0, 0, 0, 1, 0), Image.NEAREST)
    # build side as shear of narrow strip
    sd = shade(ft, 0.55).resize((d, s), Image.NEAREST)
    sdi = Image.new("RGBA", (d, s + d), (0, 0, 0, 0))
    arr = np.zeros((s + d, d, 4), np.uint8); sa = np.asarray(sd)
    for x in range(d):
        off = d - x
        arr[off:off + s, x] = sa[:, x]
    sdi = Image.fromarray(arr, "RGBA")
    im.alpha_composite(topf, (0, 0))
    im.alpha_composite(sdi, (s, 0))
    im.alpha_composite(ft, (0, d))
    dd = ImageDraw.Draw(im); dd.rectangle([0, d, s - 1, s + d - 1], outline=(0, 0, 0, 90))
    return im

# ---------------------------------------------------------------- pixel icons 16x16
ICONS = {
 "pickaxe": ["....CCCCCC......", "...CDDDDDDC.....", "..CDDCCCCDDC....", ".CDC....C.CDC...",
             ".CC....CBC.CC...", "......CBC.......", ".....CBC........", "....CBC.........",
             "...CBC..........", "..CBC...........", ".CBC............", "CBC.............",
             "CC..............", "................", "................", "................"],
 "sword": [".............CCC", "............CDDC", "...........CDDC.", "..........CDDC..",
           ".........CDDC...", "........CDDC....", "..CC...CDDC.....", "..CDC.CDDC......",
           "...CDCDDC.......", "....CDDC........", "....CBCDC.......", "...CBC.CDC......",
           "CCCBC...CC......", "CGCC............", "CCC.............", "................"],
 "chest": ["................", ".CCCCCCCCCCCCCC.", ".CWWWWWWWWWWWWC.", ".CWHHHHHHHHHHWC.", ".CWHHHHHHHHHHWC.",
           ".CCCCCCYYCCCCCC.", ".CWWWWWYYWWWWWC.", ".CWHHHHHHHHHHWC.", ".CWHHHHHHHHHHWC.",
           ".CWHHHHHHHHHHWC.", ".CWHHHHHHHHHHWC.", ".CWWWWWWWWWWWWC.", ".CCCCCCCCCCCCCC.", "................", "................", "................"],
 "heart": ["................", "................", "..CCC....CCC....", ".CRRRC..CRRRC...", "CRWRRRCCRRRRRC..",
           "CRWRRRRRRRRRRC..", "CRRRRRRRRRRRRC..", ".CRRRRRRRRRRC...", "..CRRRRRRRRC....",
           "...CRRRRRRC.....", "....CRRRRC......", ".....CRRC.......", "......CC........", "................", "................", "................"],
 "bird": ["................", "....KKKKKKK.....", "...KYYYYYYYK....", "..KYYYYYYYYYK...",
          "..KYYKKYYYYYK...", "..KYYKWYYYYYK...", "..KYYYYYYYYYKKK.", "..KYYYYYYYOOOOK.",
          "..KYYYYYYYOOOOOK", "..KYYYYYYYKOOOK.", "..KYYYYYYYYKKK..", "..KYYYYYYYYYK...",
          "...KYYYYYYYK....", "....KKKKKKK.....", "................", "................"],
}
ICOL = {"C": (20, 20, 30), "D": (90, 230, 220), "B": (120, 85, 50), "G": (60, 60, 70),
        "W": (150, 105, 50), "H": (190, 140, 70), "Y": (250, 210, 70), "R": (225, 30, 40),
        "K": (25, 20, 15), "O": (255, 140, 30)}
ICOL_BIRD = dict(ICOL); ICOL_BIRD["W"] = (255, 255, 255)
def icon(name, scale):
    rows = ICONS[name]; a = np.zeros((16, 16, 4), np.uint8)
    cols = ICOL_BIRD if name == "bird" else ICOL
    for y, row in enumerate(rows):
        for x, ch in enumerate(row[:16]):
            if ch != ".": a[y, x] = cols[ch] + (255,)
    return Image.fromarray(a, "RGBA").resize((16 * scale, 16 * scale), Image.NEAREST)

# ---------------------------------------------------------------- world / sky
def gradient(cols, h=H, w=W):
    ys = np.linspace(0, 1, h)[:, None]
    stops = np.linspace(0, 1, len(cols)); c = np.array(cols, np.float32)
    out = np.stack([np.interp(ys[:, 0], stops, c[:, i]) for i in range(3)], 1)
    return np.repeat(out[:, None, :], w, 1)

SKY_NIGHT = gradient([(6, 8, 30), (22, 20, 70), (60, 40, 110), (110, 60, 120)])
SKY_DAY = gradient([(70, 130, 240), (120, 170, 255), (180, 215, 255)])
SKY_SUNSET = gradient([(30, 20, 80), (120, 50, 130), (240, 110, 90), (255, 190, 110)])
SKY_CAVE = gradient([(12, 10, 18), (25, 20, 35), (12, 10, 18)])
STARS = [(R.uniform(0, W), R.uniform(0, H * 0.7), R.integers(2, 5), R.uniform(0, 6)) for _ in range(260)]

def make_world(B, cols, base, amp, seed, trees=True, silhouette=None):
    r = np.random.default_rng(seed)
    x = np.arange(cols)
    h = base + amp * (np.sin(x / 9 + seed) * 0.6 + np.sin(x / 4.3 + 2 * seed) * 0.3 + np.sin(x / 23) * 0.8)
    h = np.round(h).astype(int)
    rows = H // B + 2
    im = Image.new("RGBA", (cols * B, rows * B), (0, 0, 0, 0))
    if silhouette:
        d = ImageDraw.Draw(im)
        for i in range(cols): d.rectangle([i * B, h[i] * B, (i + 1) * B - 1, rows * B], fill=silhouette)
        return im, h
    T = {k: tex_s(k, B, 3).convert("RGBA") for k in ["grass_side", "dirt", "stone", "diamond_ore", "log", "leaves", "gold"]}
    for i in range(cols):
        for j in range(h[i], rows):
            k = "grass_side" if j == h[i] else ("dirt" if j < h[i] + 3 else "stone")
            if k == "stone" and r.random() < 0.05: k = "diamond_ore"
            if k == "stone" and r.random() < 0.02: k = "gold"
            im.alpha_composite(T[k], (i * B, j * B))
    if trees:
        for i in range(2, cols - 2):
            if r.random() < 0.09 and abs(h[i] - h[i - 1]) <= 1:
                th = r.integers(3, 6); top = h[i] - th
                for yy in range(top - 2, top + 1):
                    for xx in range(i - 2, i + 3):
                        if abs(xx - i) + abs(yy - top) < 4 and r.random() < 0.92:
                            im.alpha_composite(T["leaves"], (xx * B, yy * B))
                for yy in range(top + 1, h[i]): im.alpha_composite(T["log"], (i * B, yy * B))
    return im, h

WORLD, _ = make_world(48, 170, 15.5, 2.2, 1)
WORLD_FAR, _ = make_world(24, 260, 26, 6, 5, trees=False, silhouette=(255, 255, 255, 255))

def tint(img, mul, add=(0, 0, 0)):
    a = np.asarray(img).astype(np.float32)
    a[..., :3] = np.clip(a[..., :3] * np.array(mul) + np.array(add), 0, 255)
    return Image.fromarray(a.astype(np.uint8), "RGBA")

WORLD_NIGHT = tint(WORLD, (0.32, 0.36, 0.6))
WORLD_SUNSET = tint(WORLD, (0.75, 0.6, 0.65), (20, 0, 10))
FAR_NIGHT = tint(WORLD_FAR, (0.08, 0.08, 0.2)); FAR_DAY = tint(WORLD_FAR, (0.45, 0.6, 0.8)); FAR_SUNSET = tint(WORLD_FAR, (0.35, 0.18, 0.4))

def make_clouds(seed, w=4000):
    r = np.random.default_rng(seed); a = np.zeros((40, w // 24), np.uint8)
    for _ in range(40):
        x = r.integers(0, a.shape[1] - 20); y = r.integers(2, 30); cw = r.integers(5, 16); ch = r.integers(2, 5)
        a[y:y + ch, x:x + cw] = 1
        a[y + 1:y + ch - 1, max(0, x - 2):x + cw + 2] = 1
    im = Image.fromarray((a * 230).astype(np.uint8), "L").resize((a.shape[1] * 24, a.shape[0] * 24), Image.NEAREST)
    rgba = Image.new("RGBA", im.size, (255, 255, 255, 0)); rgba.putalpha(im); return rgba
CLOUDS = make_clouds(3)
CLOUDS_NIGHT = tint(CLOUDS,(0.30,0.30,0.48)); CLOUDS_SUNSET = tint(CLOUDS,(1.0,0.78,0.82))

def scroll_layer(dst, layer, offset, y=0):
    off = int(offset) % layer.width
    if layer.width - off >= W:
        part = layer.crop((off, 0, off + W, layer.height))
    else:
        part = Image.new("RGBA", (W, layer.height), (0, 0, 0, 0))
        a = layer.crop((off, 0, layer.width, layer.height)); part.paste(a, (0, 0))
        part.paste(layer.crop((0, 0, W - a.width, layer.height)), (a.width, 0))
    dst.alpha_composite(part, (0, int(y)))

def landscape(t, sky, world, far, speed, stars=0.0, clouds=0.9, celestial=None, world_y=0, cam_y=0):
    base = Image.fromarray(sky.astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(base)
    if stars > 0:
        for (x, y, s, ph) in STARS:
            b = int(255 * stars * (0.55 + 0.45 * math.sin(t * 2.5 + ph)))
            d.rectangle([x, y + cam_y * 0.2, x + s, y + s + cam_y * 0.2], fill=(b, b, min(255, b + 20), 255))
    if celestial:
        kind, cx, cy = celestial
        if kind == "moon":
            g = Image.new("RGBA", (420, 420), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
            gd.ellipse([60, 60, 360, 360], fill=(200, 210, 255, 70)); g = g.filter(ImageFilter.GaussianBlur(50))
            base.alpha_composite(g, (int(cx - 210), int(cy - 210 + cam_y * 0.3)))
            d.rectangle([cx - 70, cy - 70 + cam_y * 0.3, cx + 70, cy + 70 + cam_y * 0.3], fill=(235, 238, 250, 255))
            for (ox, oy, s) in [(-40, -30, 30), (20, 10, 40), (-10, 40, 20)]:
                d.rectangle([cx + ox, cy + oy + cam_y * 0.3, cx + ox + s, cy + oy + s + cam_y * 0.3], fill=(200, 205, 225, 255))
        else:
            g = Image.new("RGBA", (700, 700), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
            gd.ellipse([150, 150, 550, 550], fill=(255, 220, 140, 150)); g = g.filter(ImageFilter.GaussianBlur(80))
            base.alpha_composite(g, (int(cx - 350), int(cy - 350)))
            d.rectangle([cx - 90, cy - 90, cx + 90, cy + 90], fill=(255, 245, 170, 255))
            d.rectangle([cx - 60, cy - 60, cx + 60, cy + 60], fill=(255, 255, 220, 255))
    if clouds:
        cl = CLOUDS_NIGHT if stars > 0 else (CLOUDS_SUNSET if sky is SKY_SUNSET else CLOUDS)
        scroll_layer(base, cl, t * speed * 0.15 + 300, 40 + cam_y * 0.25)
    scroll_layer(base, far, t * speed * 0.35, H - far.height + 180 + world_y * 0.5 + cam_y * 0.5)
    scroll_layer(base, world, t * speed, H - world.height + 150 + world_y + cam_y)
    return base

# ---------------------------------------------------------------- logo blocks
def logo_bitmap(txt):
    f = _font("ps", 8, False); im = Image.new("L", (8 * len(txt) + 8, 12), 0)
    ImageDraw.Draw(im).text((0, 0), txt, font=f, fill=255)
    a = np.asarray(im) > 127; ys, xs = np.nonzero(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
LOGO = logo_bitmap("DZIOB")
LS, LD = 34, 12
LOGO_W = LOGO.shape[1] * LS + LD; LOGO_H = LOGO.shape[0] * LS + LD
SPR = {"gold": block_sprite("gold", "gold", LS, LD), "grass": block_sprite("grass_side", "grass_top", LS, LD)}
LOGO_BLOCKS = []
_rr = np.random.default_rng(9)
for y in range(LOGO.shape[0] - 1, -1, -1):
    for x in range(LOGO.shape[1]):
        if LOGO[y, x]:
            letter = min(4, x // 8)
            delay = LETTER_T[letter] - 0.0 + (LOGO.shape[0] - y) * 0.03 + _rr.uniform(0, 0.12)
            LOGO_BLOCKS.append((x, y, delay, "grass" if (y == 0 or not LOGO[y - 1, x]) else "gold"))

def draw_logo(t, cx, cy, settle_all=False):
    im = Image.new("RGBA", (LOGO_W, LOGO_H + 40), (0, 0, 0, 0))
    for (x, y, dl, k) in LOGO_BLOCKS:
        p = 1.0 if settle_all else lin(t, dl, dl + 0.5)
        if p <= 0: continue
        off = (1 - eo_bounce(p)) * -900
        im.alpha_composite(SPR[k], (x * LS, int(y * LS + off) + 20)) if y * LS + off + 20 > -LS - LD else None
    return im

def shine(img, t, t0, dur=0.9):
    p = lin(t, t0, t0 + dur)
    if p <= 0 or p >= 1: return img
    w, h = img.size; a = np.asarray(img).astype(np.float32)
    xs = np.arange(w)[None, :]; ys = np.arange(h)[:, None]
    pos = -h + p * (w + 2 * h)
    band = np.clip(1 - np.abs((xs + ys * 0.6) - pos) / 60, 0, 1) * 0.75
    a[..., :3] = a[..., :3] + (255 - a[..., :3]) * band[..., None] * (a[..., 3:4] / 255)
    return Image.fromarray(a.astype(np.uint8), "RGBA")

def rays_img():
    s = 2400; im = Image.new("L", (s, s), 0); d = ImageDraw.Draw(im); c = s / 2
    for i in range(18):
        a0 = i * 2 * math.pi / 18; a1 = a0 + math.pi / 30
        d.polygon([(c, c), (c + s * math.cos(a0), c + s * math.sin(a0)), (c + s * math.cos(a1), c + s * math.sin(a1))], fill=255)
    im = im.filter(ImageFilter.GaussianBlur(6))
    yy, xx = np.mgrid[0:s, 0:s]; rr = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / (s / 2)
    a = (np.asarray(im) * np.clip(1 - rr, 0, 1) ** 1.5).astype(np.uint8)
    return Image.fromarray(a, "L")
RAYS = rays_img()

def add_rays(base, t, cx, cy, col, strength):
    if strength <= 0: return
    r = RAYS.rotate(t * 12, resample=Image.BILINEAR)
    l = r.crop((int(r.width / 2 - cx), int(r.height / 2 - cy), int(r.width / 2 - cx) + W, int(r.height / 2 - cy) + H))
    a = l.point(lambda v: int(v * strength))
    layer = Image.new("RGBA", (W, H), col + (0,)); layer.putalpha(a); base.alpha_composite(layer)

# ---------------------------------------------------------------- particles
FW_COLS = [(255, 80, 80), (255, 210, 60), (90, 220, 255), (120, 255, 120), (230, 110, 255), (255, 255, 255)]
def draw_fireworks(arr, t):
    for (t0, x, y, c, n) in FIREWORKS:
        dt = t - t0
        if dt < -0.6 or dt > 2.2: continue
        col = np.array(FW_COLS[c], np.float32)
        if dt < 0:  # rocket rising
            p = (dt + 0.6) / 0.6; ry = H + 20 - (H + 20 - y) * eo_cubic(p)
            for k in range(6):
                yy = int(ry + k * 14); a = 1 - k / 6
                _sq(arr, x, yy, 5, np.array([255, 220, 160]) * a)
            continue
        rr = np.random.default_rng(int(t0 * 1000))
        ang = np.linspace(0, 2 * np.pi, n, endpoint=False) + rr.uniform(0, 1, n) * 0.2
        v = rr.uniform(260, 420, n)
        life = clamp(1 - dt / 2.0)
        for tr in range(3):
            tt = max(0, dt - tr * 0.05)
            dist = v / 2.2 * (1 - math.exp(-2.2 * tt))
            px = x + np.cos(ang) * dist; py = y + np.sin(ang) * dist + 70 * tt * tt
            fl = 1.0 if dt < 1.0 else (0.5 + 0.5 * math.sin(dt * 40))
            for i in range(n):
                _sq(arr, px[i], py[i], 7 - 2 * tr, col * life * fl * (1 - tr * 0.3))
        if dt < 0.12:
            _glow(arr, x, y, 160 * (1 - dt / 0.12), col * 0.8)

def _sq(arr, x, y, s, c):
    x0, y0 = int(x - s / 2), int(y - s / 2); x1, y1 = x0 + s, y0 + s
    if x1 < 0 or y1 < 0 or x0 >= W or y0 >= H: return
    arr[max(0, y0):min(H, y1), max(0, x0):min(W, x1)] += c

def _glow(arr, x, y, r, c):
    r = int(r)
    if r < 2: return
    x0, x1, y0, y1 = max(0, int(x - r)), min(W, int(x + r)), max(0, int(y - r)), min(H, int(y + r))
    if x1 <= x0 or y1 <= y0: return
    yy, xx = np.mgrid[y0:y1, x0:x1]; d = np.clip(1 - np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / r, 0, 1) ** 2
    arr[y0:y1, x0:x1] += d[..., None] * c

def embers(arr, t, n=70, col=(255, 200, 120), seed=3, speed=60):
    rr = np.random.default_rng(seed)
    xs = rr.uniform(0, W, n); ph = rr.uniform(0, 100, n); sp = rr.uniform(0.5, 1.5, n); sz = rr.integers(3, 8, n)
    for i in range(n):
        y = H - ((t * speed * sp[i] + ph[i] * 37) % (H + 100))
        x = xs[i] + 30 * math.sin(t * sp[i] + ph[i])
        a = 0.5 + 0.5 * math.sin(t * 3 + ph[i])
        _sq(arr, x, y, int(sz[i]), np.array(col) * a * 0.8)

# ---------------------------------------------------------------- UI pieces
def mc_panel(w, h, dark=False):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); b = 6
    if dark:
        d.rectangle([0, 0, w - 1, h - 1], fill=(16, 10, 30, 225)); d.rectangle([b, b, w - b - 1, h - b - 1], outline=(80, 30, 160, 255), width=b)
        return im
    d.rectangle([b, 0, w - b - 1, h - 1], fill=(0, 0, 0, 255)); d.rectangle([0, b, w - 1, h - b - 1], fill=(0, 0, 0, 255))
    d.rectangle([b, b, w - b - 1, h - b - 1], fill=(198, 198, 198, 255))
    d.rectangle([b, b, w - b - 1, 2 * b - 1], fill=(255, 255, 255, 255)); d.rectangle([b, b, 2 * b - 1, h - b - 1], fill=(255, 255, 255, 255))
    d.rectangle([b, h - 2 * b, w - b - 1, h - b - 1], fill=(85, 85, 85, 255)); d.rectangle([w - 2 * b, b, w - b - 1, h - b - 1], fill=(85, 85, 85, 255))
    return im

def slot(s):
    im = Image.new("RGBA", (s, s), (139, 139, 139, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, s - 1, 5], fill=(55, 55, 55, 255)); d.rectangle([0, 0, 5, s - 1], fill=(55, 55, 55, 255))
    d.rectangle([0, s - 6, s - 1, s - 1], fill=(255, 255, 255, 255)); d.rectangle([s - 6, 0, s - 1, s - 1], fill=(255, 255, 255, 255))
    return im

CARDS = [("pickaxe", "NOWY ŚWIAT", "Świeża mapa – wszyscy", "startują od zera!"),
         ("sword", "PRZYGODA", "Odkrywaj, buduj", "i walcz o swoje."),
         ("chest", "EVENTY I NAGRODY", "Konkursy i niespodzianki", "od ekipy serwera."),
         ("heart", "SPOŁECZNOŚĆ", "Graj ze znajomymi", "i poznawaj nowych!")]
def card_img(i):
    ic, title, l1, l2 = CARDS[i]
    w, h = 1180, 300; im = mc_panel(w, h)
    sl = slot(212); sl.alpha_composite(icon(ic, 11), (18, 18)); im.alpha_composite(sl, (44, 44))
    im.alpha_composite(text_img(title, 62, (63, 63, 63), "px", shadow=False), (300, 52))
    im.alpha_composite(text_img(l1, 42, (90, 90, 90), "pxr", shadow=False), (302, 150))
    im.alpha_composite(text_img(l2, 42, (90, 90, 90), "pxr", shadow=False), (302, 208))
    return im
CARD_IMGS = [card_img(i) for i in range(4)]

def toast():
    w, h = 640, 128; im = mc_panel(w, h, dark=True)
    im.alpha_composite(icon("bird", 4), (24, 32))
    im.alpha_composite(text_img("Osiągnięcie zdobyte!", 28, (255, 255, 85), "px"), (116, 22))
    im.alpha_composite(text_img("Premiera Dziob.6mc.PL", 28, (255, 255, 255), "px"), (116, 70))
    return im
TOAST = toast()

def server_entry():
    w, h = 1300, 220; im = Image.new("RGBA", (w, h), (0, 0, 0, 170)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(160, 160, 160, 255), width=4)
    ic = Image.new("RGBA", (176, 176), (60, 140, 220, 255)); ic.alpha_composite(icon("bird", 10), (8, 8))
    im.alpha_composite(ic, (22, 22))
    im.alpha_composite(text_img("Dziob.6mc.PL", 52, (255, 255, 255), "px"), (226, 26))
    im.alpha_composite(text_img("WIELKA PREMIERA", 40, (255, 170, 0), "px"), (226, 102))
    im.alpha_composite(text_img("Wbijaj już teraz!", 40, (85, 255, 255), "px"), (226, 152))
    im.alpha_composite(text_img("ONLINE", 36, (85, 255, 85), "px"), (w - 270, 32))
    for k in range(5):
        hh = 12 + k * 8; d.rectangle([w - 90 + k * 14, 70 - hh, w - 90 + k * 14 + 9, 70], fill=(85, 255, 85, 255))
    return im
SERVER = server_entry()

# ---------------------------------------------------------------- audio spectrum
MIX = np.load(os.path.join(BUILD, "mix.npy")); SR = 44100
NB = 48
def spectrum(t):
    i = int(t * SR); seg = MIX[max(0, i - 2048):i + 2048]
    if len(seg) < 4096: seg = np.pad(seg, (0, 4096 - len(seg)))
    X = np.abs(np.fft.rfft(seg * np.hanning(4096)))
    edges = np.logspace(np.log10(3), np.log10(1500), NB + 1).astype(int)
    b = np.array([X[edges[k]:max(edges[k] + 1, edges[k + 1])].mean() for k in range(NB)])
    return np.clip(np.log1p(b * 4) / 4.5, 0, 1)
def level(t):
    i = int(t * SR); seg = MIX[max(0, i - 1500):i + 1500]
    return float(np.sqrt(np.mean(seg ** 2)) * 4) if len(seg) else 0.0

def visualizer(arr, t, alpha=1.0):
    sp = spectrum(t); bw = W / NB
    for k in range(NB):
        hh = int(sp[k] * 180 / 12) * 12
        c = np.array([90 + 165 * k / NB, 230 - 100 * k / NB, 255]) * 0.55 * alpha
        for yy in range(0, hh, 12):
            arr[H - 14 - yy - 10:H - 14 - yy, int(k * bw + 3):int((k + 1) * bw - 3)] += c

# ---------------------------------------------------------------- post
yy, xx = np.mgrid[0:H, 0:W]
VIGN = (1 - 0.55 * np.clip(((xx - W / 2) ** 2 / (W * 0.62) ** 2 + (yy - H / 2) ** 2 / (H * 0.75) ** 2), 0, 1) ** 1.3).astype(np.float32)[..., None]
del yy, xx
GRAIN = [np.random.default_rng(i).normal(0, 5, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1) for i in range(6)]

def pixelate(img, k):
    k = int(k)
    if k <= 1: return img
    return img.resize((max(1, W // k), max(1, H // k)), Image.BILINEAR).resize((W, H), Image.NEAREST)

def shake(t):
    s = 0.0
    for lt in LETTER_T: s += 16 * math.exp(-max(0, t - lt - 0.55) * 9) * (t >= lt + 0.55)
    s += 40 * math.exp(-max(0, t - BOOM_T) * 3) * (t >= BOOM_T)
    s += 10 * math.exp(-max(0, t - 6.6) * 6) * (t >= 6.6)
    if t > 26.2 and t < BOOM_T: s += 3 * (t - 26.2)
    return s

# ---------------------------------------------------------------- scenes
def scene_intro(t):
    cam = (1 - eo_cubic(lin(t, 0, 6.6))) * -260
    img = landscape(t, SKY_NIGHT, WORLD_NIGHT, FAR_NIGHT, 70, stars=1.0, celestial=("moon", 1500, 230), cam_y=-cam)
    a = np.asarray(img.convert("RGB")).astype(np.float32); add = np.zeros_like(a)
    embers(add, t, 50, (150, 200, 255), 4, 40)
    visualizer(add, t, 0.6 * lin(t, 0.5, 1.5))
    img = Image.fromarray(np.clip(a + add, 0, 255).astype(np.uint8)).convert("RGBA")
    # "6mc.pl przedstawia"
    a1 = lin(t, 0.8, 1.6) * (1 - lin(t, 5.6, 6.3))
    paste(img, glow(pad_img(text_img("6MC.PL", 96, (255, 255, 255), outline=4, ocol=(20,10,50)), 30), 18), W / 2, 400, a1)
    s = "przedstawia..."; n = int(len(s) * lin(t, 1.8, 3.0))
    if n: paste(img, text_img(s[:n], 44, (210, 210, 255), "ps", outline=3, ocol=(10,5,30)), W / 2 - text_img(s, 44, (210, 210, 255), "ps", outline=3, ocol=(10,5,30)).width / 2, 530, a1, anchor="l")
    a2 = lin(t, 3.4, 4.0) * (1 - lin(t, 5.8, 6.4))
    s2 = "Nowy serwer Minecraft nadchodzi"
    if a2 > 0: paste(img, text_img(s2, 42, (255, 255, 120), "ps", outline=3, ocol=(40,20,0)), W / 2, 640 + (1 - eo_cubic(lin(t, 3.4, 4.0))) * 30, a2)
    fade = lin(t, 0, 0.8)
    if fade < 1: img = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), img, fade)
    return img

def scene_logo(t):
    img = landscape(t, SKY_NIGHT, WORLD_NIGHT, FAR_NIGHT, 40, stars=1.0, celestial=("moon", 1600, 160))
    dark = Image.new("RGBA", (W, H), (5, 0, 20, 110)); img.alpha_composite(dark)
    lv = level(t)
    add_rays(img, t, W / 2, 400, (255, 215, 90), 0.20 * lin(t, 7.2, 8.6) + 0.1 * lv)
    bob = math.sin(t * 1.6) * 8 * lin(t, 8.4, 9.0)
    logo = draw_logo(t, W / 2, 380)
    logo = shine(logo, t, 9.2); logo = shine(logo, t, 12.6)
    if t > 8.3:
        g = logo.filter(ImageFilter.GaussianBlur(22)); ga = g.getchannel("A").point(lambda v: int(min(255, v * 1.3 * lin(t, 8.3, 9.2))))
        gl = Image.new("RGBA", g.size, (255, 200, 60, 0)); gl.putalpha(ga); paste(img, gl, W / 2, 360 + bob)
    paste(img, logo, W / 2, 360 + bob)
    p = lin(t, 8.6, 9.2)
    if p > 0:
        sub = glow(pad_img(text_img(".6MC.PL", 72, (90, 230, 255), "ps"), 30), 16, 2.0)
        paste(img, sub, W / 2, 650 + bob, min(1, p * 2), scale=eo_back(p))
    s = "WIELKA PREMIERA SERWERA"; n = int(len(s) * lin(t, 10.0, 11.0))
    if n:
        full = text_img(s, 46, (255, 255, 255), "ps", outline=3, ocol=(20,10,50))
        paste(img, text_img(s[:n], 46, (255, 255, 255), "ps", outline=3, ocol=(20,10,50)), W / 2 - full.width / 2, 790, 1, anchor="l")
    a3 = lin(t, 11.6, 12.2)
    if a3: paste(img, text_img("Survival  •  Przygoda  •  Społeczność", 52, (255, 220, 120), "px", outline=3, ocol=(40,20,0)), W / 2, 880 + (1 - eo_cubic(a3)) * 30, a3)
    arr = np.asarray(img.convert("RGB")).astype(np.float32); addl = np.zeros_like(arr)
    # landing dust
    for i, lt in enumerate(LETTER_T):
        dt = t - lt - 0.55
        if 0 <= dt < 0.9:
            rr = np.random.default_rng(i)
            cx0 = W / 2 - LOGO_W / 2 + (i * 8 + 4) * LS
            for k in range(26):
                ang = rr.uniform(math.pi, 2 * math.pi); v = rr.uniform(100, 380)
                _sq(addl, cx0 + math.cos(ang) * v * dt, 360 + LOGO_H / 2 + math.sin(ang) * v * dt * 0.5 + 40 * dt * dt, 9, np.array([200, 180, 140]) * (1 - dt / 0.9) * 0.8)
    draw_fireworks(addl, t)
    embers(addl, t, 50, (255, 200, 100), 7, 70)
    visualizer(addl, t, 0.6)
    img = Image.fromarray(np.clip(arr + addl, 0, 255).astype(np.uint8)).convert("RGBA")
    return img

def scene_features(t):
    img = landscape(t, SKY_DAY, WORLD, FAR_DAY, 220, celestial=("sun", 1650, 170))
    # cards
    for i, ct in enumerate(CARD_T):
        if t < ct - 0.1 or t > ct + 2.8: continue
        pin = eo_back(lin(t, ct, ct + 0.55), 1.4); pout = ei_cubic(lin(t, ct + 2.2, ct + 2.6))
        x = W / 2 + (1 - pin) * 1500 - pout * 1700
        rot = (1 - pin) * -6 + pout * 6
        paste(img, CARD_IMGS[i], x, H / 2 + 40, 1.0, rot=rot)
        # counter dots
        for k in range(4):
            col = (255, 255, 85, 255) if k == i else (255, 255, 255, 120)
            ImageDraw.Draw(img).rectangle([W / 2 - 70 + k * 40, 900, W / 2 - 50 + k * 40, 920], fill=col)
    # header
    paste(img, text_img("CO CZEKA NA SERWERZE?", 52, (255, 255, 255), "ps", outline=4, ocol=(30,50,90)), W / 2, 210, lin(t, 14.9, 15.4), scale=1)
    # toast
    tp = eo_cubic(lin(t, 15.2, 15.7)) * (1 - ei_cubic(lin(t, 19.0, 19.4)))
    if tp > 0: img.alpha_composite(TOAST, (int(W - tp * (TOAST.width + 30)), 30))
    arr = np.asarray(img.convert("RGB")).astype(np.float32); addl = np.zeros_like(arr)
    embers(addl, t, 30, (255, 255, 200), 11, 50)
    img = Image.fromarray(np.clip(arr + addl, 0, 255).astype(np.uint8)).convert("RGBA")
    return img

TNT = block_sprite("tnt", "tnt_top", 300, 70)
DEBRIS = [block_sprite(k, k, 60, 16) for k in ["dirt", "stone", "grass_side", "gold", "diamond_ore"]]
OBS_BG = None
def cave_bg():
    t1 = tex_s("stone", 96, 2); bg = Image.new("RGBA", (W, H))
    for x in range(0, W, 96):
        for y in range(0, H, 96): bg.paste(t1, (x, y))
    return tint(bg, (0.28, 0.25, 0.35))
CAVE = cave_bg()

def scene_count(t):
    boom = t >= BOOM_T
    if not boom:
        img = CAVE.copy()
        add_rays(img, t, W / 2, H / 2 + 40, (255, 90, 40), 0.15 + 0.15 * lin(t, 26, 30))
        flash = (math.sin((t - 26.2) * (6 + (t - 26.2) * 5)) > 0.3) and t > 26.2
        sc = 1 + 0.08 * lin(t, 26.2, BOOM_T) + (0.04 * math.sin(t * 40) if t > 29.5 else 0)
        tn = TNT if not flash else Image.blend(TNT, Image.new("RGBA", TNT.size, (255, 255, 255, 0)), 0.0)
        if flash:
            a = np.asarray(TNT).astype(np.float32); a[..., :3] = a[..., :3] * 0.3 + 255 * 0.7; tn = Image.fromarray(a.astype(np.uint8), "RGBA")
        paste(img, tn, W / 2, H / 2 + 60, 1, scale=sc * eo_back(lin(t, 25.4, 26.0)))
        paste(img, text_img("ODLICZANIE DO STARTU", 40, (255, 120, 80), "ps"), W / 2, 150, lin(t, 25.6, 26.0))
        for i, ct in enumerate(COUNT_T):
            p = lin(t, ct, ct + 1.3)
            if 0 < p < 1:
                num = text_img(str(3 - i), 220, (255, 255, 255), "ps", outline=10, ocol=(120, 20, 10))
                paste(img, glow(pad_img(num, 30), 18, 1.5), W / 2, H / 2 + 50, 1 - lin(p, 0.7, 1), scale=2.6 - 1.4 * eo_cubic(min(1, p * 3)))
        return img
    dt = t - BOOM_T
    sky_mix = clamp(dt / 1.5)
    img = landscape(t, SKY_SUNSET, WORLD_SUNSET, FAR_SUNSET, 60, celestial=("sun", W / 2, 640 - 200 * eo_cubic(lin(t, BOOM_T, 33))))
    if sky_mix < 1: img = Image.blend(CAVE, img, sky_mix)
    arr = np.asarray(img.convert("RGB")).astype(np.float32); addl = np.zeros_like(arr)
    # shockwave
    r = 2200 * eo_cubic(clamp(dt / 1.0))
    if dt < 1.0:
        yy, xx = np.ogrid[0:H, 0:W]; d = np.sqrt((xx - W / 2) ** 2 + (yy - H / 2) ** 2)
        ring = np.clip(1 - np.abs(d - r) / 60, 0, 1) * (1 - dt)
        addl += ring[..., None] * np.array([255, 220, 160])
    # smoke
    rr = np.random.default_rng(5)
    for k in range(40):
        ang = rr.uniform(0, 2 * math.pi); v = rr.uniform(150, 600); s = int(40 + 120 * dt)
        x = W / 2 + math.cos(ang) * v * (1 - math.exp(-dt * 2)); y = H / 2 + math.sin(ang) * v * (1 - math.exp(-dt * 2)) - 40 * dt
        _sq(addl, x, y, s, np.array([120, 110, 110]) * clamp(1 - dt / 1.2) * 0.22)
    img = Image.fromarray(np.clip(arr + addl, 0, 255).astype(np.uint8)).convert("RGBA")
    # debris
    for k in range(34):
        ang = rr.uniform(0, 2 * math.pi); v = rr.uniform(500, 1500); spn = rr.uniform(-500, 500)
        x = W / 2 + math.cos(ang) * v * dt; y = H / 2 + math.sin(ang) * v * dt + 900 * dt * dt
        if -100 < x < W + 100 and -100 < y < H + 100:
            paste(img, DEBRIS[k % 5], x, y, 1, rot=spn * dt, resample=Image.NEAREST)
    # START text
    p = lin(t, BOOM_T + 0.15, BOOM_T + 0.7)
    if p > 0:
        st = glow(pad_img(text_img("START!", 150, (255, 255, 85), "ps", outline=8, ocol=(80, 30, 0)), 40), 24, 1.8)
        paste(img, st, W / 2, 420, 1, scale=eo_back(p, 2.2) * (1 + 0.03 * math.sin(t * 8)))
    p2 = lin(t, 31.2, 31.8)
    if p2 > 0: paste(img, text_img("SERWER JUŻ DZIAŁA!", 60, (255, 255, 255), "ps", outline=4), W / 2, 640 + (1 - eo_cubic(p2)) * 40, p2)
    arr = np.asarray(img.convert("RGB")).astype(np.float32); addl = np.zeros_like(arr)
    draw_fireworks(addl, t)
    fl = clamp(1 - dt / 0.5)
    img = Image.fromarray(np.clip(arr + addl + 255 * fl, 0, 255).astype(np.uint8)).convert("RGBA")
    return img

def scene_final(t):
    img = landscape(t, SKY_SUNSET, WORLD_SUNSET, FAR_SUNSET, 60, celestial=("sun", W / 2, 440))
    dark = Image.new("RGBA", (W, H), (10, 0, 30, 70)); img.alpha_composite(dark)
    lv = level(t)
    add_rays(img, t, W / 2, 440, (255, 200, 120), 0.12 + 0.12 * lv)
    arr = np.asarray(img.convert("RGB")).astype(np.float32); addl = np.zeros_like(arr)
    draw_fireworks(addl, t)
    img = Image.fromarray(np.clip(arr + addl, 0, 255).astype(np.uint8)).convert("RGBA")
    p = eo_back(lin(t, 33.2, 33.9), 1.2)
    paste(img, SERVER, W / 2, 250 - (1 - p) * 500, 1)
    p2 = lin(t, 34.4, 35.0)
    if p2 > 0:
        pulse = 1 + 0.04 * math.sin(t * 5)
        ip = glow(pad_img(text_img("IP: DZIOB.6MC.PL", 92, (255, 255, 255), "ps", outline=6, ocol=(40, 10, 70)), 40), 22, 1.8)
        paste(img, ip, W / 2, 560, p2, scale=eo_back(p2) * pulse)
    p3 = lin(t, 36.0, 36.5)
    if p3 > 0:
        paste(img, text_img("DOŁĄCZ JUŻ DZIŚ!", 64, (85, 255, 85), "ps", outline=4), W / 2, 720 + (1 - eo_cubic(p3)) * 40, p3)
    p4 = lin(t, 37.0, 37.4)
    if p4 > 0:  # yellow splash
        sp = text_img("Premiera!", 52, (255, 255, 0), "px")
        paste(img, sp, W / 2 + 690, 395, 1, scale=eo_back(p4) * (1 + 0.08 * abs(math.sin(t * 6))), rot=18, resample=Image.BICUBIC)
    p5 = lin(t, 38.6, 39.1)
    if p5 > 0:
        paste(img, text_img("Do zobaczenia w grze!", 60, (255, 225, 170), "px", outline=3, ocol=(40,10,40)), W / 2, 850, p5)
    arr = np.asarray(img.convert("RGB")).astype(np.float32); addl = np.zeros_like(arr)
    visualizer(addl, t, 0.7)
    img = Image.fromarray(np.clip(arr + addl, 0, 255).astype(np.uint8)).convert("RGBA")
    # end card
    e = lin(t, 44.6, 45.6)
    if e > 0:
        blk = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * e))); img.alpha_composite(blk)
        lg = draw_logo(t, 0, 0, settle_all=True)
        paste(img, lg, W / 2, 470, e, scale=0.7)
        paste(img, text_img("dziob.6mc.pl", 48, (90, 230, 255), "ps"), W / 2, 680, e)
    return img

SCENE_FUNCS = [scene_intro, scene_logo, scene_features, scene_count, scene_final]

def render(fi):
    t = fi / FPS
    si = max(i for i in range(5) if SCENES[i] <= t)
    img = SCENE_FUNCS[si](t)
    if si >= 2 and t < 44.6:  # watermark
        wm = text_img("DZIOB.6MC.PL", 22, (255, 255, 255), "ps")
        paste(img, wm, 40, 50, 0.75, anchor="l")
    img = img.convert("RGB")
    # transition pixelation
    pk = 0
    for b in SCENES[1:4] + [SCENES[4]]:
        if b == BOOM_T: continue
        dd = abs(t - b)
        if dd < 0.35: pk = max(pk, 40 * (1 - dd / 0.35) ** 2)
    if pk > 1: img = pixelate(img, pk)
    s = shake(t)
    if s > 0.5:
        rr = np.random.default_rng(fi)
        dx, dy = rr.uniform(-s, s, 2)
        img = img.transform((W, H), Image.AFFINE, (1/1.07, 0, -dx + W * 0.0327, 0, 1/1.07, -dy + H * 0.0327), Image.BILINEAR)
    a = np.asarray(img).astype(np.float32)
    a = a * VIGN + GRAIN[fi % 6]
    fade = clamp((DUR - t) / 0.6)
    a *= fade
    return np.clip(a, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    from multiprocessing import Pool
    out = sys.argv[1]
    start = float(sys.argv[2]) if len(sys.argv) > 2 else 0; end = float(sys.argv[3]) if len(sys.argv) > 3 else DUR
    frames = range(int(start * FPS), int(end * FPS))
    if len(sys.argv) > 4:  # stills
        for f in frames[::int(float(sys.argv[4]) * FPS)]:
            Image.frombytes("RGB", (W, H), render(f)).save(f"{out}/still_{f/FPS:05.1f}.jpg", quality=85)
        sys.exit()
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-ss", str(start), "-i", os.path.join(BUILD, "mix.wav"), "-shortest",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    with Pool(4) as p:
        for i, b in enumerate(p.imap(render, frames, chunksize=4)):
            ff.stdin.write(b)
            if i % 150 == 0: print("frame", i, flush=True)
    ff.stdin.close(); ff.wait()
