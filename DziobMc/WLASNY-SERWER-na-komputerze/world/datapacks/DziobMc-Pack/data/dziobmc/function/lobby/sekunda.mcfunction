# Strefa lobby: x/z -110..110, y 140..220 (świat zwykły)
tag @a remove dz.lobby
execute in minecraft:overworld run tag @a[x=-110,y=140,z=-110,dx=220,dy=80,dz=220] add dz.lobby
function dziobmc:ziemia/strefy
gamemode adventure @a[tag=dz.lobby,gamemode=survival,tag=!dz.build]
gamemode survival @a[tag=!dz.lobby,tag=!dz.strefa_obca,gamemode=adventure,tag=!dz.build]
# Strefy: arena PvP i arena bossa = walka; reszta lobby = bezpieczna (Resistance V)
tag @a remove dz.pvp_strefa
tag @a remove dz.boss_strefa
execute in minecraft:overworld run tag @a[x=-20,y=140,z=55,dx=40,dy=40,dz=40] add dz.pvp_strefa
execute in minecraft:overworld run tag @a[x=-21,y=140,z=-96,dx=42,dy=40,dz=42] add dz.boss_strefa
execute as @a[tag=dz.pvp_strefa,tag=!dz.pvp_bylo] at @s run function dziobmc:pvp/wejscie
execute as @a[tag=!dz.pvp_strefa,tag=dz.pvp_bylo] run function dziobmc:pvp/wyjscie
effect give @a[tag=dz.lobby,tag=!dz.pvp_strefa,tag=!dz.boss_strefa] minecraft:resistance 2 4 true
effect give @a[tag=dz.lobby,tag=!dz.pvp_strefa,tag=!dz.boss_strefa] minecraft:saturation 2 0 true
# Wrogie moby nie mają wstępu do lobby
execute in minecraft:overworld as @e[x=-110,y=128,z=-110,dx=220,dy=92,dz=220,type=#dziobmc:wrogie,tag=!dz.event] at @s run function dziobmc:util/usun
# Portal losowego teleportu
execute in minecraft:overworld run particle minecraft:portal 20 153 0 0.2 1.3 1.6 0.6 50 force
execute in minecraft:overworld run particle minecraft:end_rod 20 153 0 0.1 1.3 1.6 0.01 3 force
execute in minecraft:overworld as @a[x=19,y=151,z=-2,dx=1,dy=3,dz=4,tag=!dz.build] at @s run function dziobmc:ziemia/rtp
# Meta parkouru
execute as @a[tag=dz.lobby] at @s if block ~ ~-1 ~ minecraft:emerald_block run function dziobmc:lobby/parkour_meta
