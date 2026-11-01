# Usuwa encję bez dropu (moby z lobby, boss po czasie itp.)
data merge entity @s {DeathLootTable:"minecraft:empty",HandItems:[{},{}],ArmorItems:[{},{},{},{}]}
tp @s ~ -200 ~
kill @s
