"""Kaiju – gigantyczne bossy z block display (model) na niewidzialnym ravagerze (hitbox + AI).

Model: lista prostopadłościanów w układzie bossa (x w prawo, y w górę, +z do przodu).
Każda część to block_display teleportowany co tick do bossa z jego obrotem (yaw).
"""
import json
import math
from pathlib import Path

from wspolne import NS, FILES, J, t, sel, sc, tellraw, fn, jfile, firework_cmd, snbt_text
from ziemia_smp import KRAJE, SWIAT

# ------------------------------------------------------------------ narzędzia geometrii


def quat(os_, deg):
    a = math.radians(deg) / 2
    s = math.sin(a)
    x, y, z = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[os_]
    return (x * s, y * s, z * s, math.cos(a))


def qmul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz)


def qrot(q, v):
    x, y, z, w = q
    p = (v[0], v[1], v[2], 0.0)
    qc = (-x, -y, -z, w)
    r = qmul(qmul(q, p), qc)
    return r[:3]


class Model:
    def __init__(self, skala=1.0):
        self.czesci = []
        self.skala = skala

    def b(self, blok, c, s, rot=None, tagi=(), swieci=False):
        """Prostopadłościan o środku c, rozmiarze s, obrocie rot=[(oś, stopnie), ...] wokół środka."""
        k = self.skala
        c = [v * k for v in c]
        s = [v * k for v in s]
        q = (0.0, 0.0, 0.0, 1.0)
        for os_, deg in (rot or []):
            q = qmul(quat(os_, deg), q)
        half = qrot(q, (s[0] / 2, s[1] / 2, s[2] / 2))
        tr = [c[0] - half[0], c[1] - half[1], c[2] - half[2]]
        self.czesci.append({"blok": blok, "t": tr, "s": s, "q": list(q), "tagi": list(tagi), "swieci": swieci, "c": c, "rot": rot or []})
        return self


def f(v):
    return f"{v:.3f}f"


def summon_czesc(cz, tagi_bazowe):
    tagi = ",".join(f'"{x}"' for x in tagi_bazowe + cz["tagi"])
    q = cz["q"]
    nbt = (f'{{Tags:[{tagi}],block_state:{{Name:"minecraft:{cz["blok"]}"}},teleport_duration:2,interpolation_duration:10,'
           f'transformation:{{left_rotation:[{",".join(f(v) for v in q)}],right_rotation:[0f,0f,0f,1f],'
           f'translation:[{",".join(f(v) for v in cz["t"])}],scale:[{",".join(f(v) for v in cz["s"])}]}}')
    if cz["swieci"]:
        nbt += ",brightness:{sky:15,block:15}"
    return f"summon minecraft:block_display ~ ~ ~ {nbt}}}"


def translacja(cz, dx=0.0, dy=0.0, dz=0.0, rot_extra=None):
    """Translacja części po przesunięciu środka o (dx,dy,dz) i ew. dodatkowym obrocie."""
    q = tuple(cz["q"])
    if rot_extra:
        for os_, deg in rot_extra:
            q = qmul(quat(os_, deg), q)
    half = qrot(q, (cz["s"][0] / 2, cz["s"][1] / 2, cz["s"][2] / 2))
    c = cz["c"]
    tr = [c[0] + dx - half[0], c[1] + dy - half[1], c[2] + dz - half[2]]
    return tr, q


# ------------------------------------------------------------------ modele

