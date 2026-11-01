$scoreboard players set #k$(id) dz.k_czl 0
$scoreboard players set #k$(id) dz.k_skarb 0
$scoreboard players set #k$(id) dz.k_wl 0
$scoreboard players set #k$(id) dz.k_zamk 0
$scoreboard players set #k$(id) dz.k_wrog 0
$scoreboard players set #k$(id) dz.k_pkt 0
$scoreboard players set #k$(id) dz.k_wczas 0
$scoreboard players set #k$(id) dz.k_wygr 0
$scoreboard players set #k$(id) dz.k_pokoj 0
$tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" zakłada nowe państwo ","color":"yellow"},$(nj),{"text":"!","color":"yellow"}]
$function dziobmc:kraje/wejdz {id:$(id)}
