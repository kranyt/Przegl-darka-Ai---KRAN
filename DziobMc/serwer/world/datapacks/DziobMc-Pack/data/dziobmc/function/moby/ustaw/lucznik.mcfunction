# Zamienia @s w custom moba: ➶ Mroczny Łucznik
tag @s remove dz.nowy
tag @s add dz.ch
tag @s add dz.mob
tag @s add dz.m.lucznik
data merge entity @s {CustomName:'{"text":"➶ Mroczny Łucznik","color":"dark_gray","bold":true}',CanPickUpLoot:0b,DeathLootTable:"dziobmc:moby/lucznik",HandItems:[{id:"minecraft:bow",count:1,components:{"minecraft:enchantments":{levels:{"minecraft:power":3}}}},{}],HandDropChances:[0.0f,0.0f],ArmorItems:[{id:"minecraft:leather_boots",count:1,components:{"minecraft:dyed_color":{rgb:1644825}}},{id:"minecraft:leather_leggings",count:1,components:{"minecraft:dyed_color":{rgb:1644825}}},{id:"minecraft:leather_chestplate",count:1,components:{"minecraft:dyed_color":{rgb:1644825}}},{id:"minecraft:leather_helmet",count:1,components:{"minecraft:dyed_color":{rgb:1644825}}}],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f]}
function dziobmc:moby/atrybuty/lucznik
