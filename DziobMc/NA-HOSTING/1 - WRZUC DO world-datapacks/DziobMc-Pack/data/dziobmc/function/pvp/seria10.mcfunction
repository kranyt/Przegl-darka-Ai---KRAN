title @a times 5 50 15
title @a title {"text":"LEGENDARNA SERIA!","color":"dark_red","bold":true}
title @a subtitle [{"selector":"@s"},{"text":" ma 10 zabójstw z rzędu!","color":"gold"}]
execute as @a at @s run playsound minecraft:entity.ender_dragon.growl master @s ~ ~ ~ 0.6 1.2
scoreboard players set #ile dz.data 200
function dziobmc:monety/dodaj
summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16711680,16766720],has_trail:true,has_twinkle:true}]}}}}
