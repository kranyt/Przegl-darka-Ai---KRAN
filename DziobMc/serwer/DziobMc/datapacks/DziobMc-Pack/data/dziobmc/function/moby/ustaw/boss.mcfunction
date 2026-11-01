# Zamienia @s w custom moba: ♛ Król Dziobów ♛
tag @s remove dz.nowy
tag @s add dz.ch
tag @s add dz.mob
tag @s add dz.m.boss
tag @s add dz.boss
tag @s add dz.event
data merge entity @s {CustomName:'{"text":"♛ Król Dziobów ♛","color":"gold","bold":true}',CanPickUpLoot:0b,DeathLootTable:"dziobmc:moby/boss",HandItems:[{id:"minecraft:netherite_axe",count:1},{id:"minecraft:totem_of_undying",count:1}],HandDropChances:[0.0f,0.0f],ArmorItems:[{id:"minecraft:golden_boots",count:1,components:{"minecraft:enchantments":{levels:{"minecraft:protection":4}}}},{id:"minecraft:golden_leggings",count:1,components:{"minecraft:enchantments":{levels:{"minecraft:protection":4}}}},{id:"minecraft:golden_chestplate",count:1,components:{"minecraft:enchantments":{levels:{"minecraft:protection":4}}}},{id:"minecraft:golden_helmet",count:1,components:{"minecraft:enchantments":{levels:{"minecraft:protection":4}}}}],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f],IsBaby:0b,PersistenceRequired:1b,CustomNameVisible:1b,Silent:0b}
function dziobmc:moby/atrybuty/boss
