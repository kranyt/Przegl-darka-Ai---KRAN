execute unless entity @s[tag=dz.wladca] run return run tellraw @s {"text":"✖ Tylko władca państwa może wypowiadać wojny.","color":"red"}
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
tellraw @s [{"text":"   ⚔ ","color":"dark_red"},{"text":"WYPOWIEDZ WOJNĘ","color":"red","bold":true}]
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
tellraw @s {"text":" Wojna trwa 30 min. Punkt = zabicie wroga. Do 15 pkt. Zwycięzca bierze 30% skarbca wroga!","color":"gray"}
scoreboard players operation #fk dz.data = @s dz.kid
scoreboard players set #iter_tryb dz.data 4
function dziobmc:kraje/iter
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"aqua","bold":true}
