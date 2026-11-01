scoreboard players set #cena dz.data 1800
execute unless score @s dz.coins >= #cena dz.data run return run function dziobmc:sklep/brak
scoreboard players operation @s dz.coins -= #cena dz.data
give @s minecraft:netherite_pickaxe[enchantments={levels:{"minecraft:efficiency":5,"minecraft:fortune":3,"minecraft:unbreaking":3,"minecraft:mending":1}},custom_name='{"text":"Kilof Dzioba","color":"gold","italic":false,"bold":true}',lore=['{"text":"Kopie szybciej niż dziob dzięcioła","color":"gray","italic":false}']] 1
tellraw @s [{"text":"✔ Kupiono: ","color":"green"},{"text":"Kilof Dzioba","color":"gold","bold":true},{"text":" za 1800 monet!","color":"green"}]
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
