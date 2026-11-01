# Gracz zginął – reset serii
scoreboard players set @s dz.smierc 0
execute if score @s dz.streak matches 5.. run tellraw @a [{"text":"☠ Seria gracza ","color":"gray"},{"selector":"@s"},{"text":" (","color":"gray"},{"score":{"name":"@s","objective":"dz.streak"},"color":"red","bold":true},{"text":") została przerwana!","color":"gray"}]
scoreboard players set @s dz.streak 0
