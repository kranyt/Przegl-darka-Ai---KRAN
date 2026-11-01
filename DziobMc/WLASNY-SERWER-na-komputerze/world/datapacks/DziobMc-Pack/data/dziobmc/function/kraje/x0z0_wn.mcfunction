execute store result score #x dz.data run data get storage dziobmc:tmp wn.x
execute store result score #z dz.data run data get storage dziobmc:tmp wn.z
scoreboard players remove #x dz.data 64
scoreboard players remove #z dz.data 64
execute store result storage dziobmc:tmp wn.x0 int 1 run scoreboard players get #x dz.data
execute store result storage dziobmc:tmp wn.z0 int 1 run scoreboard players get #z dz.data
