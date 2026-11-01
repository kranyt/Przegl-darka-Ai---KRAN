execute if entity @s[x=-100,y=60,z=-10,dx=74,dy=100,dz=20] run return run function dziobmc:lobby/spadek_parkour
execute in minecraft:overworld run tp @s 0 151 18 180 0
playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1
title @s actionbar {"text":"Uważaj! Spadłeś z wyspy – wracasz na spawn.","color":"red"}
