tellraw @a [{"text":"⚔ ","color":"red"},{"selector":"@s"},{"text":" jest NIE DO ZATRZYMANIA! ","color":"gold","bold":true},{"text":"(seria 5) +50 monet","color":"yellow"}]
execute as @a at @s run playsound minecraft:entity.wither.ambient master @s ~ ~ ~ 0.5 1.5
scoreboard players set #ile dz.data 50
function dziobmc:monety/dodaj
effect give @s minecraft:glowing 30 0 true
