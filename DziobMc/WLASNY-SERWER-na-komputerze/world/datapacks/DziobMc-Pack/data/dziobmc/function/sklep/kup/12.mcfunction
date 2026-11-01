scoreboard players set #cena dz.data 100
execute unless score @s dz.coins >= #cena dz.data run return run function dziobmc:sklep/brak
scoreboard players operation @s dz.coins -= #cena dz.data
give @s minecraft:golden_apple 5
tellraw @s [{"text":"✔ Kupiono: ","color":"green"},{"text":"Złote jabłka x5","color":"gold","bold":true},{"text":" za 100 monet!","color":"green"}]
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
