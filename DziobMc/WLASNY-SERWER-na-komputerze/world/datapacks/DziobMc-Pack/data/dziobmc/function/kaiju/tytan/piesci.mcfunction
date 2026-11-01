execute as @e[type=block_display,tag=dz.kp2,tag=dz.rekaP,distance=..64] run data merge entity @s {start_interpolation:0,interpolation_duration:6}
function dziobmc:kaiju/tupniecie
particle minecraft:item_snowball ~ ~1 ~ 6 0.5 6 0.2 120 force
effect give @a[distance=..10,gamemode=!creative,gamemode=!spectator] minecraft:slowness 5 4
