execute if score #boss_jest dz.data matches 1 unless entity @e[type=husk,tag=dz.boss] run return run function dziobmc:event/koniec
execute in minecraft:overworld positioned 0 151 -75 run bossbar set dziobmc:boss players @a[distance=..70]
execute as @e[type=husk,tag=dz.boss] at @s run function dziobmc:moby/boss/tik
