execute if score #event dz.data matches 1.. run function dziobmc:event/koniec
scoreboard players set #event dz.data 6
scoreboard players set #left dz.data 15
bossbar set dziobmc:event max 15
bossbar set dziobmc:event color green
scoreboard players display name dz.event dz.sidebar [{"text":" ★ ","color":"gold"},{"text":"Event: ","color":"gray"},{"text":"Deszcz Monet","color":"green","bold":true}]
tellraw @a {"text":""}
tellraw @a {"text":"━━━━━━━━━━━ ✦ EVENT ✦ ━━━━━━━━━━━","color":"green","bold":true}
tellraw @a [{"text":"  » ","color":"dark_gray"},{"text":"DESZCZ MONET","color":"green","bold":true}]
tellraw @a {"text":"  każdy gracz online dostaje 100 monet","color":"gray"}
tellraw @a {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"green","bold":true}
title @a times 10 60 20
title @a title {"text":"Deszcz Monet","color":"green","bold":true}
title @a subtitle {"text":"każdy gracz online dostaje 100 monet","color":"gray"}
execute as @a at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.6 1.2
function dziobmc:event/deszcz/start
