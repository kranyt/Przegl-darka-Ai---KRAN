execute unless score #boss_zabity dz.data matches 1 run tellraw @a {"text":"♛ Król Dziobów uciekł z areny... Następnym razem!","color":"gold"}
execute as @e[tag=dz.boss] at @s run function dziobmc:util/usun
execute as @e[tag=dz.minion] at @s run function dziobmc:util/usun
bossbar set dziobmc:boss visible false
scoreboard players set #boss_jest dz.data 0
execute in minecraft:overworld run forceload remove -24 -99 24 -51
