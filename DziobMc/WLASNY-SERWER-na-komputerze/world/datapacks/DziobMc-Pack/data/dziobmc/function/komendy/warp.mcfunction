execute if score @s warp matches 11 in minecraft:overworld run tp @s 0 151 18 180 0
execute if score @s warp matches 12 in minecraft:overworld run tp @s 0 151 -57 180 0
execute if score @s warp matches 13 in minecraft:overworld run tp @s -29 151 0 90 0
execute if score @s warp matches 14 in minecraft:overworld run tp @s 0 151 50 0 0
execute if score @s warp matches 11..14 at @s run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
execute if score @s warp matches 1 run function dziobmc:komendy/menu_warp
scoreboard players set @s warp 0
