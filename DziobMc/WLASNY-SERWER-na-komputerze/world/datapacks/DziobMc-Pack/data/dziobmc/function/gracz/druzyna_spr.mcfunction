# państwo mogło zostać rozwiązane
$execute if score @s dz.kid matches 1.. unless data storage dziobmc:kraje lista[{id:$(id)}] run function dziobmc:kraje/wyczysc_gracza
$data modify storage dziobmc:tmp d merge from storage dziobmc:kraje rp.r$(r)
execute if score @s dz.kid matches 1.. run function dziobmc:gracz/druzyna_tj with storage dziobmc:tmp d
execute unless score @s dz.kid matches 1.. run function dziobmc:gracz/druzyna_bez with storage dziobmc:tmp d
execute if score @s dz.kid matches 1.. run function dziobmc:gracz/druzyna_z with storage dziobmc:tmp d
