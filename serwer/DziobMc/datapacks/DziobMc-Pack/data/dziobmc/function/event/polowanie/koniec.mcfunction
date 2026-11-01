scoreboard players set #szansa dz.data 12
execute unless score #polowanie_wygrane dz.data matches 1 run tellraw @a {"text":"⚔ Polowanie zakończone – nikt nie zdobył 10 punktów!","color":"red"}
scoreboard players set #polowanie_wygrane dz.data 0
