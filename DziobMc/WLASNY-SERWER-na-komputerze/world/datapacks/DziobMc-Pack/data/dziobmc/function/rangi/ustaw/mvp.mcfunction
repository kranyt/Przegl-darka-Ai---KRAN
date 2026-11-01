# Użycie: /execute as NICK run function dziobmc:rangi/ustaw/mvp
scoreboard players set @s dz.rid 6
function dziobmc:gracz/druzyna
scoreboard players set @s dz.rank 2
tag @s remove dz.staff
tellraw @a [{"text":"✦ ","color":"gold"},{"selector":"@s"},{"text":" otrzymał rangę ","color":"yellow"},{"text":"MVP","color":"gold","bold":true},{"text":"!","color":"yellow"}]
title @s times 10 60 20
title @s subtitle {"text":"Dzięki, że grasz na DziobMc!","color":"yellow"}
title @s title [{"text":"Ranga ","color":"white"},{"text":"MVP","color":"gold","bold":true}]
execute at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
execute at @s run summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16766720,16744192],has_trail:true,has_twinkle:true}]}}}}
