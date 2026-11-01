scoreboard players set @s dz.kid 0
scoreboard players set @s dz.kraj 0
tag @s remove dz.wladca
scoreboard players set #zero dz.data 0
execute store result storage dziobmc:tmp d.id int 1 run scoreboard players get #zero dz.data
