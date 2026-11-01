execute unless data storage dziobmc:tmp it[0] run return 0
execute if score #iter_tryb dz.data matches 1 run function dziobmc:kraje/na_sekunde with storage dziobmc:tmp it[0]
execute if score #iter_tryb dz.data matches 2 run function dziobmc:kraje/na_ranking with storage dziobmc:tmp it[0]
execute if score #iter_tryb dz.data matches 3 run function dziobmc:kraje/na_liste with storage dziobmc:tmp it[0]
execute if score #iter_tryb dz.data matches 4 run function dziobmc:kraje/na_wojne with storage dziobmc:tmp it[0]
data remove storage dziobmc:tmp it[0]
function dziobmc:kraje/iter_krok
