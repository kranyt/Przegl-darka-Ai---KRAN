scoreboard players set #ns dz.data 1
execute if score #lat dz.data matches ..-1 run scoreboard players set #ns dz.data -1
execute if score #lat dz.data matches ..-1 run scoreboard players operation #lat dz.data *= #m1 dz.data
scoreboard players set #ew dz.data 1
execute if score #lon dz.data matches ..-1 run scoreboard players set #ew dz.data -1
execute if score #lon dz.data matches ..-1 run scoreboard players operation #lon dz.data *= #m1 dz.data
scoreboard players operation #lat_c dz.data = #lat dz.data
scoreboard players operation #lat_c dz.data /= #100 dz.data
scoreboard players operation #lat_u dz.data = #lat dz.data
scoreboard players operation #lat_u dz.data %= #100 dz.data
scoreboard players operation #lon_c dz.data = #lon dz.data
scoreboard players operation #lon_c dz.data /= #100 dz.data
scoreboard players operation #lon_u dz.data = #lon dz.data
scoreboard players operation #lon_u dz.data %= #100 dz.data
tellraw @s {"text":"━━━━━━━━━━━ ✪ GDZIE JESTEM ✪ ━━━━━━━━━━━","color":"aqua","bold":true}
execute if score #lat_u dz.data matches 10.. if score #ns dz.data matches 1 run tellraw @s [{"text":" Szerokość: ","color":"gray"},{"score":{"name":"#lat_c","objective":"dz.data"},"color":"white","bold":true},{"text":".","color":"white","bold":true},{"score":{"name":"#lat_u","objective":"dz.data"},"color":"white","bold":true},{"text":"° N","color":"yellow","bold":true}]
execute if score #lat_u dz.data matches ..9 if score #ns dz.data matches 1 run tellraw @s [{"text":" Szerokość: ","color":"gray"},{"score":{"name":"#lat_c","objective":"dz.data"},"color":"white","bold":true},{"text":".0","color":"white","bold":true},{"score":{"name":"#lat_u","objective":"dz.data"},"color":"white","bold":true},{"text":"° N","color":"yellow","bold":true}]
execute if score #lat_u dz.data matches 10.. if score #ns dz.data matches -1 run tellraw @s [{"text":" Szerokość: ","color":"gray"},{"score":{"name":"#lat_c","objective":"dz.data"},"color":"white","bold":true},{"text":".","color":"white","bold":true},{"score":{"name":"#lat_u","objective":"dz.data"},"color":"white","bold":true},{"text":"° S","color":"yellow","bold":true}]
execute if score #lat_u dz.data matches ..9 if score #ns dz.data matches -1 run tellraw @s [{"text":" Szerokość: ","color":"gray"},{"score":{"name":"#lat_c","objective":"dz.data"},"color":"white","bold":true},{"text":".0","color":"white","bold":true},{"score":{"name":"#lat_u","objective":"dz.data"},"color":"white","bold":true},{"text":"° S","color":"yellow","bold":true}]
execute if score #lon_u dz.data matches 10.. if score #ew dz.data matches 1 run tellraw @s [{"text":" Długość:    ","color":"gray"},{"score":{"name":"#lon_c","objective":"dz.data"},"color":"white","bold":true},{"text":".","color":"white","bold":true},{"score":{"name":"#lon_u","objective":"dz.data"},"color":"white","bold":true},{"text":"° E","color":"yellow","bold":true}]
execute if score #lon_u dz.data matches ..9 if score #ew dz.data matches 1 run tellraw @s [{"text":" Długość:    ","color":"gray"},{"score":{"name":"#lon_c","objective":"dz.data"},"color":"white","bold":true},{"text":".0","color":"white","bold":true},{"score":{"name":"#lon_u","objective":"dz.data"},"color":"white","bold":true},{"text":"° E","color":"yellow","bold":true}]
execute if score #lon_u dz.data matches 10.. if score #ew dz.data matches -1 run tellraw @s [{"text":" Długość:    ","color":"gray"},{"score":{"name":"#lon_c","objective":"dz.data"},"color":"white","bold":true},{"text":".","color":"white","bold":true},{"score":{"name":"#lon_u","objective":"dz.data"},"color":"white","bold":true},{"text":"° W","color":"yellow","bold":true}]
execute if score #lon_u dz.data matches ..9 if score #ew dz.data matches -1 run tellraw @s [{"text":" Długość:    ","color":"gray"},{"score":{"name":"#lon_c","objective":"dz.data"},"color":"white","bold":true},{"text":".0","color":"white","bold":true},{"score":{"name":"#lon_u","objective":"dz.data"},"color":"white","bold":true},{"text":"° W","color":"yellow","bold":true}]
