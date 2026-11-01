$scoreboard players remove #k$(id) dz.k_wczas 1
$execute unless score #k$(id) dz.k_wczas matches ..0 run return 0
$execute store result storage dziobmc:tmp k.b int 1 run scoreboard players get #k$(id) dz.k_wrog
$data modify storage dziobmc:tmp k.a set value $(id)
function dziobmc:wojna/koniec with storage dziobmc:tmp k
