$execute unless data storage dziobmc:kraje lista[{id:$(id)}] run return run tellraw @s {"text":"✖ To państwo już nie istnieje.","color":"red"}
$execute if score #k$(id) dz.k_zamk matches 1 if score #k$(id) dz.k_wl matches 1 run return run function dziobmc:kraje/prosba {id:$(id)}
$function dziobmc:kraje/wejdz {id:$(id)}
