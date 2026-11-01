scoreboard players add @s dz.kc 1
execute store result bossbar dziobmc:kaiju1 value run data get entity @s Health
bossbar set dziobmc:kaiju1 players @a[distance=..120]
effect give @s minecraft:invisibility infinite 0 true
scoreboard players operation #t dz.data = @s dz.kc

scoreboard players operation #t dz.data %= #2 dz.data
execute if score #t dz.data matches 0 run function dziobmc:kaiju/anim/1l
execute if score #t dz.data matches 1 run function dziobmc:kaiju/anim/1p
scoreboard players operation #t dz.data = @s dz.kc
scoreboard players operation #t dz.data %= #12 dz.data
execute if score #t dz.data matches 10 run function dziobmc:kaiju/dziobzilla/ladowanie
execute if score #t dz.data matches 0 run function dziobmc:kaiju/dziobzilla/oddech
scoreboard players operation #t dz.data = @s dz.kc
scoreboard players operation #t dz.data %= #8 dz.data
execute if score #t dz.data matches 4 run function dziobmc:kaiju/tupniecie
scoreboard players operation #t dz.data = @s dz.kc
scoreboard players operation #t dz.data %= #6 dz.data
execute if score #t dz.data matches 2 positioned ^ ^ ^-10 as @a[distance=..7,gamemode=!creative,gamemode=!spectator] run function dziobmc:kaiju/dziobzilla/ogon
execute if score #t dz.data matches 2 positioned ^ ^2 ^-10 run particle minecraft:sweep_attack ~ ~ ~ 3 1 3 0 12
execute store result score #hp dz.data run data get entity @s Health
execute if score #hp dz.data matches ..1250 unless entity @s[tag=dz.szal] run function dziobmc:kaiju/szal
