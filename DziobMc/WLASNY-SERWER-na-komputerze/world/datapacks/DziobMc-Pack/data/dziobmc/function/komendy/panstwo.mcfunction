# /trigger panstwo: 1 menu, 2 ranking, 100+K kraj K, 20000K załóż państwo kraju K, ID>=1001 dołącz, 996 stolica tutaj, 997 granice, 998 tron, 999 opuść
scoreboard players operation #v dz.data = @s panstwo
scoreboard players set @s panstwo 0
execute if score #v dz.data matches 1 if score @s dz.kid matches 1.. run function dziobmc:kraje/info
execute if score #v dz.data matches 1 unless score @s dz.kid matches 1.. run function dziobmc:kraje/menu_wybor
execute if score #v dz.data matches 2 run function dziobmc:kraje/ranking
execute if score #v dz.data matches 996 if entity @s[tag=dz.wladca] run function dziobmc:kraje/przenies_stolice
execute if score #v dz.data matches 997 if entity @s[tag=dz.wladca] run function dziobmc:kraje/granice
execute if score #v dz.data matches 998 if score @s dz.kid matches 1.. run function dziobmc:kraje/przejmij
execute if score #v dz.data matches 999 if score @s dz.kid matches 1.. run function dziobmc:kraje/opusc
execute if score #v dz.data matches 1001..99999 run function dziobmc:kraje/dolacz
execute if score #v dz.data matches 101 run function dziobmc:kraje/kraj/1
execute if score #v dz.data matches 200001 run scoreboard players set #k dz.data 1
execute if score #v dz.data matches 102 run function dziobmc:kraje/kraj/2
execute if score #v dz.data matches 200002 run scoreboard players set #k dz.data 2
execute if score #v dz.data matches 103 run function dziobmc:kraje/kraj/3
execute if score #v dz.data matches 200003 run scoreboard players set #k dz.data 3
execute if score #v dz.data matches 104 run function dziobmc:kraje/kraj/4
execute if score #v dz.data matches 200004 run scoreboard players set #k dz.data 4
execute if score #v dz.data matches 105 run function dziobmc:kraje/kraj/5
execute if score #v dz.data matches 200005 run scoreboard players set #k dz.data 5
execute if score #v dz.data matches 106 run function dziobmc:kraje/kraj/6
execute if score #v dz.data matches 200006 run scoreboard players set #k dz.data 6
execute if score #v dz.data matches 107 run function dziobmc:kraje/kraj/7
execute if score #v dz.data matches 200007 run scoreboard players set #k dz.data 7
execute if score #v dz.data matches 108 run function dziobmc:kraje/kraj/8
execute if score #v dz.data matches 200008 run scoreboard players set #k dz.data 8
execute if score #v dz.data matches 109 run function dziobmc:kraje/kraj/9
execute if score #v dz.data matches 200009 run scoreboard players set #k dz.data 9
execute if score #v dz.data matches 110 run function dziobmc:kraje/kraj/10
execute if score #v dz.data matches 200010 run scoreboard players set #k dz.data 10
execute if score #v dz.data matches 111 run function dziobmc:kraje/kraj/11
execute if score #v dz.data matches 200011 run scoreboard players set #k dz.data 11
execute if score #v dz.data matches 112 run function dziobmc:kraje/kraj/12
execute if score #v dz.data matches 200012 run scoreboard players set #k dz.data 12
execute if score #v dz.data matches 113 run function dziobmc:kraje/kraj/13
execute if score #v dz.data matches 200013 run scoreboard players set #k dz.data 13
execute if score #v dz.data matches 114 run function dziobmc:kraje/kraj/14
execute if score #v dz.data matches 200014 run scoreboard players set #k dz.data 14
execute if score #v dz.data matches 115 run function dziobmc:kraje/kraj/15
execute if score #v dz.data matches 200015 run scoreboard players set #k dz.data 15
execute if score #v dz.data matches 116 run function dziobmc:kraje/kraj/16
execute if score #v dz.data matches 200016 run scoreboard players set #k dz.data 16
execute if score #v dz.data matches 117 run function dziobmc:kraje/kraj/17
execute if score #v dz.data matches 200017 run scoreboard players set #k dz.data 17
execute if score #v dz.data matches 118 run function dziobmc:kraje/kraj/18
execute if score #v dz.data matches 200018 run scoreboard players set #k dz.data 18
execute if score #v dz.data matches 119 run function dziobmc:kraje/kraj/19
execute if score #v dz.data matches 200019 run scoreboard players set #k dz.data 19
execute if score #v dz.data matches 120 run function dziobmc:kraje/kraj/20
execute if score #v dz.data matches 200020 run scoreboard players set #k dz.data 20
execute if score #v dz.data matches 121 run function dziobmc:kraje/kraj/21
execute if score #v dz.data matches 200021 run scoreboard players set #k dz.data 21
execute if score #v dz.data matches 122 run function dziobmc:kraje/kraj/22
execute if score #v dz.data matches 200022 run scoreboard players set #k dz.data 22
execute if score #v dz.data matches 123 run function dziobmc:kraje/kraj/23
execute if score #v dz.data matches 200023 run scoreboard players set #k dz.data 23
execute if score #v dz.data matches 124 run function dziobmc:kraje/kraj/24
execute if score #v dz.data matches 200024 run scoreboard players set #k dz.data 24
execute if score #v dz.data matches 125 run function dziobmc:kraje/kraj/25
execute if score #v dz.data matches 200025 run scoreboard players set #k dz.data 25
execute if score #v dz.data matches 126 run function dziobmc:kraje/kraj/26
execute if score #v dz.data matches 200026 run scoreboard players set #k dz.data 26
execute if score #v dz.data matches 127 run function dziobmc:kraje/kraj/27
execute if score #v dz.data matches 200027 run scoreboard players set #k dz.data 27
execute if score #v dz.data matches 128 run function dziobmc:kraje/kraj/28
execute if score #v dz.data matches 200028 run scoreboard players set #k dz.data 28
execute if score #v dz.data matches 129 run function dziobmc:kraje/kraj/29
execute if score #v dz.data matches 200029 run scoreboard players set #k dz.data 29
execute if score #v dz.data matches 130 run function dziobmc:kraje/kraj/30
execute if score #v dz.data matches 200030 run scoreboard players set #k dz.data 30
execute if score #v dz.data matches 131 run function dziobmc:kraje/kraj/31
execute if score #v dz.data matches 200031 run scoreboard players set #k dz.data 31
execute if score #v dz.data matches 132 run function dziobmc:kraje/kraj/32
execute if score #v dz.data matches 200032 run scoreboard players set #k dz.data 32
execute if score #v dz.data matches 133 run function dziobmc:kraje/kraj/33
execute if score #v dz.data matches 200033 run scoreboard players set #k dz.data 33
execute if score #v dz.data matches 134 run function dziobmc:kraje/kraj/34
execute if score #v dz.data matches 200034 run scoreboard players set #k dz.data 34
execute if score #v dz.data matches 135 run function dziobmc:kraje/kraj/35
execute if score #v dz.data matches 200035 run scoreboard players set #k dz.data 35
execute if score #v dz.data matches 136 run function dziobmc:kraje/kraj/36
execute if score #v dz.data matches 200036 run scoreboard players set #k dz.data 36
execute if score #v dz.data matches 137 run function dziobmc:kraje/kraj/37
execute if score #v dz.data matches 200037 run scoreboard players set #k dz.data 37
execute if score #v dz.data matches 138 run function dziobmc:kraje/kraj/38
execute if score #v dz.data matches 200038 run scoreboard players set #k dz.data 38
execute if score #v dz.data matches 139 run function dziobmc:kraje/kraj/39
execute if score #v dz.data matches 200039 run scoreboard players set #k dz.data 39
execute if score #v dz.data matches 140 run function dziobmc:kraje/kraj/40
execute if score #v dz.data matches 200040 run scoreboard players set #k dz.data 40
execute if score #v dz.data matches 141 run function dziobmc:kraje/kraj/41
execute if score #v dz.data matches 200041 run scoreboard players set #k dz.data 41
execute if score #v dz.data matches 142 run function dziobmc:kraje/kraj/42
execute if score #v dz.data matches 200042 run scoreboard players set #k dz.data 42
execute if score #v dz.data matches 143 run function dziobmc:kraje/kraj/43
execute if score #v dz.data matches 200043 run scoreboard players set #k dz.data 43
execute if score #v dz.data matches 144 run function dziobmc:kraje/kraj/44
execute if score #v dz.data matches 200044 run scoreboard players set #k dz.data 44
execute if score #v dz.data matches 145 run function dziobmc:kraje/kraj/45
execute if score #v dz.data matches 200045 run scoreboard players set #k dz.data 45
execute if score #v dz.data matches 146 run function dziobmc:kraje/kraj/46
execute if score #v dz.data matches 200046 run scoreboard players set #k dz.data 46
execute if score #v dz.data matches 147 run function dziobmc:kraje/kraj/47
execute if score #v dz.data matches 200047 run scoreboard players set #k dz.data 47
execute if score #v dz.data matches 148 run function dziobmc:kraje/kraj/48
execute if score #v dz.data matches 200048 run scoreboard players set #k dz.data 48
execute if score #v dz.data matches 149 run function dziobmc:kraje/kraj/49
execute if score #v dz.data matches 200049 run scoreboard players set #k dz.data 49
execute if score #v dz.data matches 150 run function dziobmc:kraje/kraj/50
execute if score #v dz.data matches 200050 run scoreboard players set #k dz.data 50
execute if score #v dz.data matches 151 run function dziobmc:kraje/kraj/51
execute if score #v dz.data matches 200051 run scoreboard players set #k dz.data 51
execute if score #v dz.data matches 152 run function dziobmc:kraje/kraj/52
execute if score #v dz.data matches 200052 run scoreboard players set #k dz.data 52
execute if score #v dz.data matches 153 run function dziobmc:kraje/kraj/53
execute if score #v dz.data matches 200053 run scoreboard players set #k dz.data 53
execute if score #v dz.data matches 154 run function dziobmc:kraje/kraj/54
execute if score #v dz.data matches 200054 run scoreboard players set #k dz.data 54
execute if score #v dz.data matches 155 run function dziobmc:kraje/kraj/55
execute if score #v dz.data matches 200055 run scoreboard players set #k dz.data 55
execute if score #v dz.data matches 156 run function dziobmc:kraje/kraj/56
execute if score #v dz.data matches 200056 run scoreboard players set #k dz.data 56
execute if score #v dz.data matches 200001..200999 run function dziobmc:kraje/zaloz
