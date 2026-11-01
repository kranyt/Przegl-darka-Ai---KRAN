execute unless score #event dz.data matches 8 run return 0
function dziobmc:kaiju/atak_spawn_m with storage dziobmc:tmp ka
execute as @e[type=marker,tag=dz.kpkt] at @s if score #kaiju_typ dz.data matches 1 run function dziobmc:kaiju/przywolaj/1
execute as @e[type=marker,tag=dz.kpkt] at @s if score #kaiju_typ dz.data matches 2 run function dziobmc:kaiju/przywolaj/2
execute as @e[type=marker,tag=dz.kpkt] at @s if score #kaiju_typ dz.data matches 3 run function dziobmc:kaiju/przywolaj/3
kill @e[type=marker,tag=dz.kpkt]
execute if entity @e[type=ravager,tag=dz.kaiju] run scoreboard players set #kaiju_jest dz.data 1
execute unless entity @e[type=ravager,tag=dz.kaiju] run schedule function dziobmc:kaiju/atak_spawn 40t replace
