scoreboard players set @s staty 0
tellraw @s {"text":""}
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"gold","bold":true}
tellraw @s [{"text":"        ✦ ","color":"yellow"},{"text":"DziobMc","color":"gold","bold":true},{"text":" » ","color":"dark_gray"},{"text":"STATYSTYKI","color":"yellow","bold":true}]
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"gold","bold":true}
tellraw @s [{"text":" Gracz: ","color":"gray"},{"selector":"@s"}]
tellraw @s [{"text":" ⛃ Monety: ","color":"gold"},{"score":{"name":"@s","objective":"dz.coins"},"color":"yellow","bold":true}]
tellraw @s [{"text":" ⚔ Zabite custom moby: ","color":"red"},{"score":{"name":"@s","objective":"dz.kills"},"color":"white","bold":true}]
tellraw @s [{"text":" ☠ Zabici gracze: ","color":"dark_red"},{"score":{"name":"@s","objective":"dz.pvp"},"color":"white","bold":true}]
tellraw @s [{"text":" ✝ Śmierci: ","color":"gray"},{"score":{"name":"@s","objective":"dz.deaths"},"color":"white","bold":true}]
tellraw @s [{"text":" ⌚ Minuty gry: ","color":"aqua"},{"score":{"name":"@s","objective":"dz.minuty"},"color":"white","bold":true}]
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"gold","bold":true}
