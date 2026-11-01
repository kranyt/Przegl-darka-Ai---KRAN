execute unless score #event dz.data matches 3 run return 0
execute in minecraft:overworld positioned 0 151 -75 run function dziobmc:moby/przywolaj/boss
execute unless entity @e[type=husk,tag=dz.boss] run return run schedule function dziobmc:event/boss/przywolaj 40t replace
scoreboard players set #boss_jest dz.data 1
bossbar set dziobmc:boss color red
bossbar set dziobmc:boss visible true
execute in minecraft:overworld run particle minecraft:explosion_emitter 0 153 -75 2 1 2 0 6 force
execute as @a at @s run playsound minecraft:entity.wither.spawn master @s ~ ~ ~ 0.8 0.8
tellraw @a [{"text":"♛ Król Dziobów ","color":"gold","bold":true},{"text":"pojawił się na arenie! ","color":"red"},{"text":"[WALCZ]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/trigger warp set 12"},"hoverEvent":{"action":"show_text","contents":{"text":"Teleport na arenę"}}}]
