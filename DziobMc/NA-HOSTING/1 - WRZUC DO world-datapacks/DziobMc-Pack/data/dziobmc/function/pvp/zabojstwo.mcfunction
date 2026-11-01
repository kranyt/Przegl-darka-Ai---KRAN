# Gracz zabił innego gracza (wywoływane co sekundę, gdy dz.zab >= 1)
scoreboard players remove @s dz.zab 1
scoreboard players add @s dz.streak 1
scoreboard players set #ile dz.data 25
execute if score #event dz.data matches 7 run scoreboard players set #ile dz.data 100
execute if score #event dz.data matches 7 run scoreboard players add @s dz.bitwa 1
tellraw @s [{"text":"⚔ Zabójstwo gracza! ","color":"red","bold":true},{"text":"Seria: ","color":"gray"},{"score":{"name":"@s","objective":"dz.streak"},"color":"yellow","bold":true}]
function dziobmc:monety/dodaj
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.8
execute if score @s dz.streak matches 3 run tellraw @a [{"text":"⚔ ","color":"red"},{"selector":"@s"},{"text":" ma serię ","color":"gold"},{"text":"3 zabójstw","color":"red","bold":true},{"text":"!","color":"gold"}]
execute if score @s dz.streak matches 5 run function dziobmc:pvp/seria5
execute if score @s dz.streak matches 10 run function dziobmc:pvp/seria10
execute if score @s dz.zab matches 1.. run function dziobmc:pvp/zabojstwo
