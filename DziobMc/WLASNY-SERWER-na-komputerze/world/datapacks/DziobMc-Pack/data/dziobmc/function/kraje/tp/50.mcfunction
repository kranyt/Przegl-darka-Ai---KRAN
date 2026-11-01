scoreboard players add @s dz.cd_stol 0
scoreboard players set #cd dz.data 600
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_stol
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_stol = #teraz dz.data
tellraw @s [{"text":"✈ Lecisz do stolicy: ","color":"aqua"},{"text":"Astana","color":"aqua","bold":true},{"text":" (","color":"gray"},{"text":"Kazachstan","color":"aqua","bold":false},{"text":")","color":"gray"}]
function dziobmc:ziemia/tp_m with storage dziobmc:kraje s.k50
