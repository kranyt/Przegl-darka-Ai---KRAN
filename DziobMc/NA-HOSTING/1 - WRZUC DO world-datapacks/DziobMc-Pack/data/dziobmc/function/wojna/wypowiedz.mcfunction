$execute unless data storage dziobmc:kraje lista[{id:$(b)}] run return 0
$execute if score #k$(a) dz.k_wrog matches 1.. run return run tellraw @s {"text":"✖ Twoje państwo już prowadzi wojnę.","color":"red"}
$execute if score #k$(b) dz.k_wrog matches 1.. run return run tellraw @s {"text":"✖ To państwo prowadzi już inną wojnę.","color":"red"}
$execute if score #k$(a) dz.k_pokoj matches 1.. run return run tellraw @s {"text":"✖ Trwa rozejm po ostatniej wojnie (30 min).","color":"red"}
$execute unless score #k$(b) dz.k_czl matches 1.. run return run tellraw @s {"text":"✖ To państwo nie ma mieszkańców.","color":"red"}
$scoreboard players set #k$(a) dz.k_wrog $(b)
$scoreboard players set #k$(b) dz.k_wrog $(a)
$scoreboard players set #k$(a) dz.k_pkt 0
$scoreboard players set #k$(b) dz.k_pkt 0
$scoreboard players set #k$(a) dz.k_wczas 1800
$scoreboard players set #k$(b) dz.k_wczas 1800
title @a times 10 70 20
title @a title [{"text":"⚔ WOJNA! ⚔","color":"dark_red","bold":true}]
$title @a subtitle [$(na),{"text":" wypowiada wojnę ","color":"gray"},$(nb)]
$tellraw @a [{"text":"⚔ ","color":"dark_red"},$(na),{"text":" wypowiada wojnę państwu ","color":"gray"},$(nb),{"text":"! 30 minut, do 15 punktów. Zwycięzca bierze 30% skarbca wroga!","color":"gray"}]
execute as @a at @s run playsound minecraft:event.raid.horn master @s ~ ~ ~ 1 1
