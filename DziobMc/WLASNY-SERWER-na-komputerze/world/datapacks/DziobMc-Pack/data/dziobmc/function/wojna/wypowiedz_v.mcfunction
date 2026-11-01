execute if score #v dz.data = @s dz.kid run return run tellraw @s {"text":"✖ Nie możesz wypowiedzieć wojny samemu sobie.","color":"red"}
execute store result storage dziobmc:tmp w.a int 1 run scoreboard players get @s dz.kid
execute store result storage dziobmc:tmp w.b int 1 run scoreboard players get #v dz.data
function dziobmc:wojna/nazwy with storage dziobmc:tmp w
function dziobmc:wojna/wypowiedz with storage dziobmc:tmp w
