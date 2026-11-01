#!/usr/bin/env python3
"""Renderuje izometryczny podgląd mapy DziobMc z wygenerowanych komend
(fill/setblock/summon). To NIE jest zrzut z gry – to wizualizacja tych
samych bloków, które postawi datapack.

Użycie: python3 narzedzia/render_podglad.py  ->  DziobMc/screeny/*.png
"""
import json
import math
import random
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FN = ROOT / "WLASNY-SERWER-na-komputerze/world/datapacks/DziobMc-Pack/data/dziobmc/function/mapa"
OUT = ROOT / "screeny"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

KOLORY = {
    "grass_block": (95, 159, 53), "dirt": (134, 96, 67), "stone": (125, 125, 125), "andesite": (136, 136, 137),
    "cobblestone": (115, 115, 115), "mossy_cobblestone": (100, 120, 90), "tuff": (108, 109, 102), "moss_block": (89, 109, 45),
    "coal_ore": (105, 105, 105), "iron_ore": (150, 135, 125), "gold_ore": (160, 145, 90), "amethyst_block": (133, 97, 191),
    "smooth_quartz": (236, 230, 223), "polished_deepslate": (72, 72, 73), "gold_block": (246, 208, 61),
    "orange_glazed_terracotta": (225, 120, 40), "yellow_concrete": (240, 175, 21), "polished_blackstone_bricks": (48, 42, 49),
    "gilded_blackstone": (90, 60, 40), "quartz_bricks": (234, 229, 221), "chiseled_quartz_block": (231, 226, 218),
    "prismarine_bricks": (99, 171, 158), "iron_block": (220, 220, 220), "smooth_quartz_slab": (236, 230, 223),
    "water": (60, 110, 230), "beacon": (130, 230, 225), "orange_stained_glass": (230, 130, 40),
    "polished_blackstone_wall": (53, 48, 56), "lantern": (255, 200, 90), "soul_lantern": (90, 220, 230),
    "obsidian": (20, 18, 30), "crying_obsidian": (60, 20, 110), "amethyst_cluster": (170, 120, 220),
    "polished_blackstone": (53, 48, 56), "red_nether_bricks": (69, 7, 9), "chiseled_polished_blackstone": (55, 50, 60),
    "polished_blackstone_brick_wall": (48, 42, 49), "soul_campfire": (80, 210, 230), "polished_blackstone_brick_slab": (48, 42, 49),
    "chain": (60, 60, 70), "blackstone": (42, 36, 41), "basalt": (80, 80, 85), "netherrack": (111, 54, 52),
    "magma_block": (140, 60, 20), "crimson_nylium": (130, 30, 30), "nether_gold_ore": (115, 60, 45), "shroomlight": (240, 145, 70),
    "light_blue_concrete": (36, 137, 199), "sea_lantern": (172, 199, 190), "emerald_block": (42, 203, 87),
    "red_concrete": (142, 32, 32), "orange_concrete": (224, 97, 0), "lime_concrete": (94, 168, 24), "blue_concrete": (44, 46, 143),
    "purple_concrete": (100, 31, 156), "magenta_concrete": (169, 48, 159), "pink_concrete": (213, 101, 142),
}
ROSLINY = {"short_grass": (110, 175, 60), "poppy": (200, 30, 30), "dandelion": (245, 220, 40), "cornflower": (70, 100, 220),
           "oxeye_daisy": (240, 240, 230), "azure_bluet": (220, 230, 240), "allium": (180, 100, 220),
           "lily_of_the_valley": (250, 250, 250)}
NIEPELNE = set(ROSLINY) | {"lantern", "soul_lantern", "amethyst_cluster", "chain", "soul_campfire",
                           "polished_blackstone_wall", "polished_blackstone_brick_wall", "water",
                           "orange_stained_glass", "smooth_quartz_slab", "polished_blackstone_brick_slab"}


