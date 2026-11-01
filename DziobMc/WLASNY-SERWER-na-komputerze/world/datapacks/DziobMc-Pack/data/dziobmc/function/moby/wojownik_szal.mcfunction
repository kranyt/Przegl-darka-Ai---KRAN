# Ranny wojownik wpada w szał
execute store result score #hp dz.data run data get entity @s Health
execute if score #hp dz.data matches 16.. run return 0
tag @s add dz.szal
effect give @s minecraft:strength infinite 1
effect give @s minecraft:speed infinite 0
particle minecraft:angry_villager ~ ~2 ~ 0.3 0.3 0.3 0 6
playsound minecraft:entity.ravager.roar hostile @a[distance=..16] ~ ~ ~ 0.8 1.4
