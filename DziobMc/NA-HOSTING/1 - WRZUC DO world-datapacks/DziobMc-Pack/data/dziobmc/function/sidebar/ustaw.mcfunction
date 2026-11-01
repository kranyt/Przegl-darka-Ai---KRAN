scoreboard players reset * dz.sidebar
scoreboard players set dz.l1 dz.sidebar 1006
scoreboard players display name dz.l1 dz.sidebar {"text":""}
scoreboard players display numberformat dz.l1 dz.sidebar blank
scoreboard players set dz.l2 dz.sidebar 1005
scoreboard players display name dz.l2 dz.sidebar [{"text":" ✦ ","color":"gold"},{"text":"Serwer: ","color":"gray"},{"text":"DziobMc","color":"yellow","bold":true}]
scoreboard players display numberformat dz.l2 dz.sidebar blank
scoreboard players set dz.l3 dz.sidebar 1004
scoreboard players display name dz.l3 dz.sidebar [{"text":" ✦ ","color":"gold"},{"text":"Wersje: ","color":"gray"},{"text":"1.16.4+","color":"white"}]
scoreboard players display numberformat dz.l3 dz.sidebar blank
scoreboard players set dz.l4 dz.sidebar 1003
scoreboard players display name dz.l4 dz.sidebar {"text":" "}
scoreboard players display numberformat dz.l4 dz.sidebar blank
scoreboard players set dz.total dz.sidebar 0
scoreboard players display name dz.total dz.sidebar [{"text":" ● ","color":"green"},{"text":"Graczy łącznie","color":"white"}]
scoreboard players display numberformat dz.total dz.sidebar styled {"color":"yellow","bold":true}
scoreboard players set dz.online dz.sidebar 0
scoreboard players display name dz.online dz.sidebar [{"text":" ● ","color":"green"},{"text":"Online","color":"white"}]
scoreboard players display numberformat dz.online dz.sidebar styled {"color":"yellow","bold":true}
scoreboard players set dz.l5 dz.sidebar -1
scoreboard players display name dz.l5 dz.sidebar {"text":"  "}
scoreboard players display numberformat dz.l5 dz.sidebar blank
scoreboard players set dz.l6 dz.sidebar -3
scoreboard players display name dz.l6 dz.sidebar [{"text":" ➤ ","color":"aqua"},{"text":"/trigger pomoc","color":"aqua"}]
scoreboard players display numberformat dz.l6 dz.sidebar blank
scoreboard players set dz.l7 dz.sidebar -4
scoreboard players display name dz.l7 dz.sidebar [{"text":" ⛃ ","color":"gold"},{"text":"Monety: lista TAB","color":"gray"}]
scoreboard players display numberformat dz.l7 dz.sidebar blank
scoreboard players set dz.l8 dz.sidebar -5
scoreboard players display name dz.l8 dz.sidebar {"text":"   "}
scoreboard players display numberformat dz.l8 dz.sidebar blank
scoreboard players set dz.l9 dz.sidebar -6
scoreboard players display name dz.l9 dz.sidebar [{"text":"    Dziob.fun","color":"yellow","bold":true}]
scoreboard players display numberformat dz.l9 dz.sidebar blank
function dziobmc:sidebar/event_linia
