scoreboard players set @s dz.kraj 16
scoreboard players set @s dz.prosba 0
scoreboard players add #k16 dz.k_czl 1
execute unless score #k16 dz.k_wl matches 1 run return run function dziobmc:kraje/wladca/16
tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" dołączył do państwa ","color":"gray"},{"text":"Szwajcaria","color":"red","bold":true},{"text":"!","color":"gray"}]
function dziobmc:gracz/druzyna
playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.4
function dziobmc:kraje/info/16
