# Dodaje #v monet do skarbca państwa gracza (@s)
execute unless score @s dz.kid matches 1.. run return 0
execute store result storage dziobmc:tmp s.id int 1 run scoreboard players get @s dz.kid
function dziobmc:kraje/do_skarbca_m with storage dziobmc:tmp s