def dziobzilla():
    m = Model(1.25)
    G, G2, BR, B = "green_terracotta", "green_concrete", "lime_terracotta", "quartz_block"
    for sx in (-1, 1):
        m.b(G, (1.5 * sx, 2.2, -0.3), (1.8, 4.4, 2.2))
        m.b(G, (1.7 * sx, 4.8, -0.5), (2.4, 2.6, 3.0))
        m.b(G2, (1.5 * sx, 0.35, 0.6), (2.2, 0.7, 3.4))
        for dxc in (0.6, 1.4, 2.2):
            m.b("white_concrete", (sx * (0.4 + dxc - 0.4 + 0.4), 0.25, 2.45), (0.35, 0.4, 0.55))
        m.b(G, (2.6 * sx, 11.0, 1.2), (0.9, 2.4, 0.9), [("x", -40)])
        m.b(G, (2.6 * sx, 9.8, 2.6), (0.8, 0.8, 1.9))
        m.b("white_concrete", (2.6 * sx, 9.7, 3.7), (0.7, 0.3, 0.5))
        m.b("shroomlight", (0.95 * sx, 15.8, 4.05), (0.45, 0.35, 0.3), swieci=True)
        m.b(G2, (0.95 * sx, 16.15, 3.9), (0.7, 0.25, 0.6))
    m.b(G, (0, 8.5, 0), (4.6, 7.5, 4.2), [("x", -10)])
    m.b(BR, (0, 8.0, 2.1), (3.4, 6.4, 0.4), [("x", -10)])
    m.b(G, (0, 12.4, 0.8), (3.8, 2.8, 3.6))
    m.b(G, (0, 13.9, 1.6), (2.6, 2.0, 2.6))
    m.b(G2, (0, 15.3, 2.6), (2.6, 2.0, 3.2))
    m.b(G2, (0, 15.0, 4.8), (2.0, 1.4, 1.6))
    m.b(G, (0, 13.9, 3.9), (1.9, 0.6, 2.8), tagi=["dz.szczeka"])
    for dxt in (-0.7, -0.25, 0.25, 0.7):
        m.b("white_concrete", (dxt, 14.2, 5.35), (0.22, 0.35, 0.22))
    ogon = [((0, 6.0, -3.6), (3.2, 3.0, 3.6), 15), ((0, 4.4, -6.8), (2.5, 2.3, 3.4), 10), ((0, 3.0, -9.8), (1.8, 1.7, 3.2), 8),
            ((0, 2.0, -12.6), (1.2, 1.2, 3.0), 5), ((0, 1.4, -15.2), (0.7, 0.7, 2.6), 3)]
    for i, (c, s, r) in enumerate(ogon, 1):
        m.b(G, c, s, [("x", r)], tagi=[f"dz.og{i}"])
    pletwy = [(13.0, -1.0, 1.6), (11.6, -1.9, 2.3), (10.0, -2.4, 2.7), (8.4, -2.7, 2.5), (6.8, -2.9, 2.0)]
    for y, z, h in pletwy:
        m.b(B, (0, y + h * 0.35, z - h * 0.25), (0.3, h, 1.3), [("x", -40)], tagi=["dz.pletwa"])
        m.b(B, (0.55, y + h * 0.2, z - h * 0.1), (0.25, h * 0.6, 0.9), [("x", -40)], tagi=["dz.pletwa"])
        m.b(B, (-0.55, y + h * 0.2, z - h * 0.1), (0.25, h * 0.6, 0.9), [("x", -40)], tagi=["dz.pletwa"])
    for i, (y, z, h) in enumerate([(7.8, -4.0, 1.6), (6.0, -7.0, 1.3), (4.4, -10.0, 1.0), (3.1, -12.8, 0.7)], 1):
        m.b(B, (0, y, z), (0.25, h, 1.0), [("x", -35)], tagi=["dz.pletwa", f"dz.og{i}"])
    return m


def tytan():
    m = Model(1.15)
    P, BI, I, S = "packed_ice", "blue_ice", "ice", "snow_block"
    for sx in (-1, 1):
        m.b(P, (1.4 * sx, 3.0, 0), (1.8, 6.0, 1.8))
        m.b(BI, (1.4 * sx, 0.4, 0.4), (2.2, 0.8, 2.6))
        m.b(BI, (3.4 * sx, 12.4, 0), (2.2, 2.0, 2.4))
        m.b(I, (3.7 * sx, 14.2, 0), (0.6, 2.4, 0.6), [("z", -20 * sx)])
        m.b(P, (3.7 * sx, 9.2, 0.3), (1.6, 5.0, 1.6), [("x", -10)], tagi=[f"dz.reka{'L' if sx < 0 else 'P'}"])
        m.b(BI, (3.7 * sx, 6.3, 0.9), (2.1, 2.1, 2.1), tagi=[f"dz.reka{'L' if sx < 0 else 'P'}"])
        m.b("sea_lantern", (0.55 * sx, 14.45, 1.42), (0.55, 0.3, 0.1), swieci=True)
    m.b(BI, (0, 6.6, 0), (4.2, 1.4, 2.4))
    m.b(P, (0, 10.0, 0), (5.2, 5.6, 3.0))
    m.b(I, (0, 10.8, 1.55), (2.2, 2.2, 0.3), [("z", 45)])
    m.b(S, (0, 14.2, 0.2), (2.4, 2.4, 2.4))
    for dx, h, r in [(-0.9, 1.6, -15), (-0.45, 2.1, -6), (0, 2.5, 0), (0.45, 2.1, 6), (0.9, 1.6, 15)]:
        m.b(I, (dx, 15.6 + h / 2, 0.2), (0.35, h, 0.35), [("z", r)])
    for dx, h, r in [(-1.2, 3.2, -25), (0, 4.0, -5), (1.2, 3.2, 25)]:
        m.b(I, (dx, 12.5, -1.9), (0.7, h, 0.7), [("x", -35), ("z", r)])
    return m


