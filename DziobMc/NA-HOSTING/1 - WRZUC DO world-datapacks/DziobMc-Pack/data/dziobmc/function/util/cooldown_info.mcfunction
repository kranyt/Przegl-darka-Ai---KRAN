# Wejście: #cd, #roznica (ticki)
scoreboard players operation #zostalo dz.data = #cd dz.data
scoreboard players operation #zostalo dz.data -= #roznica dz.data
scoreboard players operation #zostalo dz.data /= #20 dz.data
scoreboard players operation #zm dz.data = #zostalo dz.data
scoreboard players operation #zm dz.data /= #60 dz.data
scoreboard players operation #zs dz.data = #zostalo dz.data
scoreboard players operation #zs dz.data %= #60 dz.data
tellraw @s [{"text":"⌛ Poczekaj jeszcze ","color":"red"},{"score":{"name":"#zm","objective":"dz.data"},"color":"yellow","bold":true},{"text":" min ","color":"red"},{"score":{"name":"#zs","objective":"dz.data"},"color":"yellow","bold":true},{"text":" s","color":"red"}]
playsound minecraft:block.note_block.bass master @s ~ ~ ~ 1 0.7
