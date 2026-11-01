execute if score #k14 dz.k_skarb < #v dz.data run return run tellraw @s {"text":"✖ W skarbcu jest za mało monet.","color":"red"}
scoreboard players operation #k14 dz.k_skarb -= #v dz.data
scoreboard players operation @s dz.coins += #v dz.data
tellraw @a[scores={dz.kraj=14}] [{"text":"⛃ Władca ","color":"gold"},{"selector":"@s"},{"text":" wypłacił ","color":"gray"},{"score":{"name":"#v","objective":"dz.data"},"color":"gold","bold":true},{"text":" monet ze skarbca.","color":"gray"}]
