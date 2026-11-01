scoreboard players set @s dz.kraj 52
scoreboard players set @s dz.prosba 0
scoreboard players add #k52 dz.k_czl 1
execute unless score #k52 dz.k_wl matches 1 run return run function dziobmc:kraje/wladca/52
tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" dołączył do państwa ","color":"gray"},{"text":"Tajlandia","color":"blue","bold":true},{"text":"!","color":"gray"}]
function dziobmc:gracz/druzyna
playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.4
function dziobmc:kraje/info/52
