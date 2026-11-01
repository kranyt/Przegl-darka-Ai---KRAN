scoreboard players add @s dz.cd_stol 0
scoreboard players set #cd dz.data 600
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_stol
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_stol = #teraz dz.data
execute store result storage dziobmc:tmp t.id int 1 run scoreboard players get @s dz.kid
function dziobmc:kraje/tp_wlasna_m with storage dziobmc:tmp t
