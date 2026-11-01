execute if score #event dz.data matches 1.. run function dziobmc:event/koniec
scoreboard players set #event dz.data 5
scoreboard players set #left dz.data 300
bossbar set dziobmc:event max 300
bossbar set dziobmc:event color pink
scoreboard players display name dz.event dz.sidebar [{"text":" ★ ","color":"gold"},{"text":"Event: ","color":"gray"},{"text":"Polowanie","color":"red","bold":true}]
tellraw @a {"text":""}
tellraw @a {"text":"━━━━━━━━━━━ ✦ EVENT ✦ ━━━━━━━━━━━","color":"red","bold":true}
tellraw @a [{"text":"  » ","color":"dark_gray"},{"text":"POLOWANIE","color":"red","bold":true}]
tellraw @a {"text":"  pierwszy, kto zabije 10 custom mobów, wygrywa 500 monet","color":"gray"}
tellraw @a {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"red","bold":true}
title @a times 10 60 20
title @a title {"text":"Polowanie","color":"red","bold":true}
title @a subtitle {"text":"pierwszy, kto zabije 10 custom mobów, wygrywa 500 monet","color":"gray"}
execute as @a at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.6 1.2
function dziobmc:event/polowanie/start
