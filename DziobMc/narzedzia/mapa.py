"""Mapa: latająca wyspa-lobby, fontanna z beaconem, NPC, arena bossa, parkour, portal RTP."""
import math
import random
from wspolne import NS, SPAWN, J, t, snbt_text, tellraw, fn, jfile

R = random.Random(2024)  # stałe ziarno = zawsze ta sama mapa
Y = 150                  # poziom podłogi lobby

# ------------------------------------------------------------------ geometria


def spans(pred, cx, cz, rmax, y, block):
    """Wypełnia wiersze (fill) wszędzie, gdzie pred(dx,dz) jest prawdą."""
    out = []
    for dz in range(-rmax, rmax + 1):
        run = None
        for dx in range(-rmax, rmax + 2):
            ok = dx <= rmax and pred(dx, dz)
            if ok and run is None:
                run = dx
            if not ok and run is not None:
                x1, x2 = cx + run, cx + dx - 1
                z = cz + dz
                if x1 == x2:
                    out.append(f"setblock {x1} {y} {z} {block}")
                else:
                    out.append(f"fill {x1} {y} {z} {x2} {y} {z} {block}")
                run = None
    return out


def dist(dx, dz):
    return math.hypot(dx, dz)


def wyspa_spod(cx, cz, r_top, y_top, glebokosc, materialy, krawedz, seed):
    """Spód latającej wyspy – zwężający się, poszarpany stożek."""
    rr = random.Random(seed)
    out = []
    f1, f2 = rr.uniform(0, 6), rr.uniform(0, 6)
    for i in range(1, glebokosc + 1):
        y = y_top - i
        frac = 1 - i / (glebokosc + 1)
        base = r_top * (frac ** 0.55)

        def promien(dx, dz, base=base, y=y):
            a = math.atan2(dz, dx)
            p = base * (1 + 0.13 * math.sin(3 * a + f1 + y * 0.45) + 0.08 * math.sin(5 * a + f2))
            return min(p, r_top - 0.4 - (y_top - y) * 0.35)
        rmax = int(r_top * 1.25) + 1
        mat = materialy[min(len(materialy) - 1, i - 1)]
        out += spans(lambda dx, dz: dist(dx, dz) <= promien(dx, dz), cx, cz, rmax, y, mat)
        # krawędź – losowe bloki dla urozmaicenia
        for dz in range(-rmax, rmax + 1):
            for dx in range(-rmax, rmax + 1):
                d = dist(dx, dz)
                p = promien(dx, dz)
                if p - 1.2 < d <= p and rr.random() < 0.45:
                    out.append(f"setblock {cx + dx} {y} {cz + dz} {rr.choice(krawedz)}")
    return out


def yaw_do(x, z, tx, tz):
    return round(math.degrees(math.atan2(-(tx - x), tz - z)), 1)


def text_display(x, y, z, comp, tag, scale=1.0, bg=0):
    return (f"summon minecraft:text_display {x} {y} {z} {{Tags:[\"dz.map\",\"{tag}\"],"
            f"billboard:\"center\",alignment:\"center\",shadow:1b,line_width:400,background:{bg},"
            f"text:{snbt_text(comp)},"
            f"transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],"
            f"translation:[0f,0f,0f],scale:[{scale}f,{scale}f,{scale}f]}}}}")


# ------------------------------------------------------------------ elementy


def wyspa():
    out = ["# === Latająca wyspa lobby (środek 0 150 0, promień 26) ==="]
    out += spans(lambda dx, dz: dist(dx, dz) <= 26.3, 0, 0, 27, Y, "minecraft:grass_block")
    mats = ["minecraft:dirt"] * 3 + ["minecraft:stone"] * 30
    kraw = ["minecraft:andesite", "minecraft:cobblestone", "minecraft:tuff", "minecraft:moss_block",
            "minecraft:coal_ore", "minecraft:iron_ore", "minecraft:gold_ore", "minecraft:mossy_cobblestone",
            "minecraft:amethyst_block"]
    out += wyspa_spod(0, 0, 26, Y, 24, mats, kraw, 11)
    return out


