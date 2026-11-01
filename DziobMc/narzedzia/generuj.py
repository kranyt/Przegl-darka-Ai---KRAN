#!/usr/bin/env python3
"""Generator paczki serwera DziobMc (serwer Paper 1.21.4, gracze 1.16.4+ przez ViaVersion).

Użycie:  python3 narzedzia/generuj.py
Wynik:   DziobMc/serwer/ (gotowy folder serwera) + DziobMc/POBIERZ/*.zip
"""
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import wspolne  # noqa: E402
import rdzen, komendy, moby, eventy, mapa, serwer, pvp, ziemia_smp  # noqa: E401,E402

ROOT = Path(__file__).resolve().parent.parent
SERWER = ROOT / "WLASNY-SERWER-na-komputerze"
DP = SERWER / "world" / "datapacks" / "DziobMc-Pack"


def lint(files):
    bledy = []
    funkcje = {p[len("data/dziobmc/function/"):-len(".mcfunction")]
               for p in files if p.startswith("data/dziobmc/function/")}
    loot = {p[len("data/dziobmc/loot_table/"):-5] for p in files if p.startswith("data/dziobmc/loot_table/")}
    adv = {p[len("data/dziobmc/advancement/"):-5] for p in files if p.startswith("data/dziobmc/advancement/")}
    obiekty = set()
    for p, txt in files.items():
        for m in re.finditer(r"scoreboard objectives add (\S+) (\S+)", txt):
            obiekty.add(m.group(1))
            if len(m.group(1)) > 16:
                bledy.append(f"za długa nazwa celu: {m.group(1)}")

    makra = {f for f in funkcje if any(ln.startswith("$") for ln in files[f"data/dziobmc/function/{f}.mcfunction"].split("\n"))}
    for p, txt in files.items():
        for m in re.finditer(r"function dziobmc:([a-z0-9_/.]+)( with | \{)?", txt):
            if m.group(1) in makra and not m.group(2):
                bledy.append(f"{p}: makro {m.group(1)} wywołane bez argumentów")
            if m.group(2) and m.group(1) in funkcje and m.group(1) not in makra:
                bledy.append(f"{p}: {m.group(1)} wywołane z argumentami, a nie jest makrem")

    def sprawdz_ref(p, txt):
        for m in re.finditer(r"dziobmc:([a-z0-9_/.]+)", txt):
            ref = m.group(1)
            przed = txt[max(0, m.start() - 40):m.start()]
            if re.search(r"(function |\"function\":\s*\")$", przed):
                if ref not in funkcje:
                    bledy.append(f"{p}: brak funkcji {ref}")
            elif re.search(r"loot $", przed):
                if ref not in loot:
                    bledy.append(f"{p}: brak loot table {ref}")
            elif re.search(r"only $", przed):
                if ref not in adv:
                    bledy.append(f"{p}: brak advancementu {ref}")
            elif re.search(r'DeathLootTable:"$', przed):
                if ref not in loot:
                    bledy.append(f"{p}: brak loot table {ref}")

    for p, txt in files.items():
        if p.endswith(".json") or p.endswith(".mcmeta"):
            try:
                json.loads(txt)
            except Exception as e:  # noqa: BLE001
                bledy.append(f"{p}: zły JSON {e}")
            sprawdz_ref(p, txt)
            continue
        sprawdz_ref(p, txt)
        for nr, line in enumerate(txt.split("\n"), 1):
            if not line or line.startswith("#"):
                continue
            if line.startswith(" "):
                bledy.append(f"{p}:{nr}: wcięcie")
            makro = line.startswith("$")
            if makro and "$(" not in line:
                bledy.append(f"{p}:{nr}: linia makra bez zmiennej $(...)")
            if makro:
                # podstaw przykładowe wartości i sprawdź jak zwykłą linię
                line = re.sub(r"\$\((n\w*)\)", '{"text":"X"}', line[1:])
                line = re.sub(r"\$\(\w+\)", "7", line)
                makro = False
            # nawiasy
            st, q = [], None
            for ch in line:
                if q:
                    if ch == q:
                        q = None
                    continue
                if ch in "\"'":
                    q = ch
                elif ch in "([{":
                    st.append(ch)
                elif ch in ")]}":
                    if not st or "([{"[")]}".index(ch)] != st.pop():
                        bledy.append(f"{p}:{nr}: niezbalansowane nawiasy")
                        break
            if st:
                bledy.append(f"{p}:{nr}: niezamknięte nawiasy")
            # JSON w tellraw/title/bossbar/team prefix/display name
            for pat in [] if makro else [r"tellraw \S+ (.*)$", r"title \S+ (?:title|subtitle|actionbar) (.*)$",
                        r"bossbar set \S+ name (.*)$", r"team modify \S+ prefix (.*)$",
                        r"display name \S+ \S+ (.*)$", r"objectives add \S+ \S+ (.*)$",
                        r"bossbar add \S+ (.*)$", r"numberformat \S+ \S+ styled (.*)$"]:
                m = re.search(pat, line)
                if m:
                    try:
                        json.loads(m.group(1))
                    except Exception as e:  # noqa: BLE001
                        bledy.append(f"{p}:{nr}: zły JSON tekstu: {e}: {m.group(1)[:80]}")
            # SNBT teksty w '...'
            for m in re.finditer(r"(?:CustomName|text|custom_name):'([^']*)'", line):
                try:
                    json.loads(m.group(1))
                except Exception as e:  # noqa: BLE001
                    bledy.append(f"{p}:{nr}: zły JSON w SNBT: {e}")
            # cele scoreboard
            uzyte = []
            uzyte += re.findall(r"scoreboard players (?:set|add|remove|get|enable|reset) \S+ (\S+)", line)
            uzyte += re.findall(r"scoreboard players display (?:name|numberformat) \S+ (\S+)", line)
            m = re.search(r"scoreboard players operation \S+ (\S+) \S+ \S+ (\S+)", line)
            if m:
                uzyte += [m.group(1), m.group(2)]
            for m in re.finditer(r"(?:if|unless) score \S+ (\S+) (?:matches \S+|(?:<|<=|=|>=|>) \S+ (\S+))", line):
                uzyte += [g for g in m.groups() if g]
            uzyte += re.findall(r"store result score \S+ (\S+)", line)
            uzyte += re.findall(r'"objective":"([^"]+)"', line)
            uzyte += re.findall(r"scores=\{([a-z_.0-9]+)=", line)
            for u in uzyte:
                if u not in obiekty:
                    bledy.append(f"{p}:{nr}: nieznany cel scoreboard '{u}'")
    return bledy


