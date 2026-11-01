scoreboard players set #k48 dz.k_wl 1
tag @s add dz.wladca
function dziobmc:gracz/druzyna
title @a times 10 60 20
title @a title {"text":"Korea Płd.","color":"blue","bold":true}
title @a subtitle [{"selector":"@s"},{"text":" zostaje władcą!","color":"gold"}]
tellraw @a [{"text":"♛ ","color":"gold"},{"selector":"@s"},{"text":" zakłada państwo ","color":"yellow"},{"text":"Korea Płd.","color":"blue","bold":true},{"text":" i zostaje jego ","color":"yellow"},{"text":"WŁADCĄ","color":"gold","bold":true},{"text":"!","color":"yellow"}]
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.7 1
summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16766720,16744192],has_trail:true,has_twinkle:true}]}}}}
function dziobmc:kraje/info/48
