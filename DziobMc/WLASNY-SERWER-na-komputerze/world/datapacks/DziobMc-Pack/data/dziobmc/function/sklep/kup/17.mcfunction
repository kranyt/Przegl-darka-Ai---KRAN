scoreboard players set #cena dz.data 1500
execute unless score @s dz.coins >= #cena dz.data run return run function dziobmc:sklep/brak
scoreboard players operation @s dz.coins -= #cena dz.data
give @s minecraft:netherite_sword[enchantments={levels:{"minecraft:sharpness":5,"minecraft:unbreaking":3,"minecraft:fire_aspect":2,"minecraft:looting":3,"minecraft:mending":1}},custom_name='{"text":"Miecz Dzioba","color":"gold","italic":false,"bold":true}',lore=['{"text":"Legendarny miecz serwera DziobMc","color":"gray","italic":false}','{"text":"Dziob.fun","color":"gray","italic":false}']] 1
tellraw @s [{"text":"✔ Kupiono: ","color":"green"},{"text":"Miecz Dzioba","color":"gold","bold":true},{"text":" za 1500 monet!","color":"green"}]
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 1 1
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.5
