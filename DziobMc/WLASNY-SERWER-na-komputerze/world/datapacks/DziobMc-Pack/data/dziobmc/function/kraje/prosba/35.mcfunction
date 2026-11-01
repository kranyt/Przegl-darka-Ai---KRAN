scoreboard players set @s dz.prosba 35
execute unless score @s dz.id matches 1.. run function dziobmc:gracz/nadaj_id
tellraw @s [{"text":"✉ Granice państwa ","color":"gray"},{"text":"Egipt","color":"gold","bold":true},{"text":" są zamknięte – wysłano prośbę do władcy.","color":"gray"}]
execute store result storage dziobmc:tmp p.id int 1 run scoreboard players get @s dz.id
data modify storage dziobmc:tmp p.k set value 35
function dziobmc:kraje/prosba_m with storage dziobmc:tmp p
