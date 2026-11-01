# Wykonywane co sekundę jako boss
scoreboard players add #bt dz.data 1
execute store result bossbar dziobmc:boss value run data get entity @s Health
particle minecraft:wax_on ~ ~5.4 ~ 0.6 0.2 0.6 0 6
particle minecraft:soul_fire_flame ~ ~0.2 ~ 1.2 0.1 1.2 0.01 8
execute unless entity @s[x=-21,y=140,z=-96,dx=42,dy=30,dz=42] run tp @s 0 151 -75
scoreboard players operation #t dz.data = #bt dz.data
scoreboard players operation #t dz.data %= #8 dz.data
execute if score #t dz.data matches 0 run function dziobmc:moby/boss/fala
scoreboard players operation #t dz.data = #bt dz.data
scoreboard players operation #t dz.data %= #15 dz.data
execute if score #t dz.data matches 0 run function dziobmc:moby/boss/sludzy
scoreboard players operation #t dz.data = #bt dz.data
scoreboard players operation #t dz.data %= #11 dz.data
execute if score #t dz.data matches 0 run function dziobmc:moby/boss/piorun
execute store result score #hp dz.data run data get entity @s Health
execute if score #hp dz.data matches ..300 unless score #szal dz.data matches 1 run function dziobmc:moby/boss/szal
