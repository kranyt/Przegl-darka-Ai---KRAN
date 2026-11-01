execute if score #event dz.data matches 1.. run function dziobmc:event/koniec
scoreboard players set #event dz.data 4
scoreboard players set #left dz.data 600
bossbar set dziobmc:event max 600
bossbar set dziobmc:event color green
scoreboard players display name dz.event dz.sidebar [{"text":" ★ ","color":"gold"},{"text":"Event: ","color":"gray"},{"text":"Podwójne Monety","color":"yellow","bold":true}]
tellraw @a {"text":""}
tellraw @a {"text":"━━━━━━━━━━━ ✦ EVENT ✦ ━━━━━━━━━━━","color":"yellow","bold":true}
tellraw @a [{"text":"  » ","color":"dark_gray"},{"text":"PODWÓJNE MONETY","color":"yellow","bold":true}]
tellraw @a {"text":"  wszystkie monety x2","color":"gray"}
tellraw @a {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"yellow","bold":true}
title @a times 10 60 20
title @a title {"text":"Podwójne Monety","color":"yellow","bold":true}
title @a subtitle {"text":"wszystkie monety x2","color":"gray"}
execute as @a at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.6 1.2
function dziobmc:event/podwojne/start
