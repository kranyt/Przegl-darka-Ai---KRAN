"""Rdzeń: ładowanie, pętle, scoreboard, rangi, gracze, lobby, monety."""
from wspolne import (NS, SPAWN, FILES, J, t, sc, sel, tellraw, fn, jfile,
                     firework_cmd, raw)

TRIGGERY = ["pomoc", "spawn", "kit", "sklep", "nagroda", "staty", "discord",
            "event", "rtp", "warp", "rangi"]

COOLDOWNY = ["dz.cd_kit1", "dz.cd_kit2", "dz.cd_kit3", "dz.cd_kit4",
             "dz.cd_nagr", "dz.cd_spawn", "dz.cd_rtp", "dz.cd_park", "dz.cd_kit5"]

STALE = [2, 3, 4, 5, 8, 10, 11, 15, 20, 60, 100, 1200]

# id, drużyna (sortowanie w TAB), poziom, prefix (lista komponentów), kolor nicku, staff?
RANGI = [
    ("wlasciciel", "0_wlasciciel", 7, [t("WŁAŚCICIEL", "dark_red", bold=True)], "red", True),
    ("admin", "1_admin", 6, [t("ADMIN", "red", bold=True)], "red", True),
    ("moderator", "2_moderator", 5, [t("MOD", "dark_green", bold=True)], "green", True),
    ("helper", "3_helper", 4, [t("HELPER", "aqua", bold=True)], "aqua", True),
    ("youtuber", "4_youtuber", 3, [t("Y", "white", bold=True), t("T", "red", bold=True)], "white", False),
    ("legenda", "5_legenda", 3, [t("LEGENDA", "light_purple", bold=True)], "light_purple", False),
    ("mvp", "6_mvp", 2, [t("MVP", "gold", bold=True)], "gold", False),
    ("vip", "7_vip", 1, [t("VIP", "yellow", bold=True)], "yellow", False),
    ("gracz", "8_gracz", 0, [t("GRACZ", "gray")], "gray", False),
]


def prefix(parts):
    return [t("[", "dark_gray")] + parts + [t("] ", "dark_gray")]


