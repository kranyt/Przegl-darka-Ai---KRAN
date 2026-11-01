execute unless score @s dz.rank matches 0.. run return run function dziobmc:kity/brak_rangi
scoreboard players add @s dz.cd_kit1 0
scoreboard players set #cd dz.data 72000
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_kit1
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_kit1 = #teraz dz.data
function dziobmc:kity/daj/start
tellraw @s [{"text":"✔ Odebrano kit ","color":"green"},{"text":"Start","color":"gold","bold":true},{"text":"!","color":"green"}]
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.2
