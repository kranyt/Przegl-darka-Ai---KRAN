scoreboard players set #kaiju_typ dz.data 2
scoreboard players set #kaiju_jest dz.data 0
scoreboard players set #kaiju_zabity dz.data 0
data modify storage dziobmc:tmp ka set from storage dziobmc:kraje s.k11
function dziobmc:kaiju/forceload_m with storage dziobmc:tmp ka
schedule function dziobmc:kaiju/atak_spawn 60t replace
tellraw @a [{"text":"⚠ ","color":"dark_red","bold":true},{"text":"LODOWY TYTAN","color":"aqua","bold":true},{"text":" atakuje stolicę ","color":"red"},{"text":"Helsinki","color":"white","bold":true},{"text":" (","color":"gray"},{"text":"Finlandia","color":"white"},{"text":")! ","color":"gray"},{"text":"[LEĆ DO WALKI]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/trigger stolica set 111"},"hoverEvent":{"action":"show_text","contents":{"text":"Teleport do stolicy"}}}]
title @a times 10 70 20
title @a title {"text":"⚠ LODOWY TYTAN ⚠","color":"aqua","bold":true}
title @a subtitle [{"text":"atakuje ","color":"red"},{"text":"Helsinki","color":"white","bold":true},{"text":"!","color":"red"}]
execute as @a at @s run playsound minecraft:event.raid.horn master @s ~ ~ ~ 1 0.6
