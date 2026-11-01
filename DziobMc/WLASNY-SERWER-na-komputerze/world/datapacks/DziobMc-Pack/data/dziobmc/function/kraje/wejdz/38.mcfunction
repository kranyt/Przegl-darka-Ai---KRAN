scoreboard players set @s dz.kraj 38
scoreboard players set @s dz.prosba 0
scoreboard players add #k38 dz.k_czl 1
execute unless score #k38 dz.k_wl matches 1 run return run function dziobmc:kraje/wladca/38
tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" dołączył do państwa ","color":"gray"},{"text":"Nigeria","color":"green","bold":true},{"text":"!","color":"gray"}]
function dziobmc:gracz/druzyna
playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.4
function dziobmc:kraje/info/38
