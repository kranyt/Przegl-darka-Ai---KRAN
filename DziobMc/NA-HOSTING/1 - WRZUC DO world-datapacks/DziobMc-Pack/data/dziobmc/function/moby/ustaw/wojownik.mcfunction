# Zamienia @s w custom moba: ⚔ Dziobak Wojownik
tag @s remove dz.nowy
tag @s add dz.ch
tag @s add dz.mob
tag @s add dz.m.wojownik
data merge entity @s {CustomName:'{"text":"⚔ Dziobak Wojownik","color":"gold","bold":true}',CanPickUpLoot:0b,DeathLootTable:"dziobmc:moby/wojownik",HandItems:[{id:"minecraft:iron_sword",count:1},{}],HandDropChances:[0.0f,0.0f],ArmorItems:[{id:"minecraft:iron_boots",count:1},{id:"minecraft:iron_leggings",count:1},{id:"minecraft:iron_chestplate",count:1},{id:"minecraft:golden_helmet",count:1}],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f],IsBaby:0b}
function dziobmc:moby/atrybuty/wojownik
