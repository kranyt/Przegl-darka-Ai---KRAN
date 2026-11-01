function dziobmc:kaiju/szczeka/otworz
playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..120] ~ ~ ~ 3 0.6
scoreboard players set #krok dz.data 0
execute positioned ^ ^17.5 ^6 facing entity @p[distance=..60,gamemode=!spectator,gamemode=!creative] feet run function dziobmc:kaiju/dziobzilla/promien
schedule function dziobmc:kaiju/dziobzilla/po_oddechu 30t replace
