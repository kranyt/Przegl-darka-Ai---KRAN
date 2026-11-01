scoreboard players set @s dz.prosba 1
execute unless score @s dz.id matches 1.. run function dziobmc:gracz/nadaj_id
tellraw @s [{"text":"✉ Granice państwa ","color":"gray"},{"text":"Polska","color":"red","bold":true},{"text":" są zamknięte – wysłano prośbę do władcy.","color":"gray"}]
execute store result storage dziobmc:tmp p.id int 1 run scoreboard players get @s dz.id
data modify storage dziobmc:tmp p.k set value 1
function dziobmc:kraje/prosba_m with storage dziobmc:tmp p
