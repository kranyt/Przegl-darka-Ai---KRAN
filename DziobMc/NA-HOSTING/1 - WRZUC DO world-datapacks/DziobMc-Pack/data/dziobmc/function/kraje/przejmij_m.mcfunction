$execute if score #k$(id) dz.k_wl matches 1 run return run tellraw @s {"text":"✖ To państwo ma już władcę.","color":"red"}
$data modify storage dziobmc:tmp j set from storage dziobmc:kraje lista[{id:$(id)}]
function dziobmc:kraje/wladca with storage dziobmc:tmp j
