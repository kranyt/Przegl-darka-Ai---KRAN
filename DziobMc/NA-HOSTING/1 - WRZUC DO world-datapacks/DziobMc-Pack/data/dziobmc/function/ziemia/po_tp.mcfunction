execute at @s unless dimension minecraft:ziemia run return run tellraw @s {"text":"✖ Świat 'ziemia' nie istnieje. Zainstaluj plugin DziobEarth (patrz instrukcja).","color":"red"}
tag @s remove dz.lobby
gamemode survival @s[gamemode=adventure,tag=!dz.build]
effect give @s minecraft:resistance 5 4 true
effect give @s minecraft:slow_falling 6 0 true
execute at @s run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 0.8
title @s times 5 40 10
title @s title {"text":"✈ Ziemia","color":"aqua","bold":true}
title @s subtitle {"text":"/trigger gdzie – sprawdź gdzie jesteś","color":"gray"}
