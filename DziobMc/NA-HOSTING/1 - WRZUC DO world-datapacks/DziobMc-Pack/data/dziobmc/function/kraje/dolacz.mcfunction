# #v = id państwa
execute if score @s dz.kid matches 1.. run return run tellraw @s [{"text":"✖ Najpierw opuść swoje państwo: ","color":"red"},{"text":"[OPUŚĆ]","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/trigger panstwo set 999"}}]
execute store result storage dziobmc:tmp j.id int 1 run scoreboard players get #v dz.data
function dziobmc:kraje/dolacz_m with storage dziobmc:tmp j
