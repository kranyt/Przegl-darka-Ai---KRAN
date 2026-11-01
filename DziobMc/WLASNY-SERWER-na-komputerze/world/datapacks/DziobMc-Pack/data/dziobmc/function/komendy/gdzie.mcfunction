execute at @s unless dimension minecraft:ziemia run return run tellraw @s [{"text":"✖ Komenda działa na mapie Ziemi. ","color":"red"},{"text":"[LECĘ]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/trigger ziemia set 11"}}]
execute store result score #px dz.data run data get entity @s Pos[0]
execute store result score #pz dz.data run data get entity @s Pos[2]
scoreboard players operation #lon dz.data = #px dz.data
scoreboard players operation #lon dz.data *= #skala dz.data
scoreboard players operation #lon dz.data /= #1113 dz.data
scoreboard players operation #lat dz.data = #pz dz.data
scoreboard players operation #lat dz.data *= #skala dz.data
scoreboard players operation #lat dz.data /= #1113 dz.data
scoreboard players operation #lat dz.data *= #m1 dz.data
function dziobmc:ziemia/gdzie_format
scoreboard players set #min dz.data 2147483647
scoreboard players set #najbl dz.data 0
scoreboard players operation #dx dz.data = #sx1 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz1 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 1
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx2 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz2 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 2
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx3 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz3 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 3
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx4 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz4 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 4
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx5 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz5 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 5
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx6 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz6 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 6
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx7 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz7 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 7
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx8 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz8 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 8
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx9 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz9 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 9
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx10 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz10 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 10
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx11 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz11 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 11
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx12 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz12 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 12
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx13 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz13 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 13
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx14 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz14 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 14
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx15 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz15 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 15
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx16 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz16 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 16
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx17 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz17 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 17
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx18 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz18 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 18
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx19 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz19 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 19
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx20 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz20 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 20
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx21 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz21 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 21
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx22 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz22 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 22
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx23 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz23 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 23
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx24 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz24 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 24
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx25 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz25 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 25
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx26 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz26 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 26
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx27 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz27 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 27
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx28 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz28 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 28
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx29 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz29 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 29
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx30 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz30 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 30
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx31 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz31 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 31
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx32 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz32 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 32
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx33 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz33 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 33
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx34 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz34 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 34
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx35 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz35 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 35
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx36 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz36 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 36
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx37 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz37 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 37
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx38 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz38 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 38
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx39 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz39 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 39
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx40 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz40 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 40
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx41 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz41 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 41
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx42 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz42 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 42
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx43 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz43 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 43
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx44 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz44 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 44
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx45 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz45 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 45
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx46 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz46 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 46
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx47 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz47 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 47
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx48 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz48 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 48
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx49 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz49 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 49
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx50 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz50 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 50
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx51 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz51 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 51
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx52 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz52 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 52
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx53 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz53 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 53
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx54 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz54 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 54
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx55 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz55 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 55
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #dx dz.data = #sx56 dz.data
scoreboard players operation #dx dz.data -= #px dz.data
scoreboard players operation #dz dz.data = #sz56 dz.data
scoreboard players operation #dz dz.data -= #pz dz.data
scoreboard players operation #dx dz.data /= #10 dz.data
scoreboard players operation #dz dz.data /= #10 dz.data
scoreboard players operation #dx dz.data *= #dx dz.data
scoreboard players operation #dz dz.data *= #dz dz.data
scoreboard players operation #dx dz.data += #dz dz.data
execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data 56
scoreboard players operation #min dz.data < #dx dz.data
scoreboard players operation #sq dz.data = #min dz.data
function dziobmc:util/sqrt
scoreboard players operation #sq dz.data *= #10 dz.data
execute if score #najbl dz.data matches 1 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Warszawa","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Polska","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 2 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Berlin","color":"dark_gray","bold":true},{"text":" (","color":"gray"},{"text":"Niemcy","color":"dark_gray","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 3 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Paryż","color":"blue","bold":true},{"text":" (","color":"gray"},{"text":"Francja","color":"blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 4 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Londyn","color":"dark_blue","bold":true},{"text":" (","color":"gray"},{"text":"Wielka Brytania","color":"dark_blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 5 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Madryt","color":"gold","bold":true},{"text":" (","color":"gray"},{"text":"Hiszpania","color":"gold","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 6 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Rzym","color":"green","bold":true},{"text":" (","color":"gray"},{"text":"Włochy","color":"green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 7 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Kijów","color":"yellow","bold":true},{"text":" (","color":"gray"},{"text":"Ukraina","color":"yellow","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 8 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Moskwa","color":"white","bold":true},{"text":" (","color":"gray"},{"text":"Rosja","color":"white","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 9 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Sztokholm","color":"aqua","bold":true},{"text":" (","color":"gray"},{"text":"Szwecja","color":"aqua","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 10 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Oslo","color":"dark_red","bold":true},{"text":" (","color":"gray"},{"text":"Norwegia","color":"dark_red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 11 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Helsinki","color":"white","bold":true},{"text":" (","color":"gray"},{"text":"Finlandia","color":"white","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 12 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Praga","color":"blue","bold":true},{"text":" (","color":"gray"},{"text":"Czechy","color":"blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 13 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Bratysława","color":"blue","bold":true},{"text":" (","color":"gray"},{"text":"Słowacja","color":"blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 14 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Wilno","color":"yellow","bold":true},{"text":" (","color":"gray"},{"text":"Litwa","color":"yellow","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 15 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Wiedeń","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Austria","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 16 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Berno","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Szwajcaria","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 17 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Amsterdam","color":"gold","bold":true},{"text":" (","color":"gray"},{"text":"Holandia","color":"gold","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 18 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Budapeszt","color":"dark_green","bold":true},{"text":" (","color":"gray"},{"text":"Węgry","color":"dark_green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 19 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Bukareszt","color":"yellow","bold":true},{"text":" (","color":"gray"},{"text":"Rumunia","color":"yellow","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 20 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Ateny","color":"aqua","bold":true},{"text":" (","color":"gray"},{"text":"Grecja","color":"aqua","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 21 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Lizbona","color":"dark_green","bold":true},{"text":" (","color":"gray"},{"text":"Portugalia","color":"dark_green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 22 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Ankara","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Turcja","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 23 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Reykjavik","color":"blue","bold":true},{"text":" (","color":"gray"},{"text":"Islandia","color":"blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 24 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Kopenhaga","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Dania","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 25 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Waszyngton","color":"blue","bold":true},{"text":" (","color":"gray"},{"text":"USA","color":"blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 26 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Ottawa","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Kanada","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 27 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Meksyk","color":"dark_green","bold":true},{"text":" (","color":"gray"},{"text":"Meksyk","color":"dark_green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 28 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Hawana","color":"blue","bold":true},{"text":" (","color":"gray"},{"text":"Kuba","color":"blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 29 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Brasília","color":"green","bold":true},{"text":" (","color":"gray"},{"text":"Brazylia","color":"green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 30 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Buenos Aires","color":"aqua","bold":true},{"text":" (","color":"gray"},{"text":"Argentyna","color":"aqua","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 31 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Santiago","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Chile","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 32 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Lima","color":"dark_red","bold":true},{"text":" (","color":"gray"},{"text":"Peru","color":"dark_red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 33 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Bogota","color":"yellow","bold":true},{"text":" (","color":"gray"},{"text":"Kolumbia","color":"yellow","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 34 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Caracas","color":"gold","bold":true},{"text":" (","color":"gray"},{"text":"Wenezuela","color":"gold","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 35 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Kair","color":"gold","bold":true},{"text":" (","color":"gray"},{"text":"Egipt","color":"gold","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 36 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Rabat","color":"dark_red","bold":true},{"text":" (","color":"gray"},{"text":"Maroko","color":"dark_red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 37 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Algier","color":"dark_green","bold":true},{"text":" (","color":"gray"},{"text":"Algieria","color":"dark_green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 38 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Abudża","color":"green","bold":true},{"text":" (","color":"gray"},{"text":"Nigeria","color":"green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 39 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Nairobi","color":"dark_red","bold":true},{"text":" (","color":"gray"},{"text":"Kenia","color":"dark_red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 40 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Addis Abeba","color":"yellow","bold":true},{"text":" (","color":"gray"},{"text":"Etiopia","color":"yellow","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 41 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Pretoria","color":"dark_green","bold":true},{"text":" (","color":"gray"},{"text":"RPA","color":"dark_green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 42 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Antananarywa","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Madagaskar","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 43 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Rijad","color":"dark_green","bold":true},{"text":" (","color":"gray"},{"text":"Arabia Saudyjska","color":"dark_green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 44 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Teheran","color":"green","bold":true},{"text":" (","color":"gray"},{"text":"Iran","color":"green","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 45 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Nowe Delhi","color":"gold","bold":true},{"text":" (","color":"gray"},{"text":"Indie","color":"gold","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 46 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Pekin","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Chiny","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 47 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Tokio","color":"white","bold":true},{"text":" (","color":"gray"},{"text":"Japonia","color":"white","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 48 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Seul","color":"blue","bold":true},{"text":" (","color":"gray"},{"text":"Korea Płd.","color":"blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 49 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Ułan Bator","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Mongolia","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 50 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Astana","color":"aqua","bold":true},{"text":" (","color":"gray"},{"text":"Kazachstan","color":"aqua","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 51 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Dżakarta","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Indonezja","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 52 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Bangkok","color":"blue","bold":true},{"text":" (","color":"gray"},{"text":"Tajlandia","color":"blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 53 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Hanoi","color":"red","bold":true},{"text":" (","color":"gray"},{"text":"Wietnam","color":"red","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 54 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Manila","color":"blue","bold":true},{"text":" (","color":"gray"},{"text":"Filipiny","color":"blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 55 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Canberra","color":"dark_blue","bold":true},{"text":" (","color":"gray"},{"text":"Australia","color":"dark_blue","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
execute if score #najbl dz.data matches 56 run tellraw @s [{"text":" Najbliższa stolica: ","color":"gray"},{"text":"Wellington","color":"dark_aqua","bold":true},{"text":" (","color":"gray"},{"text":"Nowa Zelandia","color":"dark_aqua","bold":false},{"text":") ~","color":"gray"},{"score":{"name":"#sq","objective":"dz.data"},"color":"white","bold":true},{"text":" kratek","color":"gray"}]
scoreboard players set @s gdzie 0
