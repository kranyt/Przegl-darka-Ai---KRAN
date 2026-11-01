$execute unless score #fk dz.data matches $(k) run return 0
scoreboard players add #lista_ile dz.data 1
$tellraw @s [{"text":" • ","color":"dark_gray"},$(nj),{"text":"  ☺ ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_czl"},"color":"white"},{"text":"  ⛃ ","color":"gold"},{"score":{"name":"#k$(id)","objective":"dz.k_skarb"},"color":"yellow"},{"text":"  "},{"text":"[DOŁĄCZ]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/trigger panstwo set $(id)"}}]
