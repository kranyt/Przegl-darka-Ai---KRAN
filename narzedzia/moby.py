"""Custom moby, boss, loot tables, nagrody za zabicie."""
from wspolne import (NS, FILES, J, t, sel, snbt_text, tellraw, fn, jfile,
                     nbt_item, firework_cmd)

E = '{}'  # pusty slot

# id: (typ bazowy, nazwa, kolor, ręka, zbroja[buty,spodnie,klata,hełm], atrybuty, extra NBT, monety, opis)
MOBY = {
    "wojownik": ("zombie", "⚔ Dziobak Wojownik", "gold",
                 [nbt_item("iron_sword"), E],
                 [nbt_item("iron_boots"), nbt_item("iron_leggings"), nbt_item("iron_chestplate"), nbt_item("golden_helmet")],
                 {"max_health": 40, "attack_damage": 6, "movement_speed": 0.27, "follow_range": 40},
                 "IsBaby:0b", 15),
    "ognisty": ("zombie", "☄ Ognisty Dziob", "red",
                [nbt_item("golden_sword", {"fire_aspect": 2}), E],
                [nbt_item("golden_boots"), E, nbt_item("golden_chestplate"), nbt_item("magma_block")],
                {"max_health": 35, "attack_damage": 5, "movement_speed": 0.3, "follow_range": 40},
                'IsBaby:0b,active_effects:[{id:"minecraft:fire_resistance",amplifier:0b,duration:-1,show_particles:0b}]', 20),
    "lucznik": ("skeleton", "➶ Mroczny Łucznik", "dark_gray",
                [nbt_item("bow", {"power": 3}), E],
                [nbt_item("leather_boots", dye=1644825), nbt_item("leather_leggings", dye=1644825),
                 nbt_item("leather_chestplate", dye=1644825), nbt_item("leather_helmet", dye=1644825)],
                {"max_health": 30, "movement_speed": 0.27, "follow_range": 40},
                "", 15),
    "lodowy": ("stray", "❄ Lodowy Strażnik", "aqua",
               [nbt_item("bow", {"punch": 2}), E],
               [nbt_item("leather_boots", dye=11393254), E, nbt_item("chainmail_chestplate"), nbt_item("packed_ice")],
               {"max_health": 35, "movement_speed": 0.26, "follow_range": 40},
               "", 20),
    "pajak": ("spider", "☣ Jadowity Pająk", "dark_green", None, None,
              {"max_health": 32, "attack_damage": 4, "movement_speed": 0.36, "scale": 1.4},
              "", 15),
    "kreeper": ("creeper", "✸ Mini Kreeper", "green", None, None,
                {"max_health": 15, "movement_speed": 0.33, "scale": 0.6},
                "ExplosionRadius:2b,Fuse:18s", 20),
    "widmo": ("wither_skeleton", "☠ Widmowy Rycerz", "dark_purple",
              [nbt_item("netherite_sword", {"sharpness": 1}), E],
              [E, E, nbt_item("netherite_chestplate"), nbt_item("netherite_helmet")],
              {"max_health": 50, "attack_damage": 10, "movement_speed": 0.3, "follow_range": 40},
              "Glowing:1b", 30),
    "boss": ("husk", "♛ Król Dziobów ♛", "gold",
             [nbt_item("netherite_axe"), nbt_item("totem_of_undying")],
             [nbt_item("golden_boots", {"protection": 4}), nbt_item("golden_leggings", {"protection": 4}),
              nbt_item("golden_chestplate", {"protection": 4}), nbt_item("golden_helmet", {"protection": 4})],
             {"max_health": 600, "attack_damage": 14, "movement_speed": 0.3, "follow_range": 48,
              "knockback_resistance": 1.0, "armor": 10, "scale": 2.5},
             "IsBaby:0b,PersistenceRequired:1b,CustomNameVisible:1b,Silent:0b", 1000),
}

