scoreboard players set @s dz.leave 0
title @s times 10 50 20
title @s subtitle [{"text":"Miłej gry na ","color":"yellow"},{"text":"Dziob.fun","color":"white","bold":true}]
title @s title {"text":"Witaj ponownie!","color":"gold","bold":true}
tellraw @a [{"text":"» ","color":"dark_gray"},{"selector":"@s"},{"text":" wrócił na serwer!","color":"gray"}]
tellraw @s [{"text":"✦ Wpisz ","color":"yellow"},{"text":"/trigger pomoc","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/trigger pomoc"},"hoverEvent":{"action":"show_text","contents":{"text":"Kliknij!","color":"yellow"}}},{"text":" aby zobaczyć wszystkie komendy.","color":"yellow"}]
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1.4