def plac():
    out = ["# === Plac główny ==="]
    out += spans(lambda dx, dz: dist(dx, dz) <= 13.5, 0, 0, 14, Y, "minecraft:smooth_quartz")
    out += spans(lambda dx, dz: 12.5 < dist(dx, dz) <= 13.5, 0, 0, 14, Y, "minecraft:polished_deepslate")
    out += spans(lambda dx, dz: 11.5 < dist(dx, dz) <= 12.5, 0, 0, 13, Y, "minecraft:gold_block")
    out += spans(lambda dx, dz: 7.5 < dist(dx, dz) <= 8.3, 0, 0, 9, Y, "minecraft:orange_glazed_terracotta")
    # 8 promieni
    for dz in range(-11, 12):
        for dx in range(-11, 12):
            d = dist(dx, dz)
            if 5 <= d <= 11:
                a = math.degrees(math.atan2(dz, dx)) % 45
                if min(a, 45 - a) * math.pi / 180 * d < 0.55:
                    out.append(f"setblock {dx} {Y} {dz} minecraft:yellow_concrete")
    # ścieżki (N ciemna -> arena, S/E/W kwarcowe)
    out += [f"fill -1 {Y} -26 1 {Y} -13 minecraft:polished_blackstone_bricks",
            f"fill 0 {Y} -26 0 {Y} -14 minecraft:gilded_blackstone",
            f"fill -1 {Y} 13 1 {Y} 26 minecraft:quartz_bricks",
            f"fill 13 {Y} -1 26 {Y} 1 minecraft:quartz_bricks",
            f"fill -26 {Y} -1 -13 {Y} 1 minecraft:quartz_bricks",
            f"fill -1 {Y} 17 1 {Y} 19 minecraft:chiseled_quartz_block"]
    # fontanna z beaconem
    out += spans(lambda dx, dz: dist(dx, dz) <= 4.5, 0, 0, 5, Y, "minecraft:prismarine_bricks")
    out.append(f"fill -1 {Y} -1 1 {Y} 1 minecraft:iron_block")
    out += spans(lambda dx, dz: 3.4 < dist(dx, dz) <= 4.5, 0, 0, 5, Y + 1, "minecraft:smooth_quartz_slab[type=bottom]")
    out += spans(lambda dx, dz: dist(dx, dz) <= 3.4, 0, 0, 4, Y + 1, "minecraft:water")
    out += [f"setblock 0 {Y + 1} 0 minecraft:beacon",
            f"setblock 0 {Y + 2} 0 minecraft:orange_stained_glass"]
    # latarnie
    for x, z in [(6, 6), (-6, 6), (6, -6), (-6, -6), (3, 16), (-3, 16), (16, 3), (16, -3), (-16, 3), (-16, -3), (3, -16), (-3, -16)]:
        out += [f"fill {x} {Y + 1} {z} {x} {Y + 3} {z} minecraft:polished_blackstone_wall",
                f"setblock {x} {Y + 4} {z} minecraft:lantern"]
    # podesty NPC
    for x, z in [(10, -10), (10, 10), (-10, 10), (-10, -10)]:
        out += [f"fill {x - 1} {Y} {z - 1} {x + 1} {Y} {z + 1} minecraft:chiseled_quartz_block",
                f"setblock {x} {Y} {z} minecraft:gold_block"]
    # roślinność
    zakazane = lambda dx, dz: (abs(dx) <= 2 or abs(dz) <= 2 or dist(dx, dz) <= 14.5 or
                               any(abs(dx - nx) <= 2 and abs(dz - nz) <= 2 for nx, nz in [(10, -10), (10, 10), (-10, 10), (-10, -10)]))
    kwiaty = ["short_grass"] * 8 + ["poppy", "dandelion", "cornflower", "oxeye_daisy", "azure_bluet", "allium", "lily_of_the_valley"]
    for dz in range(-25, 26):
        for dx in range(-25, 26):
            if dist(dx, dz) <= 25 and not zakazane(dx, dz) and R.random() < 0.18:
                out.append(f"setblock {dx} {Y + 1} {dz} minecraft:{R.choice(kwiaty)}")
    # drzewa
    for i, kat in enumerate([30, 60, 120, 150, 210, 240, 300, 330]):
        a = math.radians(kat)
        x, z = round(20.5 * math.cos(a)), round(20.5 * math.sin(a))
        feat = "minecraft:cherry" if i % 2 == 0 else "minecraft:fancy_oak"
        out += [f"fill {x} {Y + 1} {z} {x} {Y + 6} {z} minecraft:air", f"place feature {feat} {x} {Y + 1} {z}"]
    # portal RTP (wschód, x=20)
    out += [f"fill 20 {Y} -3 20 {Y} 3 minecraft:obsidian",
            f"fill 20 {Y + 1} -3 20 {Y + 6} -3 minecraft:crying_obsidian",
            f"fill 20 {Y + 1} 3 20 {Y + 6} 3 minecraft:crying_obsidian",
            f"fill 20 {Y + 6} -3 20 {Y + 6} 3 minecraft:crying_obsidian",
            f"fill 20 {Y + 1} -2 20 {Y + 5} 2 minecraft:air",
            f"setblock 20 {Y + 7} 0 minecraft:amethyst_cluster",
            f"setblock 20 {Y + 1} -4 minecraft:amethyst_block", f"setblock 20 {Y + 1} 4 minecraft:amethyst_block",
            f"setblock 20 {Y + 2} -4 minecraft:amethyst_cluster", f"setblock 20 {Y + 2} 4 minecraft:amethyst_cluster"]
    return out


