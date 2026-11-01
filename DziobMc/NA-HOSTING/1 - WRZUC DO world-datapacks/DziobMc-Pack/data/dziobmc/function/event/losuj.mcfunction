execute store result score #los dz.data run random value 1..7
execute if score #los dz.data matches 1 run function dziobmc:event/start/krwawy
execute if score #los dz.data matches 2 run function dziobmc:event/start/drop
execute if score #los dz.data matches 3 run function dziobmc:event/start/boss
execute if score #los dz.data matches 4 run function dziobmc:event/start/podwojne
execute if score #los dz.data matches 5 run function dziobmc:event/start/polowanie
execute if score #los dz.data matches 6 run function dziobmc:event/start/deszcz
execute if score #los dz.data matches 7 run function dziobmc:event/start/bitwa
