scoreboard players set #ile_kr dz.data 0
scoreboard players set #iter_tryb dz.data 2
function dziobmc:kraje/iter
scoreboard players add #sb dz.data 1
execute if score #sb dz.data matches 2.. run scoreboard players set #sb dz.data 0
execute if score #sb dz.data matches 1 if score #ile_kr dz.data matches 1.. run scoreboard objectives setdisplay sidebar dz.ranking
execute unless score #sb dz.data matches 1 run scoreboard objectives setdisplay sidebar dz.sidebar
execute unless score #ile_kr dz.data matches 1.. run scoreboard objectives setdisplay sidebar dz.sidebar
