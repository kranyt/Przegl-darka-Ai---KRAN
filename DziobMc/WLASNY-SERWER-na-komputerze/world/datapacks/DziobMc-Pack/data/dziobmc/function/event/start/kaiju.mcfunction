execute if score #event dz.data matches 1.. run function dziobmc:event/koniec
scoreboard players set #event dz.data 8
scoreboard players set #left dz.data 900
bossbar set dziobmc:event max 900
bossbar set dziobmc:event color green
scoreboard players display name dz.event dz.sidebar [{"text":" ★ ","color":"gold"},{"text":"Event: ","color":"gray"},{"text":"Atak Kaiju","color":"dark_green","bold":true}]
tellraw @a {"text":""}
tellraw @a {"text":"━━━━━━━━━━━ ✦ EVENT ✦ ━━━━━━━━━━━","color":"dark_green","bold":true}
tellraw @a [{"text":"  » ","color":"dark_gray"},{"text":"ATAK KAIJU","color":"dark_green","bold":true}]
tellraw @a {"text":"  gigantyczny potwór atakuje stolicę na mapie Ziemi!","color":"gray"}
tellraw @a {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"dark_green","bold":true}
title @a times 10 60 20
title @a title {"text":"Atak Kaiju","color":"dark_green","bold":true}
title @a subtitle {"text":"gigantyczny potwór atakuje stolicę na mapie Ziemi!","color":"gray"}
execute as @a at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.6 1.2
function dziobmc:event/kaiju/start
