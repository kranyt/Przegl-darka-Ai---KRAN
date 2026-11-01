# gracz poza mapą Ziemi: stolica obok prawdziwej, przesunięta o 160 kratek na numer
execute store result score #x dz.data run data get storage dziobmc:tmp wn.x
scoreboard players operation #q dz.data = #n dz.data
scoreboard players remove #q dz.data 1
scoreboard players operation #q dz.data *= #160 dz.data
scoreboard players operation #x dz.data += #q dz.data
execute store result storage dziobmc:tmp wn.x int 1 run scoreboard players get #x dz.data
