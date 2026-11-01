scoreboard players set @s dz.kraj 4
scoreboard players set @s dz.prosba 0
scoreboard players add #k4 dz.k_czl 1
execute unless score #k4 dz.k_wl matches 1 run return run function dziobmc:kraje/wladca/4
tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" dołączył do państwa ","color":"gray"},{"text":"Wielka Brytania","color":"dark_blue","bold":true},{"text":"!","color":"gray"}]
function dziobmc:gracz/druzyna
playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.4
function dziobmc:kraje/info/4
