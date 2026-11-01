# Gracze: pierwsze wejście / powrót / brak rangi
execute as @a[tag=!dz.joined] at @s run function dziobmc:gracz/pierwsze_wejscie
execute as @a[scores={dz.leave=1..}] at @s run function dziobmc:gracz/powrot
execute as @a[team=] run function dziobmc:rangi/domyslna
# Komendy /trigger
execute as @a[scores={pomoc=1..}] at @s run function dziobmc:komendy/pomoc
execute as @a[scores={spawn=1..}] at @s run function dziobmc:komendy/spawn
execute as @a[scores={kit=1..}] at @s run function dziobmc:komendy/kit
execute as @a[scores={sklep=1..}] at @s run function dziobmc:komendy/sklep
execute as @a[scores={nagroda=1..}] at @s run function dziobmc:komendy/nagroda
execute as @a[scores={staty=1..}] at @s run function dziobmc:komendy/staty
execute as @a[scores={discord=1..}] at @s run function dziobmc:komendy/discord
execute as @a[scores={event=1..}] at @s run function dziobmc:komendy/event
execute as @a[scores={rtp=1..}] at @s run function dziobmc:komendy/rtp
execute as @a[scores={warp=1..}] at @s run function dziobmc:komendy/warp
execute as @a[scores={rangi=1..}] at @s run function dziobmc:komendy/rangi
scoreboard players enable @a pomoc
scoreboard players enable @a spawn
scoreboard players enable @a kit
scoreboard players enable @a sklep
scoreboard players enable @a nagroda
scoreboard players enable @a staty
scoreboard players enable @a discord
scoreboard players enable @a event
scoreboard players enable @a rtp
scoreboard players enable @a warp
scoreboard players enable @a rangi
# Spadanie z wyspy-lobby
execute as @a[tag=dz.lobby] at @s if entity @s[y=-64,dy=203] run function dziobmc:lobby/spadek
