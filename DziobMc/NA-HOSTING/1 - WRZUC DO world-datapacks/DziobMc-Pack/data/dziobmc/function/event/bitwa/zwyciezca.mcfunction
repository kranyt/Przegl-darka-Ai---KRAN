tellraw @a [{"text":"⚔ ","color":"red"},{"selector":"@s"},{"text":" wygrywa Bitwę PvP z wynikiem ","color":"gold","bold":true},{"score":{"name":"@s","objective":"dz.bitwa"},"color":"red","bold":true},{"text":" zabójstw! +500 monet","color":"gold"}]
title @a times 10 60 20
title @a title {"text":"BITWA WYGRANA!","color":"dark_red","bold":true}
title @a subtitle [{"text":"Zwycięzca: ","color":"gray"},{"selector":"@s"}]
scoreboard players set #ile dz.data 500
function dziobmc:monety/dodaj
summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16766720,16744192],has_trail:true,has_twinkle:true}]}}}}
