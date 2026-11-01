advancement revoke @s only dziobmc:wojna/zabojstwo
execute unless score @s dz.kid matches 1.. run return 0
scoreboard players set #ofiara dz.data 0
execute as @a[distance=..96,nbt={Health:0.0f},sort=nearest,limit=1] run scoreboard players operation #ofiara dz.data = @s dz.kid
execute unless score #ofiara dz.data matches 1.. run return 0
execute store result storage dziobmc:tmp z.a int 1 run scoreboard players get @s dz.kid
execute store result storage dziobmc:tmp z.b int 1 run scoreboard players get #ofiara dz.data
function dziobmc:wojna/punkt with storage dziobmc:tmp z
