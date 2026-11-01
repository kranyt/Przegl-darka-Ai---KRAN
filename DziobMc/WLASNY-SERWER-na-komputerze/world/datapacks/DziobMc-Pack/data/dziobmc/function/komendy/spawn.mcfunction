scoreboard players set @s spawn 0
scoreboard players add @s dz.cd_spawn 0
scoreboard players set #cd dz.data 200
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_spawn
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_spawn = #teraz dz.data
execute in minecraft:overworld run tp @s 0 151 18 180 0
execute at @s run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
execute at @s run particle minecraft:portal ~ ~1 ~ 0.4 0.8 0.4 0.5 60
title @s actionbar {"text":"✦ Witaj na spawnie DziobMc!","color":"gold"}
