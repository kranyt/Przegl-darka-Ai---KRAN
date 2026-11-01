$scoreboard players operation #lup dz.data = #k$(l) dz.k_skarb
scoreboard players operation #lup dz.data *= #3 dz.data
scoreboard players operation #lup dz.data /= #10 dz.data
$scoreboard players operation #k$(l) dz.k_skarb -= #lup dz.data
$scoreboard players operation #k$(w) dz.k_skarb += #lup dz.data
$scoreboard players add #k$(w) dz.k_wygr 1
title @a times 10 80 20
$title @a title [$(nw)]
$title @a subtitle [{"text":"wygrywa wojnę z ","color":"gold"},$(nl),{"text":"!","color":"gold"}]
$tellraw @a [{"text":"♛ ","color":"gold"},$(nw),{"text":" WYGRYWA WOJNĘ z ","color":"gold","bold":true},$(nl),{"text":" i zdobywa ","color":"gray"},{"score":{"name":"#lup","objective":"dz.data"},"color":"yellow","bold":true},{"text":" monet ze skarbca wroga!","color":"gray"}]
$execute as @a[scores={dz.kid=$(w)}] at @s run summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16766720,16744192],has_trail:true,has_twinkle:true}]}}}}
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
