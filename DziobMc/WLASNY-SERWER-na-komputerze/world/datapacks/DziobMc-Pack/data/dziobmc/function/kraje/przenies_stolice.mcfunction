execute at @s unless dimension minecraft:ziemia run return run tellraw @s {"text":"✖ Stolicę można przenieść tylko na mapie Ziemi.","color":"red"}
scoreboard players add @s dz.cd_przen 0
scoreboard players set #cd dz.data 72000
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s dz.cd_przen
execute if score #roznica dz.data < #cd dz.data run return run function dziobmc:util/cooldown_info
scoreboard players operation @s dz.cd_przen = #teraz dz.data
execute store result storage dziobmc:tmp ps.id int 1 run scoreboard players get @s dz.kid
execute store result storage dziobmc:tmp ps.x int 1 run data get entity @s Pos[0]
execute store result storage dziobmc:tmp ps.z int 1 run data get entity @s Pos[2]
execute store result score #x dz.data run data get entity @s Pos[0]
execute store result score #z dz.data run data get entity @s Pos[2]
scoreboard players remove #x dz.data 64
scoreboard players remove #z dz.data 64
execute store result storage dziobmc:tmp ps.x0 int 1 run scoreboard players get #x dz.data
execute store result storage dziobmc:tmp ps.z0 int 1 run scoreboard players get #z dz.data
function dziobmc:kraje/przenies_m with storage dziobmc:tmp ps
tellraw @s {"text":"✔ Stolica twojego państwa jest teraz tutaj! Strefa ochronna: 64 kratki.","color":"green","bold":true}
playsound minecraft:block.beacon.activate master @s ~ ~ ~ 1 1
