scoreboard players set #cena dz.data 150
execute unless score @s dz.coins >= #cena dz.data run return run function dziobmc:sklep/brak
scoreboard players operation @s dz.coins -= #cena dz.data
give @s minecraft:diamond 8
tellraw @s [{"text":"✔ Kupiono: ","color":"green"},{"text":"Diamenty x8","color":"aqua","bold":true},{"text":" za 150 monet!","color":"green"}]
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
