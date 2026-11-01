scoreboard players remove #k22 dz.k_wczas 1
execute if score #k22 dz.k_wczas matches ..0 store result storage dziobmc:tmp k.b int 1 run scoreboard players get #k22 dz.k_wrog
execute if score #k22 dz.k_wczas matches ..0 run data modify storage dziobmc:tmp k.a set value 22
execute if score #k22 dz.k_wczas matches ..0 run function dziobmc:wojna/koniec with storage dziobmc:tmp k
