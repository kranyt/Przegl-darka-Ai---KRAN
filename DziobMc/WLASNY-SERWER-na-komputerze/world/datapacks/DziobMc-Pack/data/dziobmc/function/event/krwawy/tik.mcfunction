time set 18000
execute as @a[tag=!dz.lobby] at @s run particle minecraft:crimson_spore ~ ~1 ~ 8 4 8 0 60
scoreboard players operation #t dz.data = #left dz.data
scoreboard players operation #t dz.data %= #10 dz.data
execute if score #t dz.data matches 0 as @a[gamemode=survival,tag=!dz.lobby] at @s if dimension minecraft:overworld run function dziobmc:event/krwawy/spawn
