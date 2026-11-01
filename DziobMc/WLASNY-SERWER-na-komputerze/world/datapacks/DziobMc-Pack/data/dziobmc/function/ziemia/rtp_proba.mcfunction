scoreboard players add #proby_rtp dz.data 1
execute if score #proby_rtp dz.data matches 9.. run return run function dziobmc:ziemia/rtp_stolica
execute store result score #x dz.data run random value -170..170
execute store result score #z dz.data run random value -60..55
scoreboard players operation #x dz.data *= #111320 dz.data
scoreboard players operation #x dz.data /= #skala dz.data
scoreboard players operation #z dz.data *= #111320 dz.data
scoreboard players operation #z dz.data /= #skala dz.data
execute store result storage dziobmc:tmp r.x int 1 run scoreboard players get #x dz.data
execute store result storage dziobmc:tmp r.z int 1 run scoreboard players get #z dz.data
function dziobmc:ziemia/rtp_m with storage dziobmc:tmp r
execute at @s if dimension minecraft:ziemia if block ~ ~-1 ~ minecraft:water run return run function dziobmc:ziemia/rtp_proba
execute at @s if dimension minecraft:ziemia if block ~ ~-1 ~ minecraft:ice run return run function dziobmc:ziemia/rtp_proba
function dziobmc:ziemia/po_tp
