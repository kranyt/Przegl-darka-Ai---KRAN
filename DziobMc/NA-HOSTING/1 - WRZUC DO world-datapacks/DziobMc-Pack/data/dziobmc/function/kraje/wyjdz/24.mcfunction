scoreboard players remove #k24 dz.k_czl 1
execute if score #k24 dz.k_czl matches ..-1 run scoreboard players set #k24 dz.k_czl 0
tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" opuścił państwo ","color":"gray"},{"text":"Dania","color":"red","bold":true}]
execute if entity @s[tag=dz.wladca] run scoreboard players set #k24 dz.k_wl 0
execute if entity @s[tag=dz.wladca] run tellraw @a [{"text":"♛ Tron państwa ","color":"gold"},{"text":"Dania","color":"red","bold":true},{"text":" jest wolny! Mieszkańcy mogą go przejąć.","color":"gold"}]
