advancement revoke @s only dziobmc:zabojstwa/boss
scoreboard players set #boss_zabity dz.data 1
scoreboard players add @s dz.kills 1
title @a times 10 80 20
title @a title {"text":"♛ KRÓL POKONANY! ♛","color":"gold","bold":true}
title @a subtitle [{"text":"Ostatni cios: ","color":"yellow"},{"selector":"@s"}]
tellraw @a [{"text":"♛ ","color":"gold"},{"selector":"@s"},{"text":" zadał ostatni cios ","color":"yellow"},{"text":"Królowi Dziobów","color":"gold","bold":true},{"text":" i zgarnia 1000 monet!","color":"yellow"}]
scoreboard players set #ile dz.data 1000
function dziobmc:monety/dodaj
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16766720,16711680],has_trail:true,has_twinkle:true}]}}}}
summon minecraft:firework_rocket ~2 ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16766720,65535],has_trail:true,has_twinkle:true}]}}}}
summon minecraft:firework_rocket ~-2 ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16777215,16744192],has_trail:true,has_twinkle:true}]}}}}
