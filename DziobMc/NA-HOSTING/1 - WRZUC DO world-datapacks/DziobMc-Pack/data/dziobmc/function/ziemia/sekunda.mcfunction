function dziobmc:wojna/sekunda
scoreboard players operation #t15 dz.data = #sek dz.data
scoreboard players operation #t15 dz.data %= #15 dz.data
execute if score #t15 dz.data matches 0 run function dziobmc:ziemia/ranking
scoreboard players operation #t15 dz.data = #sek dz.data
scoreboard players operation #t15 dz.data %= #60 dz.data
execute if score #t15 dz.data matches 0 run function dziobmc:ziemia/granica with storage dziobmc:tmp g
execute as @a[scores={dz.prosba=1..,dz.kraj=1..}] run scoreboard players set @s dz.prosba 0
