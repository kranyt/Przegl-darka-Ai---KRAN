scoreboard players operation #v dz.data = @s wojna
scoreboard players set @s wojna 0
execute if score #v dz.data matches 1 run function dziobmc:wojna/menu
execute if score #v dz.data matches 999 if entity @s[tag=dz.wladca] run function dziobmc:wojna/kapitulacja
execute if score #v dz.data matches 1001.. if entity @s[tag=dz.wladca] run function dziobmc:wojna/wypowiedz_v
