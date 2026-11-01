tag @s add dz.joined
scoreboard players add #gracze dz.data 1
scoreboard players set @s dz.coins 100
scoreboard players set @s dz.kills 0
scoreboard players set @s dz.rank 0
scoreboard players set @s dz.leave 0
scoreboard players set @s dz.czas 0
scoreboard players set @s dz.minuty 0
scoreboard players set @s dz.cd_kit1 -100000000
scoreboard players set @s dz.cd_kit2 -100000000
scoreboard players set @s dz.cd_kit3 -100000000
scoreboard players set @s dz.cd_kit4 -100000000
scoreboard players set @s dz.cd_nagr -100000000
scoreboard players set @s dz.cd_spawn -100000000
scoreboard players set @s dz.cd_rtp -100000000
scoreboard players set @s dz.cd_park -100000000
function dziobmc:rangi/domyslna
execute if score #mapa dz.data matches 1 in minecraft:overworld run tp @s 0 151 18 180 0
title @s times 10 80 20
title @s subtitle [{"text":"Dziob.fun","color":"yellow"},{"text":" • ","color":"dark_gray"},{"text":"Minecraft 1.16.4+","color":"white"}]
title @s title [{"text":"Witaj na ","color":"white"},{"text":"DziobMc","color":"gold","bold":true}]
tellraw @a [{"text":"✦ ","color":"gold"},{"selector":"@s","color":"yellow"},{"text":" dołączył pierwszy raz! ","color":"white"},{"text":"(gracz #","color":"gray"},{"score":{"name":"#gracze","objective":"dz.data"},"color":"gray"},{"text":")","color":"gray"}]
tellraw @s [{"text":"➤ Dostajesz ","color":"green"},{"text":"100 monet","color":"gold","bold":true},{"text":" i zestaw startowy na dobry początek!","color":"green"}]
function dziobmc:kity/daj/start
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16766720,16744192],has_trail:true,has_twinkle:true}]}}}}
function dziobmc:komendy/menu_pomoc
