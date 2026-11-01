"""PvP: arena, nagrody za zabójstwa graczy, serie zabójstw, strefy."""
from wspolne import NS, J, t, sc, sel, tellraw, fn, firework_cmd


def build():
    fn("pvp/zabojstwo", f"""
        # Gracz zabił innego gracza (wywoływane co sekundę, gdy dz.zab >= 1)
        scoreboard players remove @s dz.zab 1
        scoreboard players add @s dz.streak 1
        scoreboard players set #ile dz.data 25
        execute if score #event dz.data matches 7 run scoreboard players set #ile dz.data 100
        execute if score #event dz.data matches 7 run scoreboard players add @s dz.bitwa 1
        {tellraw("@s", t("⚔ Zabójstwo gracza! ", "red", bold=True), t("Seria: ", "gray"), sc("@s", "dz.streak", "yellow", True))}
        function {NS}:monety/dodaj
        playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.8
        execute if score @s dz.streak matches 3 run {tellraw("@a", t("⚔ ", "red"), sel("@s"), t(" ma serię ", "gold"), t("3 zabójstw", "red", bold=True), t("!", "gold"))}
        execute if score @s dz.streak matches 5 run function {NS}:pvp/seria5
        execute if score @s dz.streak matches 10 run function {NS}:pvp/seria10
        execute if score @s dz.zab matches 1.. run function {NS}:pvp/zabojstwo
    """)
    fn("pvp/seria5", f"""
        {tellraw("@a", t("⚔ ", "red"), sel("@s"), t(" jest NIE DO ZATRZYMANIA! ", "gold", bold=True), t("(seria 5) +50 monet", "yellow"))}
        execute as @a at @s run playsound minecraft:entity.wither.ambient master @s ~ ~ ~ 0.5 1.5
        scoreboard players set #ile dz.data 50
        function {NS}:monety/dodaj
        effect give @s minecraft:glowing 30 0 true
    """)
    fn("pvp/seria10", f"""
        title @a times 5 50 15
        title @a title {J(t("LEGENDARNA SERIA!", "dark_red", bold=True))}
        title @a subtitle {J([sel("@s"), t(" ma 10 zabójstw z rzędu!", "gold")])}
        execute as @a at @s run playsound minecraft:entity.ender_dragon.growl master @s ~ ~ ~ 0.6 1.2
        scoreboard players set #ile dz.data 200
        function {NS}:monety/dodaj
        {firework_cmd(colors=(16711680, 16766720))}
    """)
    fn("pvp/smierc", f"""
        # Gracz zginął – reset serii
        scoreboard players set @s dz.smierc 0
        execute if score @s dz.streak matches 5.. run {tellraw("@a", t("☠ Seria gracza ", "gray"), sel("@s"), t(" (", "gray"), sc("@s", "dz.streak", "red", True), t(") została przerwana!", "gray"))}
        scoreboard players set @s dz.streak 0
    """)
    fn("pvp/wejscie", f"""
        tag @s add dz.pvp_bylo
        title @s times 5 30 10
        title @s title {J(t("⚔ STREFA PvP ⚔", "red", bold=True))}
        title @s subtitle {J(t("Walczysz swoim ekwipunkiem – po śmierci go tracisz!", "gray"))}
        playsound minecraft:item.armor.equip_netherite master @s ~ ~ ~ 1 0.8
        {tellraw("@s", t("⚔ Strefa PvP! ", "red", bold=True), t("Kit PvP: ", "gray"), t("[ODBIERZ]", "green", bold=True, run="/trigger kit set 15", hover=t("Kit PvP co 5 minut")), t("  •  25 monet za kill, serie 3/5/10!", "gray"))}
    """)
    fn("pvp/wyjscie", f"""
        tag @s remove dz.pvp_bylo
        title @s actionbar {J(t("✔ Jesteś w strefie bezpiecznej", "green"))}
    """)
