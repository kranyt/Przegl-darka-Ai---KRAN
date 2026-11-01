# #k = kraj bazowy; zakłada państwo o najniższym wolnym numerze i robi gracza władcą
execute if score @s dz.kid matches 1.. run return run tellraw @s [{"text":"✖ Najpierw opuść swoje państwo: ","color":"red"},{"text":"[OPUŚĆ]","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/trigger panstwo set 999"}}]
function dziobmc:kraje/wolny_n
execute if score #n dz.data matches 999.. run return run tellraw @s {"text":"✖ Za dużo państw tego kraju.","color":"red"}
function dziobmc:kraje/zaloz_m with storage dziobmc:tmp wn