def main():
    wspolne.FILES.clear()
    rdzen.build()
    rdzen.build_extra()
    komendy.build()
    moby.build()
    eventy.build()
    mapa.build()
    pvp.build()
    ziemia_smp.build()
    ziemia_smp.build_tick()

    bledy = lint(wspolne.FILES)
    if bledy:
        print("BŁĘDY:")
        for b in bledy:
            print("  " + b)
        sys.exit(1)

    if SERWER.exists():
        shutil.rmtree(SERWER)
    for rel, txt in wspolne.FILES.items():
        p = DP / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt, encoding="utf-8")
    serwer.build(SERWER)

    # ZIP-y
    with zipfile.ZipFile(ROOT / "POBIERZ" / "DziobMc-Serwer.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SERWER.rglob("*")):
            if f.is_file():
                z.write(f, "DziobMc-Serwer/" + str(f.relative_to(SERWER)))
    # Paczka na gotowy hosting: foldery podpisane miejscem docelowym
    NA = ROOT / "NA-HOSTING"
    serwer.build_hosting(NA, DP, SERWER)
    with zipfile.ZipFile(ROOT / "POBIERZ" / "DziobMc-NaHosting.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(NA.rglob("*")):
            if f.is_file():
                z.write(f, "DziobMc-NaHosting/" + str(f.relative_to(NA)))
    with zipfile.ZipFile(ROOT / "POBIERZ" / "DziobMc-Datapack.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(DP.rglob("*")):
            if f.is_file():
                z.write(f, str(f.relative_to(DP)))

    n_fn = sum(1 for p in wspolne.FILES if p.endswith(".mcfunction"))
    n_cmd = sum(len([ln for ln in t.split("\n") if ln and not ln.startswith("#")])
                for p, t in wspolne.FILES.items() if p.endswith(".mcfunction"))
    print(f"OK: {len(wspolne.FILES)} plików, {n_fn} funkcji, {n_cmd} komend.")


if __name__ == "__main__":
    main()
