"""Komendy graczy (/trigger), kity, sklep, panel admina."""
from wspolne import (NS, SPAWN, J, t, sc, sel, tellraw, fn, item, cooldown,
                     firework_cmd)
from rdzen import RANGI, prefix

DISCORD = "https://discord.gg/TWOJ-LINK"   # <- podmień na swój link!
STRONA = "https://dziob.fun"

LINIA = t("━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "gold", bold=True)


def naglowek(tytul):
    return [
        tellraw("@s", t("")),
        tellraw("@s", LINIA),
        tellraw("@s", t("        ✦ ", "yellow"), t("DziobMc", "gold", bold=True), t(" » ", "dark_gray"), t(tytul, "yellow", bold=True)),
        tellraw("@s", LINIA),
    ]


def stopka():
    return [tellraw("@s", LINIA)]


def przycisk(label, cmd, color, opis, hover):
    return tellraw("@s", t(" ➤ ", "dark_gray"), t(f"[{label}]", color, bold=True, run=cmd, hover=t(hover, "yellow")), t(f" {opis}", "gray"))


# ------------------------------------------------------------------- kity
KITY = [
    # nr, id, nazwa, wymagany poziom rangi, cooldown (ticki), opis, przedmioty
    (11, "start", "Start", 0, 72000, "każdy gracz • co 1h", [
        (item("stone_sword"), 1), (item("stone_pickaxe"), 1), (item("stone_axe"), 1),
        (item("stone_shovel"), 1), (item("bread"), 16), (item("torch"), 16),
        (item("leather_helmet"), 1), (item("leather_chestplate"), 1),
        (item("leather_leggings"), 1), (item("leather_boots"), 1)]),
    (12, "vip", "VIP", 1, 144000, "ranga VIP+ • co 2h", [
        (item("iron_sword", "Miecz VIP", "yellow", {"sharpness": 2}), 1),
        (item("iron_pickaxe", "Kilof VIP", "yellow", {"efficiency": 2}), 1),
        (item("iron_helmet"), 1), (item("iron_chestplate"), 1),
        (item("iron_leggings"), 1), (item("iron_boots"), 1),
        (item("golden_apple"), 4), (item("cooked_beef"), 32)]),
    (13, "mvp", "MVP", 2, 216000, "ranga MVP+ • co 3h", [
        (item("diamond_sword", "Miecz MVP", "gold", {"sharpness": 3, "unbreaking": 2}), 1),
        (item("diamond_pickaxe", "Kilof MVP", "gold", {"efficiency": 3, "fortune": 2}), 1),
        (item("diamond_helmet", ench={"protection": 2}), 1),
        (item("diamond_chestplate", ench={"protection": 2}), 1),
        (item("diamond_leggings", ench={"protection": 2}), 1),
        (item("diamond_boots", ench={"protection": 2}), 1),
        (item("golden_apple"), 8), (item("ender_pearl"), 8), (item("cooked_beef"), 32)]),
    (14, "legenda", "Legenda", 3, 432000, "ranga LEGENDA/YT+ • co 6h", [
        (item("netherite_sword", "Ostrze Legendy", "light_purple",
              {"sharpness": 5, "looting": 3, "unbreaking": 3, "fire_aspect": 2},
              ["Wykute w ogniu Dziob.fun"]), 1),
        (item("diamond_helmet", ench={"protection": 4, "unbreaking": 3}), 1),
        (item("diamond_chestplate", ench={"protection": 4, "unbreaking": 3}), 1),
        (item("diamond_leggings", ench={"protection": 4, "unbreaking": 3}), 1),
        (item("diamond_boots", ench={"protection": 4, "unbreaking": 3, "feather_falling": 4}), 1),
        (item("totem_of_undying"), 1), (item("golden_apple"), 16),
        (item("enchanted_golden_apple"), 1)]),
]

# ------------------------------------------------------------------- sklep
SKLEP = [
    (11, "Diamenty x8", 150, "aqua", [(item("diamond"), 8)]),
    (12, "Złote jabłka x5", 100, "gold", [(item("golden_apple"), 5)]),
    (13, "Perły Endu x16", 120, "dark_aqua", [(item("ender_pearl"), 16)]),
    (14, "Butelki XP x64", 200, "green", [(item("experience_bottle"), 64)]),
    (15, "Totem Nieśmiertelności", 400, "yellow", [(item("totem_of_undying"), 1)]),
    (16, "Skrzynia Szczęścia", 250, "light_purple", "LOOT"),
    (17, "Miecz Dzioba", 1500, "gold", [(item(
        "netherite_sword", "Miecz Dzioba", "gold",
        {"sharpness": 5, "unbreaking": 3, "fire_aspect": 2, "looting": 3, "mending": 1},
        ["Legendarny miecz serwera DziobMc", "Dziob.fun"]), 1)]),
    (18, "Kilof Dzioba", 1800, "gold", [(item(
        "netherite_pickaxe", "Kilof Dzioba", "gold",
        {"efficiency": 5, "fortune": 3, "unbreaking": 3, "mending": 1},
        ["Kopie szybciej niż dziob dzięcioła"]), 1)]),
    (19, "Elytra + 32 fajerwerki", 2500, "dark_purple", [
        (item("elytra", "Skrzydła Dzioba", "dark_purple", {"unbreaking": 3}), 1),
        (item("firework_rocket"), 32)]),
]


def build():
    # ------------------------------------------------------------ pomoc
    fn("komendy/pomoc", f"""
        scoreboard players set @s pomoc 0
        function {NS}:komendy/menu_pomoc
    """)
    fn("komendy/menu_pomoc", "\n".join(naglowek("KOMENDY") + [
        przycisk("SPAWN", "/trigger spawn", "green", "teleport na spawn", "/trigger spawn"),
        przycisk("LOSOWY TP", "/trigger rtp", "dark_purple", "teleport w losowe miejsce świata", "/trigger rtp"),
        przycisk("WARPY", "/trigger warp", "aqua", "arena bossa, parkour, spawn", "/trigger warp"),
        przycisk("KITY", "/trigger kit", "yellow", "darmowe zestawy przedmiotów", "/trigger kit"),
        przycisk("SKLEP", "/trigger sklep", "gold", "kupuj przedmioty za monety ⛃", "/trigger sklep"),
        przycisk("NAGRODA", "/trigger nagroda", "light_purple", "darmowe monety co godzinę", "/trigger nagroda"),
        przycisk("STATYSTYKI", "/trigger staty", "red", "twoje monety, kille, czas gry", "/trigger staty"),
        przycisk("EVENTY", "/trigger event", "dark_red", "aktualny i następny event", "/trigger event"),
        przycisk("RANGI", "/trigger rangi", "white", "lista rang i ich bonusy", "/trigger rangi"),
        przycisk("DISCORD", "/trigger discord", "blue", "dołącz do społeczności", "/trigger discord"),
        tellraw("@s", t(" Klikaj w przyciski albo wpisuj ", "gray"), t("/trigger <nazwa>", "yellow")),
    ] + stopka()))

    # ------------------------------------------------------------ spawn
    fn("komendy/spawn", f"""
        scoreboard players set @s spawn 0
        {cooldown("dz.cd_spawn", 200)}
        execute in minecraft:overworld run tp @s {SPAWN}
        execute at @s run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
        execute at @s run particle minecraft:portal ~ ~1 ~ 0.4 0.8 0.4 0.5 60
        title @s actionbar {J(t("✦ Witaj na spawnie DziobMc!", "gold"))}
    """)

    # ------------------------------------------------------------ rtp
    fn("komendy/rtp", f"""
        scoreboard players set @s rtp 0
        function {NS}:komendy/rtp_teleport
    """)
    fn("komendy/rtp_teleport", f"""
        {cooldown("dz.cd_rtp", 1200)}
        tag @s remove dz.lobby
        gamemode survival @s[gamemode=adventure,tag=!dz.build]
        title @s actionbar {J(t("✦ Szukam bezpiecznego miejsca...", "light_purple"))}
        execute in minecraft:overworld run spreadplayers 0 0 1 3000 false @s
        effect give @s minecraft:resistance 5 4 true
        effect give @s minecraft:slow_falling 6 0 true
        execute at @s run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 0.8
        title @s times 5 40 10
        title @s title {J(t("✦ Losowy teleport ✦", "light_purple", bold=True))}
        title @s subtitle {J(t("Powodzenia w przygodzie!", "gray"))}
    """)

    # ------------------------------------------------------------ warp
    fn("komendy/warp", f"""
        execute if score @s warp matches 11 in minecraft:overworld run tp @s {SPAWN}
        execute if score @s warp matches 12 in minecraft:overworld run tp @s 0 151 -57 180 0
        execute if score @s warp matches 13 in minecraft:overworld run tp @s -29 151 0 90 0
        execute if score @s warp matches 11..13 at @s run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
        execute if score @s warp matches 1 run function {NS}:komendy/menu_warp
        scoreboard players set @s warp 0
    """)
    fn("komendy/menu_warp", "\n".join(naglowek("WARPY") + [
        przycisk("SPAWN", "/trigger warp set 11", "green", "główna wyspa", "Teleportuj"),
        przycisk("ARENA BOSSA", "/trigger warp set 12", "red", "tu walczy się z Królem Dziobów", "Teleportuj"),
        przycisk("PARKOUR", "/trigger warp set 13", "aqua", "ukończ go i zgarnij 75 monet!", "Teleportuj"),
        przycisk("LOSOWY TP", "/trigger rtp", "dark_purple", "dziki świat survival", "Teleportuj"),
    ] + stopka()))

    # ------------------------------------------------------------ kity
    menu = naglowek("KITY")
    disp = [f"execute if score @s kit matches 1 run function {NS}:komendy/menu_kit"]
    for nr, kid, nazwa, lvl, cd, opis, przedmioty in KITY:
        menu.append(przycisk(f"KIT {nazwa.upper()}", f"/trigger kit set {nr}", "yellow", opis, "Kliknij, aby odebrać"))
        disp.append(f"execute if score @s kit matches {nr} run function {NS}:kity/odbierz/{kid}")
        rangi_ok = [r for r in RANGI if r[2] >= lvl]
        fn(f"kity/odbierz/{kid}", f"""
            execute unless score @s dz.rank matches {lvl}.. run return run function {NS}:kity/brak_rangi
            {cooldown("dz.cd_kit" + str(nr - 10), cd)}
            function {NS}:kity/daj/{kid}
            {tellraw("@s", t("✔ Odebrano kit ", "green"), t(nazwa, "gold", bold=True), t("!", "green"))}
            playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.2
        """)
        _ = rangi_ok
        fn(f"kity/daj/{kid}", "\n".join(f"give @s {it} {n}" for it, n in przedmioty))
    menu += stopka()
    fn("komendy/menu_kit", "\n".join(menu))
    disp.append("scoreboard players set @s kit 0")
    fn("komendy/kit", "\n".join(disp))
    fn("kity/brak_rangi", f"""
        {tellraw("@s", t("✖ Ten kit wymaga wyższej rangi! ", "red"), t("[Zobacz rangi]", "yellow", bold=True, run="/trigger rangi", hover=t("Kliknij")))}
        playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.7
    """)

    # ------------------------------------------------------------ sklep
    menu = naglowek("SKLEP") + [tellraw("@s", t(" Twoje monety: ", "gray"), sc("@s", "dz.coins", "gold", True), t(" ⛃", "gold"))]
    disp = [f"execute if score @s sklep matches 1 run function {NS}:komendy/menu_sklep"]
    for nr, nazwa, cena, kolor, przedmioty in SKLEP:
        menu.append(tellraw("@s", t(" ➤ ", "dark_gray"), t("[KUP]", "green", bold=True, run=f"/trigger sklep set {nr}", hover=t(f"Kup: {nazwa} za {cena} monet", "yellow")),
                            t(f" {nazwa} ", kolor), t(f"» {cena} ⛃", "gold")))
        disp.append(f"execute if score @s sklep matches {nr} run function {NS}:sklep/kup/{nr}")
        if przedmioty == "LOOT":
            daj = f"loot give @s loot {NS}:skrzynia_szczescia"
        else:
            daj = "\n".join(f"give @s {it} {n}" for it, n in przedmioty)
        fn(f"sklep/kup/{nr}", f"""
            scoreboard players set #cena dz.data {cena}
            execute unless score @s dz.coins >= #cena dz.data run return run function {NS}:sklep/brak
            scoreboard players operation @s dz.coins -= #cena dz.data
            {daj}
            {tellraw("@s", t("✔ Kupiono: ", "green"), t(nazwa, kolor, bold=True), t(f" za {cena} monet!", "green"))}
            playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
            playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
        """)
    menu += [tellraw("@s", t(" Monety zdobywasz za custom moby, eventy, parkour i grę!", "gray", italic=True))] + stopka()
    fn("komendy/menu_sklep", "\n".join(menu))
    disp.append("scoreboard players set @s sklep 0")
    fn("komendy/sklep", "\n".join(disp))
    fn("sklep/brak", f"""
        {tellraw("@s", t("✖ Masz za mało monet! Potrzebujesz ", "red"), sc("#cena", "dz.data", "gold", True), t(" ⛃, masz ", "red"), sc("@s", "dz.coins", "gold", True), t(" ⛃", "red"))}
        playsound minecraft:entity.villager.no master @s ~ ~ ~ 1 1
    """)

    # ------------------------------------------------------------ nagroda
    fn("komendy/nagroda", f"""
        scoreboard players set @s nagroda 0
        {cooldown("dz.cd_nagr", 72000)}
        execute store result score #ile dz.data run random value 50..150
        {tellraw("@s", t("🎁 ", "light_purple"), t("Nagroda godzinowa odebrana!", "light_purple", bold=True))}
        function {NS}:monety/dodaj
        loot give @s loot {NS}:nagroda
        playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1
        {firework_cmd(colors=(11141290, 16733695))}
    """.replace("🎁", "✿"))

    # ------------------------------------------------------------ staty
    fn("komendy/staty", "\n".join(["scoreboard players set @s staty 0"] + naglowek("STATYSTYKI") + [
        tellraw("@s", t(" Gracz: ", "gray"), sel("@s")),
        tellraw("@s", t(" ⛃ Monety: ", "gold"), sc("@s", "dz.coins", "yellow", True)),
        tellraw("@s", t(" ⚔ Zabite custom moby: ", "red"), sc("@s", "dz.kills", "white", True)),
        tellraw("@s", t(" ☠ Zabici gracze: ", "dark_red"), sc("@s", "dz.pvp", "white", True)),
        tellraw("@s", t(" ✝ Śmierci: ", "gray"), sc("@s", "dz.deaths", "white", True)),
        tellraw("@s", t(" ⌚ Minuty gry: ", "aqua"), sc("@s", "dz.minuty", "white", True)),
    ] + stopka()))

    # ------------------------------------------------------------ discord
    fn("komendy/discord", "\n".join(["scoreboard players set @s discord 0"] + naglowek("DISCORD & WWW") + [
        tellraw("@s", t(" ➤ ", "dark_gray"), t("[DISCORD]", "blue", bold=True, url=DISCORD, hover=t("Kliknij, aby otworzyć", "yellow")), t(" konkursy, ogłoszenia, pomoc", "gray")),
        tellraw("@s", t(" ➤ ", "dark_gray"), t("[STRONA]", "gold", bold=True, url=STRONA, hover=t("Dziob.fun", "yellow")), t(" Dziob.fun – sklep z rangami", "gray")),
        tellraw("@s", t(" IP serwera: ", "gray"), t("Dziob.fun", "yellow", bold=True)),
    ] + stopka()))

    # ------------------------------------------------------------ rangi
    opisy = {
        "vip": "+25% monet • kit VIP",
        "mvp": "+50% monet • kit VIP i MVP",
        "legenda": "+50% monet • wszystkie kity",
        "youtuber": "+50% monet • wszystkie kity",
        "helper": "pomaga graczom",
        "moderator": "pilnuje porządku",
        "admin": "administracja serwera",
        "wlasciciel": "właściciel DziobMc",
        "gracz": "kit Start • monety za grę",
    }
    linie = naglowek("RANGI")
    for rid, team, lvl, pre, col, staff in RANGI:
        linie.append(tellraw("@s", t(" ", "gray"), *prefix(pre), t(opisy[rid], "gray")))
    linie.append(tellraw("@s", t(" Rangi kupisz na ", "gray"), t("Dziob.fun", "gold", bold=True, url=STRONA, hover=t("Otwórz stronę"))))
    linie += stopka()
    fn("komendy/rangi", "\n".join(["scoreboard players set @s rangi 0"] + linie))

    # ------------------------------------------------------------ panel admina
    panel = naglowek("PANEL ADMINA") + [
        przycisk("ZBUDUJ MAPĘ", f"/function {NS}:mapa/zbuduj", "green", "spawn, arena, parkour (od nowa)", "Buduje lobby na 0 150 0"),
        przycisk("EVENT TERAZ", f"/function {NS}:admin/event_teraz", "gold", "losowy event za 10 s", "Skraca odliczanie"),
        tellraw("@s", t(" Start eventu: ", "gray"),
                t("[Krwawy]", "dark_red", run=f"/function {NS}:event/start/krwawy"), t(" "),
                t("[Drop]", "aqua", run=f"/function {NS}:event/start/drop"), t(" "),
                t("[Boss]", "red", run=f"/function {NS}:event/start/boss"), t(" "),
                t("[x2]", "gold", run=f"/function {NS}:event/start/podwojne"), t(" "),
                t("[Polowanie]", "yellow", run=f"/function {NS}:event/start/polowanie"), t(" "),
                t("[Deszcz]", "green", run=f"/function {NS}:event/start/deszcz")),
        przycisk("ZAKOŃCZ EVENT", f"/function {NS}:event/koniec", "red", "przerywa aktualny event", "Stop"),
        przycisk("TRYB BUDOWANIA", f"/function {NS}:admin/budowanie", "yellow", "wł/wył – lobby nie wymusza trybu przygody", "Przełącz"),
        tellraw("@s", t(" Przywołaj moba: ", "gray"), *[
            x for m in ["wojownik", "lucznik", "pajak", "ognisty", "lodowy", "widmo", "kreeper", "boss"]
            for x in (t(f"[{m}]", "light_purple", run=f"/function {NS}:moby/przywolaj/{m}"), t(" "))]),
        tellraw("@s", t(" Nadaj rangę: ", "gray"), *[
            x for r in RANGI for x in (t(f"[{r[0]}]", r[4], suggest=f"/execute as NICK run function {NS}:rangi/ustaw/{r[0]}", hover=t("Wstawi komendę – podmień NICK")), t(" "))]),
        tellraw("@s", t(" Monety: ", "gray"), t("/scoreboard players add NICK dz.coins 100", "yellow", suggest="/scoreboard players add NICK dz.coins 100")),
    ] + stopka()
    fn("admin/panel", "\n".join(panel))
    fn("admin/event_teraz", f"""
        execute if score #event dz.data matches 1.. run function {NS}:event/koniec
        scoreboard players set #next dz.data 10
        {tellraw("@a", t("✦ Admin przyspieszył event! Start za 10 sekund!", "gold", bold=True))}
    """)
    fn("admin/budowanie", f"""
        execute if entity @s[tag=dz.build] run return run function {NS}:admin/budowanie_off
        tag @s add dz.build
        gamemode creative @s
        {tellraw("@s", t("✔ Tryb budowania WŁĄCZONY", "green", bold=True))}
    """)
    fn("admin/budowanie_off", f"""
        tag @s remove dz.build
        gamemode survival @s
        {tellraw("@s", t("✖ Tryb budowania WYŁĄCZONY", "red", bold=True))}
    """)
    _ = firework_cmd
