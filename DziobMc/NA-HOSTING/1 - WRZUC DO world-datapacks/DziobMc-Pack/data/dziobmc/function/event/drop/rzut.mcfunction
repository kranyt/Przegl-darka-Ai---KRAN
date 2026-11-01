tp @s ~ ~ ~ ~47 0
execute positioned ^ ^ ^5 run loot spawn ~ ~ ~ loot dziobmc:drop_party
execute positioned ^ ^ ^11 run loot spawn ~ ~ ~ loot dziobmc:drop_party
execute positioned ^ ^ ^17 run loot spawn ~ ~ ~ loot dziobmc:drop_party
particle minecraft:firework ~ ~ ~ 6 1 6 0.05 40 force
playsound minecraft:entity.chicken.egg master @a[distance=..60] ~ ~ ~ 1 1.2
scoreboard players operation #t dz.data = #left dz.data
scoreboard players operation #t dz.data %= #5 dz.data
execute if score #t dz.data matches 0 run summon minecraft:firework_rocket ~ ~ ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;5636095,16777045,16733695],has_trail:true,has_twinkle:true}]}}}}
