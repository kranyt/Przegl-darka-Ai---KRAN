execute if score #event dz.data matches 1.. run function dziobmc:event/koniec
scoreboard players set #event dz.data 1
scoreboard players set #left dz.data 300
bossbar set dziobmc:event max 300
bossbar set dziobmc:event color red
scoreboard players display name dz.event dz.sidebar [{"text":" ★ ","color":"gold"},{"text":"Event: ","color":"gray"},{"text":"Krwawy Księżyc","color":"dark_red","bold":true}]
tellraw @a {"text":""}
tellraw @a {"text":"━━━━━━━━━━━ ✦ EVENT ✦ ━━━━━━━━━━━","color":"dark_red","bold":true}
tellraw @a [{"text":"  » ","color":"dark_gray"},{"text":"KRWAWY KSIĘŻYC","color":"dark_red","bold":true}]
tellraw @a {"text":"  noc, a custom moby pojawiają się 5x częściej","color":"gray"}
tellraw @a {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"dark_red","bold":true}
title @a times 10 60 20
title @a title {"text":"Krwawy Księżyc","color":"dark_red","bold":true}
title @a subtitle {"text":"noc, a custom moby pojawiają się 5x częściej","color":"gray"}
execute as @a at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.6 1.2
function dziobmc:event/krwawy/start
