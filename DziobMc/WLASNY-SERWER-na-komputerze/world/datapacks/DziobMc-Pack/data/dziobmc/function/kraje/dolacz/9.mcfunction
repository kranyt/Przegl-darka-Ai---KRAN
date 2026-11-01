execute if score @s dz.kraj matches 1.. run return run tellraw @s [{"text":"✖ Najpierw opuść swoje państwo: ","color":"red"},{"text":"[OPUŚĆ]","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/trigger panstwo set 999"}}]
execute if score #k9 dz.k_zamk matches 1 if score #k9 dz.k_wl matches 1 run return run function dziobmc:kraje/prosba/9
function dziobmc:kraje/wejdz/9
