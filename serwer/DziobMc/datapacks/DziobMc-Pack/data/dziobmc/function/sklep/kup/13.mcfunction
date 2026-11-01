scoreboard players set #cena dz.data 120
execute unless score @s dz.coins >= #cena dz.data run return run function dziobmc:sklep/brak
scoreboard players operation @s dz.coins -= #cena dz.data
give @s minecraft:ender_pearl 16
tellraw @s [{"text":"✔ Kupiono: ","color":"green"},{"text":"Perły Endu x16","color":"dark_aqua","bold":true},{"text":" za 120 monet!","color":"green"}]
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
