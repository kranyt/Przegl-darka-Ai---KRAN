# ===================== DziobMc • Dziob.fun =====================
scoreboard objectives add dz.data dummy
scoreboard objectives add dz.coins dummy {"text":"⛃ Monety","color":"gold"}
scoreboard objectives add dz.kills dummy {"text":"Zabite moby","color":"red"}
scoreboard objectives add dz.pvp playerKillCount {"text":"Zabici gracze","color":"dark_red"}
scoreboard objectives add dz.deaths deathCount {"text":"Śmierci","color":"gray"}
scoreboard objectives add dz.hp health {"text":"❤","color":"red"}
scoreboard objectives add dz.leave minecraft.custom:minecraft.leave_game
scoreboard objectives add dz.rank dummy
scoreboard objectives add dz.czas dummy
scoreboard objectives add dz.minuty dummy
scoreboard objectives add dz.hunt dummy
scoreboard objectives add dz.zab playerKillCount
scoreboard objectives add dz.smierc deathCount
scoreboard objectives add dz.streak dummy
scoreboard objectives add dz.bitwa dummy
scoreboard objectives add dz.sidebar dummy [{"text":"✦ ","color":"yellow"},{"text":"DziobMc","color":"gold","bold":true},{"text":" ✦","color":"yellow"}]
scoreboard objectives add dz.cd_kit1 dummy
scoreboard objectives add dz.cd_kit2 dummy
scoreboard objectives add dz.cd_kit3 dummy
scoreboard objectives add dz.cd_kit4 dummy
scoreboard objectives add dz.cd_nagr dummy
scoreboard objectives add dz.cd_spawn dummy
scoreboard objectives add dz.cd_rtp dummy
scoreboard objectives add dz.cd_park dummy
scoreboard objectives add dz.cd_kit5 dummy
scoreboard objectives add pomoc trigger
scoreboard objectives add spawn trigger
scoreboard objectives add kit trigger
scoreboard objectives add sklep trigger
scoreboard objectives add nagroda trigger
scoreboard objectives add staty trigger
scoreboard objectives add discord trigger
scoreboard objectives add event trigger
scoreboard objectives add rtp trigger
scoreboard objectives add warp trigger
scoreboard objectives add rangi trigger
scoreboard objectives setdisplay sidebar dz.sidebar
scoreboard objectives setdisplay list dz.coins
scoreboard objectives setdisplay below_name dz.hp
scoreboard players set #2 dz.data 2
scoreboard players set #3 dz.data 3
scoreboard players set #4 dz.data 4
scoreboard players set #5 dz.data 5
scoreboard players set #8 dz.data 8
scoreboard players set #10 dz.data 10
scoreboard players set #11 dz.data 11
scoreboard players set #15 dz.data 15
scoreboard players set #20 dz.data 20
scoreboard players set #60 dz.data 60
scoreboard players set #100 dz.data 100
scoreboard players set #1200 dz.data 1200
execute unless score #init dz.data matches 1 run function dziobmc:init
function dziobmc:ziemia/init
function dziobmc:sidebar/ustaw
bossbar add dziobmc:event {"text":"DziobMc","color":"gold"}
bossbar set dziobmc:event color yellow
bossbar set dziobmc:event style notched_20
bossbar set dziobmc:event visible true
bossbar add dziobmc:boss {"text":"♛ Król Dziobów ♛","color":"gold","bold":true}
bossbar set dziobmc:boss color red
bossbar set dziobmc:boss style notched_10
bossbar set dziobmc:boss max 600
execute unless score #event dz.data matches 3 run bossbar set dziobmc:boss visible false
gamerule spawnRadius 0
schedule function dziobmc:petla/sekunda 20t replace
execute unless score #mapa dz.data matches 1 run schedule function dziobmc:mapa/zbuduj 100t replace
tellraw @a [{"text":"✦ ","color":"gold"},{"text":"DziobMc","color":"gold","bold":true},{"text":" » Paczka załadowana! ","color":"yellow"},{"text":"Dziob.fun","color":"white","underlined":true}]
