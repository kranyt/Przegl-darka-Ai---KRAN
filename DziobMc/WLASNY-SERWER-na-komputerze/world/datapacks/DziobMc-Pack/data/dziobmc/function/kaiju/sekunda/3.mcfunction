scoreboard players add @s dz.kc 1
execute store result bossbar dziobmc:kaiju3 value run data get entity @s Health
bossbar set dziobmc:kaiju3 players @a[distance=..120]
effect give @s minecraft:invisibility infinite 0 true
scoreboard players operation #t dz.data = @s dz.kc

scoreboard players operation #t dz.data %= #6 dz.data
execute if score #t dz.data matches 0 as @p[distance=..14,gamemode=!creative,gamemode=!spectator] run function dziobmc:kaiju/kolos/zadlo
scoreboard players operation #t dz.data = @s dz.kc
scoreboard players operation #t dz.data %= #10 dz.data
execute if score #t dz.data matches 5 run function dziobmc:kaiju/kolos/burza
scoreboard players operation #t dz.data = @s dz.kc
scoreboard players operation #t dz.data %= #15 dz.data
execute if score #t dz.data matches 8 run function dziobmc:kaiju/kolos/skorpionki
execute store result score #hp dz.data run data get entity @s Health
execute if score #hp dz.data matches ..900 unless entity @s[tag=dz.szal] run function dziobmc:kaiju/szal
