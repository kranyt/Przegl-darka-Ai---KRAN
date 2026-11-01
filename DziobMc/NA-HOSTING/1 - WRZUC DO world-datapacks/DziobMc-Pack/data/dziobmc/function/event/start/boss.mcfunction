execute if score #event dz.data matches 1.. run function dziobmc:event/koniec
scoreboard players set #event dz.data 3
scoreboard players set #left dz.data 600
bossbar set dziobmc:event max 600
bossbar set dziobmc:event color yellow
scoreboard players display name dz.event dz.sidebar [{"text":" ★ ","color":"gold"},{"text":"Event: ","color":"gray"},{"text":"Król Dziobów","color":"gold","bold":true}]
tellraw @a {"text":""}
tellraw @a {"text":"━━━━━━━━━━━ ✦ EVENT ✦ ━━━━━━━━━━━","color":"gold","bold":true}
tellraw @a [{"text":"  » ","color":"dark_gray"},{"text":"KRÓL DZIOBÓW","color":"gold","bold":true}]
tellraw @a {"text":"  boss na arenie – 1000 monet za ostatni cios","color":"gray"}
tellraw @a [{"text":"  ➤ ","color":"dark_gray"},{"text":"[TELEPORTUJ NA ARENĘ]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/trigger warp set 12"},"hoverEvent":{"action":"show_text","contents":{"text":"Kliknij!","color":"yellow"}}}]
tellraw @a {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"gold","bold":true}
title @a times 10 60 20
title @a title {"text":"Król Dziobów","color":"gold","bold":true}
title @a subtitle {"text":"boss na arenie – 1000 monet za ostatni cios","color":"gray"}
execute as @a at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.6 1.2
function dziobmc:event/boss/start
