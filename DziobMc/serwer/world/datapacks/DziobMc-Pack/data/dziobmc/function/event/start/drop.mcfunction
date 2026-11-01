execute if score #event dz.data matches 1.. run function dziobmc:event/koniec
scoreboard players set #event dz.data 2
scoreboard players set #left dz.data 60
bossbar set dziobmc:event max 60
bossbar set dziobmc:event color blue
scoreboard players display name dz.event dz.sidebar [{"text":" ★ ","color":"gold"},{"text":"Event: ","color":"gray"},{"text":"Drop Party","color":"aqua","bold":true}]
tellraw @a {"text":""}
tellraw @a {"text":"━━━━━━━━━━━ ✦ EVENT ✦ ━━━━━━━━━━━","color":"aqua","bold":true}
tellraw @a [{"text":"  » ","color":"dark_gray"},{"text":"DROP PARTY","color":"aqua","bold":true}]
tellraw @a {"text":"  z nieba na spawnie lecą przedmioty","color":"gray"}
tellraw @a [{"text":"  ➤ ","color":"dark_gray"},{"text":"[TELEPORTUJ NA SPAWN]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/trigger warp set 11"},"hoverEvent":{"action":"show_text","contents":{"text":"Kliknij!","color":"yellow"}}}]
tellraw @a {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
title @a times 10 60 20
title @a title {"text":"Drop Party","color":"aqua","bold":true}
title @a subtitle {"text":"z nieba na spawnie lecą przedmioty","color":"gray"}
execute as @a at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.6 1.2
function dziobmc:event/drop/start
