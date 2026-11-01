particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1
particle minecraft:sweep_attack ~ ~1 ~ 3 0.2 3 0 30
playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 1 0.6
execute as @a[distance=..7,gamemode=!creative,gamemode=!spectator] run damage @s 8 minecraft:mob_attack by @e[type=husk,tag=dz.boss,limit=1]
effect give @a[distance=..7,gamemode=!creative,gamemode=!spectator] minecraft:slowness 3 2
tellraw @a[distance=..48] [{"text":"♛ Król Dziobów: ","color":"gold","bold":true},{"text":"CZUJCIE MOJĄ MOC!","color":"red"}]
