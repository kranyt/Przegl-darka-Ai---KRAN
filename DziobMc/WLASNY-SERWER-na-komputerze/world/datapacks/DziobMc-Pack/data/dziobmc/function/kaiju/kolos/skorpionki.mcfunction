execute store result score #ile_sl dz.data if entity @e[type=cave_spider,tag=dz.minion,distance=..40]
execute if score #ile_sl dz.data matches 6.. run return 0
summon minecraft:cave_spider ~2 ~ ~2 {Tags:["dz.minion","dz.event"],CustomName:'{"text":"Skorpionek","color":"gold"}'}
summon minecraft:cave_spider ~-2 ~ ~2 {Tags:["dz.minion","dz.event"],CustomName:'{"text":"Skorpionek","color":"gold"}'}
summon minecraft:cave_spider ~ ~ ~-3 {Tags:["dz.minion","dz.event"],CustomName:'{"text":"Skorpionek","color":"gold"}'}
