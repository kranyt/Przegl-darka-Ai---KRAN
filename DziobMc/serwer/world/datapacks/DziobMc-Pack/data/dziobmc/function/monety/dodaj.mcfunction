# Wejście: #ile dz.data – mnożnik eventu i bonus rangi
scoreboard players operation #ile dz.data *= #mult dz.data
execute if score @s dz.rank matches 1 run function dziobmc:monety/bonus_vip
execute if score @s dz.rank matches 2.. run function dziobmc:monety/bonus_mvp
scoreboard players operation @s dz.coins += #ile dz.data
tellraw @s [{"text":"  + ","color":"gold"},{"score":{"name":"#ile","objective":"dz.data"},"color":"gold","bold":true},{"text":" monet ⛃","color":"yellow"}]
playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 0.6 1.6
