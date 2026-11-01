# Zamienia @s w custom moba: ☄ Ognisty Dziob
tag @s remove dz.nowy
tag @s add dz.ch
tag @s add dz.mob
tag @s add dz.m.ognisty
data merge entity @s {CustomName:'{"text":"☄ Ognisty Dziob","color":"red","bold":true}',CanPickUpLoot:0b,DeathLootTable:"dziobmc:moby/ognisty",HandItems:[{id:"minecraft:golden_sword",count:1,components:{"minecraft:enchantments":{levels:{"minecraft:fire_aspect":2}}}},{}],HandDropChances:[0.0f,0.0f],ArmorItems:[{id:"minecraft:golden_boots",count:1},{},{id:"minecraft:golden_chestplate",count:1},{id:"minecraft:magma_block",count:1}],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f],IsBaby:0b,active_effects:[{id:"minecraft:fire_resistance",amplifier:0b,duration:-1,show_particles:0b}]}
function dziobmc:moby/atrybuty/ognisty
