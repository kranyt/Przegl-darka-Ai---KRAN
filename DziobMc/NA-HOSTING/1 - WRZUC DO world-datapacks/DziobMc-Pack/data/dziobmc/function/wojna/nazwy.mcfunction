$execute unless data storage dziobmc:kraje lista[{id:$(b)}] run return run tellraw @s {"text":"✖ To państwo nie istnieje.","color":"red"}
$data modify storage dziobmc:tmp w.na set from storage dziobmc:kraje lista[{id:$(a)}].nj
$data modify storage dziobmc:tmp w.nb set from storage dziobmc:kraje lista[{id:$(b)}].nj