def most_i_arena():
    out = ["# === Most na arenę ==="]
    out += [f"fill -1 {Y} -54 1 {Y} -27 minecraft:polished_blackstone_bricks",
            f"fill 0 {Y} -54 0 {Y} -27 minecraft:gilded_blackstone",
            f"fill -2 {Y} -54 -2 {Y} -27 minecraft:polished_blackstone",
            f"fill 2 {Y} -54 2 {Y} -27 minecraft:polished_blackstone",
            f"fill -2 {Y + 1} -54 -2 {Y + 1} -27 minecraft:polished_blackstone_wall",
            f"fill 2 {Y + 1} -54 2 {Y + 1} -27 minecraft:polished_blackstone_wall",
            f"fill -1 {Y - 1} -54 1 {Y - 1} -27 minecraft:polished_blackstone_brick_slab[type=top]"]
    for z in range(-29, -54, -6):
        out += [f"setblock -2 {Y + 2} {z} minecraft:soul_lantern", f"setblock 2 {Y + 2} {z} minecraft:soul_lantern",
                f"setblock -1 {Y - 1} {z} minecraft:chain", f"setblock 1 {Y - 1} {z} minecraft:chain",
                f"setblock -1 {Y - 2} {z} minecraft:soul_lantern[hanging=true]", f"setblock 1 {Y - 2} {z} minecraft:soul_lantern[hanging=true]"]
    out.append("# === Arena bossa (środek 0 150 -75, promień 20) ===")
    cz = -75
    out += spans(lambda dx, dz: dist(dx, dz) <= 20.5, 0, cz, 21, Y, "minecraft:polished_blackstone")
    out += spans(lambda dx, dz: 15.5 < dist(dx, dz) <= 16.4, 0, cz, 17, Y, "minecraft:crying_obsidian")
    out += spans(lambda dx, dz: 11.5 < dist(dx, dz) <= 12.4, 0, cz, 13, Y, "minecraft:gilded_blackstone")
    out += spans(lambda dx, dz: 5.5 < dist(dx, dz) <= 6.4, 0, cz, 7, Y, "minecraft:red_nether_bricks")
    out += spans(lambda dx, dz: (abs(dx) <= 0 or abs(dz) <= 0) and 6.4 < dist(dx, dz) <= 15.5, 0, cz, 16, Y, "minecraft:red_nether_bricks")
    out.append(f"fill -1 {Y} {cz - 1} 1 {Y} {cz + 1} minecraft:chiseled_polished_blackstone")
    sciana = lambda dx, dz: 19.5 < dist(dx, dz) <= 20.5 and not (abs(dx) <= 2 and dz > 0)
    out += spans(sciana, 0, cz, 21, Y + 1, "minecraft:polished_blackstone_bricks")
    out += spans(sciana, 0, cz, 21, Y + 2, "minecraft:polished_blackstone_brick_wall")
    for x, z in [(13, 13), (-13, 13), (13, -13), (-13, -13)]:
        out += [f"fill {x} {Y + 1} {cz + z} {x} {Y + 3} {cz + z} minecraft:polished_blackstone_bricks",
                f"setblock {x} {Y + 4} {cz + z} minecraft:soul_campfire[lit=true]"]
    for x in (-3, 3):
        out += [f"fill {x} {Y + 1} -55 {x} {Y + 5} -55 minecraft:polished_blackstone_bricks",
                f"setblock {x} {Y + 6} -55 minecraft:soul_lantern"]
    mats = ["minecraft:blackstone"] * 6 + ["minecraft:basalt"] * 6 + ["minecraft:netherrack"] * 30
    kraw = ["minecraft:magma_block", "minecraft:gilded_blackstone", "minecraft:crimson_nylium",
            "minecraft:nether_gold_ore", "minecraft:blackstone", "minecraft:shroomlight"]
    out += wyspa_spod(0, cz, 20, Y, 18, mats, kraw, 77)
    return out


