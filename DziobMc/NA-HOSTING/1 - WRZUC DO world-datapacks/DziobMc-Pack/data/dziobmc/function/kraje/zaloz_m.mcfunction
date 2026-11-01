$data modify storage dziobmc:tmp wn.nj set value '{"text":"$(nazwa)$(nn)","color":"$(kol)","bold":true}'
$data modify storage dziobmc:tmp wn.tj set value '{"text":"$(kod)$(nn)","color":"$(kol)","bold":true}'
# stolica: pierwsze państwo = prawdziwa stolica, kolejne = miejsce założenia (na mapie Ziemi)
$data modify storage dziobmc:tmp wn.x set from storage dziobmc:kraje s.k$(k).x
$data modify storage dziobmc:tmp wn.z set from storage dziobmc:kraje s.k$(k).z
execute unless score #n dz.data matches 1 at @s if dimension minecraft:ziemia run function dziobmc:kraje/stolica_tutaj_wn
execute unless score #n dz.data matches 1 at @s unless dimension minecraft:ziemia run function dziobmc:kraje/stolica_przesun_wn
function dziobmc:kraje/x0z0_wn
data modify storage dziobmc:kraje lista append from storage dziobmc:tmp wn
function dziobmc:kraje/zaloz_m2 with storage dziobmc:tmp wn
