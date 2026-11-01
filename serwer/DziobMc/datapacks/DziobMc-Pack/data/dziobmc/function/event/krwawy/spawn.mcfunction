# Przywołuje 2 losowe custom moby w promieniu ~14 bloków od gracza
summon minecraft:marker ~ ~ ~ {Tags:["dz.pkt"]}
summon minecraft:marker ~ ~ ~ {Tags:["dz.pkt"]}
spreadplayers ~ ~ 1 14 false @e[type=marker,tag=dz.pkt,distance=..1]
execute as @e[type=marker,tag=dz.pkt] at @s run function dziobmc:moby/przywolaj/losowy
kill @e[type=marker,tag=dz.pkt]
