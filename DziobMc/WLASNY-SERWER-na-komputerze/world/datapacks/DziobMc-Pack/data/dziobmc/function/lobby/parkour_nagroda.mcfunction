scoreboard players add @s dz.cd_park 0
scoreboard players set #cd dz.data 12000
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_park
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_park = #teraz dz.data
scoreboard players set #ile dz.data 75
function dziobmc:monety/dodaj