def parkour():
    out = ["# === Parkour (zachód) ==="]
    out += [f"fill -31 {Y} -2 -27 {Y} 2 minecraft:light_blue_concrete",
            f"fill -31 {Y - 1} -2 -27 {Y - 1} 2 minecraft:stone",
            f"setblock -29 {Y} 0 minecraft:sea_lantern"]
    kolory = ["red", "orange", "yellow", "lime", "light_blue", "blue", "purple", "magenta", "pink"]
    x, y, z = -31, Y, 0
    for i in range(18):
        dy = R.choice([0, 0, 1, 1, -1]) if y > Y else R.choice([0, 1, 1])
        if y >= Y + 9:
            dy = R.choice([0, -1])
        dx = 3 if dy >= 1 else R.choice([3, 4]) if dy == 0 else 4
        x -= dx
        y += dy
        z = max(-4, min(4, z + R.choice([-1, 0, 1])))
        out.append(f"setblock {x} {y} {z} minecraft:{kolory[i % len(kolory)]}_concrete")
    x -= 3
    out += [f"fill {x - 2} {y} {z - 1} {x} {y} {z + 1} minecraft:emerald_block",
            f"fill {x - 2} {y - 1} {z - 1} {x} {y - 1} {z + 1} minecraft:gold_block"]
    meta = (x - 1, y + 3, z)
    return out, meta


# ------------------------------------------------------------------ build


