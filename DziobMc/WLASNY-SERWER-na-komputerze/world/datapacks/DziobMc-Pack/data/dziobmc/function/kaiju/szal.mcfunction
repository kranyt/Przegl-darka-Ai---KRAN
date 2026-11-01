tag @s add dz.szal
effect give @s minecraft:strength infinite 1
effect give @s minecraft:speed infinite 1
title @a[distance=..120] times 5 40 10
title @a[distance=..120] title {"text":"POTWÓR WPADA W SZAŁ!","color":"dark_red","bold":true}
execute as @a[distance=..120] at @s run playsound minecraft:entity.ender_dragon.growl hostile @s ~ ~ ~ 1 0.6
summon minecraft:husk ~3 ~ ~ {Tags:["dz.nowy","dz.minion","dz.event"],IsBaby:0b}
summon minecraft:husk ~-3 ~ ~ {Tags:["dz.nowy","dz.minion","dz.event"],IsBaby:0b}
execute as @e[tag=dz.nowy] run function dziobmc:moby/ustaw/ognisty