LOOT = {
    "wojownik": [("iron_ingot", 1, 3, 0.7), ("rotten_flesh", 0, 2, 1), ("emerald", 1, 2, 0.25)],
    "ognisty": [("blaze_rod", 1, 2, 0.6), ("gold_ingot", 1, 3, 0.6), ("magma_cream", 1, 2, 0.4)],
    "lucznik": [("arrow", 4, 12, 1), ("bone", 1, 3, 1), ("bow", 1, 1, 0.15)],
    "lodowy": [("packed_ice", 2, 6, 0.8), ("diamond", 1, 1, 0.1), ("arrow", 4, 10, 1)],
    "pajak": [("string", 2, 5, 1), ("spider_eye", 1, 2, 0.8), ("slime_ball", 1, 2, 0.3)],
    "kreeper": [("gunpowder", 2, 5, 1), ("tnt", 1, 1, 0.2)],
    "widmo": [("wither_skeleton_skull", 1, 1, 0.15), ("netherite_scrap", 1, 1, 0.2), ("diamond", 1, 2, 0.4), ("coal", 2, 5, 1)],
    "boss": [("netherite_ingot", 1, 2, 1), ("diamond", 6, 12, 1), ("enchanted_golden_apple", 1, 2, 1),
             ("totem_of_undying", 1, 1, 1), ("experience_bottle", 16, 32, 1)],
}


def loot_pool(entries):
    pools = []
    for iid, mn, mx, ch in entries:
        p = {"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"minecraft:{iid}",
                                      "functions": [{"function": "minecraft:set_count",
                                                     "count": {"type": "minecraft:uniform", "min": mn, "max": mx}}]}]}
        if ch < 1:
            p["conditions"] = [{"condition": "minecraft:random_chance", "chance": ch}]
        pools.append(p)
    return pools


def atrybuty_cmds(attrs, nowe_id):
    out = []
    for k, v in attrs.items():
        aid = f"minecraft:{k}" if nowe_id else f"minecraft:generic.{k}"
        out.append(f"attribute @s {aid} base set {v}")
    if "max_health" in attrs:
        out.append(f"data modify entity @s Health set value {float(attrs['max_health'])}f")
    return "\n".join(out) + "\n"


