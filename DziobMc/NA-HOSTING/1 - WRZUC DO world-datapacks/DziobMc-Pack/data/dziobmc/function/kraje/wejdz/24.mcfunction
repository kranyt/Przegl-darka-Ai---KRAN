scoreboard players set @s dz.kraj 24
scoreboard players set @s dz.prosba 0
scoreboard players add #k24 dz.k_czl 1
execute unless score #k24 dz.k_wl matches 1 run return run function dziobmc:kraje/wladca/24
tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" dołączył do państwa ","color":"gray"},{"text":"Dania","color":"red","bold":true},{"text":"!","color":"gray"}]
function dziobmc:gracz/druzyna
playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.4
function dziobmc:kraje/info/24
