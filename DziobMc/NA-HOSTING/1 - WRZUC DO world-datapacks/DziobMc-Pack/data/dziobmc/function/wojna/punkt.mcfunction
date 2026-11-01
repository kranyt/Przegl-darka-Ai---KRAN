$execute unless score #k$(a) dz.k_wrog matches $(b) run return 0
$scoreboard players add #k$(a) dz.k_pkt 1
$tellraw @a[scores={dz.kraj=$(a)}] [{"text":"⚔ +1 punkt wojenny! Wynik: ","color":"gold"},{"score":{"name":"#k$(a)","objective":"dz.k_pkt"},"color":"green","bold":true},{"text":" : ","color":"gray"},{"score":{"name":"#k$(b)","objective":"dz.k_pkt"},"color":"red","bold":true}]
$tellraw @a[scores={dz.kraj=$(b)}] [{"text":"⚔ Wróg zdobywa punkt! Wynik: ","color":"red"},{"score":{"name":"#k$(b)","objective":"dz.k_pkt"},"color":"green","bold":true},{"text":" : ","color":"gray"},{"score":{"name":"#k$(a)","objective":"dz.k_pkt"},"color":"red","bold":true}]
$execute if score #k$(a) dz.k_pkt matches 15.. run function dziobmc:wojna/koniec {a:$(a),b:$(b)}
