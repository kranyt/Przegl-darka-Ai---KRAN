execute as @a[scores={panstwo=1..}] at @s run function dziobmc:komendy/panstwo
execute as @a[scores={stolica=1..}] at @s run function dziobmc:komendy/stolica
execute as @a[scores={skarbiec=1..}] at @s run function dziobmc:komendy/skarbiec
execute as @a[scores={wojna=1..}] at @s run function dziobmc:komendy/wojna
execute as @a[scores={przyjmij=1..}] at @s run function dziobmc:komendy/przyjmij
execute as @a[scores={ziemia=1..}] at @s run function dziobmc:komendy/ziemia
execute as @a[scores={gdzie=1..}] at @s run function dziobmc:komendy/gdzie
execute as @a[scores={skarbiec=..-1}] at @s run function dziobmc:komendy/skarbiec
scoreboard players enable @a panstwo
scoreboard players enable @a stolica
scoreboard players enable @a skarbiec
scoreboard players enable @a wojna
scoreboard players enable @a przyjmij
scoreboard players enable @a ziemia
scoreboard players enable @a gdzie
