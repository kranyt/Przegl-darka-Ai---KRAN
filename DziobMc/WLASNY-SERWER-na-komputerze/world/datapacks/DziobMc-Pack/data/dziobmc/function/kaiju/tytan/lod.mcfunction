summon minecraft:falling_block ~ ~14 ~ {BlockState:{Name:"minecraft:packed_ice"},Time:1,HurtEntities:1b,FallHurtMax:16,FallHurtAmount:3.0f,DropItem:0b,CancelDrop:1b}
particle minecraft:snowflake ~ ~12 ~ 0.5 1 0.5 0.05 30 force
playsound minecraft:block.glass.break hostile @a[distance=..40] ~ ~ ~ 1 0.6
