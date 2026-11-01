particle minecraft:explosion_emitter ~ ~ ~ 4 0 4 0 4 force
particle minecraft:campfire_cosy_smoke ~ ~0.5 ~ 6 0.2 6 0.02 60 force
playsound minecraft:entity.generic.explode hostile @a[distance=..80] ~ ~ ~ 2 0.5
playsound minecraft:entity.ravager.stunned hostile @a[distance=..80] ~ ~ ~ 2 0.5
execute as @a[distance=..10,gamemode=!creative,gamemode=!spectator] run damage @s 10 minecraft:mob_attack by @e[type=ravager,tag=dz.kaiju,limit=1,sort=nearest]
effect give @a[distance=..10,gamemode=!creative,gamemode=!spectator] minecraft:levitation 1 8 true
effect give @a[distance=..14,gamemode=!creative,gamemode=!spectator] minecraft:slowness 3 2
