execute store result score #r dz.data run random value 1..7
execute if score #r dz.data matches 1 run function dziobmc:moby/przywolaj/wojownik
execute if score #r dz.data matches 2 run function dziobmc:moby/przywolaj/ognisty
execute if score #r dz.data matches 3 run function dziobmc:moby/przywolaj/lucznik
execute if score #r dz.data matches 4 run function dziobmc:moby/przywolaj/lodowy
execute if score #r dz.data matches 5 run function dziobmc:moby/przywolaj/pajak
execute if score #r dz.data matches 6 run function dziobmc:moby/przywolaj/kreeper
execute if score #r dz.data matches 7 run function dziobmc:moby/przywolaj/widmo
