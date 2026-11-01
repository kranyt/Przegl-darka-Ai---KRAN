scoreboard players set #szal dz.data 1
effect give @s minecraft:strength infinite 1
effect give @s minecraft:speed infinite 0
bossbar set dziobmc:boss color purple
title @a[distance=..60] times 5 40 10
title @a[distance=..60] title {"text":"KRÓL WPADA W SZAŁ!","color":"dark_red","bold":true}
execute as @a[distance=..60] at @s run playsound minecraft:entity.ender_dragon.growl hostile @s ~ ~ ~ 1 0.8
