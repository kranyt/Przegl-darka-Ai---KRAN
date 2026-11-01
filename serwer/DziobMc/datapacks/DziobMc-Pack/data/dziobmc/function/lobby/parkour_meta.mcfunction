execute in minecraft:overworld run tp @s 0 151 18 180 0
tellraw @a [{"text":"✔ ","color":"green"},{"selector":"@s","color":"yellow"},{"text":" ukończył parkour na spawnie!","color":"green"}]
title @s times 5 50 15
title @s title {"text":"PARKOUR UKOŃCZONY!","color":"green","bold":true}
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;5635925,16777045],has_trail:true,has_twinkle:true}]}}}}
function dziobmc:lobby/parkour_nagroda
