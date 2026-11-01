$execute if score #fk dz.data matches $(id) run return 0
$tellraw @s [{"text":" ⚔ ","color":"dark_red"},$(nj),{"text":"  ☺ ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_czl"},"color":"white"},{"text":"  "},{"text":"[WYPOWIEDZ WOJNĘ]","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/trigger wojna set $(id)"}}]
