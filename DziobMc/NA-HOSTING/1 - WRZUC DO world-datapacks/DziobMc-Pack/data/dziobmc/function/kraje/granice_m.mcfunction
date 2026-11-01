$execute if score #k$(id) dz.k_zamk matches 1 run return run function dziobmc:kraje/granice_otworz {id:$(id)}
$scoreboard players set #k$(id) dz.k_zamk 1
tellraw @s {"text":"✔ Granice zamknięte – nowi gracze muszą wysłać prośbę.","color":"yellow"}
