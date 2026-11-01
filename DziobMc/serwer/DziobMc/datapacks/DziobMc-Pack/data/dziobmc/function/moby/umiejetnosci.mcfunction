execute if entity @s[tag=dz.m.ognisty] run particle minecraft:flame ~ ~1.2 ~ 0.3 0.5 0.3 0.02 6
execute if entity @s[tag=dz.m.pajak] run effect give @a[distance=..2.5,gamemode=!creative,gamemode=!spectator] minecraft:poison 4 0
execute if entity @s[tag=dz.m.pajak] run particle minecraft:item_slime ~ ~0.5 ~ 0.4 0.2 0.4 0 4
execute if entity @s[tag=dz.m.lodowy] run effect give @a[distance=..4,gamemode=!creative,gamemode=!spectator] minecraft:slowness 2 1
execute if entity @s[tag=dz.m.lodowy] run particle minecraft:snowflake ~ ~1.2 ~ 0.4 0.6 0.4 0.01 6
execute if entity @s[tag=dz.m.widmo] run particle minecraft:soul ~ ~1.2 ~ 0.3 0.6 0.3 0.02 3
execute if entity @s[tag=dz.m.kreeper] run particle minecraft:electric_spark ~ ~0.6 ~ 0.2 0.3 0.2 0.05 3
execute if entity @s[tag=dz.m.wojownik,tag=!dz.szal] run function dziobmc:moby/wojownik_szal
