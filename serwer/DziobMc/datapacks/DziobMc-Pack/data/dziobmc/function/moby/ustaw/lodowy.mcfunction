# Zamienia @s w custom moba: ❄ Lodowy Strażnik
tag @s remove dz.nowy
tag @s add dz.ch
tag @s add dz.mob
tag @s add dz.m.lodowy
data merge entity @s {CustomName:'{"text":"❄ Lodowy Strażnik","color":"aqua","bold":true}',CanPickUpLoot:0b,DeathLootTable:"dziobmc:moby/lodowy",HandItems:[{id:"minecraft:bow",count:1,components:{"minecraft:enchantments":{levels:{"minecraft:punch":2}}}},{}],HandDropChances:[0.0f,0.0f],ArmorItems:[{id:"minecraft:leather_boots",count:1,components:{"minecraft:dyed_color":{rgb:11393254}}},{},{id:"minecraft:chainmail_chestplate",count:1},{id:"minecraft:packed_ice",count:1}],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f]}
function dziobmc:moby/atrybuty/lodowy