def kolos():
    m = Model(1.6)
    T, O, R = "terracotta", "orange_terracotta", "smooth_red_sandstone"
    m.b(R, (0, 2.4, 2.0), (4.0, 2.0, 3.2))
    m.b(O, (0, 2.3, -1.2), (4.2, 1.8, 1.6))
    m.b(T, (0, 2.2, -2.8), (3.8, 1.7, 1.6))
    m.b(O, (0, 2.1, -4.3), (3.2, 1.6, 1.4))
    for sx in (-1, 1):
        for i in range(4):
            z = 2.2 - i * 1.7
            m.b(T, (3.0 * sx, 2.6, z), (2.4, 0.45, 0.45), [("z", 25 * sx)], tagi=[f"dz.noga{i % 2}"])
            m.b(T, (4.3 * sx, 1.1, z + 0.2), (0.45, 2.4, 0.45), [("z", -15 * sx)], tagi=[f"dz.noga{i % 2}"])
        m.b(R, (2.2 * sx, 2.6, 4.4), (0.7, 0.7, 2.6), [("y", 20 * sx)])
        m.b(O, (2.7 * sx, 2.7, 6.2), (1.5, 1.1, 1.8))
        m.b(T, (2.25 * sx, 2.8, 7.6), (0.35, 0.5, 1.3), [("y", 12 * sx)], tagi=["dz.szczypce"])
        m.b(T, (3.15 * sx, 2.8, 7.6), (0.35, 0.5, 1.3), [("y", -12 * sx)], tagi=["dz.szczypce"])
        m.b("redstone_block", (0.6 * sx, 3.5, 3.62), (0.3, 0.3, 0.15), swieci=True)
    ogon = [((0, 3.2, -5.6), (1.2, 1.2, 1.6), 30), ((0, 4.6, -6.3), (1.1, 1.1, 1.6), 60), ((0, 6.2, -6.2), (1.0, 1.0, 1.6), 100),
            ((0, 7.4, -5.2), (0.9, 0.9, 1.5), 140)]
    for c, s, r in ogon:
        m.b(O, c, s, [("x", -r)], tagi=["dz.ogon"])
    m.b("crying_obsidian", (0, 7.4, -3.8), (0.5, 0.5, 1.4), [("x", -170)], tagi=["dz.ogon"], swieci=True)
    return m


# id, nazwa, kolor, model, hp, obrażenia, skala hitboxa, monety, stolice (id z KRAJE), kolor bossbara
KAIJU = [
    (1, "Dziobzilla", "dark_green", dziobzilla, 2500, 22, 4.0, 3000, [47, 48, 54, 4, 21, 25], "green"),
    (2, "Lodowy Tytan", "aqua", tytan, 2000, 18, 3.6, 2500, [8, 10, 11, 23, 26, 9], "blue"),
    (3, "Pustynny Kolos", "gold", kolos, 1800, 16, 3.4, 2500, [35, 43, 37, 44, 55, 36], "yellow"),
]
KRAJ = {k[0]: k for k in KRAJE}


