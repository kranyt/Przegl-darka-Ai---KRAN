# Zamienia @s w custom moba: ☠ Widmowy Rycerz
tag @s remove dz.nowy
tag @s add dz.ch
tag @s add dz.mob
tag @s add dz.m.widmo
data merge entity @s {CustomName:'{"text":"☠ Widmowy Rycerz","color":"dark_purple","bold":true}',CanPickUpLoot:0b,DeathLootTable:"dziobmc:moby/widmo",HandItems:[{id:"minecraft:netherite_sword",count:1,components:{"minecraft:enchantments":{levels:{"minecraft:sharpness":1}}}},{}],HandDropChances:[0.0f,0.0f],ArmorItems:[{},{},{id:"minecraft:netherite_chestplate",count:1},{id:"minecraft:netherite_helmet",count:1}],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f],Glowing:1b}
function dziobmc:moby/atrybuty/widmo
