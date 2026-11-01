execute if score #event dz.data matches 1.. run function dziobmc:event/koniec
scoreboard players set #event dz.data 7
scoreboard players set #left dz.data 300
bossbar set dziobmc:event max 300
bossbar set dziobmc:event color red
scoreboard players display name dz.event dz.sidebar [{"text":" ★ ","color":"gold"},{"text":"Event: ","color":"gray"},{"text":"Bitwa PvP","color":"dark_red","bold":true}]
tellraw @a {"text":""}
tellraw @a {"text":"━━━━━━━━━━━ ✦ EVENT ✦ ━━━━━━━━━━━","color":"dark_red","bold":true}
tellraw @a [{"text":"  » ","color":"dark_gray"},{"text":"BITWA PVP","color":"dark_red","bold":true}]
tellraw @a {"text":"  kill na graczu = 100 monet, najlepszy wojownik +500","color":"gray"}
tellraw @a [{"text":"  ➤ ","color":"dark_gray"},{"text":"[TELEPORTUJ NA ARENĘ PvP]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/trigger warp set 14"},"hoverEvent":{"action":"show_text","contents":{"text":"Kliknij!","color":"yellow"}}}]
tellraw @a {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"dark_red","bold":true}
title @a times 10 60 20
title @a title {"text":"Bitwa PvP","color":"dark_red","bold":true}
title @a subtitle {"text":"kill na graczu = 100 monet, najlepszy wojownik +500","color":"gray"}
execute as @a at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.6 1.2
function dziobmc:event/bitwa/start
