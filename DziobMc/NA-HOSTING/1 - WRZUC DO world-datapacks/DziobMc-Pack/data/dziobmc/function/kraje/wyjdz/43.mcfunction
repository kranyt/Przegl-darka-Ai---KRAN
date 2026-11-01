scoreboard players remove #k43 dz.k_czl 1
execute if score #k43 dz.k_czl matches ..-1 run scoreboard players set #k43 dz.k_czl 0
tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" opuścił państwo ","color":"gray"},{"text":"Arabia Saudyjska","color":"dark_green","bold":true}]
execute if entity @s[tag=dz.wladca] run scoreboard players set #k43 dz.k_wl 0
execute if entity @s[tag=dz.wladca] run tellraw @a [{"text":"♛ Tron państwa ","color":"gold"},{"text":"Arabia Saudyjska","color":"dark_green","bold":true},{"text":" jest wolny! Mieszkańcy mogą go przejąć.","color":"gold"}]
