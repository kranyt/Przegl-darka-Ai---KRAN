# Władca przyjmuje gracza o podanym ID
execute unless entity @s[tag=dz.wladca] run return run function dziobmc:komendy/przyjmij_reset
scoreboard players operation #v dz.data = @s przyjmij
scoreboard players operation #lk dz.data = @s dz.kraj
execute as @a[scores={dz.prosba=1..}] if score @s dz.id = #v dz.data if score @s dz.prosba = #lk dz.data at @s run function dziobmc:kraje/wejdz_prosba
scoreboard players set @s przyjmij 0
