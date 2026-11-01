advancement revoke @s only dziobmc:wojna/zab48
execute unless score @s dz.kraj matches 1.. run return 0
execute store result storage dziobmc:tmp z.a int 1 run scoreboard players get @s dz.kraj
data modify storage dziobmc:tmp z.b set value 48
function dziobmc:wojna/punkt with storage dziobmc:tmp z
