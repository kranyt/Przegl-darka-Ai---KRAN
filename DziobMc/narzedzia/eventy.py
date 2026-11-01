"""System eventów: odliczanie na bossbarze + 6 eventów."""
from wspolne import NS, SPAWN, J, t, sc, sel, tellraw, fn, firework_cmd

# nr, id, nazwa, kolor, czas trwania (s), kolor bossbara, opis
EVENTY = [
    (1, "krwawy", "Krwawy Księżyc", "dark_red", 300, "red", "noc, a custom moby pojawiają się 5x częściej"),
    (2, "drop", "Drop Party", "aqua", 60, "blue", "z nieba na spawnie lecą przedmioty"),
    (3, "boss", "Król Dziobów", "gold", 600, "yellow", "boss na arenie – 1000 monet za ostatni cios"),
    (4, "podwojne", "Podwójne Monety", "yellow", 600, "green", "wszystkie monety x2"),
    (5, "polowanie", "Polowanie", "red", 300, "pink", "pierwszy, kto zabije 10 custom mobów, wygrywa 500 monet"),
    (6, "deszcz", "Deszcz Monet", "green", 15, "green", "każdy gracz online dostaje 100 monet"),
    (7, "bitwa", "Bitwa PvP", "dark_red", 300, "red", "kill na graczu = 100 monet, najlepszy wojownik +500"),
    (8, "kaiju", "Atak Kaiju", "dark_green", 900, "green", "gigantyczny potwór atakuje stolicę na mapie Ziemi!"),
]


def ogloszenie(nazwa, kolor, opis, przycisk=None):
    linie = [
        tellraw("@a", t("")),
        tellraw("@a", t("━━━━━━━━━━━ ✦ EVENT ✦ ━━━━━━━━━━━", kolor, bold=True)),
        tellraw("@a", t("  » ", "dark_gray"), t(nazwa.upper(), kolor, bold=True)),
        tellraw("@a", t("  " + opis, "gray")),
    ]
    if przycisk:
        linie.append(tellraw("@a", t("  ➤ ", "dark_gray"), t(przycisk[0], "green", bold=True, run=przycisk[1], hover=t("Kliknij!", "yellow"))))
    linie += [
        tellraw("@a", t("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", kolor, bold=True)),
        "title @a times 10 60 20",
        f"title @a title {J(t(nazwa, kolor, bold=True))}",
        f"title @a subtitle {J(t(opis, 'gray'))}",
        "execute as @a at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.6 1.2",
    ]
    return "\n".join(linie)


