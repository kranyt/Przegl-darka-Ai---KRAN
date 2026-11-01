tag @s add dz.pvp_bylo
title @s times 5 30 10
title @s title {"text":"⚔ STREFA PvP ⚔","color":"red","bold":true}
title @s subtitle {"text":"Walczysz swoim ekwipunkiem – po śmierci go tracisz!","color":"gray"}
playsound minecraft:item.armor.equip_netherite master @s ~ ~ ~ 1 0.8
tellraw @s [{"text":"⚔ Strefa PvP! ","color":"red","bold":true},{"text":"Kit PvP: ","color":"gray"},{"text":"[ODBIERZ]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/trigger kit set 15"},"hoverEvent":{"action":"show_text","contents":{"text":"Kit PvP co 5 minut"}}},{"text":"  •  25 monet za kill, serie 3/5/10!","color":"gray"}]
