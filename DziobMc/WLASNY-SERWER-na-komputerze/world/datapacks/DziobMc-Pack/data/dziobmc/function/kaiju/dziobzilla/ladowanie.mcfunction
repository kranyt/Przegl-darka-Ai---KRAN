execute as @e[type=block_display,tag=dz.kp1,tag=dz.pletwa,distance=..64] run data merge entity @s {block_state:{Name:"minecraft:sea_lantern"},brightness:{sky:15,block:15},Glowing:1b}
playsound minecraft:block.beacon.power_select hostile @a[distance=..80] ~ ~ ~ 2 0.5
particle minecraft:electric_spark ~ ~12 ~ 2 4 2 0.2 80 force
