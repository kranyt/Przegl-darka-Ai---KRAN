$execute in minecraft:ziemia as @a[x=$(x0),y=-64,z=$(z0),dx=128,dy=400,dz=128] unless score @s dz.kid matches $(id) unless score @s dz.mojwrog matches $(id) run tag @s add dz.strefa_obca
$execute if score #k$(id) dz.k_pokoj matches 1.. run scoreboard players remove #k$(id) dz.k_pokoj 1
$execute if score #k$(id) dz.k_wrog matches 1.. run function dziobmc:wojna/tik {id:$(id)}
