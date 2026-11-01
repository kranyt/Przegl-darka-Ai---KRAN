execute store result score #ile_sl dz.data if entity @e[tag=dz.minion]
execute if score #ile_sl dz.data matches 6.. run return 0
summon minecraft:zombie ~3 ~ ~ {Tags:["dz.nowy","dz.minion","dz.event"],IsBaby:0b}
summon minecraft:zombie ~-3 ~ ~ {Tags:["dz.nowy","dz.minion","dz.event"],IsBaby:0b}
execute as @e[tag=dz.nowy] run function dziobmc:moby/ustaw/wojownik
particle minecraft:large_smoke ~ ~1 ~ 3 1 3 0.05 60
playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..48] ~ ~ ~ 1 0.8
tellraw @a[distance=..48] [{"text":"♛ Król Dziobów: ","color":"gold","bold":true},{"text":"Słudzy, do mnie!","color":"red"}]
