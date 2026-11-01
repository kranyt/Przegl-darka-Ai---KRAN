scoreboard players remove #k34 dz.k_czl 1
execute if score #k34 dz.k_czl matches ..-1 run scoreboard players set #k34 dz.k_czl 0
tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" opuścił państwo ","color":"gray"},{"text":"Wenezuela","color":"gold","bold":true}]
execute if entity @s[tag=dz.wladca] run scoreboard players set #k34 dz.k_wl 0
execute if entity @s[tag=dz.wladca] run tellraw @a [{"text":"♛ Tron państwa ","color":"gold"},{"text":"Wenezuela","color":"gold","bold":true},{"text":" jest wolny! Mieszkańcy mogą go przejąć.","color":"gold"}]
