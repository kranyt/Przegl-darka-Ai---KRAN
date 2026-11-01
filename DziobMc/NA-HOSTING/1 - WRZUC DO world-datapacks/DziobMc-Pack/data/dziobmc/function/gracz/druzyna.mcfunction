# Wpisuje gracza do drużyny r<ranga>i<id państwa> (tworzy ją, jeśli trzeba)
execute unless score @s dz.rid matches 0.. run scoreboard players set @s dz.rid 8
scoreboard players add @s dz.kid 0
execute store result storage dziobmc:tmp d.r int 1 run scoreboard players get @s dz.rid
execute store result storage dziobmc:tmp d.id int 1 run scoreboard players get @s dz.kid
function dziobmc:gracz/druzyna_spr with storage dziobmc:tmp d