def build():
    modele = {}
    for kid, nazwa, kol, mf, hp, dmg, skala, monety, stolice, bkol in KAIJU:
        m = mf()
        modele[kid] = m
        tag_b = f"dz.kj{kid}"
        tag_p = f"dz.kp{kid}"
        nazwa_j = t(nazwa.upper(), kol, bold=True)
        # ---------------------------------------------------------- przywołanie
        lines = [f"# Przywołuje kaiju: {nazwa}",
                 f"execute if entity @e[type=ravager,tag={tag_b}] run return run " + tellraw("@a", t(f"✖ {nazwa} już chodzi po świecie!", "red")),
                 f'summon minecraft:ravager ~ ~ ~ {{Tags:["dz.kaiju","{tag_b}","dz.event","dz.ch"],PersistenceRequired:1b,Silent:1b,'
                 f'CustomName:{snbt_text(t(nazwa, kol, bold=True))},DeathLootTable:"{NS}:kaiju/{kid}",'
                 f'active_effects:[{{id:"minecraft:invisibility",amplifier:0b,duration:-1,show_particles:0b}},'
                 f'{{id:"minecraft:fire_resistance",amplifier:0b,duration:-1,show_particles:0b}}]}}',
                 f"execute as @e[type=ravager,tag={tag_b}] run function {NS}:kaiju/atrybuty/{kid}"]
        lines += [summon_czesc(cz, ["dz.kp", tag_p]) for cz in m.czesci]
        lines += [f"bossbar add dziobmc:kaiju{kid} " + J(t(f"☠ {nazwa} ☠", kol, bold=True)),
                  f"bossbar set dziobmc:kaiju{kid} color {bkol}", f"bossbar set dziobmc:kaiju{kid} style notched_20",
                  f"bossbar set dziobmc:kaiju{kid} max {hp}", f"bossbar set dziobmc:kaiju{kid} visible true",
                  "particle minecraft:explosion_emitter ~ ~3 ~ 3 2 3 0 8 force",
                  "execute as @a[distance=..200] at @s run playsound minecraft:entity.ender_dragon.growl hostile @s ~ ~ ~ 1 0.5",
                  "execute as @a[distance=..200] at @s run playsound minecraft:entity.wither.spawn hostile @s ~ ~ ~ 0.6 0.6",
                  "title @a[distance=..200] times 10 60 20",
                  f"title @a[distance=..200] title {J(nazwa_j)}",
                  f"title @a[distance=..200] subtitle {J(t('Gigantyczny potwór nadchodzi!', 'red'))}"]
        fn(f"kaiju/przywolaj/{kid}", "\n".join(lines))
        fn(f"kaiju/przywolaj/{nazwa.split()[0].lower().replace('ó', 'o')}", f"function {NS}:kaiju/przywolaj/{kid}")
        # atrybuty (+ overlay 1.21.2)
        for nowe in (False, True):
            pre = "minecraft:" if nowe else "minecraft:generic."
            txt = "\n".join([f"attribute @s {pre}max_health base set {hp}", f"attribute @s {pre}attack_damage base set {dmg}",
                             f"attribute @s {pre}scale base set {skala}", f"attribute @s {pre}knockback_resistance base set 1.0",
                             f"attribute @s {pre}armor base set 15", f"attribute @s {pre}movement_speed base set 0.26",
                             f"attribute @s {pre}follow_range base set 64", f"data modify entity @s Health set value {hp}.0f"]) + "\n"
            FILES[("ov_1_21_2/" if nowe else "") + f"data/{NS}/function/kaiju/atrybuty/{kid}.mcfunction"] = txt
        # ---------------------------------------------------------- tik (co tick: model podąża za bossem)
        fn(f"kaiju/tik/{kid}", f"tp @e[type=block_display,tag={tag_p},distance=..64] ~ ~ ~ ~ 0")
        # ---------------------------------------------------------- sprzątanie
        fn(f"kaiju/sprzatnij/{kid}", f"""
            execute as @e[type=block_display,tag={tag_p}] at @s run particle minecraft:poof ~ ~2 ~ 1 2 1 0.05 4
            kill @e[type=block_display,tag={tag_p}]
            bossbar set dziobmc:kaiju{kid} visible false
        """)
        # ---------------------------------------------------------- nagroda za zabicie
        jfile(f"data/{NS}/advancement/kaiju/{kid}.json", {
            "criteria": {"zabicie": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"nbt": "{Tags:[\"" + tag_b + "\"]}"}}]}}},
            "rewards": {"function": f"{NS}:kaiju/pokonany/{kid}"}})
        wplata = f"scoreboard players set #v dz.data 2000\nfunction {NS}:kraje/do_skarbca"
        fn(f"kaiju/pokonany/{kid}", f"""
            advancement revoke @s only {NS}:kaiju/{kid}
            scoreboard players set #kaiju_zabity dz.data 1
            title @a times 10 90 20
            title @a title {J(t(f"☠ {nazwa.upper()} POKONANY! ☠", kol, bold=True))}
            title @a subtitle {J([t("Ostatni cios: ", "yellow"), sel("@s")])}
            {tellraw("@a", t("☠ ", "dark_red"), sel("@s"), t(" zadał ostatni cios ", "yellow"), t(nazwa, kol, bold=True), t(f"! +{monety} monet, a skarbiec jego państwa +2000!", "yellow"))}
            scoreboard players set #ile dz.data {monety}
            function {NS}:monety/dodaj
            {wplata}
            execute as @a[distance=..96] unless entity @s[tag=dz.zabojca_kaiju] at @s run function {NS}:kaiju/uczestnik
            execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 0.8
            {firework_cmd("~ ~2 ~", (16711680, 16766720))}
            {firework_cmd("~3 ~2 ~", (65280, 16777215))}
            {firework_cmd("~-3 ~2 ~", (255, 16766720))}
        """)
        # ---------------------------------------------------------- loot
        jfile(f"data/{NS}/loot_table/kaiju/{kid}.json", {"type": "minecraft:entity", "pools": [
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": "minecraft:netherite_ingot",
                                      "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 2, "max": 4}}]}]},
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": "minecraft:diamond_block",
                                      "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 2, "max": 5}}]}]},
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": "minecraft:enchanted_golden_apple",
                                      "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 2, "max": 3}}]}]},
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": {1: "minecraft:prismarine_shard", 2: "minecraft:blue_ice", 3: "minecraft:blaze_rod"}[kid],
                                      "functions": [{"function": "minecraft:set_count", "count": 3},
                                                    {"function": "minecraft:set_name", "name": t({1: "Łuska Dziobzilli", 2: "Serce Tytana", 3: "Żądło Kolosa"}[kid], kol, italic=False, bold=True)},
                                                    {"function": "minecraft:set_enchantments", "enchantments": {"minecraft:unbreaking": 1}}]}]},
            {"rolls": 1, "entries": [{"type": "minecraft:item", "name": "minecraft:totem_of_undying"}]},
        ]})
    fn("kaiju/uczestnik", f"""
        scoreboard players set #ile dz.data 500
        {tellraw("@s", t("☠ Nagroda za udział w walce z kaiju:", "gold"))}
        function {NS}:monety/dodaj
    """)

    # ------------------------------------------------------------------ pętle
    fn("kaiju/tick", "\n".join(f"execute as @e[type=ravager,tag=dz.kj{k[0]}] at @s run function {NS}:kaiju/tik/{k[0]}" for k in KAIJU))
    sek = []
    for k in KAIJU:
        kid = k[0]
        sek.append(f"execute as @e[type=ravager,tag=dz.kj{kid}] at @s run function {NS}:kaiju/sekunda/{kid}")
        sek.append(f"execute unless entity @e[type=ravager,tag=dz.kj{kid}] if entity @e[type=block_display,tag=dz.kp{kid}] run function {NS}:kaiju/sprzatnij/{kid}")
    fn("kaiju/sekunda", "\n".join(sek))

    # wspólne dla każdego kaiju co sekundę
    def wspolne(kid, hp):
        return f"""
            scoreboard players add @s dz.kc 1
            execute store result bossbar dziobmc:kaiju{kid} value run data get entity @s Health
            bossbar set dziobmc:kaiju{kid} players @a[distance=..120]
            effect give @s minecraft:invisibility infinite 0 true
            scoreboard players operation #t dz.data = @s dz.kc
        """

    # --- Dziobzilla
    m = modele[1]
    og = [cz for cz in m.czesci if any(x.startswith("dz.og") for x in cz["tagi"])]
    anim = {}
    for strona, znak in (("L", -1), ("P", 1)):
        out = []
        for cz in og:
            nr = int([x for x in cz["tagi"] if x.startswith("dz.og")][0][5:])
            tr, q = translacja(cz, dx=znak * 0.35 * nr * m.skala)
            extra = [x for x in cz["tagi"] if x.startswith("dz.og")][0]
            pl = "dz.pletwa" in cz["tagi"]
            sel_ = f"@e[type=block_display,tag=dz.kp1,tag={extra},{'tag=dz.pletwa' if pl else 'tag=!dz.pletwa'},distance=..64,limit=1]"
            out.append(f"data merge entity {sel_} {{start_interpolation:0,interpolation_duration:20,transformation:{{translation:[{','.join(f(v) for v in tr)}]}}}}")
        anim[strona] = out
    fn("kaiju/anim/1l", "\n".join(anim["L"]))
    fn("kaiju/anim/1p", "\n".join(anim["P"]))
    szcz = [cz for cz in m.czesci if "dz.szczeka" in cz["tagi"]][0]
    tr_o, q_o = translacja(szcz, dy=-0.5 * m.skala, dz=0.3 * m.skala, rot_extra=[("x", 25)])
    tr_z, q_z = translacja(szcz)
    fn("kaiju/szczeka/otworz", f"data merge entity @e[type=block_display,tag=dz.kp1,tag=dz.szczeka,distance=..64,limit=1] {{start_interpolation:0,interpolation_duration:8,transformation:{{translation:[{','.join(f(v) for v in tr_o)}],left_rotation:[{','.join(f(v) for v in q_o)}]}}}}")
    fn("kaiju/szczeka/zamknij", f"data merge entity @e[type=block_display,tag=dz.kp1,tag=dz.szczeka,distance=..64,limit=1] {{start_interpolation:0,interpolation_duration:8,transformation:{{translation:[{','.join(f(v) for v in tr_z)}],left_rotation:[{','.join(f(v) for v in q_z)}]}}}}")
    fn("kaiju/sekunda/1", wspolne(1, 2500) + f"""
        scoreboard players operation #t dz.data %= #2 dz.data
        execute if score #t dz.data matches 0 run function {NS}:kaiju/anim/1l
        execute if score #t dz.data matches 1 run function {NS}:kaiju/anim/1p
        scoreboard players operation #t dz.data = @s dz.kc
        scoreboard players operation #t dz.data %= #12 dz.data
        execute if score #t dz.data matches 10 run function {NS}:kaiju/dziobzilla/ladowanie
        execute if score #t dz.data matches 0 run function {NS}:kaiju/dziobzilla/oddech
        scoreboard players operation #t dz.data = @s dz.kc
        scoreboard players operation #t dz.data %= #8 dz.data
        execute if score #t dz.data matches 4 run function {NS}:kaiju/tupniecie
        scoreboard players operation #t dz.data = @s dz.kc
        scoreboard players operation #t dz.data %= #6 dz.data
        execute if score #t dz.data matches 2 positioned ^ ^ ^-10 as @a[distance=..7,gamemode=!creative,gamemode=!spectator] run function {NS}:kaiju/dziobzilla/ogon
        execute if score #t dz.data matches 2 positioned ^ ^2 ^-10 run particle minecraft:sweep_attack ~ ~ ~ 3 1 3 0 12
        execute store result score #hp dz.data run data get entity @s Health
        execute if score #hp dz.data matches ..1250 unless entity @s[tag=dz.szal] run function {NS}:kaiju/szal
    """)
    fn("kaiju/dziobzilla/ladowanie", f"""
        execute as @e[type=block_display,tag=dz.kp1,tag=dz.pletwa,distance=..64] run data merge entity @s {{block_state:{{Name:"minecraft:sea_lantern"}},brightness:{{sky:15,block:15}},Glowing:1b}}
        playsound minecraft:block.beacon.power_select hostile @a[distance=..80] ~ ~ ~ 2 0.5
        particle minecraft:electric_spark ~ ~12 ~ 2 4 2 0.2 80 force
    """)
    fn("kaiju/dziobzilla/oddech", f"""
        function {NS}:kaiju/szczeka/otworz
        playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..120] ~ ~ ~ 3 0.6
        scoreboard players set #krok dz.data 0
        execute positioned ^ ^17.5 ^6 facing entity @p[distance=..60,gamemode=!spectator,gamemode=!creative] feet run function {NS}:kaiju/dziobzilla/promien
        schedule function {NS}:kaiju/dziobzilla/po_oddechu 30t replace
    """)
    fn("kaiju/dziobzilla/promien", f"""
        scoreboard players add #krok dz.data 1
        particle minecraft:soul_fire_flame ~ ~ ~ 0.3 0.3 0.3 0.02 6 force
        particle minecraft:electric_spark ~ ~ ~ 0.4 0.4 0.4 0.1 4 force
        particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.02 2 force
        execute as @a[distance=..2.5,gamemode=!creative,gamemode=!spectator] run damage @s 14 minecraft:mob_attack by @e[type=ravager,tag=dz.kj1,limit=1,sort=nearest]
        execute as @a[distance=..2.5,gamemode=!creative,gamemode=!spectator] run effect give @s minecraft:wither 4 1
        execute if score #krok dz.data matches ..60 positioned ^ ^ ^1 run function {NS}:kaiju/dziobzilla/promien
    """)
    fn("kaiju/dziobzilla/po_oddechu", f"""
        execute as @e[type=block_display,tag=dz.kp1,tag=dz.pletwa] run data merge entity @s {{block_state:{{Name:"minecraft:quartz_block"}},Glowing:0b}}
        execute as @e[type=ravager,tag=dz.kj1] at @s run function {NS}:kaiju/szczeka/zamknij
    """)
    fn("kaiju/dziobzilla/ogon", """
        damage @s 12 minecraft:mob_attack by @e[type=ravager,tag=dz.kj1,limit=1,sort=nearest]
        effect give @s minecraft:levitation 1 6 true
    """)
    fn("kaiju/tupniecie", """
        particle minecraft:explosion_emitter ~ ~ ~ 4 0 4 0 4 force
        particle minecraft:campfire_cosy_smoke ~ ~0.5 ~ 6 0.2 6 0.02 60 force
        playsound minecraft:entity.generic.explode hostile @a[distance=..80] ~ ~ ~ 2 0.5
        playsound minecraft:entity.ravager.stunned hostile @a[distance=..80] ~ ~ ~ 2 0.5
        execute as @a[distance=..10,gamemode=!creative,gamemode=!spectator] run damage @s 10 minecraft:mob_attack by @e[type=ravager,tag=dz.kaiju,limit=1,sort=nearest]
        effect give @a[distance=..10,gamemode=!creative,gamemode=!spectator] minecraft:levitation 1 8 true
        effect give @a[distance=..14,gamemode=!creative,gamemode=!spectator] minecraft:slowness 3 2
    """)
    fn("kaiju/szal", f"""
        tag @s add dz.szal
        effect give @s minecraft:strength infinite 1
        effect give @s minecraft:speed infinite 1
        title @a[distance=..120] times 5 40 10
        title @a[distance=..120] title {J(t("POTWÓR WPADA W SZAŁ!", "dark_red", bold=True))}
        execute as @a[distance=..120] at @s run playsound minecraft:entity.ender_dragon.growl hostile @s ~ ~ ~ 1 0.6
        summon minecraft:husk ~3 ~ ~ {{Tags:["dz.nowy","dz.minion","dz.event"],IsBaby:0b}}
        summon minecraft:husk ~-3 ~ ~ {{Tags:["dz.nowy","dz.minion","dz.event"],IsBaby:0b}}
        execute as @e[tag=dz.nowy] run function {NS}:moby/ustaw/ognisty
    """)

    # --- Lodowy Tytan
    fn("kaiju/sekunda/2", wspolne(2, 2000) + f"""
        effect give @a[distance=..14,gamemode=!creative,gamemode=!spectator] minecraft:slowness 2 1 true
        effect give @a[distance=..14,gamemode=!creative,gamemode=!spectator] minecraft:mining_fatigue 2 1 true
        particle minecraft:snowflake ~ ~8 ~ 8 6 8 0.02 80 force
        scoreboard players operation #t dz.data %= #10 dz.data
        execute if score #t dz.data matches 0 as @a[distance=..35,gamemode=!creative,gamemode=!spectator,sort=random,limit=4] at @s run function {NS}:kaiju/tytan/lod
        scoreboard players operation #t dz.data = @s dz.kc
        scoreboard players operation #t dz.data %= #7 dz.data
        execute if score #t dz.data matches 3 run function {NS}:kaiju/tytan/piesci
        execute store result score #hp dz.data run data get entity @s Health
        execute if score #hp dz.data matches ..1000 unless entity @s[tag=dz.szal] run function {NS}:kaiju/szal
    """)
    fn("kaiju/tytan/lod", """
        summon minecraft:falling_block ~ ~14 ~ {BlockState:{Name:"minecraft:packed_ice"},Time:1,HurtEntities:1b,FallHurtMax:16,FallHurtAmount:3.0f,DropItem:0b,CancelDrop:1b}
        particle minecraft:snowflake ~ ~12 ~ 0.5 1 0.5 0.05 30 force
        playsound minecraft:block.glass.break hostile @a[distance=..40] ~ ~ ~ 1 0.6
    """)
    fn("kaiju/tytan/piesci", f"""
        execute as @e[type=block_display,tag=dz.kp2,tag=dz.rekaP,distance=..64] run data merge entity @s {{start_interpolation:0,interpolation_duration:6}}
        function {NS}:kaiju/tupniecie
        particle minecraft:item_snowball ~ ~1 ~ 6 0.5 6 0.2 120 force
        effect give @a[distance=..10,gamemode=!creative,gamemode=!spectator] minecraft:slowness 5 4
    """)

    # --- Pustynny Kolos
    fn("kaiju/sekunda/3", wspolne(3, 1800) + f"""
        scoreboard players operation #t dz.data %= #6 dz.data
        execute if score #t dz.data matches 0 as @p[distance=..14,gamemode=!creative,gamemode=!spectator] run function {NS}:kaiju/kolos/zadlo
        scoreboard players operation #t dz.data = @s dz.kc
        scoreboard players operation #t dz.data %= #10 dz.data
        execute if score #t dz.data matches 5 run function {NS}:kaiju/kolos/burza
        scoreboard players operation #t dz.data = @s dz.kc
        scoreboard players operation #t dz.data %= #15 dz.data
        execute if score #t dz.data matches 8 run function {NS}:kaiju/kolos/skorpionki
        execute store result score #hp dz.data run data get entity @s Health
        execute if score #hp dz.data matches ..900 unless entity @s[tag=dz.szal] run function {NS}:kaiju/szal
    """)
    fn("kaiju/kolos/zadlo", """
        damage @s 12 minecraft:mob_attack by @e[type=ravager,tag=dz.kj3,limit=1,sort=nearest]
        effect give @s minecraft:poison 8 2
        execute at @s run particle minecraft:witch ~ ~1 ~ 0.4 0.6 0.4 0.1 30
        execute at @s run playsound minecraft:entity.bee.sting hostile @a[distance=..30] ~ ~ ~ 2 0.5
    """)
    fn("kaiju/kolos/burza", """
        particle minecraft:falling_dust{block_state:{Name:"minecraft:sand"}} ~ ~6 ~ 12 5 12 0 400 force
        particle minecraft:campfire_cosy_smoke ~ ~2 ~ 10 2 10 0.02 60 force
        playsound minecraft:weather.rain.above hostile @a[distance=..60] ~ ~ ~ 2 0.5
        effect give @a[distance=..22,gamemode=!creative,gamemode=!spectator] minecraft:blindness 4 0
        effect give @a[distance=..22,gamemode=!creative,gamemode=!spectator] minecraft:slowness 4 1
    """)
    fn("kaiju/kolos/skorpionki", f"""
        execute store result score #ile_sl dz.data if entity @e[type=cave_spider,tag=dz.minion,distance=..40]
        execute if score #ile_sl dz.data matches 6.. run return 0
        summon minecraft:cave_spider ~2 ~ ~2 {{Tags:["dz.minion","dz.event"],CustomName:{snbt_text(t("Skorpionek", "gold"))}}}
        summon minecraft:cave_spider ~-2 ~ ~2 {{Tags:["dz.minion","dz.event"],CustomName:{snbt_text(t("Skorpionek", "gold"))}}}
        summon minecraft:cave_spider ~ ~ ~-3 {{Tags:["dz.minion","dz.event"],CustomName:{snbt_text(t("Skorpionek", "gold"))}}}
    """)

    # ------------------------------------------------------------------ event "Atak Kaiju"
    ataki = []
    for kid, nazwa, kol, *_r in KAIJU:
        for sid in _r[5]:
            k = KRAJ[sid]
            ataki.append((kid, nazwa, kol, k))
    los = [f"execute store result score #los dz.data run random value 1..{len(ataki)}"]
    for n, (kid, nazwa, kol, k) in enumerate(ataki, 1):
        los.append(f"execute if score #los dz.data matches {n} run function {NS}:kaiju/atak/{n}")
        fn(f"kaiju/atak/{n}", f"""
            scoreboard players set #kaiju_typ dz.data {kid}
            scoreboard players set #kaiju_jest dz.data 0
            scoreboard players set #kaiju_zabity dz.data 0
            data modify storage dziobmc:tmp ka set from storage dziobmc:kraje s.k{k[0]}
            function {NS}:kaiju/forceload_m with storage dziobmc:tmp ka
            schedule function {NS}:kaiju/atak_spawn 60t replace
            {tellraw("@a", t("⚠ ", "dark_red", bold=True), t(nazwa.upper(), kol, bold=True), t(" atakuje stolicę ", "red"), t(k[4], k[3], bold=True), t(" (", "gray"), t(k[1], k[3]), t(")! ", "gray"),
                     t("[LEĆ DO WALKI]", "green", bold=True, run=f"/trigger stolica set {100 + k[0]}", hover=t("Teleport do stolicy")))}
            title @a times 10 70 20
            title @a title {J(t(f"⚠ {nazwa.upper()} ⚠", kol, bold=True))}
            title @a subtitle {J([t("atakuje ", "red"), t(k[4], k[3], bold=True), t("!", "red")])}
            execute as @a at @s run playsound minecraft:event.raid.horn master @s ~ ~ ~ 1 0.6
        """)
    fn("kaiju/losuj_atak", "\n".join(los))
    fn("kaiju/forceload_m", f"""
        $execute in {SWIAT} run forceload add $(x) $(z)
    """)
    fn("kaiju/forceload_usun_m", f"""
        $execute in {SWIAT} run forceload remove $(x) $(z)
    """)
    fn("kaiju/atak_spawn", f"""
        execute unless score #event dz.data matches 8 run return 0
        function {NS}:kaiju/atak_spawn_m with storage dziobmc:tmp ka
        execute as @e[type=marker,tag=dz.kpkt] at @s if score #kaiju_typ dz.data matches 1 run function {NS}:kaiju/przywolaj/1
        execute as @e[type=marker,tag=dz.kpkt] at @s if score #kaiju_typ dz.data matches 2 run function {NS}:kaiju/przywolaj/2
        execute as @e[type=marker,tag=dz.kpkt] at @s if score #kaiju_typ dz.data matches 3 run function {NS}:kaiju/przywolaj/3
        kill @e[type=marker,tag=dz.kpkt]
        execute if entity @e[type=ravager,tag=dz.kaiju] run scoreboard players set #kaiju_jest dz.data 1
        execute unless entity @e[type=ravager,tag=dz.kaiju] run schedule function {NS}:kaiju/atak_spawn 40t replace
    """)
    fn("kaiju/atak_spawn_m", f"""
        $execute in {SWIAT} run summon minecraft:marker $(x) 140 $(z) {{Tags:["dz.kpkt"]}}
        $execute in {SWIAT} run spreadplayers $(x) $(z) 0 40 false @e[type=marker,tag=dz.kpkt]
    """)
    fn("event/kaiju/start", f"function {NS}:kaiju/losuj_atak")
    fn("event/kaiju/tik", f"""
        execute if score #kaiju_jest dz.data matches 1 unless entity @e[type=ravager,tag=dz.kaiju] if score #kaiju_zabity dz.data matches 1 run function {NS}:event/koniec
    """)
    fn("event/kaiju/koniec", f"""
        execute unless score #kaiju_zabity dz.data matches 1 if entity @e[type=ravager,tag=dz.kaiju] run {tellraw("@a", t("☠ Potwór odchodzi w głąb lądu... Tym razem przetrwał.", "gray"))}
        execute as @e[type=ravager,tag=dz.kaiju] at @s run function {NS}:util/usun
        function {NS}:kaiju/forceload_usun_m with storage dziobmc:tmp ka
        scoreboard players set #kaiju_jest dz.data 0
    """)

    # ------------------------------------------------------------------ eksport modeli dla renderu 3D
    out = {kid: [{"blok": c["blok"], "t": c["t"], "s": c["s"], "q": c["q"], "swieci": c["swieci"]} for c in m.czesci] for kid, m in modele.items()}
    Path(__file__).resolve().parent.joinpath("render3d", "kaiju_modele.json").write_text(json.dumps(out), encoding="utf-8")
