scoreboard players operation @s dz.coins -= #v dz.data
scoreboard players operation #k16 dz.k_skarb += #v dz.data
tellraw @a[scores={dz.kraj=16}] [{"text":"⛃ ","color":"gold"},{"selector":"@s"},{"text":" wpłacił ","color":"gray"},{"score":{"name":"#v","objective":"dz.data"},"color":"gold","bold":true},{"text":" monet do skarbca. Stan: ","color":"gray"},{"score":{"name":"#k16","objective":"dz.k_skarb"},"color":"yellow","bold":true}]
