scoreboard players remove #next dz.data 1
execute store result bossbar dziobmc:event value run scoreboard players get #next dz.data
scoreboard players operation #min dz.data = #next dz.data
scoreboard players operation #min dz.data /= #60 dz.data
scoreboard players operation #s dz.data = #next dz.data
scoreboard players operation #s dz.data %= #60 dz.data
bossbar set dziobmc:event name [{"text":"✦ Następny event za ","color":"gold"},{"score":{"name":"#min","objective":"dz.data"},"color":"yellow","bold":true},{"text":"m ","color":"yellow"},{"score":{"name":"#s","objective":"dz.data"},"color":"yellow","bold":true},{"text":"s","color":"yellow"},{"text":"  •  Dziob.fun","color":"gray"}]
bossbar set dziobmc:event players @a
execute if score #next dz.data matches 60 run tellraw @a [{"text":"✦ ","color":"gold"},{"text":"Event wystartuje za 1 minutę!","color":"yellow","bold":true}]
execute if score #next dz.data matches 1..5 as @a at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 1.5
execute if score #next dz.data matches 1..5 run title @a actionbar [{"text":"Event za ","color":"gold"},{"score":{"name":"#next","objective":"dz.data"},"color":"yellow","bold":true},{"text":"...","color":"gold"}]
execute if score #next dz.data matches ..0 run function dziobmc:event/losuj
