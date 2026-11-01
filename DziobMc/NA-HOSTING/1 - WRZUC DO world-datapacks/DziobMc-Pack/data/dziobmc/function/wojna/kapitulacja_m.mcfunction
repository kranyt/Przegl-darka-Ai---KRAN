$execute unless score #k$(l) dz.k_wrog matches 1.. run return run tellraw @s {"text":"✖ Twoje państwo nie prowadzi wojny.","color":"red"}
$execute store result storage dziobmc:tmp c.w int 1 run scoreboard players get #k$(l) dz.k_wrog
tellraw @a [{"text":"⚑ ","color":"white"},{"text":"Państwo kapituluje!","color":"gray"}]
function dziobmc:wojna/kapitulacja_m2 with storage dziobmc:tmp c
