scoreboard players set #cena dz.data 400
execute unless score @s dz.coins >= #cena dz.data run return run function dziobmc:sklep/brak
scoreboard players operation @s dz.coins -= #cena dz.data
give @s minecraft:totem_of_undying 1
tellraw @s [{"text":"✔ Kupiono: ","color":"green"},{"text":"Totem Nieśmiertelności","color":"yellow","bold":true},{"text":" za 400 monet!","color":"green"}]
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
