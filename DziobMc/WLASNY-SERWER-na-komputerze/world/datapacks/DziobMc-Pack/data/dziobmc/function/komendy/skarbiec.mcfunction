scoreboard players operation #v dz.data = @s skarbiec
scoreboard players set @s skarbiec 0
execute unless score @s dz.kraj matches 1.. run return run tellraw @s {"text":"✖ Nie należysz do żadnego państwa.","color":"red"}
execute if score #v dz.data matches 2.. unless score @s dz.coins >= #v dz.data run return run tellraw @s {"text":"✖ Masz za mało monet.","color":"red"}
execute if score #v dz.data matches 2.. run return run function dziobmc:kraje/skarbiec_wplata
execute if score #v dz.data matches ..-1 unless entity @s[tag=dz.wladca] run return run tellraw @s {"text":"✖ Tylko władca może wypłacać ze skarbca.","color":"red"}
execute if score #v dz.data matches ..-1 run scoreboard players operation #v dz.data *= #m1 dz.data
execute if score #v dz.data matches 1.. run function dziobmc:kraje/skarbiec_wyplata
