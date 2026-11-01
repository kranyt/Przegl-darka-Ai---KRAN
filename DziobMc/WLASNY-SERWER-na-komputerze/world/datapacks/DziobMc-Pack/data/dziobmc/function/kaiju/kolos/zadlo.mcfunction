damage @s 12 minecraft:mob_attack by @e[type=ravager,tag=dz.kj3,limit=1,sort=nearest]
effect give @s minecraft:poison 8 2
execute at @s run particle minecraft:witch ~ ~1 ~ 0.4 0.6 0.4 0.1 30
execute at @s run playsound minecraft:entity.bee.sting hostile @a[distance=..30] ~ ~ ~ 2 0.5