def wczytaj():
    W, drzewa, encje = {}, [], []
    for nazwa in ["etap/wyspa", "etap/plac", "etap/arena", "etap/parkour", "dekoracje"]:
        for ln in (FN / f"{nazwa}.mcfunction").read_text(encoding="utf-8").splitlines():
            m = re.match(r"fill (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) minecraft:(\w+)", ln)
            if m:
                a = list(map(int, m.groups()[:6]))
                for x in range(min(a[0], a[3]), max(a[0], a[3]) + 1):
                    for y in range(min(a[1], a[4]), max(a[1], a[4]) + 1):
                        for z in range(min(a[2], a[5]), max(a[2], a[5]) + 1):
                            if m.group(7) == "air":
                                W.pop((x, y, z), None)
                            else:
                                W[(x, y, z)] = m.group(7)
                continue
            m = re.match(r"setblock (-?\d+) (-?\d+) (-?\d+) minecraft:(\w+)", ln)
            if m:
                W[tuple(map(int, m.groups()[:3]))] = m.group(4)
                continue
            m = re.match(r"place feature minecraft:(\w+) (-?\d+) (-?\d+) (-?\d+)", ln)
            if m:
                drzewa.append((m.group(1), *map(int, m.groups()[1:])))
                continue
            m = re.match(r"summon minecraft:(\w+) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (.*)$", ln)
            if m:
                typ = m.group(1)
                x, y, z = map(float, m.groups()[1:4])
                tekst = None
                tm = re.search(r"text:'(.*?)',transformation", m.group(5))
                sc = re.search(r"scale:\[([\d.]+)f", m.group(5))
                if tm:
                    comp = json.loads(tm.group(1))
                    comp = comp if isinstance(comp, list) else [comp]
                    tekst = [(c["text"], c.get("color", "white")) for c in comp]
                encje.append((typ, x, y, z, tekst, float(sc.group(1)) if sc else 1.0))
    # drzewa – proste przybliżenie
    rr = random.Random(5)
    for typ, x, y, z in drzewa:
        h = 6 if typ == "cherry" else 7
        lisc = "cherry_leaves" if typ == "cherry" else "oak_leaves"
        pien = "cherry_log" if typ == "cherry" else "oak_log"
        for dy in range(h):
            W[(x, y + dy, z)] = pien
        r = 3.6 if typ == "cherry" else 3.0
        for dx in range(-4, 5):
            for dz in range(-4, 5):
                for dy in range(-2, 3):
                    if (dx * dx + dz * dz) / (r * r) + (dy * dy) / 4.5 <= 1 and rr.random() > 0.12:
                        if (x + dx, y + h - 1 + dy, z + dz) not in W:
                            W[(x + dx, y + h - 1 + dy, z + dz)] = lisc
    return W, encje


KOLORY.update({"cherry_leaves": (240, 170, 200), "oak_leaves": (60, 130, 40), "cherry_log": (60, 35, 45), "oak_log": (100, 80, 50)})
MC = {"gold": (255, 170, 0), "yellow": (255, 255, 85), "white": (255, 255, 255), "gray": (170, 170, 170),
      "aqua": (85, 255, 255), "red": (255, 85, 85), "green": (85, 255, 85), "light_purple": (255, 85, 255),
      "dark_gray": (85, 85, 85), "dark_red": (170, 0, 0), "blue": (85, 85, 255), "dark_purple": (170, 0, 170),
      "dark_green": (0, 170, 0), "dark_aqua": (0, 170, 170)}


def shade(c, f, seed):
    n = ((seed * 2654435761) % 1000) / 1000 * 0.12 - 0.06
    return tuple(max(0, min(255, int(v * (f + n)))) for v in c)


