scoreboard players set #cena dz.data 250
execute unless score @s dz.coins >= #cena dz.data run return run function dziobmc:sklep/brak
scoreboard players operation @s dz.coins -= #cena dz.data
loot give @s loot dziobmc:skrzynia_szczescia
tellraw @s [{"text":"✔ Kupiono: ","color":"green"},{"text":"Skrzynia Szczęścia","color":"light_purple","bold":true},{"text":" za 250 monet!","color":"green"}]
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
