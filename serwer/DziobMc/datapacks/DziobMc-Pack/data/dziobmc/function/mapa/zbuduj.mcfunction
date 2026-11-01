# Buduje całą mapę lobby. Można uruchomić ponownie (/function dziobmc:mapa/zbuduj)
tellraw @a [{"text":"✦ ","color":"gold"},{"text":"Ładowanie terenu pod mapę DziobMc...","color":"yellow"}]
execute in minecraft:overworld run forceload add -112 -112 112 112
scoreboard players set #proby dz.data 0
schedule function dziobmc:mapa/czekaj 40t replace
