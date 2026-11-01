execute unless score #kaiju_zabity dz.data matches 1 if entity @e[type=ravager,tag=dz.kaiju] run tellraw @a {"text":"☠ Potwór odchodzi w głąb lądu... Tym razem przetrwał.","color":"gray"}
execute as @e[type=ravager,tag=dz.kaiju] at @s run function dziobmc:util/usun
function dziobmc:kaiju/forceload_usun_m with storage dziobmc:tmp ka
scoreboard players set #kaiju_jest dz.data 0
