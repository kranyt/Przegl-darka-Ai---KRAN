scoreboard players remove #k52 dz.k_wczas 1
execute if score #k52 dz.k_wczas matches ..0 store result storage dziobmc:tmp k.b int 1 run scoreboard players get #k52 dz.k_wrog
execute if score #k52 dz.k_wczas matches ..0 run data modify storage dziobmc:tmp k.a set value 52
execute if score #k52 dz.k_wczas matches ..0 run function dziobmc:wojna/koniec with storage dziobmc:tmp k
