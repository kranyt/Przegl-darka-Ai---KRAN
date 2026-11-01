scoreboard players set #cena dz.data 200
execute unless score @s dz.coins >= #cena dz.data run return run function dziobmc:sklep/brak
scoreboard players operation @s dz.coins -= #cena dz.data
give @s minecraft:experience_bottle 64
tellraw @s [{"text":"✔ Kupiono: ","color":"green"},{"text":"Butelki XP x64","color":"green","bold":true},{"text":" za 200 monet!","color":"green"}]
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
