tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
tellraw @s [{"text":"   ✪ ","color":"aqua"},{"text":"RANKING PAŃSTW","color":"gold","bold":true},{"text":"  (patrz też scoreboard)","color":"gray"}]
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
scoreboard players set #lista_ile dz.data 0
scoreboard players set #fk dz.data -1
scoreboard players set #iter_tryb dz.data 5
function dziobmc:kraje/iter_ranking
execute if score #lista_ile dz.data matches 0 run tellraw @s {"text":" Nie ma jeszcze żadnych państw – załóż pierwsze!","color":"gray","italic":true}
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
