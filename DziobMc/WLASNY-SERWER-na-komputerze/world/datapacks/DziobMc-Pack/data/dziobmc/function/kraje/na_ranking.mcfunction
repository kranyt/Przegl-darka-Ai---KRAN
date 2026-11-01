$scoreboard players operation #p dz.data = #k$(id) dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
$scoreboard players operation #q dz.data = #k$(id) dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
$scoreboard players operation #q dz.data = #k$(id) dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
$scoreboard players operation k$(kod)$(nn) dz.ranking = #p dz.data
$scoreboard players display name k$(kod)$(nn) dz.ranking $(nj)
scoreboard players add #ile_kr dz.data 1
