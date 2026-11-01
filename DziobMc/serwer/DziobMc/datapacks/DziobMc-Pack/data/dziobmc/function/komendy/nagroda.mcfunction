scoreboard players set @s nagroda 0
scoreboard players add @s dz.cd_nagr 0
scoreboard players set #cd dz.data 72000
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_nagr
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_nagr = #teraz dz.data
execute store result score #ile dz.data run random value 50..150
tellraw @s [{"text":"✿ ","color":"light_purple"},{"text":"Nagroda godzinowa odebrana!","color":"light_purple","bold":true}]
function dziobmc:monety/dodaj
loot give @s loot dziobmc:nagroda
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1
summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"large_ball",colors:[I;11141290,16733695],has_trail:true,has_twinkle:true}]}}}}
