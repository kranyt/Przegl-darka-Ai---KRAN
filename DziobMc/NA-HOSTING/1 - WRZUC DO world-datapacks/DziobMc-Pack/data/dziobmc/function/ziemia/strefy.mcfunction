tag @a remove dz.strefa_obca
scoreboard players set @a dz.mojwrog 0
execute as @a[scores={dz.kid=1..}] run function dziobmc:kraje/mojwrog
scoreboard players set #iter_tryb dz.data 1
function dziobmc:kraje/iter
gamemode adventure @a[tag=dz.strefa_obca,gamemode=survival,tag=!dz.build]
execute as @a[tag=dz.strefa_obca,tag=!dz.strefa_bylo] run tellraw @s {"text":"⛨ Wchodzisz do chronionej stolicy obcego państwa – nie możesz tu niszczyć bloków.","color":"gold"}
tag @a[tag=dz.strefa_obca] add dz.strefa_bylo
gamemode survival @a[tag=!dz.strefa_obca,tag=dz.strefa_bylo,tag=!dz.lobby,gamemode=adventure,tag=!dz.build]
tag @a[tag=!dz.strefa_obca] remove dz.strefa_bylo
