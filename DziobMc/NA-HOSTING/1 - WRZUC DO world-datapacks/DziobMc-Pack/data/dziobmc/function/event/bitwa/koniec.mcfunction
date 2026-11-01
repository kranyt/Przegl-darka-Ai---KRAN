scoreboard players add @a dz.bitwa 0
scoreboard players set #max dz.data 0
scoreboard players operation #max dz.data > @a dz.bitwa
execute if score #max dz.data matches 0 run tellraw @a {"text":"⚔ Bitwa PvP zakończona – nikt nikogo nie pokonał!","color":"red"}
execute if score #max dz.data matches 1.. as @a if score @s dz.bitwa = #max dz.data at @s run function dziobmc:event/bitwa/zwyciezca
