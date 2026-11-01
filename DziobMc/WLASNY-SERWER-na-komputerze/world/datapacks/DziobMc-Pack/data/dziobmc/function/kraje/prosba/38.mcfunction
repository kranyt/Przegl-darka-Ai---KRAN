scoreboard players set @s dz.prosba 38
execute unless score @s dz.id matches 1.. run function dziobmc:gracz/nadaj_id
tellraw @s [{"text":"✉ Granice państwa ","color":"gray"},{"text":"Nigeria","color":"green","bold":true},{"text":" są zamknięte – wysłano prośbę do władcy.","color":"gray"}]
execute store result storage dziobmc:tmp p.id int 1 run scoreboard players get @s dz.id
data modify storage dziobmc:tmp p.k set value 38
function dziobmc:kraje/prosba_m with storage dziobmc:tmp p
