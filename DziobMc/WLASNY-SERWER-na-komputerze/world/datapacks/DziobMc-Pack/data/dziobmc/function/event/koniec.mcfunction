execute if score #event dz.data matches 1 run function dziobmc:event/krwawy/koniec
execute if score #event dz.data matches 2 run function dziobmc:event/drop/koniec
execute if score #event dz.data matches 3 run function dziobmc:event/boss/koniec
execute if score #event dz.data matches 4 run function dziobmc:event/podwojne/koniec
execute if score #event dz.data matches 5 run function dziobmc:event/polowanie/koniec
execute if score #event dz.data matches 6 run function dziobmc:event/deszcz/koniec
execute if score #event dz.data matches 7 run function dziobmc:event/bitwa/koniec
scoreboard players set #event dz.data 0
scoreboard players set #left dz.data 0
scoreboard players set #next dz.data 1200
bossbar set dziobmc:event max 1200
bossbar set dziobmc:event color yellow
function dziobmc:sidebar/event_linia
execute as @a at @s run playsound minecraft:block.beacon.deactivate master @s ~ ~ ~ 0.7 1