def build():
    # ---------------------------------------------------------------- pack
    jfile("pack.mcmeta", {
        "pack": {
            "pack_format": 48,
            "supported_formats": [48, 61],
            "description": [t("DziobMc ", "gold", bold=True), t("• Dziob.fun", "yellow")],
        },
        "overlays": {"entries": [{"formats": [57, 61], "directory": "ov_1_21_2"}]},
    })
    jfile("data/minecraft/tags/function/load.json", {"values": [f"{NS}:load"]})
    jfile("data/minecraft/tags/function/tick.json", {"values": [f"{NS}:tick"]})

    # ---------------------------------------------------------------- load
    obj = [
        "scoreboard objectives add dz.data dummy",
        "scoreboard objectives add dz.coins dummy " + J(t("⛃ Monety", "gold")),
        "scoreboard objectives add dz.kills dummy " + J(t("Zabite moby", "red")),
        "scoreboard objectives add dz.pvp playerKillCount " + J(t("Zabici gracze", "dark_red")),
        "scoreboard objectives add dz.deaths deathCount " + J(t("Śmierci", "gray")),
        "scoreboard objectives add dz.hp health " + J(t("❤", "red")),
        "scoreboard objectives add dz.leave minecraft.custom:minecraft.leave_game",
        "scoreboard objectives add dz.rank dummy",
        "scoreboard objectives add dz.czas dummy",
        "scoreboard objectives add dz.minuty dummy",
        "scoreboard objectives add dz.hunt dummy",
        "scoreboard objectives add dz.zab playerKillCount",
        "scoreboard objectives add dz.smierc deathCount",
        "scoreboard objectives add dz.streak dummy",
        "scoreboard objectives add dz.bitwa dummy",
        "scoreboard objectives add dz.sidebar dummy " + J([t("✦ ", "yellow"), t("DziobMc", "gold", bold=True), t(" ✦", "yellow")]),
    ]
    obj += [f"scoreboard objectives add {c} dummy" for c in COOLDOWNY]
    obj += [f"scoreboard objectives add {tr} trigger" for tr in TRIGGERY]
    stale = [f"scoreboard players set #{n} dz.data {n}" for n in STALE]

    fn("load", "\n".join([
        "# ===================== DziobMc • Dziob.fun =====================",
        *obj,
        "scoreboard objectives setdisplay sidebar dz.sidebar",
        "scoreboard objectives setdisplay list dz.coins",
        "scoreboard objectives setdisplay below_name dz.hp",
        *stale,
        f"execute unless score #init dz.data matches 1 run function {NS}:init",
        f"function {NS}:rangi/druzyny",
        f"function {NS}:sidebar/ustaw",
        "bossbar add dziobmc:event " + J(t("DziobMc", "gold")),
        "bossbar set dziobmc:event color yellow",
        "bossbar set dziobmc:event style notched_20",
        "bossbar set dziobmc:event visible true",
        "bossbar add dziobmc:boss " + J(t("♛ Król Dziobów ♛", "gold", bold=True)),
        "bossbar set dziobmc:boss color red",
        "bossbar set dziobmc:boss style notched_10",
        "bossbar set dziobmc:boss max 600",
        "execute unless score #event dz.data matches 3 run bossbar set dziobmc:boss visible false",
        "gamerule spawnRadius 0",
        f"schedule function {NS}:petla/sekunda 20t replace",
        f"execute unless score #mapa dz.data matches 1 run schedule function {NS}:mapa/zbuduj 100t replace",
        tellraw("@a", t("✦ ", "gold"), t("DziobMc", "gold", bold=True), t(" » Paczka załadowana! ", "yellow"), t("Dziob.fun", "white", underlined=True)),
    ]))

    fn("init", """
        # Jednorazowa inicjalizacja zmiennych globalnych
        scoreboard players set #init dz.data 1
        scoreboard players set #next dz.data 1200
        scoreboard players set #event dz.data 0
        scoreboard players set #left dz.data 0
        scoreboard players set #mult dz.data 1
        scoreboard players set #szansa dz.data 12
        scoreboard players set #gracze dz.data 0
        scoreboard players set #mapa dz.data 0
    """)

    # ---------------------------------------------------------------- tick
    tick = [
        "# Gracze: pierwsze wejście / powrót / brak rangi",
        f"execute as @a[tag=!dz.joined] at @s run function {NS}:gracz/pierwsze_wejscie",
        f"execute as @a[scores={{dz.leave=1..}}] at @s run function {NS}:gracz/powrot",
        f"execute as @a[team=] run function {NS}:rangi/domyslna",
        "# Komendy /trigger",
    ]
    tick += [f"execute as @a[scores={{{tr}=1..}}] at @s run function {NS}:komendy/{tr}" for tr in TRIGGERY]
    tick += [f"scoreboard players enable @a {tr}" for tr in TRIGGERY]
    tick += [
        "# Spadanie z wyspy-lobby",
        f"execute as @a[tag=dz.lobby] at @s if entity @s[y=-64,dy=203] run function {NS}:lobby/spadek",
    ]
    fn("tick", "\n".join(tick))

    # ---------------------------------------------------------------- pętla 1 s
    fn("petla/sekunda", f"""
        schedule function {NS}:petla/sekunda 20t replace
        scoreboard players add #sek dz.data 1
        function {NS}:lobby/sekunda
        function {NS}:sidebar/odswiez
        function {NS}:event/zegar
        function {NS}:moby/sekunda
        function {NS}:mapa/animacja
        execute as @a at @s run function {NS}:gracz/sekunda
    """)

    # ---------------------------------------------------------------- rangi
    druzyny = []
    for rid, team, lvl, pre, col, staff in RANGI:
        druzyny += [
            f"team add {team}",
            f"team modify {team} prefix {J(prefix(pre))}",
            f"team modify {team} color {col}",
            f"team modify {team} collisionRule never",
            f"team modify {team} nametagVisibility always",
            f"team modify {team} friendlyFire true",
        ]
        fn(f"rangi/ustaw/{rid}", "\n".join([
            f"# Użycie: /execute as NICK run function {NS}:rangi/ustaw/{rid}",
            f"team join {team} @s",
            f"scoreboard players set @s dz.rank {lvl}",
            "tag @s add dz.staff" if staff else "tag @s remove dz.staff",
            tellraw("@a", t("✦ ", "gold"), sel("@s"), t(" otrzymał rangę ", "yellow"), *pre, t("!", "yellow")),
            "title @s times 10 60 20",
            "title @s subtitle " + J(t("Dzięki, że grasz na DziobMc!", "yellow")),
            "title @s title " + J([t("Ranga ", "white")] + pre),
            "execute at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1",
            "execute at @s run " + firework_cmd(),
        ]))
    fn("rangi/druzyny", "\n".join(druzyny))
    fn("rangi/domyslna", """
        team join 8_gracz @s
        scoreboard players add @s dz.rank 0
    """)

    # ---------------------------------------------------------------- gracze
    cds = "\n".join(f"scoreboard players set @s {c} -100000000" for c in COOLDOWNY)
    fn("gracz/pierwsze_wejscie", f"""
        tag @s add dz.joined
        scoreboard players add #gracze dz.data 1
        scoreboard players set @s dz.coins 100
        scoreboard players set @s dz.kills 0
        scoreboard players set @s dz.rank 0
        scoreboard players set @s dz.leave 0
        scoreboard players set @s dz.czas 0
        scoreboard players set @s dz.minuty 0
        {cds}
        function {NS}:rangi/domyslna
        execute if score #mapa dz.data matches 1 in minecraft:overworld run tp @s {SPAWN}
        title @s times 10 80 20
        title @s subtitle {J([t("Dziob.fun", "yellow"), t(" • ", "dark_gray"), t("Minecraft 1.16.4+", "white")])}
        title @s title {J([t("Witaj na ", "white"), t("DziobMc", "gold", bold=True)])}
        {tellraw("@a", t("✦ ", "gold"), sel("@s", "yellow"), t(" dołączył pierwszy raz! ", "white"), t("(gracz #", "gray"), sc("#gracze", "dz.data", "gray"), t(")", "gray"))}
        {tellraw("@s", t("➤ Dostajesz ", "green"), t("100 monet", "gold", bold=True), t(" i zestaw startowy na dobry początek!", "green"))}
        function {NS}:kity/daj/start
        playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
        {firework_cmd()}
        function {NS}:komendy/menu_pomoc
    """)
    fn("gracz/powrot", f"""
        scoreboard players set @s dz.leave 0
        title @s times 10 50 20
        title @s subtitle {J([t("Miłej gry na ", "yellow"), t("Dziob.fun", "white", bold=True)])}
        title @s title {J(t("Witaj ponownie!", "gold", bold=True))}
        {tellraw("@a", t("» ", "dark_gray"), sel("@s"), t(" wrócił na serwer!", "gray"))}
        {tellraw("@s", t("✦ Wpisz ", "yellow"), t("/trigger pomoc", "gold", bold=True, run="/trigger pomoc", hover=t("Kliknij!", "yellow")), t(" aby zobaczyć wszystkie komendy.", "yellow"))}
        playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.4
    """)
    fn("gracz/sekunda", f"""
        # Co sekundę dla każdego gracza
        scoreboard players add @s dz.czas 1
        execute if score @s dz.czas matches 300.. run function {NS}:gracz/wyplata
        execute if score @s dz.zab matches 1.. run function {NS}:pvp/zabojstwo
        execute if score @s dz.smierc matches 1.. run function {NS}:pvp/smierc
        function {NS}:gracz/hud
    """)
    fn("gracz/wyplata", f"""
        # Nagroda za każde 5 minut gry
        scoreboard players set @s dz.czas 0
        scoreboard players add @s dz.minuty 5
        scoreboard players set #ile dz.data 10
        {tellraw("@s", t("⌚ Nagroda za aktywną grę (5 min):", "aqua"))}
        function {NS}:monety/dodaj
    """)
    hud = [t("⛃ ", "gold"), sc("@s", "dz.coins", "yellow", True), t("   ⚔ Moby: ", "red"),
           sc("@s", "dz.kills", "white"), t("   ☠ PvP: ", "dark_red"), sc("@s", "dz.pvp", "white"),
           t("   🔥 ", "gold"), sc("@s", "dz.streak", "yellow")]
    hud[-2]["text"] = "   ✸ Seria: "
    hud_hunt = [t("⚔ POLOWANIE: ", "red", bold=True), sc("@s", "dz.hunt", "yellow", True),
                t("/10", "gold"), t("   ⛃ ", "gold"), sc("@s", "dz.coins", "yellow")]
    fn("gracz/hud", f"""
        execute if score #event dz.data matches 5 run return run title @s actionbar {J(hud_hunt)}
        title @s actionbar {J(hud)}
    """)

    # ---------------------------------------------------------------- monety
    fn("monety/dodaj", f"""
        # Wejście: #ile dz.data – mnożnik eventu i bonus rangi
        scoreboard players operation #ile dz.data *= #mult dz.data
        execute if score @s dz.rank matches 1 run function {NS}:monety/bonus_vip
        execute if score @s dz.rank matches 2.. run function {NS}:monety/bonus_mvp
        scoreboard players operation @s dz.coins += #ile dz.data
        {tellraw("@s", t("  + ", "gold"), sc("#ile", "dz.data", "gold", True), t(" monet ⛃", "yellow"))}
        playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 0.6 1.6
    """)
    fn("monety/bonus_vip", """
        # VIP: +25%
        scoreboard players operation #ile dz.data *= #5 dz.data
        scoreboard players operation #ile dz.data /= #4 dz.data
    """)
    fn("monety/bonus_mvp", """
        # MVP i wyżej: +50%
        scoreboard players operation #ile dz.data *= #3 dz.data
        scoreboard players operation #ile dz.data /= #2 dz.data
    """)

    # ---------------------------------------------------------------- sidebar
    linie = [
        ("dz.l1", 1006, t("")),
        ("dz.l2", 1005, [t(" ✦ ", "gold"), t("Serwer: ", "gray"), t("DziobMc", "yellow", bold=True)]),
        ("dz.l3", 1004, [t(" ✦ ", "gold"), t("Wersje: ", "gray"), t("1.16.4+", "white")]),
        ("dz.l4", 1003, t(" ")),
        ("dz.total", None, [t(" ● ", "green"), t("Graczy łącznie", "white")]),
        ("dz.online", None, [t(" ● ", "green"), t("Online", "white")]),
        ("dz.l5", -1, t("  ")),
        ("dz.l6", -3, [t(" ➤ ", "aqua"), t("/trigger pomoc", "aqua")]),
        ("dz.l7", -4, [t(" ⛃ ", "gold"), t("Monety: lista TAB", "gray")]),
        ("dz.l8", -5, t("   ")),
        ("dz.l9", -6, [t("    Dziob.fun", "yellow", bold=True)]),
    ]
    s = ["scoreboard players reset * dz.sidebar"]
    for name, score, disp in linie:
        s.append(f"scoreboard players set {name} dz.sidebar {score if score is not None else 0}")
        s.append(f"scoreboard players display name {name} dz.sidebar {J(disp)}")
        if score is None:
            s.append(f'scoreboard players display numberformat {name} dz.sidebar styled {J({"color": "yellow", "bold": True})}')
        else:
            s.append(f"scoreboard players display numberformat {name} dz.sidebar blank")
    s.append(f"function {NS}:sidebar/event_linia")
    fn("sidebar/ustaw", "\n".join(s))
    fn("sidebar/odswiez", """
        execute store result score dz.online dz.sidebar if entity @a
        scoreboard players operation dz.total dz.sidebar = #gracze dz.data
    """)

    # ---------------------------------------------------------------- lobby
    fn("lobby/sekunda", f"""
        # Strefa lobby: x/z -110..110, y 140..220 (świat zwykły)
        tag @a remove dz.lobby
        execute in minecraft:overworld run tag @a[x=-110,y=140,z=-110,dx=220,dy=80,dz=220] add dz.lobby
        gamemode adventure @a[tag=dz.lobby,gamemode=survival,tag=!dz.build]
        gamemode survival @a[tag=!dz.lobby,gamemode=adventure,tag=!dz.build]
        # Strefy: arena PvP i arena bossa = walka; reszta lobby = bezpieczna (Resistance V)
        tag @a remove dz.pvp_strefa
        tag @a remove dz.boss_strefa
        execute in minecraft:overworld run tag @a[x=-20,y=140,z=55,dx=40,dy=40,dz=40] add dz.pvp_strefa
        execute in minecraft:overworld run tag @a[x=-21,y=140,z=-96,dx=42,dy=40,dz=42] add dz.boss_strefa
        execute as @a[tag=dz.pvp_strefa,tag=!dz.pvp_bylo] at @s run function {NS}:pvp/wejscie
        execute as @a[tag=!dz.pvp_strefa,tag=dz.pvp_bylo] run function {NS}:pvp/wyjscie
        effect give @a[tag=dz.lobby,tag=!dz.pvp_strefa,tag=!dz.boss_strefa] minecraft:resistance 2 4 true
        effect give @a[tag=dz.lobby,tag=!dz.pvp_strefa,tag=!dz.boss_strefa] minecraft:saturation 2 0 true
        # Wrogie moby nie mają wstępu do lobby
        execute in minecraft:overworld as @e[x=-110,y=128,z=-110,dx=220,dy=92,dz=220,type=#{NS}:wrogie,tag=!dz.event] at @s run function {NS}:util/usun
        # Portal losowego teleportu
        execute in minecraft:overworld run particle minecraft:portal 20 153 0 0.2 1.3 1.6 0.6 50 force
        execute in minecraft:overworld run particle minecraft:end_rod 20 153 0 0.1 1.3 1.6 0.01 3 force
        execute in minecraft:overworld as @a[x=19,y=151,z=-2,dx=1,dy=3,dz=4,tag=!dz.build] at @s run function {NS}:komendy/rtp_teleport
        # Meta parkouru
        execute as @a[tag=dz.lobby] at @s if block ~ ~-1 ~ minecraft:emerald_block run function {NS}:lobby/parkour_meta
    """)
    fn("lobby/spadek", f"""
        execute if entity @s[x=-100,y=60,z=-10,dx=74,dy=100,dz=20] run return run function {NS}:lobby/spadek_parkour
        execute in minecraft:overworld run tp @s {SPAWN}
        playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
        title @s actionbar {J(t("Uważaj! Spadłeś z wyspy – wracasz na spawn.", "red"))}
    """)
    fn("lobby/spadek_parkour", f"""
        execute in minecraft:overworld run tp @s -29 151 0 90 0
        playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1.3
        title @s actionbar {J(t("Spróbuj jeszcze raz! Dasz radę!", "yellow"))}
    """)
    fn("lobby/parkour_meta", f"""
        execute in minecraft:overworld run tp @s {SPAWN}
        {tellraw("@a", t("✔ ", "green"), sel("@s", "yellow"), t(" ukończył parkour na spawnie!", "green"))}
        title @s times 5 50 15
        title @s title {J(t("PARKOUR UKOŃCZONY!", "green", bold=True))}
        playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
        {firework_cmd(colors=(5635925, 16777045))}
        {cooldown_park()}
    """)

    # ---------------------------------------------------------------- util
    fn("util/usun", """
        # Usuwa encję bez dropu (moby z lobby, boss po czasie itp.)
        data merge entity @s {DeathLootTable:"minecraft:empty",HandItems:[{},{}],ArmorItems:[{},{},{},{}]}
        tp @s ~ -200 ~
        kill @s
    """)
    fn("util/cooldown_info", f"""
        # Wejście: #cd, #roznica (ticki)
        scoreboard players operation #zostalo dz.data = #cd dz.data
        scoreboard players operation #zostalo dz.data -= #roznica dz.data
        scoreboard players operation #zostalo dz.data /= #20 dz.data
        scoreboard players operation #zm dz.data = #zostalo dz.data
        scoreboard players operation #zm dz.data /= #60 dz.data
        scoreboard players operation #zs dz.data = #zostalo dz.data
        scoreboard players operation #zs dz.data %= #60 dz.data
        {tellraw("@s", t("⌛ Poczekaj jeszcze ", "red"), sc("#zm", "dz.data", "yellow", True), t(" min ", "red"), sc("#zs", "dz.data", "yellow", True), t(" s", "red"))}
        playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.7
    """)
    fn("efekty/fajerwerk", firework_cmd())

    # ---------------------------------------------------------------- tagi encji
    jfile(f"data/{NS}/tags/entity_type/wrogie.json", {"values": [
        "minecraft:zombie", "minecraft:husk", "minecraft:drowned", "minecraft:zombie_villager",
        "minecraft:skeleton", "minecraft:stray", "minecraft:bogged", "minecraft:wither_skeleton",
        "minecraft:spider", "minecraft:cave_spider", "minecraft:creeper", "minecraft:witch",
        "minecraft:enderman", "minecraft:phantom", "minecraft:slime", "minecraft:pillager",
        "minecraft:silverfish", "minecraft:breeze"]})
    jfile(f"data/{NS}/tags/entity_type/konwertowalne.json", {"values": [
        "minecraft:zombie", "minecraft:husk", "minecraft:skeleton", "minecraft:stray",
        "minecraft:spider", "minecraft:creeper", "minecraft:wither_skeleton"]})


def cooldown_park():
    # nagroda za parkour co 10 minut
    return f"""function {NS}:lobby/parkour_nagroda"""


def build_extra():
    from wspolne import cooldown
    fn("lobby/parkour_nagroda", f"""
        {cooldown("dz.cd_park", 12000)}
        scoreboard players set #ile dz.data 75
        function {NS}:monety/dodaj
    """)


_ = (FILES, raw)
