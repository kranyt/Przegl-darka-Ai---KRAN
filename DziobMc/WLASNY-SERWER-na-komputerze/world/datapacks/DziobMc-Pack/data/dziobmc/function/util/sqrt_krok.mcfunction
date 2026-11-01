scoreboard players operation #q dz.data = #n dz.data
scoreboard players operation #q dz.data /= #r dz.data
scoreboard players operation #r dz.data += #q dz.data
scoreboard players operation #r dz.data /= #2 dz.data
execute if score #r dz.data matches ..0 run scoreboard players set #r dz.data 1
