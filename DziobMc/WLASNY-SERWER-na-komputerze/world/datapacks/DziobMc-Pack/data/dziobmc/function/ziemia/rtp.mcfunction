scoreboard players add @s dz.cd_rtp 0
scoreboard players set #cd dz.data 1200
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_rtp
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_rtp = #teraz dz.data
scoreboard players set #proby_rtp dz.data 0
tellraw @s {"text":"✈ Szukam lądu na mapie Ziemi...","color":"aqua"}
function dziobmc:ziemia/rtp_proba
