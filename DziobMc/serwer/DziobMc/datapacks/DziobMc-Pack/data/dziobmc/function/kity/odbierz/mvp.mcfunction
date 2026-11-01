execute unless score @s dz.rank matches 2.. run return run function dziobmc:kity/brak_rangi
scoreboard players add @s dz.cd_kit3 0
scoreboard players set #cd dz.data 216000
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_kit3
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_kit3 = #teraz dz.data
function dziobmc:kity/daj/mvp
tellraw @s [{"text":"✔ Odebrano kit ","color":"green"},{"text":"MVP","color":"gold","bold":true},{"text":"!","color":"green"}]
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.2