def build():
    # ------------------------------------------------------------ zegar
    fn("event/zegar", f"""
        # Wywoływany co sekundę. Eventy działają tylko gdy ktoś jest online.
        execute unless entity @a run return 0
        execute if score #event dz.data matches 1.. run return run function {NS}:event/trwa
        function {NS}:event/odliczanie
    """)
    fn("event/odliczanie", f"""
        scoreboard players remove #next dz.data 1
        execute store result bossbar dziobmc:event value run scoreboard players get #next dz.data
        scoreboard players operation #min dz.data = #next dz.data
        scoreboard players operation #min dz.data /= #60 dz.data
        scoreboard players operation #s dz.data = #next dz.data
        scoreboard players operation #s dz.data %= #60 dz.data
        bossbar set dziobmc:event name {J([t("✦ Następny event za ", "gold"), sc("#min", "dz.data", "yellow", True), t("m ", "yellow"), sc("#s", "dz.data", "yellow", True), t("s", "yellow"), t("  •  Dziob.fun", "gray")])}
        bossbar set dziobmc:event players @a
        execute if score #next dz.data matches 60 run {tellraw("@a", t("✦ ", "gold"), t("Event wystartuje za 1 minutę!", "yellow", bold=True))}
        execute if score #next dz.data matches 1..5 as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 1.5
        execute if score #next dz.data matches 1..5 run title @a actionbar {J([t("Event za ", "gold"), sc("#next", "dz.data", "yellow", True), t("...", "gold")])}
        execute if score #next dz.data matches ..0 run function {NS}:event/losuj
    """)
    los = [f"execute store result score #los dz.data run random value 1..{len(EVENTY)}"]
    for nr, eid, *_ in EVENTY:
        los.append(f"execute if score #los dz.data matches {nr} run function {NS}:event/start/{eid}")
    fn("event/losuj", "\n".join(los))

    fn("event/trwa", f"""
        scoreboard players remove #left dz.data 1
        execute store result bossbar dziobmc:event value run scoreboard players get #left dz.data
        scoreboard players operation #min dz.data = #left dz.data
        scoreboard players operation #min dz.data /= #60 dz.data
        scoreboard players operation #s dz.data = #left dz.data
        scoreboard players operation #s dz.data %= #60 dz.data
        """ + "\n".join(
        f"execute if score #event dz.data matches {nr} run bossbar set dziobmc:event name "
        + J([t("★ EVENT: ", "white", bold=True), t(nazwa, kol, bold=True), t("  •  zostało ", "gray"),
             sc("#min", "dz.data", "white"), t("m ", "white"), sc("#s", "dz.data", "white"), t("s", "white")])
        for nr, eid, nazwa, kol, *_ in EVENTY) + "\n" + "\n".join(
        f"execute if score #event dz.data matches {nr} run function {NS}:event/{eid}/tik"
        for nr, eid, *_ in EVENTY) + f"""
        execute if score #event dz.data matches 1.. if score #left dz.data matches ..0 run function {NS}:event/koniec
    """)

    # ------------------------------------------------------------ start / koniec
    for nr, eid, nazwa, kol, czas, bkol, opis in EVENTY:
        przycisk = {
            "drop": ("[TELEPORTUJ NA SPAWN]", "/trigger warp set 11"),
            "boss": ("[TELEPORTUJ NA ARENĘ]", "/trigger warp set 12"),
            "bitwa": ("[TELEPORTUJ NA ARENĘ PvP]", "/trigger warp set 14"),
        }.get(eid)
        fn(f"event/start/{eid}", f"""
            execute if score #event dz.data matches 1.. run function {NS}:event/koniec
            scoreboard players set #event dz.data {nr}
            scoreboard players set #left dz.data {czas}
            bossbar set dziobmc:event max {czas}
            bossbar set dziobmc:event color {bkol}
            scoreboard players display name dz.event dz.sidebar {J([t(" ★ ", "gold"), t("Event: ", "gray"), t(nazwa, kol, bold=True)])}
            {ogloszenie(nazwa, kol, opis, przycisk)}
            function {NS}:event/{eid}/start
        """)
    fn("event/koniec", f"""
        """ + "\n".join(f"execute if score #event dz.data matches {nr} run function {NS}:event/{eid}/koniec" for nr, eid, *_ in EVENTY) + f"""
        scoreboard players set #event dz.data 0
        scoreboard players set #left dz.data 0
        scoreboard players set #next dz.data 1200
        bossbar set dziobmc:event max 1200
        bossbar set dziobmc:event color yellow
        function {NS}:sidebar/event_linia
        execute as @a at @s run playsound minecraft:block.beacon.deactivate master @s ~ ~ ~ 0.7 1
    """)
    fn("sidebar/event_linia", f"""
        scoreboard players set dz.event dz.sidebar -2
        scoreboard players display numberformat dz.event dz.sidebar blank
        scoreboard players display name dz.event dz.sidebar {J([t(" ★ ", "gold"), t("Event: ", "gray"), t("wkrótce...", "white")])}
    """)

    # ------------------------------------------------------------ info /trigger event
    info = [
        "scoreboard players set @s event 0",
        tellraw("@s", t("━━━━━━━━━━━ ✦ EVENTY ✦ ━━━━━━━━━━━", "gold", bold=True)),
        "execute if score #event dz.data matches 0 run " + tellraw("@s", t(" Następny event za: ", "gray"), sc("#next", "dz.data", "yellow", True), t(" s", "yellow")),
    ]
    for nr, eid, nazwa, kol, czas, bkol, opis in EVENTY:
        info.append(f"execute if score #event dz.data matches {nr} run " + tellraw("@s", t(" TRWA: ", "green", bold=True), t(nazwa, kol, bold=True), t(" (zostało ", "gray"), sc("#left", "dz.data", "white"), t(" s)", "gray")))
    info.append(tellraw("@s", t(" Eventy losują się co 20 minut gry:", "gray")))
    for nr, eid, nazwa, kol, czas, bkol, opis in EVENTY:
        info.append(tellraw("@s", t("  • ", "dark_gray"), t(nazwa, kol, bold=True), t(" – " + opis, "gray")))
    info.append(tellraw("@s", t("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "gold", bold=True)))
    fn("komendy/event", "\n".join(info))

    # ------------------------------------------------------------ 1. Krwawy Księżyc
    fn("event/krwawy/start", """
        scoreboard players set #szansa dz.data 60
        time set 18000
        weather clear
        execute as @a at @s run playsound minecraft:entity.wither.spawn master @s ~ ~ ~ 0.5 0.6
    """)
    fn("event/krwawy/tik", f"""
        time set 18000
        execute as @a[tag=!dz.lobby] at @s run particle minecraft:crimson_spore ~ ~1 ~ 8 4 8 0 60
        scoreboard players operation #t dz.data = #left dz.data
        scoreboard players operation #t dz.data %= #10 dz.data
        execute if score #t dz.data matches 0 as @a[gamemode=survival,tag=!dz.lobby] at @s unless dimension minecraft:the_nether unless dimension minecraft:the_end run function {NS}:event/krwawy/spawn
    """)
    fn("event/krwawy/spawn", f"""
        # Przywołuje 2 losowe custom moby w promieniu ~14 bloków od gracza
        summon minecraft:marker ~ ~ ~ {{Tags:["dz.pkt"]}}
        summon minecraft:marker ~ ~ ~ {{Tags:["dz.pkt"]}}
        spreadplayers ~ ~ 1 14 false @e[type=marker,tag=dz.pkt,distance=..1]
        execute as @e[type=marker,tag=dz.pkt] at @s run function {NS}:moby/przywolaj/losowy
        kill @e[type=marker,tag=dz.pkt]
    """)
    fn("event/krwawy/koniec", f"""
        scoreboard players set #szansa dz.data 12
        time set 1000
        {tellraw("@a", t("☀ Krwawy Księżyc zaszedł... na razie.", "yellow"))}
    """)

    # ------------------------------------------------------------ 2. Drop Party
    fn("event/drop/start", """
        execute in minecraft:overworld run summon minecraft:marker 0 160 0 {Tags:["dz.dp"]}
    """)
    fn("event/drop/tik", f"""
        execute in minecraft:overworld as @e[type=marker,tag=dz.dp] at @s run function {NS}:event/drop/rzut
    """)
    fn("event/drop/rzut", f"""
        tp @s ~ ~ ~ ~47 0
        execute positioned ^ ^ ^5 run loot spawn ~ ~ ~ loot {NS}:drop_party
        execute positioned ^ ^ ^11 run loot spawn ~ ~ ~ loot {NS}:drop_party
        execute positioned ^ ^ ^17 run loot spawn ~ ~ ~ loot {NS}:drop_party
        particle minecraft:firework ~ ~ ~ 6 1 6 0.05 40 force
        playsound minecraft:entity.chicken.egg master @a[distance=..60] ~ ~ ~ 1 1.2
        scoreboard players operation #t dz.data = #left dz.data
        scoreboard players operation #t dz.data %= #5 dz.data
        execute if score #t dz.data matches 0 run {firework_cmd("~ ~ ~", (5636095, 16777045, 16733695))}
    """)
    fn("event/drop/koniec", f"""
        kill @e[type=marker,tag=dz.dp]
        {tellraw("@a", t("✦ Drop Party zakończone! Dzięki za zabawę!", "aqua"))}
    """)

    # ------------------------------------------------------------ 3. Boss
    fn("event/boss/start", f"""
        scoreboard players set #boss_zabity dz.data 0
        scoreboard players set #boss_jest dz.data 0
        scoreboard players set #szal dz.data 0
        scoreboard players set #bt dz.data 0
        execute in minecraft:overworld run forceload add -24 -99 24 -51
        schedule function {NS}:event/boss/przywolaj 60t replace
    """)
    fn("event/boss/przywolaj", f"""
        execute unless score #event dz.data matches 3 run return 0
        execute in minecraft:overworld positioned 0 151 -75 run function {NS}:moby/przywolaj/boss
        execute unless entity @e[type=husk,tag=dz.boss] run return run schedule function {NS}:event/boss/przywolaj 40t replace
        scoreboard players set #boss_jest dz.data 1
        bossbar set dziobmc:boss color red
        bossbar set dziobmc:boss visible true
        execute in minecraft:overworld run particle minecraft:explosion_emitter 0 153 -75 2 1 2 0 6 force
        execute as @a at @s run playsound minecraft:entity.wither.spawn master @s ~ ~ ~ 0.8 0.8
        {tellraw("@a", t("♛ Król Dziobów ", "gold", bold=True), t("pojawił się na arenie! ", "red"), t("[WALCZ]", "green", bold=True, run="/trigger warp set 12", hover=t("Teleport na arenę")))}
    """)
    fn("event/boss/tik", f"""
        execute if score #boss_jest dz.data matches 1 unless entity @e[type=husk,tag=dz.boss] run return run function {NS}:event/koniec
        execute in minecraft:overworld positioned 0 151 -75 run bossbar set dziobmc:boss players @a[distance=..70]
        execute as @e[type=husk,tag=dz.boss] at @s run function {NS}:moby/boss/tik
    """)
    fn("event/boss/koniec", f"""
        execute unless score #boss_zabity dz.data matches 1 run {tellraw("@a", t("♛ Król Dziobów uciekł z areny... Następnym razem!", "gold"))}
        execute as @e[tag=dz.boss] at @s run function {NS}:util/usun
        execute as @e[tag=dz.minion] at @s run function {NS}:util/usun
        bossbar set dziobmc:boss visible false
        scoreboard players set #boss_jest dz.data 0
        execute in minecraft:overworld run forceload remove -24 -99 24 -51
    """)

    # ------------------------------------------------------------ 4. Podwójne monety
    fn("event/podwojne/start", "scoreboard players set #mult dz.data 2")
    fn("event/podwojne/tik", "execute as @a at @s run particle minecraft:wax_on ~ ~2.2 ~ 0.3 0.1 0.3 0 1")
    fn("event/podwojne/koniec", f"""
        scoreboard players set #mult dz.data 1
        {tellraw("@a", t("⛃ Podwójne monety zakończone.", "yellow"))}
    """)

    # ------------------------------------------------------------ 5. Polowanie
    fn("event/polowanie/start", """
        scoreboard players reset * dz.hunt
        scoreboard players set @a dz.hunt 0
        scoreboard players set #szansa dz.data 30
    """)
    fn("event/polowanie/tik", "")
    fn("event/polowanie/punkt", f"""
        scoreboard players add @s dz.hunt 1
        execute if score @s dz.hunt matches 10.. if score #event dz.data matches 5 run function {NS}:event/polowanie/wygrana
    """)
    fn("event/polowanie/wygrana", f"""
        {tellraw("@a", t("⚔ ", "red"), sel("@s"), t(" wygrywa Polowanie i zgarnia 500 monet!", "gold", bold=True))}
        title @a times 10 60 20
        title @a title {J(t("POLOWANIE WYGRANE!", "gold", bold=True))}
        title @a subtitle {J([t("Zwycięzca: ", "yellow"), sel("@s")])}
        scoreboard players set #ile dz.data 500
        function {NS}:monety/dodaj
        {firework_cmd()}
        scoreboard players set #polowanie_wygrane dz.data 1
        function {NS}:event/koniec
    """)
    fn("event/polowanie/koniec", f"""
        scoreboard players set #szansa dz.data 12
        execute unless score #polowanie_wygrane dz.data matches 1 run {tellraw("@a", t("⚔ Polowanie zakończone – nikt nie zdobył 10 punktów!", "red"))}
        scoreboard players set #polowanie_wygrane dz.data 0
    """)

    # ------------------------------------------------------------ 6. Deszcz monet
    fn("event/deszcz/start", f"""
        execute as @a at @s run function {NS}:event/deszcz/gracz
    """)
    fn("event/deszcz/gracz", f"""
        scoreboard players set #ile dz.data 100
        function {NS}:monety/dodaj
        playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.6
    """)
    fn("event/deszcz/tik", "execute as @a at @s run particle minecraft:totem_of_undying ~ ~3 ~ 1.5 0.5 1.5 0.1 25")
    fn("event/deszcz/koniec", "")

    # ------------------------------------------------------------ 7. Bitwa PvP
    fn("event/bitwa/start", """
        scoreboard players reset * dz.bitwa
        scoreboard players set @a dz.bitwa 0
    """)
    fn("event/bitwa/tik", "execute in minecraft:overworld run particle minecraft:flame 0 155 75 12 3 12 0.01 30 force")
    fn("event/bitwa/koniec", f"""
        scoreboard players add @a dz.bitwa 0
        scoreboard players set #max dz.data 0
        scoreboard players operation #max dz.data > @a dz.bitwa
        execute if score #max dz.data matches 0 run {tellraw("@a", t("⚔ Bitwa PvP zakończona – nikt nikogo nie pokonał!", "red"))}
        execute if score #max dz.data matches 1.. as @a if score @s dz.bitwa = #max dz.data at @s run function {NS}:event/bitwa/zwyciezca
    """)
    fn("event/bitwa/zwyciezca", f"""
        {tellraw("@a", t("⚔ ", "red"), sel("@s"), t(" wygrywa Bitwę PvP z wynikiem ", "gold", bold=True), sc("@s", "dz.bitwa", "red", True), t(" zabójstw! +500 monet", "gold"))}
        title @a times 10 60 20
        title @a title {J(t("BITWA WYGRANA!", "dark_red", bold=True))}
        title @a subtitle {J([t("Zwycięzca: ", "gray"), sel("@s")])}
        scoreboard players set #ile dz.data 500
        function {NS}:monety/dodaj
        {firework_cmd()}
    """)
    _ = SPAWN
