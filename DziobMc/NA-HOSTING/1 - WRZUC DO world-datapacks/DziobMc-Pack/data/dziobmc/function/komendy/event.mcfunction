scoreboard players set @s event 0
tellraw @s {"text":"━━━━━━━━━━━ ✦ EVENTY ✦ ━━━━━━━━━━━","color":"gold","bold":true}
execute if score #event dz.data matches 0 run tellraw @s [{"text":" Następny event za: ","color":"gray"},{"score":{"name":"#next","objective":"dz.data"},"color":"yellow","bold":true},{"text":" s","color":"yellow"}]
execute if score #event dz.data matches 1 run tellraw @s [{"text":" TRWA: ","color":"green","bold":true},{"text":"Krwawy Księżyc","color":"dark_red","bold":true},{"text":" (zostało ","color":"gray"},{"score":{"name":"#left","objective":"dz.data"},"color":"white"},{"text":" s)","color":"gray"}]
execute if score #event dz.data matches 2 run tellraw @s [{"text":" TRWA: ","color":"green","bold":true},{"text":"Drop Party","color":"aqua","bold":true},{"text":" (zostało ","color":"gray"},{"score":{"name":"#left","objective":"dz.data"},"color":"white"},{"text":" s)","color":"gray"}]
execute if score #event dz.data matches 3 run tellraw @s [{"text":" TRWA: ","color":"green","bold":true},{"text":"Król Dziobów","color":"gold","bold":true},{"text":" (zostało ","color":"gray"},{"score":{"name":"#left","objective":"dz.data"},"color":"white"},{"text":" s)","color":"gray"}]
execute if score #event dz.data matches 4 run tellraw @s [{"text":" TRWA: ","color":"green","bold":true},{"text":"Podwójne Monety","color":"yellow","bold":true},{"text":" (zostało ","color":"gray"},{"score":{"name":"#left","objective":"dz.data"},"color":"white"},{"text":" s)","color":"gray"}]
execute if score #event dz.data matches 5 run tellraw @s [{"text":" TRWA: ","color":"green","bold":true},{"text":"Polowanie","color":"red","bold":true},{"text":" (zostało ","color":"gray"},{"score":{"name":"#left","objective":"dz.data"},"color":"white"},{"text":" s)","color":"gray"}]
execute if score #event dz.data matches 6 run tellraw @s [{"text":" TRWA: ","color":"green","bold":true},{"text":"Deszcz Monet","color":"green","bold":true},{"text":" (zostało ","color":"gray"},{"score":{"name":"#left","objective":"dz.data"},"color":"white"},{"text":" s)","color":"gray"}]
execute if score #event dz.data matches 7 run tellraw @s [{"text":" TRWA: ","color":"green","bold":true},{"text":"Bitwa PvP","color":"dark_red","bold":true},{"text":" (zostało ","color":"gray"},{"score":{"name":"#left","objective":"dz.data"},"color":"white"},{"text":" s)","color":"gray"}]
tellraw @s {"text":" Eventy losują się co 20 minut gry:","color":"gray"}
tellraw @s [{"text":"  • ","color":"dark_gray"},{"text":"Krwawy Księżyc","color":"dark_red","bold":true},{"text":" – noc, a custom moby pojawiają się 5x częściej","color":"gray"}]
tellraw @s [{"text":"  • ","color":"dark_gray"},{"text":"Drop Party","color":"aqua","bold":true},{"text":" – z nieba na spawnie lecą przedmioty","color":"gray"}]
tellraw @s [{"text":"  • ","color":"dark_gray"},{"text":"Król Dziobów","color":"gold","bold":true},{"text":" – boss na arenie – 1000 monet za ostatni cios","color":"gray"}]
tellraw @s [{"text":"  • ","color":"dark_gray"},{"text":"Podwójne Monety","color":"yellow","bold":true},{"text":" – wszystkie monety x2","color":"gray"}]
tellraw @s [{"text":"  • ","color":"dark_gray"},{"text":"Polowanie","color":"red","bold":true},{"text":" – pierwszy, kto zabije 10 custom mobów, wygrywa 500 monet","color":"gray"}]
tellraw @s [{"text":"  • ","color":"dark_gray"},{"text":"Deszcz Monet","color":"green","bold":true},{"text":" – każdy gracz online dostaje 100 monet","color":"gray"}]
tellraw @s [{"text":"  • ","color":"dark_gray"},{"text":"Bitwa PvP","color":"dark_red","bold":true},{"text":" – kill na graczu = 100 monet, najlepszy wojownik +500","color":"gray"}]
tellraw @s {"text":"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━","color":"gold","bold":true}
