# Earth SMP – inicjalizacja
scoreboard objectives add dz.kraj dummy
scoreboard objectives add dz.id dummy
scoreboard objectives add dz.prosba dummy
scoreboard objectives add dz.rid dummy
scoreboard objectives add dz.mojwrog dummy
scoreboard objectives add dz.k_czl dummy
scoreboard objectives add dz.k_skarb dummy
scoreboard objectives add dz.k_wl dummy
scoreboard objectives add dz.k_zamk dummy
scoreboard objectives add dz.k_wrog dummy
scoreboard objectives add dz.k_pkt dummy
scoreboard objectives add dz.k_wczas dummy
scoreboard objectives add dz.k_wygr dummy
scoreboard objectives add dz.k_pokoj dummy
scoreboard objectives add dz.cd_stol dummy
scoreboard objectives add dz.kc dummy
scoreboard objectives add panstwo trigger
scoreboard objectives add stolica trigger
scoreboard objectives add skarbiec trigger
scoreboard objectives add wojna trigger
scoreboard objectives add przyjmij trigger
scoreboard objectives add ziemia trigger
scoreboard objectives add gdzie trigger
scoreboard objectives add dz.ranking dummy [{"text":"✪ ","color":"aqua"},{"text":"Potęga państw","color":"gold","bold":true}]
execute unless score #skala dz.data matches 1.. run scoreboard players set #skala dz.data 2000
scoreboard players set #11132 dz.data 11132
scoreboard players set #m11132 dz.data -11132
scoreboard players set #1113 dz.data 1113
scoreboard players set #111320 dz.data 111320
scoreboard players set #40075200 dz.data 40075200
scoreboard players set #30 dz.data 30
scoreboard players set #500 dz.data 500
scoreboard players set #1000 dz.data 1000
scoreboard players set #m1 dz.data -1
scoreboard players add #k1 dz.k_czl 0
scoreboard players add #k1 dz.k_skarb 0
scoreboard players add #k1 dz.k_wl 0
scoreboard players add #k1 dz.k_zamk 0
scoreboard players add #k1 dz.k_wrog 0
scoreboard players add #k1 dz.k_pkt 0
scoreboard players add #k1 dz.k_wczas 0
scoreboard players add #k1 dz.k_wygr 0
scoreboard players add #k1 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k1 set value '{"text":"Polska","color":"red","bold":true}'
scoreboard players display name kPOL dz.ranking [{"text":"POL ","color":"dark_gray"},{"text":"Polska","color":"red","bold":false}]
scoreboard players add #k2 dz.k_czl 0
scoreboard players add #k2 dz.k_skarb 0
scoreboard players add #k2 dz.k_wl 0
scoreboard players add #k2 dz.k_zamk 0
scoreboard players add #k2 dz.k_wrog 0
scoreboard players add #k2 dz.k_pkt 0
scoreboard players add #k2 dz.k_wczas 0
scoreboard players add #k2 dz.k_wygr 0
scoreboard players add #k2 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k2 set value '{"text":"Niemcy","color":"dark_gray","bold":true}'
scoreboard players display name kGER dz.ranking [{"text":"GER ","color":"dark_gray"},{"text":"Niemcy","color":"dark_gray","bold":false}]
scoreboard players add #k3 dz.k_czl 0
scoreboard players add #k3 dz.k_skarb 0
scoreboard players add #k3 dz.k_wl 0
scoreboard players add #k3 dz.k_zamk 0
scoreboard players add #k3 dz.k_wrog 0
scoreboard players add #k3 dz.k_pkt 0
scoreboard players add #k3 dz.k_wczas 0
scoreboard players add #k3 dz.k_wygr 0
scoreboard players add #k3 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k3 set value '{"text":"Francja","color":"blue","bold":true}'
scoreboard players display name kFRA dz.ranking [{"text":"FRA ","color":"dark_gray"},{"text":"Francja","color":"blue","bold":false}]
scoreboard players add #k4 dz.k_czl 0
scoreboard players add #k4 dz.k_skarb 0
scoreboard players add #k4 dz.k_wl 0
scoreboard players add #k4 dz.k_zamk 0
scoreboard players add #k4 dz.k_wrog 0
scoreboard players add #k4 dz.k_pkt 0
scoreboard players add #k4 dz.k_wczas 0
scoreboard players add #k4 dz.k_wygr 0
scoreboard players add #k4 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k4 set value '{"text":"Wielka Brytania","color":"dark_blue","bold":true}'
scoreboard players display name kGBR dz.ranking [{"text":"GBR ","color":"dark_gray"},{"text":"Wielka Brytania","color":"dark_blue","bold":false}]
scoreboard players add #k5 dz.k_czl 0
scoreboard players add #k5 dz.k_skarb 0
scoreboard players add #k5 dz.k_wl 0
scoreboard players add #k5 dz.k_zamk 0
scoreboard players add #k5 dz.k_wrog 0
scoreboard players add #k5 dz.k_pkt 0
scoreboard players add #k5 dz.k_wczas 0
scoreboard players add #k5 dz.k_wygr 0
scoreboard players add #k5 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k5 set value '{"text":"Hiszpania","color":"gold","bold":true}'
scoreboard players display name kESP dz.ranking [{"text":"ESP ","color":"dark_gray"},{"text":"Hiszpania","color":"gold","bold":false}]
scoreboard players add #k6 dz.k_czl 0
scoreboard players add #k6 dz.k_skarb 0
scoreboard players add #k6 dz.k_wl 0
scoreboard players add #k6 dz.k_zamk 0
scoreboard players add #k6 dz.k_wrog 0
scoreboard players add #k6 dz.k_pkt 0
scoreboard players add #k6 dz.k_wczas 0
scoreboard players add #k6 dz.k_wygr 0
scoreboard players add #k6 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k6 set value '{"text":"Włochy","color":"green","bold":true}'
scoreboard players display name kITA dz.ranking [{"text":"ITA ","color":"dark_gray"},{"text":"Włochy","color":"green","bold":false}]
scoreboard players add #k7 dz.k_czl 0
scoreboard players add #k7 dz.k_skarb 0
scoreboard players add #k7 dz.k_wl 0
scoreboard players add #k7 dz.k_zamk 0
scoreboard players add #k7 dz.k_wrog 0
scoreboard players add #k7 dz.k_pkt 0
scoreboard players add #k7 dz.k_wczas 0
scoreboard players add #k7 dz.k_wygr 0
scoreboard players add #k7 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k7 set value '{"text":"Ukraina","color":"yellow","bold":true}'
scoreboard players display name kUKR dz.ranking [{"text":"UKR ","color":"dark_gray"},{"text":"Ukraina","color":"yellow","bold":false}]
scoreboard players add #k8 dz.k_czl 0
scoreboard players add #k8 dz.k_skarb 0
scoreboard players add #k8 dz.k_wl 0
scoreboard players add #k8 dz.k_zamk 0
scoreboard players add #k8 dz.k_wrog 0
scoreboard players add #k8 dz.k_pkt 0
scoreboard players add #k8 dz.k_wczas 0
scoreboard players add #k8 dz.k_wygr 0
scoreboard players add #k8 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k8 set value '{"text":"Rosja","color":"white","bold":true}'
scoreboard players display name kRUS dz.ranking [{"text":"RUS ","color":"dark_gray"},{"text":"Rosja","color":"white","bold":false}]
scoreboard players add #k9 dz.k_czl 0
scoreboard players add #k9 dz.k_skarb 0
scoreboard players add #k9 dz.k_wl 0
scoreboard players add #k9 dz.k_zamk 0
scoreboard players add #k9 dz.k_wrog 0
scoreboard players add #k9 dz.k_pkt 0
scoreboard players add #k9 dz.k_wczas 0
scoreboard players add #k9 dz.k_wygr 0
scoreboard players add #k9 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k9 set value '{"text":"Szwecja","color":"aqua","bold":true}'
scoreboard players display name kSWE dz.ranking [{"text":"SWE ","color":"dark_gray"},{"text":"Szwecja","color":"aqua","bold":false}]
scoreboard players add #k10 dz.k_czl 0
scoreboard players add #k10 dz.k_skarb 0
scoreboard players add #k10 dz.k_wl 0
scoreboard players add #k10 dz.k_zamk 0
scoreboard players add #k10 dz.k_wrog 0
scoreboard players add #k10 dz.k_pkt 0
scoreboard players add #k10 dz.k_wczas 0
scoreboard players add #k10 dz.k_wygr 0
scoreboard players add #k10 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k10 set value '{"text":"Norwegia","color":"dark_red","bold":true}'
scoreboard players display name kNOR dz.ranking [{"text":"NOR ","color":"dark_gray"},{"text":"Norwegia","color":"dark_red","bold":false}]
scoreboard players add #k11 dz.k_czl 0
scoreboard players add #k11 dz.k_skarb 0
scoreboard players add #k11 dz.k_wl 0
scoreboard players add #k11 dz.k_zamk 0
scoreboard players add #k11 dz.k_wrog 0
scoreboard players add #k11 dz.k_pkt 0
scoreboard players add #k11 dz.k_wczas 0
scoreboard players add #k11 dz.k_wygr 0
scoreboard players add #k11 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k11 set value '{"text":"Finlandia","color":"white","bold":true}'
scoreboard players display name kFIN dz.ranking [{"text":"FIN ","color":"dark_gray"},{"text":"Finlandia","color":"white","bold":false}]
scoreboard players add #k12 dz.k_czl 0
scoreboard players add #k12 dz.k_skarb 0
scoreboard players add #k12 dz.k_wl 0
scoreboard players add #k12 dz.k_zamk 0
scoreboard players add #k12 dz.k_wrog 0
scoreboard players add #k12 dz.k_pkt 0
scoreboard players add #k12 dz.k_wczas 0
scoreboard players add #k12 dz.k_wygr 0
scoreboard players add #k12 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k12 set value '{"text":"Czechy","color":"blue","bold":true}'
scoreboard players display name kCZE dz.ranking [{"text":"CZE ","color":"dark_gray"},{"text":"Czechy","color":"blue","bold":false}]
scoreboard players add #k13 dz.k_czl 0
scoreboard players add #k13 dz.k_skarb 0
scoreboard players add #k13 dz.k_wl 0
scoreboard players add #k13 dz.k_zamk 0
scoreboard players add #k13 dz.k_wrog 0
scoreboard players add #k13 dz.k_pkt 0
scoreboard players add #k13 dz.k_wczas 0
scoreboard players add #k13 dz.k_wygr 0
scoreboard players add #k13 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k13 set value '{"text":"Słowacja","color":"blue","bold":true}'
scoreboard players display name kSVK dz.ranking [{"text":"SVK ","color":"dark_gray"},{"text":"Słowacja","color":"blue","bold":false}]
scoreboard players add #k14 dz.k_czl 0
scoreboard players add #k14 dz.k_skarb 0
scoreboard players add #k14 dz.k_wl 0
scoreboard players add #k14 dz.k_zamk 0
scoreboard players add #k14 dz.k_wrog 0
scoreboard players add #k14 dz.k_pkt 0
scoreboard players add #k14 dz.k_wczas 0
scoreboard players add #k14 dz.k_wygr 0
scoreboard players add #k14 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k14 set value '{"text":"Litwa","color":"yellow","bold":true}'
scoreboard players display name kLTU dz.ranking [{"text":"LTU ","color":"dark_gray"},{"text":"Litwa","color":"yellow","bold":false}]
scoreboard players add #k15 dz.k_czl 0
scoreboard players add #k15 dz.k_skarb 0
scoreboard players add #k15 dz.k_wl 0
scoreboard players add #k15 dz.k_zamk 0
scoreboard players add #k15 dz.k_wrog 0
scoreboard players add #k15 dz.k_pkt 0
scoreboard players add #k15 dz.k_wczas 0
scoreboard players add #k15 dz.k_wygr 0
scoreboard players add #k15 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k15 set value '{"text":"Austria","color":"red","bold":true}'
scoreboard players display name kAUT dz.ranking [{"text":"AUT ","color":"dark_gray"},{"text":"Austria","color":"red","bold":false}]
scoreboard players add #k16 dz.k_czl 0
scoreboard players add #k16 dz.k_skarb 0
scoreboard players add #k16 dz.k_wl 0
scoreboard players add #k16 dz.k_zamk 0
scoreboard players add #k16 dz.k_wrog 0
scoreboard players add #k16 dz.k_pkt 0
scoreboard players add #k16 dz.k_wczas 0
scoreboard players add #k16 dz.k_wygr 0
scoreboard players add #k16 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k16 set value '{"text":"Szwajcaria","color":"red","bold":true}'
scoreboard players display name kCHE dz.ranking [{"text":"CHE ","color":"dark_gray"},{"text":"Szwajcaria","color":"red","bold":false}]
scoreboard players add #k17 dz.k_czl 0
scoreboard players add #k17 dz.k_skarb 0
scoreboard players add #k17 dz.k_wl 0
scoreboard players add #k17 dz.k_zamk 0
scoreboard players add #k17 dz.k_wrog 0
scoreboard players add #k17 dz.k_pkt 0
scoreboard players add #k17 dz.k_wczas 0
scoreboard players add #k17 dz.k_wygr 0
scoreboard players add #k17 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k17 set value '{"text":"Holandia","color":"gold","bold":true}'
scoreboard players display name kNLD dz.ranking [{"text":"NLD ","color":"dark_gray"},{"text":"Holandia","color":"gold","bold":false}]
scoreboard players add #k18 dz.k_czl 0
scoreboard players add #k18 dz.k_skarb 0
scoreboard players add #k18 dz.k_wl 0
scoreboard players add #k18 dz.k_zamk 0
scoreboard players add #k18 dz.k_wrog 0
scoreboard players add #k18 dz.k_pkt 0
scoreboard players add #k18 dz.k_wczas 0
scoreboard players add #k18 dz.k_wygr 0
scoreboard players add #k18 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k18 set value '{"text":"Węgry","color":"dark_green","bold":true}'
scoreboard players display name kHUN dz.ranking [{"text":"HUN ","color":"dark_gray"},{"text":"Węgry","color":"dark_green","bold":false}]
scoreboard players add #k19 dz.k_czl 0
scoreboard players add #k19 dz.k_skarb 0
scoreboard players add #k19 dz.k_wl 0
scoreboard players add #k19 dz.k_zamk 0
scoreboard players add #k19 dz.k_wrog 0
scoreboard players add #k19 dz.k_pkt 0
scoreboard players add #k19 dz.k_wczas 0
scoreboard players add #k19 dz.k_wygr 0
scoreboard players add #k19 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k19 set value '{"text":"Rumunia","color":"yellow","bold":true}'
scoreboard players display name kROU dz.ranking [{"text":"ROU ","color":"dark_gray"},{"text":"Rumunia","color":"yellow","bold":false}]
scoreboard players add #k20 dz.k_czl 0
scoreboard players add #k20 dz.k_skarb 0
scoreboard players add #k20 dz.k_wl 0
scoreboard players add #k20 dz.k_zamk 0
scoreboard players add #k20 dz.k_wrog 0
scoreboard players add #k20 dz.k_pkt 0
scoreboard players add #k20 dz.k_wczas 0
scoreboard players add #k20 dz.k_wygr 0
scoreboard players add #k20 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k20 set value '{"text":"Grecja","color":"aqua","bold":true}'
scoreboard players display name kGRC dz.ranking [{"text":"GRC ","color":"dark_gray"},{"text":"Grecja","color":"aqua","bold":false}]
scoreboard players add #k21 dz.k_czl 0
scoreboard players add #k21 dz.k_skarb 0
scoreboard players add #k21 dz.k_wl 0
scoreboard players add #k21 dz.k_zamk 0
scoreboard players add #k21 dz.k_wrog 0
scoreboard players add #k21 dz.k_pkt 0
scoreboard players add #k21 dz.k_wczas 0
scoreboard players add #k21 dz.k_wygr 0
scoreboard players add #k21 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k21 set value '{"text":"Portugalia","color":"dark_green","bold":true}'
scoreboard players display name kPRT dz.ranking [{"text":"PRT ","color":"dark_gray"},{"text":"Portugalia","color":"dark_green","bold":false}]
scoreboard players add #k22 dz.k_czl 0
scoreboard players add #k22 dz.k_skarb 0
scoreboard players add #k22 dz.k_wl 0
scoreboard players add #k22 dz.k_zamk 0
scoreboard players add #k22 dz.k_wrog 0
scoreboard players add #k22 dz.k_pkt 0
scoreboard players add #k22 dz.k_wczas 0
scoreboard players add #k22 dz.k_wygr 0
scoreboard players add #k22 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k22 set value '{"text":"Turcja","color":"red","bold":true}'
scoreboard players display name kTUR dz.ranking [{"text":"TUR ","color":"dark_gray"},{"text":"Turcja","color":"red","bold":false}]
scoreboard players add #k23 dz.k_czl 0
scoreboard players add #k23 dz.k_skarb 0
scoreboard players add #k23 dz.k_wl 0
scoreboard players add #k23 dz.k_zamk 0
scoreboard players add #k23 dz.k_wrog 0
scoreboard players add #k23 dz.k_pkt 0
scoreboard players add #k23 dz.k_wczas 0
scoreboard players add #k23 dz.k_wygr 0
scoreboard players add #k23 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k23 set value '{"text":"Islandia","color":"blue","bold":true}'
scoreboard players display name kISL dz.ranking [{"text":"ISL ","color":"dark_gray"},{"text":"Islandia","color":"blue","bold":false}]
scoreboard players add #k24 dz.k_czl 0
scoreboard players add #k24 dz.k_skarb 0
scoreboard players add #k24 dz.k_wl 0
scoreboard players add #k24 dz.k_zamk 0
scoreboard players add #k24 dz.k_wrog 0
scoreboard players add #k24 dz.k_pkt 0
scoreboard players add #k24 dz.k_wczas 0
scoreboard players add #k24 dz.k_wygr 0
scoreboard players add #k24 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k24 set value '{"text":"Dania","color":"red","bold":true}'
scoreboard players display name kDNK dz.ranking [{"text":"DNK ","color":"dark_gray"},{"text":"Dania","color":"red","bold":false}]
scoreboard players add #k25 dz.k_czl 0
scoreboard players add #k25 dz.k_skarb 0
scoreboard players add #k25 dz.k_wl 0
scoreboard players add #k25 dz.k_zamk 0
scoreboard players add #k25 dz.k_wrog 0
scoreboard players add #k25 dz.k_pkt 0
scoreboard players add #k25 dz.k_wczas 0
scoreboard players add #k25 dz.k_wygr 0
scoreboard players add #k25 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k25 set value '{"text":"USA","color":"blue","bold":true}'
scoreboard players display name kUSA dz.ranking [{"text":"USA ","color":"dark_gray"},{"text":"USA","color":"blue","bold":false}]
scoreboard players add #k26 dz.k_czl 0
scoreboard players add #k26 dz.k_skarb 0
scoreboard players add #k26 dz.k_wl 0
scoreboard players add #k26 dz.k_zamk 0
scoreboard players add #k26 dz.k_wrog 0
scoreboard players add #k26 dz.k_pkt 0
scoreboard players add #k26 dz.k_wczas 0
scoreboard players add #k26 dz.k_wygr 0
scoreboard players add #k26 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k26 set value '{"text":"Kanada","color":"red","bold":true}'
scoreboard players display name kCAN dz.ranking [{"text":"CAN ","color":"dark_gray"},{"text":"Kanada","color":"red","bold":false}]
scoreboard players add #k27 dz.k_czl 0
scoreboard players add #k27 dz.k_skarb 0
scoreboard players add #k27 dz.k_wl 0
scoreboard players add #k27 dz.k_zamk 0
scoreboard players add #k27 dz.k_wrog 0
scoreboard players add #k27 dz.k_pkt 0
scoreboard players add #k27 dz.k_wczas 0
scoreboard players add #k27 dz.k_wygr 0
scoreboard players add #k27 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k27 set value '{"text":"Meksyk","color":"dark_green","bold":true}'
scoreboard players display name kMEX dz.ranking [{"text":"MEX ","color":"dark_gray"},{"text":"Meksyk","color":"dark_green","bold":false}]
scoreboard players add #k28 dz.k_czl 0
scoreboard players add #k28 dz.k_skarb 0
scoreboard players add #k28 dz.k_wl 0
scoreboard players add #k28 dz.k_zamk 0
scoreboard players add #k28 dz.k_wrog 0
scoreboard players add #k28 dz.k_pkt 0
scoreboard players add #k28 dz.k_wczas 0
scoreboard players add #k28 dz.k_wygr 0
scoreboard players add #k28 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k28 set value '{"text":"Kuba","color":"blue","bold":true}'
scoreboard players display name kCUB dz.ranking [{"text":"CUB ","color":"dark_gray"},{"text":"Kuba","color":"blue","bold":false}]
scoreboard players add #k29 dz.k_czl 0
scoreboard players add #k29 dz.k_skarb 0
scoreboard players add #k29 dz.k_wl 0
scoreboard players add #k29 dz.k_zamk 0
scoreboard players add #k29 dz.k_wrog 0
scoreboard players add #k29 dz.k_pkt 0
scoreboard players add #k29 dz.k_wczas 0
scoreboard players add #k29 dz.k_wygr 0
scoreboard players add #k29 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k29 set value '{"text":"Brazylia","color":"green","bold":true}'
scoreboard players display name kBRA dz.ranking [{"text":"BRA ","color":"dark_gray"},{"text":"Brazylia","color":"green","bold":false}]
scoreboard players add #k30 dz.k_czl 0
scoreboard players add #k30 dz.k_skarb 0
scoreboard players add #k30 dz.k_wl 0
scoreboard players add #k30 dz.k_zamk 0
scoreboard players add #k30 dz.k_wrog 0
scoreboard players add #k30 dz.k_pkt 0
scoreboard players add #k30 dz.k_wczas 0
scoreboard players add #k30 dz.k_wygr 0
scoreboard players add #k30 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k30 set value '{"text":"Argentyna","color":"aqua","bold":true}'
scoreboard players display name kARG dz.ranking [{"text":"ARG ","color":"dark_gray"},{"text":"Argentyna","color":"aqua","bold":false}]
scoreboard players add #k31 dz.k_czl 0
scoreboard players add #k31 dz.k_skarb 0
scoreboard players add #k31 dz.k_wl 0
scoreboard players add #k31 dz.k_zamk 0
scoreboard players add #k31 dz.k_wrog 0
scoreboard players add #k31 dz.k_pkt 0
scoreboard players add #k31 dz.k_wczas 0
scoreboard players add #k31 dz.k_wygr 0
scoreboard players add #k31 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k31 set value '{"text":"Chile","color":"red","bold":true}'
scoreboard players display name kCHL dz.ranking [{"text":"CHL ","color":"dark_gray"},{"text":"Chile","color":"red","bold":false}]
scoreboard players add #k32 dz.k_czl 0
scoreboard players add #k32 dz.k_skarb 0
scoreboard players add #k32 dz.k_wl 0
scoreboard players add #k32 dz.k_zamk 0
scoreboard players add #k32 dz.k_wrog 0
scoreboard players add #k32 dz.k_pkt 0
scoreboard players add #k32 dz.k_wczas 0
scoreboard players add #k32 dz.k_wygr 0
scoreboard players add #k32 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k32 set value '{"text":"Peru","color":"dark_red","bold":true}'
scoreboard players display name kPER dz.ranking [{"text":"PER ","color":"dark_gray"},{"text":"Peru","color":"dark_red","bold":false}]
scoreboard players add #k33 dz.k_czl 0
scoreboard players add #k33 dz.k_skarb 0
scoreboard players add #k33 dz.k_wl 0
scoreboard players add #k33 dz.k_zamk 0
scoreboard players add #k33 dz.k_wrog 0
scoreboard players add #k33 dz.k_pkt 0
scoreboard players add #k33 dz.k_wczas 0
scoreboard players add #k33 dz.k_wygr 0
scoreboard players add #k33 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k33 set value '{"text":"Kolumbia","color":"yellow","bold":true}'
scoreboard players display name kCOL dz.ranking [{"text":"COL ","color":"dark_gray"},{"text":"Kolumbia","color":"yellow","bold":false}]
scoreboard players add #k34 dz.k_czl 0
scoreboard players add #k34 dz.k_skarb 0
scoreboard players add #k34 dz.k_wl 0
scoreboard players add #k34 dz.k_zamk 0
scoreboard players add #k34 dz.k_wrog 0
scoreboard players add #k34 dz.k_pkt 0
scoreboard players add #k34 dz.k_wczas 0
scoreboard players add #k34 dz.k_wygr 0
scoreboard players add #k34 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k34 set value '{"text":"Wenezuela","color":"gold","bold":true}'
scoreboard players display name kVEN dz.ranking [{"text":"VEN ","color":"dark_gray"},{"text":"Wenezuela","color":"gold","bold":false}]
scoreboard players add #k35 dz.k_czl 0
scoreboard players add #k35 dz.k_skarb 0
scoreboard players add #k35 dz.k_wl 0
scoreboard players add #k35 dz.k_zamk 0
scoreboard players add #k35 dz.k_wrog 0
scoreboard players add #k35 dz.k_pkt 0
scoreboard players add #k35 dz.k_wczas 0
scoreboard players add #k35 dz.k_wygr 0
scoreboard players add #k35 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k35 set value '{"text":"Egipt","color":"gold","bold":true}'
scoreboard players display name kEGY dz.ranking [{"text":"EGY ","color":"dark_gray"},{"text":"Egipt","color":"gold","bold":false}]
scoreboard players add #k36 dz.k_czl 0
scoreboard players add #k36 dz.k_skarb 0
scoreboard players add #k36 dz.k_wl 0
scoreboard players add #k36 dz.k_zamk 0
scoreboard players add #k36 dz.k_wrog 0
scoreboard players add #k36 dz.k_pkt 0
scoreboard players add #k36 dz.k_wczas 0
scoreboard players add #k36 dz.k_wygr 0
scoreboard players add #k36 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k36 set value '{"text":"Maroko","color":"dark_red","bold":true}'
scoreboard players display name kMAR dz.ranking [{"text":"MAR ","color":"dark_gray"},{"text":"Maroko","color":"dark_red","bold":false}]
scoreboard players add #k37 dz.k_czl 0
scoreboard players add #k37 dz.k_skarb 0
scoreboard players add #k37 dz.k_wl 0
scoreboard players add #k37 dz.k_zamk 0
scoreboard players add #k37 dz.k_wrog 0
scoreboard players add #k37 dz.k_pkt 0
scoreboard players add #k37 dz.k_wczas 0
scoreboard players add #k37 dz.k_wygr 0
scoreboard players add #k37 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k37 set value '{"text":"Algieria","color":"dark_green","bold":true}'
scoreboard players display name kDZA dz.ranking [{"text":"DZA ","color":"dark_gray"},{"text":"Algieria","color":"dark_green","bold":false}]
scoreboard players add #k38 dz.k_czl 0
scoreboard players add #k38 dz.k_skarb 0
scoreboard players add #k38 dz.k_wl 0
scoreboard players add #k38 dz.k_zamk 0
scoreboard players add #k38 dz.k_wrog 0
scoreboard players add #k38 dz.k_pkt 0
scoreboard players add #k38 dz.k_wczas 0
scoreboard players add #k38 dz.k_wygr 0
scoreboard players add #k38 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k38 set value '{"text":"Nigeria","color":"green","bold":true}'
scoreboard players display name kNGA dz.ranking [{"text":"NGA ","color":"dark_gray"},{"text":"Nigeria","color":"green","bold":false}]
scoreboard players add #k39 dz.k_czl 0
scoreboard players add #k39 dz.k_skarb 0
scoreboard players add #k39 dz.k_wl 0
scoreboard players add #k39 dz.k_zamk 0
scoreboard players add #k39 dz.k_wrog 0
scoreboard players add #k39 dz.k_pkt 0
scoreboard players add #k39 dz.k_wczas 0
scoreboard players add #k39 dz.k_wygr 0
scoreboard players add #k39 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k39 set value '{"text":"Kenia","color":"dark_red","bold":true}'
scoreboard players display name kKEN dz.ranking [{"text":"KEN ","color":"dark_gray"},{"text":"Kenia","color":"dark_red","bold":false}]
scoreboard players add #k40 dz.k_czl 0
scoreboard players add #k40 dz.k_skarb 0
scoreboard players add #k40 dz.k_wl 0
scoreboard players add #k40 dz.k_zamk 0
scoreboard players add #k40 dz.k_wrog 0
scoreboard players add #k40 dz.k_pkt 0
scoreboard players add #k40 dz.k_wczas 0
scoreboard players add #k40 dz.k_wygr 0
scoreboard players add #k40 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k40 set value '{"text":"Etiopia","color":"yellow","bold":true}'
scoreboard players display name kETH dz.ranking [{"text":"ETH ","color":"dark_gray"},{"text":"Etiopia","color":"yellow","bold":false}]
scoreboard players add #k41 dz.k_czl 0
scoreboard players add #k41 dz.k_skarb 0
scoreboard players add #k41 dz.k_wl 0
scoreboard players add #k41 dz.k_zamk 0
scoreboard players add #k41 dz.k_wrog 0
scoreboard players add #k41 dz.k_pkt 0
scoreboard players add #k41 dz.k_wczas 0
scoreboard players add #k41 dz.k_wygr 0
scoreboard players add #k41 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k41 set value '{"text":"RPA","color":"dark_green","bold":true}'
scoreboard players display name kZAF dz.ranking [{"text":"ZAF ","color":"dark_gray"},{"text":"RPA","color":"dark_green","bold":false}]
scoreboard players add #k42 dz.k_czl 0
scoreboard players add #k42 dz.k_skarb 0
scoreboard players add #k42 dz.k_wl 0
scoreboard players add #k42 dz.k_zamk 0
scoreboard players add #k42 dz.k_wrog 0
scoreboard players add #k42 dz.k_pkt 0
scoreboard players add #k42 dz.k_wczas 0
scoreboard players add #k42 dz.k_wygr 0
scoreboard players add #k42 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k42 set value '{"text":"Madagaskar","color":"red","bold":true}'
scoreboard players display name kMDG dz.ranking [{"text":"MDG ","color":"dark_gray"},{"text":"Madagaskar","color":"red","bold":false}]
scoreboard players add #k43 dz.k_czl 0
scoreboard players add #k43 dz.k_skarb 0
scoreboard players add #k43 dz.k_wl 0
scoreboard players add #k43 dz.k_zamk 0
scoreboard players add #k43 dz.k_wrog 0
scoreboard players add #k43 dz.k_pkt 0
scoreboard players add #k43 dz.k_wczas 0
scoreboard players add #k43 dz.k_wygr 0
scoreboard players add #k43 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k43 set value '{"text":"Arabia Saudyjska","color":"dark_green","bold":true}'
scoreboard players display name kSAU dz.ranking [{"text":"SAU ","color":"dark_gray"},{"text":"Arabia Saudyjska","color":"dark_green","bold":false}]
scoreboard players add #k44 dz.k_czl 0
scoreboard players add #k44 dz.k_skarb 0
scoreboard players add #k44 dz.k_wl 0
scoreboard players add #k44 dz.k_zamk 0
scoreboard players add #k44 dz.k_wrog 0
scoreboard players add #k44 dz.k_pkt 0
scoreboard players add #k44 dz.k_wczas 0
scoreboard players add #k44 dz.k_wygr 0
scoreboard players add #k44 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k44 set value '{"text":"Iran","color":"green","bold":true}'
scoreboard players display name kIRN dz.ranking [{"text":"IRN ","color":"dark_gray"},{"text":"Iran","color":"green","bold":false}]
scoreboard players add #k45 dz.k_czl 0
scoreboard players add #k45 dz.k_skarb 0
scoreboard players add #k45 dz.k_wl 0
scoreboard players add #k45 dz.k_zamk 0
scoreboard players add #k45 dz.k_wrog 0
scoreboard players add #k45 dz.k_pkt 0
scoreboard players add #k45 dz.k_wczas 0
scoreboard players add #k45 dz.k_wygr 0
scoreboard players add #k45 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k45 set value '{"text":"Indie","color":"gold","bold":true}'
scoreboard players display name kIND dz.ranking [{"text":"IND ","color":"dark_gray"},{"text":"Indie","color":"gold","bold":false}]
scoreboard players add #k46 dz.k_czl 0
scoreboard players add #k46 dz.k_skarb 0
scoreboard players add #k46 dz.k_wl 0
scoreboard players add #k46 dz.k_zamk 0
scoreboard players add #k46 dz.k_wrog 0
scoreboard players add #k46 dz.k_pkt 0
scoreboard players add #k46 dz.k_wczas 0
scoreboard players add #k46 dz.k_wygr 0
scoreboard players add #k46 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k46 set value '{"text":"Chiny","color":"red","bold":true}'
scoreboard players display name kCHN dz.ranking [{"text":"CHN ","color":"dark_gray"},{"text":"Chiny","color":"red","bold":false}]
scoreboard players add #k47 dz.k_czl 0
scoreboard players add #k47 dz.k_skarb 0
scoreboard players add #k47 dz.k_wl 0
scoreboard players add #k47 dz.k_zamk 0
scoreboard players add #k47 dz.k_wrog 0
scoreboard players add #k47 dz.k_pkt 0
scoreboard players add #k47 dz.k_wczas 0
scoreboard players add #k47 dz.k_wygr 0
scoreboard players add #k47 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k47 set value '{"text":"Japonia","color":"white","bold":true}'
scoreboard players display name kJPN dz.ranking [{"text":"JPN ","color":"dark_gray"},{"text":"Japonia","color":"white","bold":false}]
scoreboard players add #k48 dz.k_czl 0
scoreboard players add #k48 dz.k_skarb 0
scoreboard players add #k48 dz.k_wl 0
scoreboard players add #k48 dz.k_zamk 0
scoreboard players add #k48 dz.k_wrog 0
scoreboard players add #k48 dz.k_pkt 0
scoreboard players add #k48 dz.k_wczas 0
scoreboard players add #k48 dz.k_wygr 0
scoreboard players add #k48 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k48 set value '{"text":"Korea Płd.","color":"blue","bold":true}'
scoreboard players display name kKOR dz.ranking [{"text":"KOR ","color":"dark_gray"},{"text":"Korea Płd.","color":"blue","bold":false}]
scoreboard players add #k49 dz.k_czl 0
scoreboard players add #k49 dz.k_skarb 0
scoreboard players add #k49 dz.k_wl 0
scoreboard players add #k49 dz.k_zamk 0
scoreboard players add #k49 dz.k_wrog 0
scoreboard players add #k49 dz.k_pkt 0
scoreboard players add #k49 dz.k_wczas 0
scoreboard players add #k49 dz.k_wygr 0
scoreboard players add #k49 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k49 set value '{"text":"Mongolia","color":"red","bold":true}'
scoreboard players display name kMNG dz.ranking [{"text":"MNG ","color":"dark_gray"},{"text":"Mongolia","color":"red","bold":false}]
scoreboard players add #k50 dz.k_czl 0
scoreboard players add #k50 dz.k_skarb 0
scoreboard players add #k50 dz.k_wl 0
scoreboard players add #k50 dz.k_zamk 0
scoreboard players add #k50 dz.k_wrog 0
scoreboard players add #k50 dz.k_pkt 0
scoreboard players add #k50 dz.k_wczas 0
scoreboard players add #k50 dz.k_wygr 0
scoreboard players add #k50 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k50 set value '{"text":"Kazachstan","color":"aqua","bold":true}'
scoreboard players display name kKAZ dz.ranking [{"text":"KAZ ","color":"dark_gray"},{"text":"Kazachstan","color":"aqua","bold":false}]
scoreboard players add #k51 dz.k_czl 0
scoreboard players add #k51 dz.k_skarb 0
scoreboard players add #k51 dz.k_wl 0
scoreboard players add #k51 dz.k_zamk 0
scoreboard players add #k51 dz.k_wrog 0
scoreboard players add #k51 dz.k_pkt 0
scoreboard players add #k51 dz.k_wczas 0
scoreboard players add #k51 dz.k_wygr 0
scoreboard players add #k51 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k51 set value '{"text":"Indonezja","color":"red","bold":true}'
scoreboard players display name kIDN dz.ranking [{"text":"IDN ","color":"dark_gray"},{"text":"Indonezja","color":"red","bold":false}]
scoreboard players add #k52 dz.k_czl 0
scoreboard players add #k52 dz.k_skarb 0
scoreboard players add #k52 dz.k_wl 0
scoreboard players add #k52 dz.k_zamk 0
scoreboard players add #k52 dz.k_wrog 0
scoreboard players add #k52 dz.k_pkt 0
scoreboard players add #k52 dz.k_wczas 0
scoreboard players add #k52 dz.k_wygr 0
scoreboard players add #k52 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k52 set value '{"text":"Tajlandia","color":"blue","bold":true}'
scoreboard players display name kTHA dz.ranking [{"text":"THA ","color":"dark_gray"},{"text":"Tajlandia","color":"blue","bold":false}]
scoreboard players add #k53 dz.k_czl 0
scoreboard players add #k53 dz.k_skarb 0
scoreboard players add #k53 dz.k_wl 0
scoreboard players add #k53 dz.k_zamk 0
scoreboard players add #k53 dz.k_wrog 0
scoreboard players add #k53 dz.k_pkt 0
scoreboard players add #k53 dz.k_wczas 0
scoreboard players add #k53 dz.k_wygr 0
scoreboard players add #k53 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k53 set value '{"text":"Wietnam","color":"red","bold":true}'
scoreboard players display name kVNM dz.ranking [{"text":"VNM ","color":"dark_gray"},{"text":"Wietnam","color":"red","bold":false}]
scoreboard players add #k54 dz.k_czl 0
scoreboard players add #k54 dz.k_skarb 0
scoreboard players add #k54 dz.k_wl 0
scoreboard players add #k54 dz.k_zamk 0
scoreboard players add #k54 dz.k_wrog 0
scoreboard players add #k54 dz.k_pkt 0
scoreboard players add #k54 dz.k_wczas 0
scoreboard players add #k54 dz.k_wygr 0
scoreboard players add #k54 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k54 set value '{"text":"Filipiny","color":"blue","bold":true}'
scoreboard players display name kPHL dz.ranking [{"text":"PHL ","color":"dark_gray"},{"text":"Filipiny","color":"blue","bold":false}]
scoreboard players add #k55 dz.k_czl 0
scoreboard players add #k55 dz.k_skarb 0
scoreboard players add #k55 dz.k_wl 0
scoreboard players add #k55 dz.k_zamk 0
scoreboard players add #k55 dz.k_wrog 0
scoreboard players add #k55 dz.k_pkt 0
scoreboard players add #k55 dz.k_wczas 0
scoreboard players add #k55 dz.k_wygr 0
scoreboard players add #k55 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k55 set value '{"text":"Australia","color":"dark_blue","bold":true}'
scoreboard players display name kAUS dz.ranking [{"text":"AUS ","color":"dark_gray"},{"text":"Australia","color":"dark_blue","bold":false}]
scoreboard players add #k56 dz.k_czl 0
scoreboard players add #k56 dz.k_skarb 0
scoreboard players add #k56 dz.k_wl 0
scoreboard players add #k56 dz.k_zamk 0
scoreboard players add #k56 dz.k_wrog 0
scoreboard players add #k56 dz.k_pkt 0
scoreboard players add #k56 dz.k_wczas 0
scoreboard players add #k56 dz.k_wygr 0
scoreboard players add #k56 dz.k_pokoj 0
data modify storage dziobmc:kraje n.k56 set value '{"text":"Nowa Zelandia","color":"dark_aqua","bold":true}'
scoreboard players display name kNZL dz.ranking [{"text":"NZL ","color":"dark_gray"},{"text":"Nowa Zelandia","color":"dark_aqua","bold":false}]
function dziobmc:ziemia/przelicz
function dziobmc:ziemia/druzyny
