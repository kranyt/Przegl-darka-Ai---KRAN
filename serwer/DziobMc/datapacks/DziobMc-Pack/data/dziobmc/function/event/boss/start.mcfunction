scoreboard players set #boss_zabity dz.data 0
scoreboard players set #boss_jest dz.data 0
scoreboard players set #szal dz.data 0
scoreboard players set #bt dz.data 0
execute in minecraft:overworld run forceload add -24 -99 24 -51
schedule function dziobmc:event/boss/przywolaj 60t replace