def build():
    fn("mapa/etap/wyspa", "\n".join(wyspa()))
    fn("mapa/etap/plac", "\n".join(plac()))
    fn("mapa/etap/arena", "\n".join(most_i_arena()))
    pk, meta = parkour()
    fn("mapa/etap/parkour", "\n".join(pk))

    # -------------------------------------------------------- dekoracje / NPC
    dek = ["kill @e[tag=dz.map]"]
    dek.append(text_display(0, 157.2, 0, [t("DziobMc", "gold", bold=True)], "dz.holo.tytul", 4.0))
    dek.append(text_display(0, 156.3, 0, t("Dziob.fun", "yellow", bold=True), "dz.holo", 2.0))
    dek.append(text_display(0, 155.7, 0, [t("★ ", "gold"), t("Wersje 1.16.4+ • Survival • Eventy", "white"), t(" ★", "gold")], "dz.holo", 1.0))
    npc = [
        ("sklep", 10, -10, "librarian", [t("⛃ SKLEP", "gold", bold=True), t("\nKliknij PPM", "gray")]),
        ("kit", 10, 10, "armorer", [t("⚔ KITY", "yellow", bold=True), t("\nKliknij PPM", "gray")]),
        ("nagroda", -10, 10, "cleric", [t("✿ NAGRODA", "light_purple", bold=True), t("\nCo godzinę!", "gray")]),
        ("pomoc", -10, -10, "cartographer", [t("? POMOC", "aqua", bold=True), t("\nWszystkie komendy", "gray")]),
    ]
    for nid, x, z, prof, napis in npc:
        yaw = yaw_do(x, z, 0, 0)
        dek.append(f"summon minecraft:villager {x} {Y + 1} {z} {{Tags:[\"dz.map\",\"dz.npc\"],NoAI:1b,Invulnerable:1b,Silent:1b,"
                   f"PersistenceRequired:1b,Rotation:[{yaw}f,0f],VillagerData:{{profession:\"minecraft:{prof}\",level:5,type:\"minecraft:plains\"}},"
                   f"Offers:{{Recipes:[]}}}}")
        dek.append(f"summon minecraft:interaction {x} {Y + 1} {z} {{Tags:[\"dz.map\",\"dz.int.{nid}\"],width:1.3f,height:2.3f,response:1b}}")
        dek.append(text_display(x, Y + 3.4, z, napis, "dz.holo", 1.3))
        jfile(f"data/{NS}/advancement/npc/{nid}.json", {
            "criteria": {"klik": {"trigger": "minecraft:player_interacted_with_entity", "conditions": {
                "entity": [{"condition": "minecraft:entity_properties", "entity": "this",
                            "predicate": {"type": "minecraft:interaction", "nbt": "{Tags:[\"dz.int." + nid + "\"]}"}}]}}},
            "rewards": {"function": f"{NS}:npc/{nid}"}})
        cel = {"sklep": "komendy/menu_sklep", "kit": "komendy/menu_kit", "nagroda": "komendy/nagroda", "pomoc": "komendy/menu_pomoc"}[nid]
        fn(f"npc/{nid}", f"""
            advancement revoke @s only {NS}:npc/{nid}
            playsound minecraft:entity.villager.ambient master @s ~ ~ ~ 1 1
            function {NS}:{cel}
        """)
    dek.append(text_display(20, Y + 8.2, 0, [t("✦ LOSOWY TELEPORT ✦", "light_purple", bold=True), t("\nWejdź do portalu, aby ruszyć w świat!", "gray")], "dz.holo", 1.4))
    dek.append(text_display(0, Y + 6.5, -55, [t("⚔ ARENA BOSSA ⚔", "red", bold=True), t("\nTu pojawia się Król Dziobów", "gray")], "dz.holo", 1.6))
    dek.append(text_display(-29, Y + 3, 0, [t("PARKOUR ➜", "aqua", bold=True), t("\nNagroda: 75 monet", "gray")], "dz.holo", 1.4))
    dek.append(text_display(meta[0], meta[1], meta[2], [t("✔ META ✔", "green", bold=True), t("\nStań na szmaragdach!", "gray")], "dz.holo", 1.4))
    dek.append(text_display(0, Y + 2.8, 14, [t("Witaj na ", "white"), t("DziobMc", "gold", bold=True), t("!\nKliknij NPC albo wpisz /trigger pomoc", "gray")], "dz.holo", 1.1))
    fn("mapa/dekoracje", "\n".join(dek))

    # -------------------------------------------------------- budowanie
    punkty = [(x, z) for x in (-112, -56, 0, 56, 112) for z in (-112, -56, 0, 56, 112)]
    warunek = " ".join(f"if loaded {x} 0 {z}" for x, z in punkty)
    fn("mapa/zbuduj", f"""
        # Buduje całą mapę lobby. Można uruchomić ponownie (/function {NS}:mapa/zbuduj)
        {tellraw("@a", t("✦ ", "gold"), t("Ładowanie terenu pod mapę DziobMc...", "yellow"))}
        execute in minecraft:overworld run forceload add -112 -112 112 112
        scoreboard players set #proby dz.data 0
        schedule function {NS}:mapa/czekaj 40t replace
    """)
    fn("mapa/czekaj", f"""
        execute in minecraft:overworld {warunek} run return run function {NS}:mapa/buduj
        scoreboard players add #proby dz.data 1
        execute if score #proby dz.data matches 60.. run return run {tellraw("@a", t("✖ Nie udało się załadować terenu. Spróbuj ponownie: /function dziobmc:mapa/zbuduj", "red"))}
        schedule function {NS}:mapa/czekaj 20t replace
    """)
    fn("mapa/buduj", f"""
        execute in minecraft:overworld run function {NS}:mapa/buduj_wszystko
    """)
    fn("mapa/buduj_wszystko", f"""
        function {NS}:mapa/etap/wyspa
        function {NS}:mapa/etap/plac
        function {NS}:mapa/etap/arena
        function {NS}:mapa/etap/parkour
        function {NS}:mapa/dekoracje
        setworldspawn 0 151 18
        scoreboard players set #mapa dz.data 1
        tp @a {SPAWN}
        {tellraw("@a", t("✔ ", "green"), t("Mapa DziobMc zbudowana! ", "green", bold=True), t("Spawn: 0 151 18", "gray"))}
        schedule function {NS}:mapa/zakoncz 100t replace
    """)
    fn("mapa/zakoncz", "execute in minecraft:overworld run forceload remove -112 -112 112 112")

    # -------------------------------------------------------- animacja napisu
    grad = ["yellow", "gold", "gold", "red", "gold", "yellow", "white"]
    klatki = []
    for k in range(4):
        litery = [t(ch, grad[(i + k * 2) % len(grad)], bold=True) for i, ch in enumerate("DziobMc")]
        klatki.append(litery)
    anim = ["scoreboard players operation #t dz.data = #sek dz.data",
            "scoreboard players operation #t dz.data %= #4 dz.data"]
    for k, kl in enumerate(klatki):
        anim.append(f"execute if score #t dz.data matches {k} in minecraft:overworld run data merge entity @e[type=text_display,tag=dz.holo.tytul,limit=1] {{text:{snbt_text(kl)}}}")
    anim.append("execute in minecraft:overworld run particle minecraft:end_rod 0 157 0 2.5 0.6 0.2 0.01 4 force @a[tag=dz.lobby]")
    fn("mapa/animacja", "\n".join(anim))
    _ = J
