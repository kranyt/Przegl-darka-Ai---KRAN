execute store result storage dziobmc:tmp o.id int 1 run scoreboard players get @s dz.kid
function dziobmc:kraje/opusc_m with storage dziobmc:tmp o
tag @s remove dz.wladca
scoreboard players set @s dz.kid 0
scoreboard players set @s dz.kraj 0
function dziobmc:gracz/druzyna
