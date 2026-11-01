$data modify storage dziobmc:tmp o merge from storage dziobmc:kraje lista[{id:$(id)}]
$scoreboard players remove #k$(id) dz.k_czl 1
tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" opuścił państwo ","color":"gray"},{"nbt":"o.nj","storage":"dziobmc:tmp","interpret":true}]
$execute if entity @s[tag=dz.wladca] run scoreboard players set #k$(id) dz.k_wl 0
$execute if score #k$(id) dz.k_czl matches ..0 run return run function dziobmc:kraje/rozwiaz with storage dziobmc:tmp o
execute if entity @s[tag=dz.wladca] run tellraw @a [{"text":"♛ Tron państwa ","color":"gold"},{"nbt":"o.nj","storage":"dziobmc:tmp","interpret":true},{"text":" jest wolny! Mieszkańcy mogą go przejąć.","color":"gold"}]
