scoreboard players add @s dz.kc 1
execute store result bossbar dziobmc:kaiju2 value run data get entity @s Health
bossbar set dziobmc:kaiju2 players @a[distance=..120]
effect give @s minecraft:invisibility infinite 0 true
scoreboard players operation #t dz.data = @s dz.kc

effect give @a[distance=..14,gamemode=!creative,gamemode=!spectator] minecraft:slowness 2 1 true
effect give @a[distance=..14,gamemode=!creative,gamemode=!spectator] minecraft:mining_fatigue 2 1 true
particle minecraft:snowflake ~ ~8 ~ 8 6 8 0.02 80 force
scoreboard players operation #t dz.data %= #10 dz.data
execute if score #t dz.data matches 0 as @a[distance=..35,gamemode=!creative,gamemode=!spectator,sort=random,limit=4] at @s run function dziobmc:kaiju/tytan/lod
scoreboard players operation #t dz.data = @s dz.kc
scoreboard players operation #t dz.data %= #7 dz.data
execute if score #t dz.data matches 3 run function dziobmc:kaiju/tytan/piesci
execute store result score #hp dz.data run data get entity @s Health
execute if score #hp dz.data matches ..1000 unless entity @s[tag=dz.szal] run function dziobmc:kaiju/szal
