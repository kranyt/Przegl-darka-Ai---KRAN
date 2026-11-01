scoreboard players add #n dz.data 1
scoreboard players operation #id dz.data = #k dz.data
scoreboard players operation #id dz.data *= #1000 dz.data
scoreboard players operation #id dz.data += #n dz.data
execute store result storage dziobmc:tmp wn.id int 1 run scoreboard players get #id dz.data
execute store result storage dziobmc:tmp wn.k int 1 run scoreboard players get #k dz.data
execute store result storage dziobmc:tmp wn.n int 1 run scoreboard players get #n dz.data
scoreboard players set #zal dz.data 200000
scoreboard players operation #zal dz.data += #k dz.data
execute store result storage dziobmc:tmp wn.zal int 1 run scoreboard players get #zal dz.data
execute if score #n dz.data matches 999.. run return 0
function dziobmc:kraje/wolny_n_spr with storage dziobmc:tmp wn
