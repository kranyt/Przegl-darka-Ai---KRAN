advancement revoke @s only dziobmc:kaiju/2
scoreboard players set #kaiju_zabity dz.data 1
title @a times 10 90 20
title @a title {"text":"☠ LODOWY TYTAN POKONANY! ☠","color":"aqua","bold":true}
title @a subtitle [{"text":"Ostatni cios: ","color":"yellow"},{"selector":"@s"}]
tellraw @a [{"text":"☠ ","color":"dark_red"},{"selector":"@s"},{"text":" zadał ostatni cios ","color":"yellow"},{"text":"Lodowy Tytan","color":"aqua","bold":true},{"text":"! +2500 monet, a skarbiec jego państwa +2000!","color":"yellow"}]
scoreboard players set #ile dz.data 2500
function dziobmc:monety/dodaj
scoreboard players set #v dz.data 2000
function dziobmc:kraje/do_skarbca
execute as @a[distance=..96] unless entity @s[tag=dz.zabojca_kaiju] at @s run function dziobmc:kaiju/uczestnik
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 0.8
summon minecraft:firework_rocket ~ ~2 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;16711680,16766720],has_trail:true,has_twinkle:true}]}}}}
summon minecraft:firework_rocket ~3 ~2 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;65280,16777215],has_trail:true,has_twinkle:true}]}}}}
summon minecraft:firework_rocket ~-3 ~2 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;255,16766720],has_trail:true,has_twinkle:true}]}}}}
