scoreboard players add #krok dz.data 1
particle minecraft:soul_fire_flame ~ ~ ~ 0.3 0.3 0.3 0.02 6 force
particle minecraft:electric_spark ~ ~ ~ 0.4 0.4 0.4 0.1 4 force
particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.02 2 force
execute as @a[distance=..2.5,gamemode=!creative,gamemode=!spectator] run damage @s 14 minecraft:mob_attack by @e[type=ravager,tag=dz.kj1,limit=1,sort=nearest]
execute as @a[distance=..2.5,gamemode=!creative,gamemode=!spectator] run effect give @s minecraft:wither 4 1
execute if score #krok dz.data matches ..60 positioned ^ ^ ^1 run function dziobmc:kaiju/dziobzilla/promien
