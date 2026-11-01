tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
tellraw @s [{"text":"   ✪ ","color":"aqua"},{"text":"PAŃSTWA: CHILE","color":"red","bold":true}]
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
scoreboard players set #lista_ile dz.data 0
scoreboard players set #fk dz.data 31
scoreboard players set #iter_tryb dz.data 3
function dziobmc:kraje/iter
execute if score #lista_ile dz.data matches 0 run tellraw @s {"text":" Nikt jeszcze nie założył tu państwa!","color":"gray","italic":true}
scoreboard players set #k dz.data 31
function dziobmc:kraje/wolny_n
function dziobmc:kraje/przycisk_zaloz with storage dziobmc:tmp wn
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
