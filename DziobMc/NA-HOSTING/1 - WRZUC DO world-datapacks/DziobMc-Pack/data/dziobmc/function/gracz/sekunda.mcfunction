# Co sekundę dla każdego gracza
scoreboard players add @s dz.czas 1
execute if score @s dz.czas matches 300.. run function dziobmc:gracz/wyplata
function dziobmc:gracz/hud
