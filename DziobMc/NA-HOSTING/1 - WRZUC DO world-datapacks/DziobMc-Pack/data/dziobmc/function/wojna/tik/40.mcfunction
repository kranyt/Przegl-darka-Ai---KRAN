scoreboard players remove #k40 dz.k_wczas 1
execute if score #k40 dz.k_wczas matches ..0 store result storage dziobmc:tmp k.b int 1 run scoreboard players get #k40 dz.k_wrog
execute if score #k40 dz.k_wczas matches ..0 run data modify storage dziobmc:tmp k.a set value 40
execute if score #k40 dz.k_wczas matches ..0 run function dziobmc:wojna/koniec with storage dziobmc:tmp k
