# Earth SMP – inicjalizacja
scoreboard objectives add dz.kraj dummy
scoreboard objectives add dz.id dummy
scoreboard objectives add dz.prosba dummy
scoreboard objectives add dz.rid dummy
scoreboard objectives add dz.mojwrog dummy
scoreboard objectives add dz.k_czl dummy
scoreboard objectives add dz.k_skarb dummy
scoreboard objectives add dz.k_wl dummy
scoreboard objectives add dz.k_zamk dummy
scoreboard objectives add dz.k_wrog dummy
scoreboard objectives add dz.k_pkt dummy
scoreboard objectives add dz.k_wczas dummy
scoreboard objectives add dz.k_wygr dummy
scoreboard objectives add dz.k_pokoj dummy
scoreboard objectives add dz.cd_stol dummy
scoreboard objectives add dz.kc dummy
scoreboard objectives add panstwo trigger
scoreboard objectives add stolica trigger
scoreboard objectives add skarbiec trigger
scoreboard objectives add wojna trigger
scoreboard objectives add przyjmij trigger
scoreboard objectives add ziemia trigger
scoreboard objectives add gdzie trigger
scoreboard objectives add dz.ranking dummy [{"text":"✪ ","color":"aqua"},{"text":"Potęga państw","color":"gold","bold":true}]
execute unless score #skala dz.data matches 1.. run scoreboard players set #skala dz.data 2000
scoreboard players set #11132 dz.data 11132
scoreboard players set #m11132 dz.data -11132
scoreboard players set #1113 dz.data 1113
scoreboard players set #111320 dz.data 111320
scoreboard players set #40075200 dz.data 40075200
scoreboard players set #30 dz.data 30
scoreboard players set #500 dz.data 500
scoreboard players set #1000 dz.data 1000
scoreboard players set #m1 dz.data -1
function dziobmc:kraje/init
function dziobmc:ziemia/przelicz
