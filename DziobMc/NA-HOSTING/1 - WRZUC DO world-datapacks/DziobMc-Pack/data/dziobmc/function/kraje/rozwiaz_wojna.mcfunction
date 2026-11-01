$execute store result storage dziobmc:tmp rw.w int 1 run scoreboard players get #k$(id) dz.k_wrog
$data modify storage dziobmc:tmp rw.l set value $(id)
function dziobmc:kraje/rozwiaz_wojna2 with storage dziobmc:tmp rw
