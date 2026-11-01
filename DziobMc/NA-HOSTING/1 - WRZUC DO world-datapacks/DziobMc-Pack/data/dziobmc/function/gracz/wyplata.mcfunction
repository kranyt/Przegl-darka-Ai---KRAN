# Nagroda za każde 5 minut gry
scoreboard players set @s dz.czas 0
scoreboard players add @s dz.minuty 5
scoreboard players set #ile dz.data 10
tellraw @s {"text":"⌚ Nagroda za aktywną grę (5 min):","color":"aqua"}
function dziobmc:monety/dodaj