def render(W, encje, a, obszar, plik, tytul, niebo=True):
    x0, x1, z0, z1 = obszar
    bloki = {k: v for k, v in W.items() if x0 <= k[0] <= x1 and z0 <= k[2] <= z1}
    pelne = {k for k, v in bloki.items() if v not in NIEPELNE}

    def scr(x, y, z):
        return ((x - z) * a, (x + z) * a * 0.5 - y * a)

    pts = [scr(x, y, z) for x, y, z in bloki]
    minx = min(p[0] for p in pts) - 6 * a
    maxx = max(p[0] for p in pts) + 6 * a
    miny = min(p[1] for p in pts) - 14 * a
    maxy = max(p[1] for p in pts) + 3 * a
    Wd, Hd = int(maxx - minx), int(maxy - miny)
    img = Image.new("RGB", (Wd, Hd))
    d = ImageDraw.Draw(img)
    if niebo:
        for yy in range(Hd):
            t = yy / Hd
            d.line([(0, yy), (Wd, yy)], fill=(int(90 + 80 * t), int(150 + 60 * t), int(235 + 10 * t)))
    rr = random.Random(1)
    for _ in range(int(Wd * Hd / 9000)):
        cx, cy = rr.randrange(Wd), rr.randrange(int(Hd * 0.9))
        for k in range(5):
            d.ellipse([cx + k * 14 - 30, cy - 10 - (k % 2) * 6, cx + k * 14 + 10, cy + 12], fill=(245, 248, 252))

    ox, oy = -minx, -miny

    def P(x, y, z):
        sx, sy = scr(x, y, z)
        return (sx + ox, sy + oy)

    swiatla = []
    for (x, y, z) in sorted(bloki, key=lambda k: (k[0] + k[2], k[1], k[0])):
        b = bloki[(x, y, z)]
        seed = x * 73856093 ^ y * 19349663 ^ z * 83492791
        if b in ROSLINY:
            cx, cy = P(x + 0.5, y + 0.35, z + 0.5)
            d.line([(cx, cy + a * 0.3), (cx, cy - a * 0.1)], fill=(60, 120, 40), width=max(1, a // 6))
            r = a * 0.18
            d.ellipse([cx - r, cy - r - a * 0.1, cx + r, cy + r - a * 0.1], fill=ROSLINY[b])
            continue
        c = KOLORY.get(b, (200, 0, 200))
        h = 1.0
        inset = 0.0
        if b in ("smooth_quartz_slab", "polished_blackstone_brick_slab"):
            h = 0.5
        if b == "water":
            h = 0.85
        if b in ("polished_blackstone_wall", "polished_blackstone_brick_wall", "chain"):
            inset = 0.3
        if b in ("lantern", "soul_lantern", "amethyst_cluster", "soul_campfire"):
            inset, h = 0.3, 0.5
            swiatla.append((P(x + 0.5, y + 0.3, z + 0.5), c))
        xa, xb, za, zb = x + inset, x + 1 - inset, z + inset, z + 1 - inset
        top_vis = (x, y + 1, z) not in pelne or h < 1
        right_vis = (x + 1, y, z) not in pelne or inset > 0
        left_vis = (x, y, z + 1) not in pelne or inset > 0
        if top_vis:
            d.polygon([P(xa, y + h, za), P(xb, y + h, za), P(xb, y + h, zb), P(xa, y + h, zb)], fill=shade(c, 1.0, seed))
        if right_vis:
            d.polygon([P(xb, y + h, za), P(xb, y + h, zb), P(xb, y, zb), P(xb, y, za)], fill=shade(c, 0.78, seed + 1))
        if left_vis:
            d.polygon([P(xa, y + h, zb), P(xb, y + h, zb), P(xb, y, zb), P(xa, y, zb)], fill=shade(c, 0.6, seed + 2))

    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for (gx, gy), c in swiatla:
        gd.ellipse([gx - a * 1.4, gy - a * 1.4, gx + a * 1.4, gy + a * 1.4], fill=c + (60,))
    img = Image.alpha_composite(img.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(a * 0.6))).convert("RGB")
    d = ImageDraw.Draw(img)

    # promień beacona
    if x0 <= 0 <= x1 and z0 <= 0 <= z1:
        beam = Image.new("RGBA", img.size, (0, 0, 0, 0))
        bd = ImageDraw.Draw(beam)
        bx, by = P(0.5, 152, 0.5)
        bd.rectangle([bx - a * 0.25, 0, bx + a * 0.25, by], fill=(255, 160, 40, 150))
        img = Image.alpha_composite(img.convert("RGBA"), beam.filter(ImageFilter.GaussianBlur(a * 0.3))).convert("RGB")
        d = ImageDraw.Draw(img)

    # NPC (villagery) i napisy (text_display)
    for typ, x, y, z, tekst, scale in encje:
        if not (x0 <= x <= x1 and z0 <= z <= z1):
            continue
        if typ == "villager":
            for dy, col in [(0, (90, 60, 40)), (1, (120, 85, 60))]:
                X, Y = int(x), int(y) + dy
                d.polygon([P(X + .2, Y + 1, Z := int(z) + .2), P(X + .8, Y + 1, Z), P(X + .8, Y + 1, Z + .6), P(X + .2, Y + 1, Z + .6)], fill=shade(col, 1, 1))
                d.polygon([P(X + .8, Y + 1, Z), P(X + .8, Y + 1, Z + .6), P(X + .8, Y, Z + .6), P(X + .8, Y, Z)], fill=shade(col, .78, 1))
                d.polygon([P(X + .2, Y + 1, Z + .6), P(X + .8, Y + 1, Z + .6), P(X + .8, Y, Z + .6), P(X + .2, Y, Z + .6)], fill=shade(col, .6, 1))
        if typ == "text_display" and tekst:
            linie = [[]]
            for txt, col in tekst:
                parts = txt.split("\n")
                for i, p in enumerate(parts):
                    if i:
                        linie.append([])
                    if p:
                        linie[-1].append((p, col))
            size = max(9, int(a * 0.3 * scale))
            f = ImageFont.truetype(FONT, size)
            cx, cy = P(x, y, z)
            cy -= size * len(linie) * 1.15
            for li in linie:
                w = sum(d.textlength(p, font=f) for p, _ in li)
                xx = cx - w / 2
                for p, col in li:
                    d.text((xx + max(1, size // 10), cy + max(1, size // 10)), p, font=f, fill=(40, 40, 40))
                    d.text((xx, cy), p, font=f, fill=MC.get(col, (255, 255, 255)))
                    xx += d.textlength(p, font=f)
                cy += size * 1.15

    f = ImageFont.truetype(FONT, 26)
    d.rectangle([0, 0, Wd, 44], fill=(20, 16, 30))
    d.text((14, 8), tytul, font=f, fill=(255, 190, 40))
    d.text((Wd - 330, 12), "wizualizacja bloków z paczki", font=ImageFont.truetype(FONT, 16), fill=(170, 170, 170))
    img.save(plik)
    print("zapisano", plik, img.size)


def main():
    OUT.mkdir(exist_ok=True)
    W, encje = wczytaj()
    render(W, encje, 9, (-100, 30, -100, 30), OUT / "1-cala-mapa.png", "DziobMc – cała mapa lobby (Dziob.fun)")
    render(W, encje, 24, (-28, 28, -28, 28), OUT / "2-spawn.png", "DziobMc – spawn: fontanna z beaconem, NPC, portal")
    render(W, encje, 22, (-22, 22, -97, -53), OUT / "3-arena-bossa.png", "DziobMc – arena bossa (Król Dziobów)")


if __name__ == "__main__":
    sys.exit(main())
