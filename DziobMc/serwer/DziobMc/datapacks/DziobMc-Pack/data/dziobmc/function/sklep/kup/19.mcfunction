scoreboard players set #cena dz.data 2500
execute unless score @s dz.coins >= #cena dz.data run return run function dziobmc:sklep/brak
scoreboard players operation @s dz.coins -= #cena dz.data
give @s minecraft:elytra[enchantments={levels:{"minecraft:unbreaking":3}},custom_name='{"text":"Skrzydła Dzioba","color":"dark_purple","italic":false,"bold":true}'] 1
give @s minecraft:firework_rocket 32
tellraw @s [{"text":"✔ Kupiono: ","color":"green"},{"text":"Elytra + 32 fajerwerki","color":"dark_purple","bold":true},{"text":" za 2500 monet!","color":"green"}]
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
