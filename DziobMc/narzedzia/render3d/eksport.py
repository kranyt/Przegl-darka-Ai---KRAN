#!/usr/bin/env python3
"""Eksportuje bloki i encje z wygenerowanych komend paczki do scena.json
(dla renderu 3D w render3d.html)."""
import json
import math
import random
import re
import sys
from pathlib import Path

TU = Path(__file__).resolve().parent
ROOT = TU.parent.parent
FN = ROOT / "WLASNY-SERWER-na-komputerze/world/datapacks/DziobMc-Pack/data/dziobmc/function/mapa"
ETAPY = ["etap/wyspa", "etap/plac", "etap/arena", "etap/parkour", "etap/arena_pvp", "dekoracje"]


def drzewo(W, typ, x, y, z, rr):
    h = 6 if typ == "cherry" else 7
    lisc = "cherry_leaves" if typ == "cherry" else "oak_leaves"
    pien = "cherry_log" if typ == "cherry" else "oak_log"
    for dy in range(h):
        W[(x, y + dy, z)] = pien
    r = 3.6 if typ == "cherry" else 3.0
    for dx in range(-4, 5):
        for dz in range(-4, 5):
            for dy in range(-2, 3):
                if (dx * dx + dz * dz) / (r * r) + (dy * dy) / 4.5 <= 1 and rr.random() > 0.1:
                    W.setdefault((x + dx, y + h - 1 + dy, z + dz), lisc)


def main():
    W, enc = {}, []
    rr = random.Random(5)
    for e in ETAPY:
        for ln in (FN / f"{e}.mcfunction").read_text(encoding="utf-8").splitlines():
            m = re.match(r"fill (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) minecraft:(\w+)(\[[^\]]*\])?", ln)
            if m:
                a = list(map(int, m.groups()[:6]))
                b = m.group(7) + (m.group(8) or "")
                for x in range(min(a[0], a[3]), max(a[0], a[3]) + 1):
                    for y in range(min(a[1], a[4]), max(a[1], a[4]) + 1):
                        for z in range(min(a[2], a[5]), max(a[2], a[5]) + 1):
                            if b == "air":
                                W.pop((x, y, z), None)
                            else:
                                W[(x, y, z)] = b
                continue
            m = re.match(r"setblock (-?\d+) (-?\d+) (-?\d+) minecraft:(\w+)(\[[^\]]*\])?", ln)
            if m:
                W[tuple(map(int, m.groups()[:3]))] = m.group(4) + (m.group(5) or "")
                continue
            m = re.match(r"place feature minecraft:(\w+) (-?\d+) (-?\d+) (-?\d+)", ln)
            if m:
                drzewo(W, m.group(1), *map(int, m.groups()[1:]), rr)
                continue
            m = re.match(r"summon minecraft:(\w+) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (.*)$", ln)
            if m:
                typ = m.group(1)
                x, y, z = map(float, m.groups()[1:4])
                d = {"typ": typ, "x": x, "y": y, "z": z}
                tm = re.search(r"text:'(.*?)',transformation", m.group(5))
                if tm:
                    comp = json.loads(tm.group(1))
                    d["tekst"] = comp if isinstance(comp, list) else [comp]
                    d["skala"] = float(re.search(r"scale:\[([\d.]+)f", m.group(5)).group(1))
                rot = re.search(r"Rotation:\[(-?[\d.]+)f", m.group(5))
                if rot:
                    d["yaw"] = float(rot.group(1))
                prof = re.search(r'profession:"minecraft:(\w+)"', m.group(5))
                if prof:
                    d["prof"] = prof.group(1)
                if typ in ("text_display", "villager"):
                    enc.append(d)
    typy = sorted(set(W.values()))
    idx = {t: i for i, t in enumerate(typy)}
    bloki = [[x, y, z, idx[b]] for (x, y, z), b in W.items()]
    out = TU / "scena.json"
    out.write_text(json.dumps({"typy": typy, "bloki": bloki, "encje": enc}), encoding="utf-8")
    print("bloki:", len(bloki), "typy:", len(typy), "encje:", len(enc), "->", out)


if __name__ == "__main__":
    sys.exit(main())
