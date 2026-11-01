# a, b – państwa w wojnie. Zwycięża to z większą liczbą punktów.
$execute store result score #pa dz.data run scoreboard players get #k$(a) dz.k_pkt
$execute store result score #pb dz.data run scoreboard players get #k$(b) dz.k_pkt
$data modify storage dziobmc:tmp e1 set value {w:$(a),l:$(b)}
$data modify storage dziobmc:tmp e2 set value {w:$(b),l:$(a)}
function dziobmc:wojna/e_nazwy
execute if score #pa dz.data > #pb dz.data run function dziobmc:wojna/wygrana with storage dziobmc:tmp e1
execute if score #pb dz.data > #pa dz.data run function dziobmc:wojna/wygrana with storage dziobmc:tmp e2
execute if score #pa dz.data = #pb dz.data run function dziobmc:wojna/remis with storage dziobmc:tmp e1
$function dziobmc:wojna/reset {a:$(a),b:$(b)}
