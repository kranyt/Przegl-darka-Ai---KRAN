tellraw @a [{"text":"⚔ ","color":"red"},{"selector":"@s"},{"text":" wygrywa Polowanie i zgarnia 500 monet!","color":"gold","bold":true}]
title @a times 10 60 20
title @a title {"text":"POLOWANIE WYGRANE!","color":"gold","bold":true}
title @a subtitle [{"text":"Zwycięzca: ","color":"yellow"},{"selector":"@s"}]
scoreboard players set #ile dz.data 500
function dziobmc:monety/dodaj
summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16766720,16744192],has_trail:true,has_twinkle:true}]}}}}
scoreboard players set #polowanie_wygrane dz.data 1
function dziobmc:event/koniec
