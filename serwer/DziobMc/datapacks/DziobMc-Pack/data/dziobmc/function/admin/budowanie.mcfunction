execute if entity @s[tag=dz.build] run return run function dziobmc:admin/budowanie_off
tag @s add dz.build
gamemode creative @s
tellraw @s {"text":"✔ Tryb budowania WŁĄCZONY","color":"green","bold":true}
