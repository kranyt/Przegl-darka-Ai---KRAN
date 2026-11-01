$scoreboard players set @s dz.kid $(id)
$scoreboard players set #q dz.data $(id)
scoreboard players operation #q dz.data /= #1000 dz.data
scoreboard players operation @s dz.kraj = #q dz.data
scoreboard players set @s dz.prosba 0
$scoreboard players add #k$(id) dz.k_czl 1
$data modify storage dziobmc:tmp j set from storage dziobmc:kraje lista[{id:$(id)}]
$execute unless score #k$(id) dz.k_wl matches 1 run return run function dziobmc:kraje/wladca with storage dziobmc:tmp j
function dziobmc:kraje/wejdz_ogloszenie with storage dziobmc:tmp j
function dziobmc:gracz/druzyna
playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.4
function dziobmc:kraje/info
