$tellraw @a [{"text":"✖ Państwo ","color":"gray"},$(nj),{"text":" zostało rozwiązane (brak mieszkańców).","color":"gray"}]
$execute if score #k$(id) dz.k_wrog matches 1.. run function dziobmc:kraje/rozwiaz_wojna {id:$(id)}
$data remove storage dziobmc:kraje lista[{id:$(id)}]
$scoreboard players reset #k$(id)
$scoreboard players reset k$(kod)$(nn) dz.ranking
