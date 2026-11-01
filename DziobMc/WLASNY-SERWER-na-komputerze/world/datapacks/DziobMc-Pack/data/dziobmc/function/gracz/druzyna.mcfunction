# Wpisuje gracza do drużyny r<ranga>k<państwo>
execute unless score @s dz.rid matches 0.. run scoreboard players set @s dz.rid 8
scoreboard players add @s dz.kraj 0
execute store result storage dziobmc:tmp d.r int 1 run scoreboard players get @s dz.rid
execute store result storage dziobmc:tmp d.k int 1 run scoreboard players get @s dz.kraj
function dziobmc:gracz/druzyna_m with storage dziobmc:tmp d
