scoreboard players remove #left dz.data 1
execute store result bossbar dziobmc:event value run scoreboard players get #left dz.data
scoreboard players operation #min dz.data = #left dz.data
scoreboard players operation #min dz.data /= #60 dz.data
scoreboard players operation #s dz.data = #left dz.data
scoreboard players operation #s dz.data %= #60 dz.data
execute if score #event dz.data matches 1 run bossbar set dziobmc:event name [{"text":"★ EVENT: ","color":"white","bold":true},{"text":"Krwawy Księżyc","color":"dark_red","bold":true},{"text":"  •  zostało ","color":"gray"},{"score":{"name":"#min","objective":"dz.data"},"color":"white"},{"text":"m ","color":"white"},{"score":{"name":"#s","objective":"dz.data"},"color":"white"},{"text":"s","color":"white"}]
execute if score #event dz.data matches 2 run bossbar set dziobmc:event name [{"text":"★ EVENT: ","color":"white","bold":true},{"text":"Drop Party","color":"aqua","bold":true},{"text":"  •  zostało ","color":"gray"},{"score":{"name":"#min","objective":"dz.data"},"color":"white"},{"text":"m ","color":"white"},{"score":{"name":"#s","objective":"dz.data"},"color":"white"},{"text":"s","color":"white"}]
execute if score #event dz.data matches 3 run bossbar set dziobmc:event name [{"text":"★ EVENT: ","color":"white","bold":true},{"text":"Król Dziobów","color":"gold","bold":true},{"text":"  •  zostało ","color":"gray"},{"score":{"name":"#min","objective":"dz.data"},"color":"white"},{"text":"m ","color":"white"},{"score":{"name":"#s","objective":"dz.data"},"color":"white"},{"text":"s","color":"white"}]
execute if score #event dz.data matches 4 run bossbar set dziobmc:event name [{"text":"★ EVENT: ","color":"white","bold":true},{"text":"Podwójne Monety","color":"yellow","bold":true},{"text":"  •  zostało ","color":"gray"},{"score":{"name":"#min","objective":"dz.data"},"color":"white"},{"text":"m ","color":"white"},{"score":{"name":"#s","objective":"dz.data"},"color":"white"},{"text":"s","color":"white"}]
execute if score #event dz.data matches 5 run bossbar set dziobmc:event name [{"text":"★ EVENT: ","color":"white","bold":true},{"text":"Polowanie","color":"red","bold":true},{"text":"  •  zostało ","color":"gray"},{"score":{"name":"#min","objective":"dz.data"},"color":"white"},{"text":"m ","color":"white"},{"score":{"name":"#s","objective":"dz.data"},"color":"white"},{"text":"s","color":"white"}]
execute if score #event dz.data matches 6 run bossbar set dziobmc:event name [{"text":"★ EVENT: ","color":"white","bold":true},{"text":"Deszcz Monet","color":"green","bold":true},{"text":"  •  zostało ","color":"gray"},{"score":{"name":"#min","objective":"dz.data"},"color":"white"},{"text":"m ","color":"white"},{"score":{"name":"#s","objective":"dz.data"},"color":"white"},{"text":"s","color":"white"}]
execute if score #event dz.data matches 1 run function dziobmc:event/krwawy/tik
execute if score #event dz.data matches 2 run function dziobmc:event/drop/tik
execute if score #event dz.data matches 3 run function dziobmc:event/boss/tik
execute if score #event dz.data matches 4 run function dziobmc:event/podwojne/tik
execute if score #event dz.data matches 5 run function dziobmc:event/polowanie/tik
execute if score #event dz.data matches 6 run function dziobmc:event/deszcz/tik
execute if score #event dz.data matches 1.. if score #left dz.data matches ..0 run function dziobmc:event/koniec
