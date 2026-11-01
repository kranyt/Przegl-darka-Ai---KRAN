function dziobmc:mapa/etap/wyspa
function dziobmc:mapa/etap/plac
function dziobmc:mapa/etap/arena
function dziobmc:mapa/etap/parkour
function dziobmc:mapa/dekoracje
setworldspawn 0 151 18
scoreboard players set #mapa dz.data 1
tp @a 0 151 18 180 0
tellraw @a [{"text":"✔ ","color":"green"},{"text":"Mapa DziobMc zbudowana! ","color":"green","bold":true},{"text":"Spawn: 0 151 18","color":"gray"}]
schedule function dziobmc:mapa/zakoncz 100t replace
