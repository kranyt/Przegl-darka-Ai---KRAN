# Co sekundę dla każdego gracza
scoreboard players add @s dz.czas 1
execute if score @s dz.czas matches 300.. run function dziobmc:gracz/wyplata
execute if score @s dz.zab matches 1.. run function dziobmc:pvp/zabojstwo
execute if score @s dz.smierc matches 1.. run function dziobmc:pvp/smierc
function dziobmc:gracz/hud
