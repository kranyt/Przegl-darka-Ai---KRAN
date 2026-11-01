particle minecraft:falling_dust{block_state:{Name:"minecraft:sand"}} ~ ~6 ~ 12 5 12 0 400 force
particle minecraft:campfire_cosy_smoke ~ ~2 ~ 10 2 10 0.02 60 force
playsound minecraft:weather.rain.above hostile @a[distance=..60] ~ ~ ~ 2 0.5
effect give @a[distance=..22,gamemode=!creative,gamemode=!spectator] minecraft:blindness 4 0
effect give @a[distance=..22,gamemode=!creative,gamemode=!spectator] minecraft:slowness 4 1
