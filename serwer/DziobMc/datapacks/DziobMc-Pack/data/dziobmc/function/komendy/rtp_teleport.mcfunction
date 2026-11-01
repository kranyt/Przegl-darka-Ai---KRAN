scoreboard players add @s dz.cd_rtp 0
scoreboard players set #cd dz.data 1200
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_rtp
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_rtp = #teraz dz.data
tag @s remove dz.lobby
gamemode survival @s[gamemode=adventure,tag=!dz.build]
title @s actionbar {"text":"✦ Szukam bezpiecznego miejsca...","color":"light_purple"}
execute in minecraft:overworld run spreadplayers 0 0 1 3000 false @s
effect give @s minecraft:resistance 5 4 true
effect give @s minecraft:slow_falling 6 0 true
execute at @s run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 0.8
title @s times 5 40 10
title @s title {"text":"✦ Losowy teleport ✦","color":"light_purple","bold":true}
title @s subtitle {"text":"Powodzenia w przygodzie!","color":"gray"}