def build():
    wszystkie = list(MOBY)
    for mid, (typ, nazwa, kolor, reka, zbroja, attrs, extra, monety) in MOBY.items():
        nbt = [f"CustomName:{snbt_text({'text': nazwa, 'color': kolor, 'bold': True})}",
               "CanPickUpLoot:0b", f'DeathLootTable:"{NS}:moby/{mid}"']
        if reka:
            nbt += [f"HandItems:[{','.join(reka)}]", "HandDropChances:[0.0f,0.0f]"]
        if zbroja:
            nbt += [f"ArmorItems:[{','.join(zbroja)}]", "ArmorDropChances:[0.0f,0.0f,0.0f,0.0f]"]
        if extra:
            nbt.append(extra)
        tagi = ["dz.ch", "dz.mob", f"dz.m.{mid}"] + (["dz.boss", "dz.event"] if mid == "boss" else [])
        fn(f"moby/ustaw/{mid}", "\n".join(
            ["# Zamienia @s w custom moba: " + nazwa, "tag @s remove dz.nowy"] +
            [f"tag @s add {tg}" for tg in tagi] +
            ["data merge entity @s {" + ",".join(nbt) + "}",
             f"function {NS}:moby/atrybuty/{mid}"]))
        # atrybuty: 1.21–1.21.1 (generic.*) + overlay dla 1.21.2–1.21.4
        FILES[f"data/{NS}/function/moby/atrybuty/{mid}.mcfunction"] = atrybuty_cmds(attrs, False)
        FILES[f"ov_1_21_2/data/{NS}/function/moby/atrybuty/{mid}.mcfunction"] = atrybuty_cmds(attrs, True)
        # przywołanie
        fn(f"moby/przywolaj/{mid}", f"""
            summon minecraft:{typ} ~ ~ ~ {{Tags:["dz.nowy"],IsBaby:0b}}
            execute as @e[tag=dz.nowy] run function {NS}:moby/ustaw/{mid}
            particle minecraft:large_smoke ~ ~1 ~ 0.4 0.6 0.4 0.03 15
        """.replace(",IsBaby:0b", ",IsBaby:0b" if typ in ("zombie", "husk") else ""))
        # loot
        jfile(f"data/{NS}/loot_table/moby/{mid}.json", {"type": "minecraft:entity", "pools": loot_pool(LOOT[mid])})
        # advancement: zabicie
        jfile(f"data/{NS}/advancement/zabojstwa/{mid}.json", {
            "criteria": {"zabicie": {"trigger": "minecraft:player_killed_entity", "conditions": {
                "entity": [{"condition": "minecraft:entity_properties", "entity": "this",
                            "predicate": {"nbt": "{Tags:[\"dz.m." + mid + "\"]}"}}]}}},
            "rewards": {"function": f"{NS}:nagrody/zabicie/{mid}"}})
        if mid == "boss":
            continue
        fn(f"nagrody/zabicie/{mid}", f"""
            advancement revoke @s only {NS}:zabojstwa/{mid}
            scoreboard players set #ile dz.data {monety}
            {tellraw("@s", t("⚔ Pokonano: ", "gray"), t(nazwa, kolor, bold=True))}
            function {NS}:nagrody/zabicie/wspolne
        """)

    fn("nagrody/zabicie/wspolne", f"""
        scoreboard players add @s dz.kills 1
        function {NS}:monety/dodaj
        execute if score #event dz.data matches 5 run function {NS}:event/polowanie/punkt
    """)
    fn("nagrody/zabicie/boss", f"""
        advancement revoke @s only {NS}:zabojstwa/boss
        scoreboard players set #boss_zabity dz.data 1
        scoreboard players add @s dz.kills 1
        title @a times 10 80 20
        title @a title {J(t("♛ KRÓL POKONANY! ♛", "gold", bold=True))}
        title @a subtitle {J([t("Ostatni cios: ", "yellow"), sel("@s")])}
        {tellraw("@a", t("♛ ", "gold"), sel("@s"), t(" zadał ostatni cios ", "yellow"), t("Królowi Dziobów", "gold", bold=True), t(" i zgarnia 1000 monet!", "yellow"))}
        scoreboard players set #ile dz.data 1000
        function {NS}:monety/dodaj
        execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
        {firework_cmd("~ ~1 ~", (16766720, 16711680))}
        {firework_cmd("~2 ~1 ~", (16766720, 65535))}
        {firework_cmd("~-2 ~1 ~", (16777215, 16744192))}
    """)

    # ------------------------------------------------------------ losowy mob
    los = ["execute store result score #r dz.data run random value 1..7"]
    for i, mid in enumerate([m for m in wszystkie if m != "boss"], 1):
        los.append(f"execute if score #r dz.data matches {i} run function {NS}:moby/przywolaj/{mid}")
    fn("moby/przywolaj/losowy", "\n".join(los))

    # ------------------------------------------------------------ naturalne spawny
    fn("moby/naturalne/sprawdz", f"""
        # Część naturalnych mobów zamienia się w custom moby (#szansa %)
        tag @s add dz.ch
        execute store result score #r dz.data run random value 1..100
        execute if score #r dz.data > #szansa dz.data run return 0
        execute store result score #r dz.data run random value 1..2
        execute if entity @s[type=zombie] if score #r dz.data matches 1 run return run function {NS}:moby/ustaw/wojownik
        execute if entity @s[type=zombie] run return run function {NS}:moby/ustaw/ognisty
        execute if entity @s[type=husk] run return run function {NS}:moby/ustaw/ognisty
        execute if entity @s[type=skeleton] if score #r dz.data matches 1 run return run function {NS}:moby/ustaw/lucznik
        execute if entity @s[type=skeleton] run return run function {NS}:moby/ustaw/lodowy
        execute if entity @s[type=stray] run return run function {NS}:moby/ustaw/lodowy
        execute if entity @s[type=spider] run return run function {NS}:moby/ustaw/pajak
        execute if entity @s[type=creeper] run return run function {NS}:moby/ustaw/kreeper
        execute if entity @s[type=wither_skeleton] run return run function {NS}:moby/ustaw/widmo
    """)

    fn("moby/sekunda", f"""
        execute as @e[type=#{NS}:konwertowalne,tag=!dz.ch] at @s run function {NS}:moby/naturalne/sprawdz
        execute as @e[tag=dz.mob,tag=!dz.boss] at @s run function {NS}:moby/umiejetnosci
    """)
    fn("moby/umiejetnosci", f"""
        execute if entity @s[tag=dz.m.ognisty] run particle minecraft:flame ~ ~1.2 ~ 0.3 0.5 0.3 0.02 6
        execute if entity @s[tag=dz.m.pajak] run effect give @a[distance=..2.5,gamemode=!creative,gamemode=!spectator] minecraft:poison 4 0
        execute if entity @s[tag=dz.m.pajak] run particle minecraft:item_slime ~ ~0.5 ~ 0.4 0.2 0.4 0 4
        execute if entity @s[tag=dz.m.lodowy] run effect give @a[distance=..4,gamemode=!creative,gamemode=!spectator] minecraft:slowness 2 1
        execute if entity @s[tag=dz.m.lodowy] run particle minecraft:snowflake ~ ~1.2 ~ 0.4 0.6 0.4 0.01 6
        execute if entity @s[tag=dz.m.widmo] run particle minecraft:soul ~ ~1.2 ~ 0.3 0.6 0.3 0.02 3
        execute if entity @s[tag=dz.m.kreeper] run particle minecraft:electric_spark ~ ~0.6 ~ 0.2 0.3 0.2 0.05 3
        execute if entity @s[tag=dz.m.wojownik,tag=!dz.szal] run function {NS}:moby/wojownik_szal
    """)
    fn("moby/wojownik_szal", f"""
        # Ranny wojownik wpada w szał
        execute store result score #hp dz.data run data get entity @s Health
        execute if score #hp dz.data matches 16.. run return 0
        tag @s add dz.szal
        effect give @s minecraft:strength infinite 1
        effect give @s minecraft:speed infinite 0
        particle minecraft:angry_villager ~ ~2 ~ 0.3 0.3 0.3 0 6
        playsound minecraft:entity.ravager.roar hostile @a[distance=..16] ~ ~ ~ 0.8 1.4
    """)

    # ------------------------------------------------------------ boss AI
    fn("moby/boss/tik", f"""
        # Wykonywane co sekundę jako boss
        scoreboard players add #bt dz.data 1
        execute store result bossbar dziobmc:boss value run data get entity @s Health
        particle minecraft:wax_on ~ ~5.4 ~ 0.6 0.2 0.6 0 6
        particle minecraft:soul_fire_flame ~ ~0.2 ~ 1.2 0.1 1.2 0.01 8
        execute unless entity @s[x=-21,y=140,z=-96,dx=42,dy=30,dz=42] run tp @s 0 151 -75
        scoreboard players operation #t dz.data = #bt dz.data
        scoreboard players operation #t dz.data %= #8 dz.data
        execute if score #t dz.data matches 0 run function {NS}:moby/boss/fala
        scoreboard players operation #t dz.data = #bt dz.data
        scoreboard players operation #t dz.data %= #15 dz.data
        execute if score #t dz.data matches 0 run function {NS}:moby/boss/sludzy
        scoreboard players operation #t dz.data = #bt dz.data
        scoreboard players operation #t dz.data %= #11 dz.data
        execute if score #t dz.data matches 0 run function {NS}:moby/boss/piorun
        execute store result score #hp dz.data run data get entity @s Health
        execute if score #hp dz.data matches ..300 unless score #szal dz.data matches 1 run function {NS}:moby/boss/szal
    """)
    fn("moby/boss/fala", f"""
        particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1
        particle minecraft:sweep_attack ~ ~1 ~ 3 0.2 3 0 30
        playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.6
        execute as @a[distance=..7,gamemode=!creative,gamemode=!spectator] run damage @s 8 minecraft:mob_attack by @e[type=husk,tag=dz.boss,limit=1]
        effect give @a[distance=..7,gamemode=!creative,gamemode=!spectator] minecraft:slowness 3 2
        {tellraw("@a[distance=..48]", t("♛ Król Dziobów: ", "gold", bold=True), t("CZUJCIE MOJĄ MOC!", "red"))}
    """)
    fn("moby/boss/sludzy", f"""
        execute store result score #ile_sl dz.data if entity @e[tag=dz.minion]
        execute if score #ile_sl dz.data matches 6.. run return 0
        summon minecraft:zombie ~3 ~ ~ {{Tags:["dz.nowy","dz.minion","dz.event"],IsBaby:0b}}
        summon minecraft:zombie ~-3 ~ ~ {{Tags:["dz.nowy","dz.minion","dz.event"],IsBaby:0b}}
        execute as @e[tag=dz.nowy] run function {NS}:moby/ustaw/wojownik
        particle minecraft:large_smoke ~ ~1 ~ 3 1 3 0.05 60
        playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..48] ~ ~ ~ 1 0.8
        {tellraw("@a[distance=..48]", t("♛ Król Dziobów: ", "gold", bold=True), t("Słudzy, do mnie!", "red"))}
    """)
    fn("moby/boss/piorun", """
        execute as @a[distance=..30,gamemode=!creative,gamemode=!spectator,sort=random,limit=1] at @s run summon minecraft:lightning_bolt ~ ~ ~
    """)
    fn("moby/boss/szal", f"""
        scoreboard players set #szal dz.data 1
        effect give @s minecraft:strength infinite 1
        effect give @s minecraft:speed infinite 0
        bossbar set dziobmc:boss color purple
        title @a[distance=..60] times 5 40 10
        title @a[distance=..60] title {J(t("KRÓL WPADA W SZAŁ!", "dark_red", bold=True))}
        execute as @a[distance=..60] at @s run playsound minecraft:entity.ender_dragon.growl hostile @s ~ ~ ~ 1 0.8
    """)

    # ------------------------------------------------------------ inne loot tables
    def eq(iid, w, mn=1, mx=1, extra=None):
        e = {"type": "minecraft:item", "name": f"minecraft:{iid}", "weight": w,
             "functions": [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": mn, "max": mx}}]}
        if extra:
            e["functions"] += extra
        return e
    enchant = [{"function": "minecraft:enchant_randomly"}]
    jfile(f"data/{NS}/loot_table/drop_party.json", {"type": "minecraft:chest", "pools": [{"rolls": 1, "entries": [
        eq("diamond", 6, 1, 3), eq("gold_ingot", 12, 2, 6), eq("emerald", 10, 1, 4), eq("golden_apple", 6, 1, 2),
        eq("experience_bottle", 10, 4, 12), eq("ender_pearl", 6, 1, 4), eq("iron_ingot", 14, 2, 8),
        eq("cake", 3), eq("firework_rocket", 6, 3, 8), eq("book", 4, 1, 1, enchant), eq("enchanted_golden_apple", 1),
        eq("netherite_scrap", 2), eq("cookie", 8, 4, 16)]}]})
    jfile(f"data/{NS}/loot_table/skrzynia_szczescia.json", {"type": "minecraft:chest", "pools": [
        {"rolls": {"type": "minecraft:uniform", "min": 3, "max": 5}, "entries": [
            eq("diamond", 10, 2, 6), eq("netherite_ingot", 2), eq("enchanted_golden_apple", 2),
            eq("totem_of_undying", 3), eq("golden_apple", 10, 2, 5), eq("emerald_block", 6, 1, 3),
            eq("diamond_sword", 5, 1, 1, enchant), eq("diamond_chestplate", 4, 1, 1, enchant),
            eq("book", 8, 1, 1, enchant), eq("experience_bottle", 10, 16, 32), eq("shulker_shell", 3, 1, 2),
            eq("beacon", 1), eq("elytra", 1)]}]})
    jfile(f"data/{NS}/loot_table/nagroda.json", {"type": "minecraft:chest", "pools": [{"rolls": 1, "entries": [
        eq("diamond", 5, 1, 2), eq("golden_apple", 8, 1, 2), eq("iron_ingot", 12, 4, 10), eq("emerald", 10, 2, 6),
        eq("experience_bottle", 10, 8, 16), eq("ender_pearl", 6, 2, 4), eq("book", 5, 1, 1, enchant)]}]})
