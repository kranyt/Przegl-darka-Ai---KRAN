$scoreboard players set @s dz.prosba $(id)
execute unless score @s dz.id matches 1.. run function dziobmc:gracz/nadaj_id
tellraw @s {"text":"✉ Granice tego państwa są zamknięte – wysłano prośbę do władcy.","color":"gray"}
execute store result storage dziobmc:tmp p.pid int 1 run scoreboard players get @s dz.id
$data modify storage dziobmc:tmp p.id set value $(id)
function dziobmc:kraje/prosba_m with storage dziobmc:tmp p
