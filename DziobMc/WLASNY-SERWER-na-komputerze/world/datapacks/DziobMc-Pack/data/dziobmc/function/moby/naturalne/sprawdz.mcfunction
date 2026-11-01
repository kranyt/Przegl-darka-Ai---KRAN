# Część naturalnych mobów zamienia się w custom moby (#szansa %)
tag @s add dz.ch
execute store result score #r dz.data run random value 1..100
execute if score #r dz.data > #szansa dz.data run return 0
execute store result score #r dz.data run random value 1..2
execute if entity @s[type=zombie] if score #r dz.data matches 1 run return run function dziobmc:moby/ustaw/wojownik
execute if entity @s[type=zombie] run return run function dziobmc:moby/ustaw/ognisty
execute if entity @s[type=husk] run return run function dziobmc:moby/ustaw/ognisty
execute if entity @s[type=skeleton] if score #r dz.data matches 1 run return run function dziobmc:moby/ustaw/lucznik
execute if entity @s[type=skeleton] run return run function dziobmc:moby/ustaw/lodowy
execute if entity @s[type=stray] run return run function dziobmc:moby/ustaw/lodowy
execute if entity @s[type=spider] run return run function dziobmc:moby/ustaw/pajak
execute if entity @s[type=creeper] run return run function dziobmc:moby/ustaw/kreeper
execute if entity @s[type=wither_skeleton] run return run function dziobmc:moby/ustaw/widmo
