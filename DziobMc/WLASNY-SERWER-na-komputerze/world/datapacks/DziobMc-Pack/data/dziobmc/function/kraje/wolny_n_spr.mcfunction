$execute if data storage dziobmc:kraje lista[{id:$(id)}] run function dziobmc:kraje/wolny_n_krok
$data modify storage dziobmc:tmp wn merge from storage dziobmc:kraje b.k$(k)
execute if score #n dz.data matches 1 run data modify storage dziobmc:tmp wn.nn set value ""
execute unless score #n dz.data matches 1 store result storage dziobmc:tmp wn.nn int 1 run scoreboard players get #n dz.data
