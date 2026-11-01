scoreboard players operation #p dz.data = #k1 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k1 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k1 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k1 dz.k_czl matches 1.. run scoreboard players operation kPOL dz.ranking = #p dz.data
execute if score #k1 dz.k_czl matches 1.. run scoreboard players display name kPOL dz.ranking [{"text":"POL ","color":"dark_gray"},{"text":"Polska","color":"red","bold":false}]
execute unless score #k1 dz.k_czl matches 1.. run scoreboard players reset kPOL dz.ranking
scoreboard players operation #p dz.data = #k2 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k2 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k2 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k2 dz.k_czl matches 1.. run scoreboard players operation kGER dz.ranking = #p dz.data
execute if score #k2 dz.k_czl matches 1.. run scoreboard players display name kGER dz.ranking [{"text":"GER ","color":"dark_gray"},{"text":"Niemcy","color":"dark_gray","bold":false}]
execute unless score #k2 dz.k_czl matches 1.. run scoreboard players reset kGER dz.ranking
scoreboard players operation #p dz.data = #k3 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k3 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k3 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k3 dz.k_czl matches 1.. run scoreboard players operation kFRA dz.ranking = #p dz.data
execute if score #k3 dz.k_czl matches 1.. run scoreboard players display name kFRA dz.ranking [{"text":"FRA ","color":"dark_gray"},{"text":"Francja","color":"blue","bold":false}]
execute unless score #k3 dz.k_czl matches 1.. run scoreboard players reset kFRA dz.ranking
scoreboard players operation #p dz.data = #k4 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k4 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k4 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k4 dz.k_czl matches 1.. run scoreboard players operation kGBR dz.ranking = #p dz.data
execute if score #k4 dz.k_czl matches 1.. run scoreboard players display name kGBR dz.ranking [{"text":"GBR ","color":"dark_gray"},{"text":"Wielka Brytania","color":"dark_blue","bold":false}]
execute unless score #k4 dz.k_czl matches 1.. run scoreboard players reset kGBR dz.ranking
scoreboard players operation #p dz.data = #k5 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k5 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k5 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k5 dz.k_czl matches 1.. run scoreboard players operation kESP dz.ranking = #p dz.data
execute if score #k5 dz.k_czl matches 1.. run scoreboard players display name kESP dz.ranking [{"text":"ESP ","color":"dark_gray"},{"text":"Hiszpania","color":"gold","bold":false}]
execute unless score #k5 dz.k_czl matches 1.. run scoreboard players reset kESP dz.ranking
scoreboard players operation #p dz.data = #k6 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k6 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k6 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k6 dz.k_czl matches 1.. run scoreboard players operation kITA dz.ranking = #p dz.data
execute if score #k6 dz.k_czl matches 1.. run scoreboard players display name kITA dz.ranking [{"text":"ITA ","color":"dark_gray"},{"text":"Włochy","color":"green","bold":false}]
execute unless score #k6 dz.k_czl matches 1.. run scoreboard players reset kITA dz.ranking
scoreboard players operation #p dz.data = #k7 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k7 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k7 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k7 dz.k_czl matches 1.. run scoreboard players operation kUKR dz.ranking = #p dz.data
execute if score #k7 dz.k_czl matches 1.. run scoreboard players display name kUKR dz.ranking [{"text":"UKR ","color":"dark_gray"},{"text":"Ukraina","color":"yellow","bold":false}]
execute unless score #k7 dz.k_czl matches 1.. run scoreboard players reset kUKR dz.ranking
scoreboard players operation #p dz.data = #k8 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k8 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k8 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k8 dz.k_czl matches 1.. run scoreboard players operation kRUS dz.ranking = #p dz.data
execute if score #k8 dz.k_czl matches 1.. run scoreboard players display name kRUS dz.ranking [{"text":"RUS ","color":"dark_gray"},{"text":"Rosja","color":"white","bold":false}]
execute unless score #k8 dz.k_czl matches 1.. run scoreboard players reset kRUS dz.ranking
scoreboard players operation #p dz.data = #k9 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k9 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k9 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k9 dz.k_czl matches 1.. run scoreboard players operation kSWE dz.ranking = #p dz.data
execute if score #k9 dz.k_czl matches 1.. run scoreboard players display name kSWE dz.ranking [{"text":"SWE ","color":"dark_gray"},{"text":"Szwecja","color":"aqua","bold":false}]
execute unless score #k9 dz.k_czl matches 1.. run scoreboard players reset kSWE dz.ranking
scoreboard players operation #p dz.data = #k10 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k10 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k10 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k10 dz.k_czl matches 1.. run scoreboard players operation kNOR dz.ranking = #p dz.data
execute if score #k10 dz.k_czl matches 1.. run scoreboard players display name kNOR dz.ranking [{"text":"NOR ","color":"dark_gray"},{"text":"Norwegia","color":"dark_red","bold":false}]
execute unless score #k10 dz.k_czl matches 1.. run scoreboard players reset kNOR dz.ranking
scoreboard players operation #p dz.data = #k11 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k11 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k11 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k11 dz.k_czl matches 1.. run scoreboard players operation kFIN dz.ranking = #p dz.data
execute if score #k11 dz.k_czl matches 1.. run scoreboard players display name kFIN dz.ranking [{"text":"FIN ","color":"dark_gray"},{"text":"Finlandia","color":"white","bold":false}]
execute unless score #k11 dz.k_czl matches 1.. run scoreboard players reset kFIN dz.ranking
scoreboard players operation #p dz.data = #k12 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k12 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k12 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k12 dz.k_czl matches 1.. run scoreboard players operation kCZE dz.ranking = #p dz.data
execute if score #k12 dz.k_czl matches 1.. run scoreboard players display name kCZE dz.ranking [{"text":"CZE ","color":"dark_gray"},{"text":"Czechy","color":"blue","bold":false}]
execute unless score #k12 dz.k_czl matches 1.. run scoreboard players reset kCZE dz.ranking
scoreboard players operation #p dz.data = #k13 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k13 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k13 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k13 dz.k_czl matches 1.. run scoreboard players operation kSVK dz.ranking = #p dz.data
execute if score #k13 dz.k_czl matches 1.. run scoreboard players display name kSVK dz.ranking [{"text":"SVK ","color":"dark_gray"},{"text":"Słowacja","color":"blue","bold":false}]
execute unless score #k13 dz.k_czl matches 1.. run scoreboard players reset kSVK dz.ranking
scoreboard players operation #p dz.data = #k14 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k14 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k14 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k14 dz.k_czl matches 1.. run scoreboard players operation kLTU dz.ranking = #p dz.data
execute if score #k14 dz.k_czl matches 1.. run scoreboard players display name kLTU dz.ranking [{"text":"LTU ","color":"dark_gray"},{"text":"Litwa","color":"yellow","bold":false}]
execute unless score #k14 dz.k_czl matches 1.. run scoreboard players reset kLTU dz.ranking
scoreboard players operation #p dz.data = #k15 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k15 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k15 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k15 dz.k_czl matches 1.. run scoreboard players operation kAUT dz.ranking = #p dz.data
execute if score #k15 dz.k_czl matches 1.. run scoreboard players display name kAUT dz.ranking [{"text":"AUT ","color":"dark_gray"},{"text":"Austria","color":"red","bold":false}]
execute unless score #k15 dz.k_czl matches 1.. run scoreboard players reset kAUT dz.ranking
scoreboard players operation #p dz.data = #k16 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k16 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k16 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k16 dz.k_czl matches 1.. run scoreboard players operation kCHE dz.ranking = #p dz.data
execute if score #k16 dz.k_czl matches 1.. run scoreboard players display name kCHE dz.ranking [{"text":"CHE ","color":"dark_gray"},{"text":"Szwajcaria","color":"red","bold":false}]
execute unless score #k16 dz.k_czl matches 1.. run scoreboard players reset kCHE dz.ranking
scoreboard players operation #p dz.data = #k17 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k17 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k17 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k17 dz.k_czl matches 1.. run scoreboard players operation kNLD dz.ranking = #p dz.data
execute if score #k17 dz.k_czl matches 1.. run scoreboard players display name kNLD dz.ranking [{"text":"NLD ","color":"dark_gray"},{"text":"Holandia","color":"gold","bold":false}]
execute unless score #k17 dz.k_czl matches 1.. run scoreboard players reset kNLD dz.ranking
scoreboard players operation #p dz.data = #k18 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k18 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k18 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k18 dz.k_czl matches 1.. run scoreboard players operation kHUN dz.ranking = #p dz.data
execute if score #k18 dz.k_czl matches 1.. run scoreboard players display name kHUN dz.ranking [{"text":"HUN ","color":"dark_gray"},{"text":"Węgry","color":"dark_green","bold":false}]
execute unless score #k18 dz.k_czl matches 1.. run scoreboard players reset kHUN dz.ranking
scoreboard players operation #p dz.data = #k19 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k19 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k19 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k19 dz.k_czl matches 1.. run scoreboard players operation kROU dz.ranking = #p dz.data
execute if score #k19 dz.k_czl matches 1.. run scoreboard players display name kROU dz.ranking [{"text":"ROU ","color":"dark_gray"},{"text":"Rumunia","color":"yellow","bold":false}]
execute unless score #k19 dz.k_czl matches 1.. run scoreboard players reset kROU dz.ranking
scoreboard players operation #p dz.data = #k20 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k20 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k20 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k20 dz.k_czl matches 1.. run scoreboard players operation kGRC dz.ranking = #p dz.data
execute if score #k20 dz.k_czl matches 1.. run scoreboard players display name kGRC dz.ranking [{"text":"GRC ","color":"dark_gray"},{"text":"Grecja","color":"aqua","bold":false}]
execute unless score #k20 dz.k_czl matches 1.. run scoreboard players reset kGRC dz.ranking
scoreboard players operation #p dz.data = #k21 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k21 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k21 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k21 dz.k_czl matches 1.. run scoreboard players operation kPRT dz.ranking = #p dz.data
execute if score #k21 dz.k_czl matches 1.. run scoreboard players display name kPRT dz.ranking [{"text":"PRT ","color":"dark_gray"},{"text":"Portugalia","color":"dark_green","bold":false}]
execute unless score #k21 dz.k_czl matches 1.. run scoreboard players reset kPRT dz.ranking
scoreboard players operation #p dz.data = #k22 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k22 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k22 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k22 dz.k_czl matches 1.. run scoreboard players operation kTUR dz.ranking = #p dz.data
execute if score #k22 dz.k_czl matches 1.. run scoreboard players display name kTUR dz.ranking [{"text":"TUR ","color":"dark_gray"},{"text":"Turcja","color":"red","bold":false}]
execute unless score #k22 dz.k_czl matches 1.. run scoreboard players reset kTUR dz.ranking
scoreboard players operation #p dz.data = #k23 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k23 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k23 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k23 dz.k_czl matches 1.. run scoreboard players operation kISL dz.ranking = #p dz.data
execute if score #k23 dz.k_czl matches 1.. run scoreboard players display name kISL dz.ranking [{"text":"ISL ","color":"dark_gray"},{"text":"Islandia","color":"blue","bold":false}]
execute unless score #k23 dz.k_czl matches 1.. run scoreboard players reset kISL dz.ranking
scoreboard players operation #p dz.data = #k24 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k24 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k24 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k24 dz.k_czl matches 1.. run scoreboard players operation kDNK dz.ranking = #p dz.data
execute if score #k24 dz.k_czl matches 1.. run scoreboard players display name kDNK dz.ranking [{"text":"DNK ","color":"dark_gray"},{"text":"Dania","color":"red","bold":false}]
execute unless score #k24 dz.k_czl matches 1.. run scoreboard players reset kDNK dz.ranking
scoreboard players operation #p dz.data = #k25 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k25 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k25 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k25 dz.k_czl matches 1.. run scoreboard players operation kUSA dz.ranking = #p dz.data
execute if score #k25 dz.k_czl matches 1.. run scoreboard players display name kUSA dz.ranking [{"text":"USA ","color":"dark_gray"},{"text":"USA","color":"blue","bold":false}]
execute unless score #k25 dz.k_czl matches 1.. run scoreboard players reset kUSA dz.ranking
scoreboard players operation #p dz.data = #k26 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k26 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k26 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k26 dz.k_czl matches 1.. run scoreboard players operation kCAN dz.ranking = #p dz.data
execute if score #k26 dz.k_czl matches 1.. run scoreboard players display name kCAN dz.ranking [{"text":"CAN ","color":"dark_gray"},{"text":"Kanada","color":"red","bold":false}]
execute unless score #k26 dz.k_czl matches 1.. run scoreboard players reset kCAN dz.ranking
scoreboard players operation #p dz.data = #k27 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k27 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k27 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k27 dz.k_czl matches 1.. run scoreboard players operation kMEX dz.ranking = #p dz.data
execute if score #k27 dz.k_czl matches 1.. run scoreboard players display name kMEX dz.ranking [{"text":"MEX ","color":"dark_gray"},{"text":"Meksyk","color":"dark_green","bold":false}]
execute unless score #k27 dz.k_czl matches 1.. run scoreboard players reset kMEX dz.ranking
scoreboard players operation #p dz.data = #k28 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k28 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k28 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k28 dz.k_czl matches 1.. run scoreboard players operation kCUB dz.ranking = #p dz.data
execute if score #k28 dz.k_czl matches 1.. run scoreboard players display name kCUB dz.ranking [{"text":"CUB ","color":"dark_gray"},{"text":"Kuba","color":"blue","bold":false}]
execute unless score #k28 dz.k_czl matches 1.. run scoreboard players reset kCUB dz.ranking
scoreboard players operation #p dz.data = #k29 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k29 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k29 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k29 dz.k_czl matches 1.. run scoreboard players operation kBRA dz.ranking = #p dz.data
execute if score #k29 dz.k_czl matches 1.. run scoreboard players display name kBRA dz.ranking [{"text":"BRA ","color":"dark_gray"},{"text":"Brazylia","color":"green","bold":false}]
execute unless score #k29 dz.k_czl matches 1.. run scoreboard players reset kBRA dz.ranking
scoreboard players operation #p dz.data = #k30 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k30 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k30 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k30 dz.k_czl matches 1.. run scoreboard players operation kARG dz.ranking = #p dz.data
execute if score #k30 dz.k_czl matches 1.. run scoreboard players display name kARG dz.ranking [{"text":"ARG ","color":"dark_gray"},{"text":"Argentyna","color":"aqua","bold":false}]
execute unless score #k30 dz.k_czl matches 1.. run scoreboard players reset kARG dz.ranking
scoreboard players operation #p dz.data = #k31 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k31 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k31 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k31 dz.k_czl matches 1.. run scoreboard players operation kCHL dz.ranking = #p dz.data
execute if score #k31 dz.k_czl matches 1.. run scoreboard players display name kCHL dz.ranking [{"text":"CHL ","color":"dark_gray"},{"text":"Chile","color":"red","bold":false}]
execute unless score #k31 dz.k_czl matches 1.. run scoreboard players reset kCHL dz.ranking
scoreboard players operation #p dz.data = #k32 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k32 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k32 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k32 dz.k_czl matches 1.. run scoreboard players operation kPER dz.ranking = #p dz.data
execute if score #k32 dz.k_czl matches 1.. run scoreboard players display name kPER dz.ranking [{"text":"PER ","color":"dark_gray"},{"text":"Peru","color":"dark_red","bold":false}]
execute unless score #k32 dz.k_czl matches 1.. run scoreboard players reset kPER dz.ranking
scoreboard players operation #p dz.data = #k33 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k33 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k33 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k33 dz.k_czl matches 1.. run scoreboard players operation kCOL dz.ranking = #p dz.data
execute if score #k33 dz.k_czl matches 1.. run scoreboard players display name kCOL dz.ranking [{"text":"COL ","color":"dark_gray"},{"text":"Kolumbia","color":"yellow","bold":false}]
execute unless score #k33 dz.k_czl matches 1.. run scoreboard players reset kCOL dz.ranking
scoreboard players operation #p dz.data = #k34 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k34 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k34 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k34 dz.k_czl matches 1.. run scoreboard players operation kVEN dz.ranking = #p dz.data
execute if score #k34 dz.k_czl matches 1.. run scoreboard players display name kVEN dz.ranking [{"text":"VEN ","color":"dark_gray"},{"text":"Wenezuela","color":"gold","bold":false}]
execute unless score #k34 dz.k_czl matches 1.. run scoreboard players reset kVEN dz.ranking
scoreboard players operation #p dz.data = #k35 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k35 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k35 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k35 dz.k_czl matches 1.. run scoreboard players operation kEGY dz.ranking = #p dz.data
execute if score #k35 dz.k_czl matches 1.. run scoreboard players display name kEGY dz.ranking [{"text":"EGY ","color":"dark_gray"},{"text":"Egipt","color":"gold","bold":false}]
execute unless score #k35 dz.k_czl matches 1.. run scoreboard players reset kEGY dz.ranking
scoreboard players operation #p dz.data = #k36 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k36 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k36 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k36 dz.k_czl matches 1.. run scoreboard players operation kMAR dz.ranking = #p dz.data
execute if score #k36 dz.k_czl matches 1.. run scoreboard players display name kMAR dz.ranking [{"text":"MAR ","color":"dark_gray"},{"text":"Maroko","color":"dark_red","bold":false}]
execute unless score #k36 dz.k_czl matches 1.. run scoreboard players reset kMAR dz.ranking
scoreboard players operation #p dz.data = #k37 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k37 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k37 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k37 dz.k_czl matches 1.. run scoreboard players operation kDZA dz.ranking = #p dz.data
execute if score #k37 dz.k_czl matches 1.. run scoreboard players display name kDZA dz.ranking [{"text":"DZA ","color":"dark_gray"},{"text":"Algieria","color":"dark_green","bold":false}]
execute unless score #k37 dz.k_czl matches 1.. run scoreboard players reset kDZA dz.ranking
scoreboard players operation #p dz.data = #k38 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k38 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k38 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k38 dz.k_czl matches 1.. run scoreboard players operation kNGA dz.ranking = #p dz.data
execute if score #k38 dz.k_czl matches 1.. run scoreboard players display name kNGA dz.ranking [{"text":"NGA ","color":"dark_gray"},{"text":"Nigeria","color":"green","bold":false}]
execute unless score #k38 dz.k_czl matches 1.. run scoreboard players reset kNGA dz.ranking
scoreboard players operation #p dz.data = #k39 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k39 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k39 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k39 dz.k_czl matches 1.. run scoreboard players operation kKEN dz.ranking = #p dz.data
execute if score #k39 dz.k_czl matches 1.. run scoreboard players display name kKEN dz.ranking [{"text":"KEN ","color":"dark_gray"},{"text":"Kenia","color":"dark_red","bold":false}]
execute unless score #k39 dz.k_czl matches 1.. run scoreboard players reset kKEN dz.ranking
scoreboard players operation #p dz.data = #k40 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k40 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k40 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k40 dz.k_czl matches 1.. run scoreboard players operation kETH dz.ranking = #p dz.data
execute if score #k40 dz.k_czl matches 1.. run scoreboard players display name kETH dz.ranking [{"text":"ETH ","color":"dark_gray"},{"text":"Etiopia","color":"yellow","bold":false}]
execute unless score #k40 dz.k_czl matches 1.. run scoreboard players reset kETH dz.ranking
scoreboard players operation #p dz.data = #k41 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k41 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k41 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k41 dz.k_czl matches 1.. run scoreboard players operation kZAF dz.ranking = #p dz.data
execute if score #k41 dz.k_czl matches 1.. run scoreboard players display name kZAF dz.ranking [{"text":"ZAF ","color":"dark_gray"},{"text":"RPA","color":"dark_green","bold":false}]
execute unless score #k41 dz.k_czl matches 1.. run scoreboard players reset kZAF dz.ranking
scoreboard players operation #p dz.data = #k42 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k42 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k42 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k42 dz.k_czl matches 1.. run scoreboard players operation kMDG dz.ranking = #p dz.data
execute if score #k42 dz.k_czl matches 1.. run scoreboard players display name kMDG dz.ranking [{"text":"MDG ","color":"dark_gray"},{"text":"Madagaskar","color":"red","bold":false}]
execute unless score #k42 dz.k_czl matches 1.. run scoreboard players reset kMDG dz.ranking
scoreboard players operation #p dz.data = #k43 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k43 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k43 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k43 dz.k_czl matches 1.. run scoreboard players operation kSAU dz.ranking = #p dz.data
execute if score #k43 dz.k_czl matches 1.. run scoreboard players display name kSAU dz.ranking [{"text":"SAU ","color":"dark_gray"},{"text":"Arabia Saudyjska","color":"dark_green","bold":false}]
execute unless score #k43 dz.k_czl matches 1.. run scoreboard players reset kSAU dz.ranking
scoreboard players operation #p dz.data = #k44 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k44 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k44 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k44 dz.k_czl matches 1.. run scoreboard players operation kIRN dz.ranking = #p dz.data
execute if score #k44 dz.k_czl matches 1.. run scoreboard players display name kIRN dz.ranking [{"text":"IRN ","color":"dark_gray"},{"text":"Iran","color":"green","bold":false}]
execute unless score #k44 dz.k_czl matches 1.. run scoreboard players reset kIRN dz.ranking
scoreboard players operation #p dz.data = #k45 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k45 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k45 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k45 dz.k_czl matches 1.. run scoreboard players operation kIND dz.ranking = #p dz.data
execute if score #k45 dz.k_czl matches 1.. run scoreboard players display name kIND dz.ranking [{"text":"IND ","color":"dark_gray"},{"text":"Indie","color":"gold","bold":false}]
execute unless score #k45 dz.k_czl matches 1.. run scoreboard players reset kIND dz.ranking
scoreboard players operation #p dz.data = #k46 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k46 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k46 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k46 dz.k_czl matches 1.. run scoreboard players operation kCHN dz.ranking = #p dz.data
execute if score #k46 dz.k_czl matches 1.. run scoreboard players display name kCHN dz.ranking [{"text":"CHN ","color":"dark_gray"},{"text":"Chiny","color":"red","bold":false}]
execute unless score #k46 dz.k_czl matches 1.. run scoreboard players reset kCHN dz.ranking
scoreboard players operation #p dz.data = #k47 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k47 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k47 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k47 dz.k_czl matches 1.. run scoreboard players operation kJPN dz.ranking = #p dz.data
execute if score #k47 dz.k_czl matches 1.. run scoreboard players display name kJPN dz.ranking [{"text":"JPN ","color":"dark_gray"},{"text":"Japonia","color":"white","bold":false}]
execute unless score #k47 dz.k_czl matches 1.. run scoreboard players reset kJPN dz.ranking
scoreboard players operation #p dz.data = #k48 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k48 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k48 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k48 dz.k_czl matches 1.. run scoreboard players operation kKOR dz.ranking = #p dz.data
execute if score #k48 dz.k_czl matches 1.. run scoreboard players display name kKOR dz.ranking [{"text":"KOR ","color":"dark_gray"},{"text":"Korea Płd.","color":"blue","bold":false}]
execute unless score #k48 dz.k_czl matches 1.. run scoreboard players reset kKOR dz.ranking
scoreboard players operation #p dz.data = #k49 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k49 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k49 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k49 dz.k_czl matches 1.. run scoreboard players operation kMNG dz.ranking = #p dz.data
execute if score #k49 dz.k_czl matches 1.. run scoreboard players display name kMNG dz.ranking [{"text":"MNG ","color":"dark_gray"},{"text":"Mongolia","color":"red","bold":false}]
execute unless score #k49 dz.k_czl matches 1.. run scoreboard players reset kMNG dz.ranking
scoreboard players operation #p dz.data = #k50 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k50 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k50 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k50 dz.k_czl matches 1.. run scoreboard players operation kKAZ dz.ranking = #p dz.data
execute if score #k50 dz.k_czl matches 1.. run scoreboard players display name kKAZ dz.ranking [{"text":"KAZ ","color":"dark_gray"},{"text":"Kazachstan","color":"aqua","bold":false}]
execute unless score #k50 dz.k_czl matches 1.. run scoreboard players reset kKAZ dz.ranking
scoreboard players operation #p dz.data = #k51 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k51 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k51 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k51 dz.k_czl matches 1.. run scoreboard players operation kIDN dz.ranking = #p dz.data
execute if score #k51 dz.k_czl matches 1.. run scoreboard players display name kIDN dz.ranking [{"text":"IDN ","color":"dark_gray"},{"text":"Indonezja","color":"red","bold":false}]
execute unless score #k51 dz.k_czl matches 1.. run scoreboard players reset kIDN dz.ranking
scoreboard players operation #p dz.data = #k52 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k52 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k52 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k52 dz.k_czl matches 1.. run scoreboard players operation kTHA dz.ranking = #p dz.data
execute if score #k52 dz.k_czl matches 1.. run scoreboard players display name kTHA dz.ranking [{"text":"THA ","color":"dark_gray"},{"text":"Tajlandia","color":"blue","bold":false}]
execute unless score #k52 dz.k_czl matches 1.. run scoreboard players reset kTHA dz.ranking
scoreboard players operation #p dz.data = #k53 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k53 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k53 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k53 dz.k_czl matches 1.. run scoreboard players operation kVNM dz.ranking = #p dz.data
execute if score #k53 dz.k_czl matches 1.. run scoreboard players display name kVNM dz.ranking [{"text":"VNM ","color":"dark_gray"},{"text":"Wietnam","color":"red","bold":false}]
execute unless score #k53 dz.k_czl matches 1.. run scoreboard players reset kVNM dz.ranking
scoreboard players operation #p dz.data = #k54 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k54 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k54 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k54 dz.k_czl matches 1.. run scoreboard players operation kPHL dz.ranking = #p dz.data
execute if score #k54 dz.k_czl matches 1.. run scoreboard players display name kPHL dz.ranking [{"text":"PHL ","color":"dark_gray"},{"text":"Filipiny","color":"blue","bold":false}]
execute unless score #k54 dz.k_czl matches 1.. run scoreboard players reset kPHL dz.ranking
scoreboard players operation #p dz.data = #k55 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k55 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k55 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k55 dz.k_czl matches 1.. run scoreboard players operation kAUS dz.ranking = #p dz.data
execute if score #k55 dz.k_czl matches 1.. run scoreboard players display name kAUS dz.ranking [{"text":"AUS ","color":"dark_gray"},{"text":"Australia","color":"dark_blue","bold":false}]
execute unless score #k55 dz.k_czl matches 1.. run scoreboard players reset kAUS dz.ranking
scoreboard players operation #p dz.data = #k56 dz.k_czl
scoreboard players operation #p dz.data *= #100 dz.data
scoreboard players operation #q dz.data = #k56 dz.k_skarb
scoreboard players operation #q dz.data /= #10 dz.data
scoreboard players operation #p dz.data += #q dz.data
scoreboard players operation #q dz.data = #k56 dz.k_wygr
scoreboard players operation #q dz.data *= #500 dz.data
scoreboard players operation #p dz.data += #q dz.data
execute if score #k56 dz.k_czl matches 1.. run scoreboard players operation kNZL dz.ranking = #p dz.data
execute if score #k56 dz.k_czl matches 1.. run scoreboard players display name kNZL dz.ranking [{"text":"NZL ","color":"dark_gray"},{"text":"Nowa Zelandia","color":"dark_aqua","bold":false}]
execute unless score #k56 dz.k_czl matches 1.. run scoreboard players reset kNZL dz.ranking
scoreboard players set #ile_kr dz.data 0
execute if score #k1 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k2 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k3 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k4 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k5 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k6 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k7 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k8 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k9 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k10 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k11 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k12 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k13 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k14 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k15 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k16 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k17 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k18 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k19 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k20 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k21 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k22 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k23 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k24 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k25 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k26 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k27 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k28 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k29 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k30 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k31 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k32 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k33 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k34 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k35 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k36 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k37 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k38 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k39 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k40 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k41 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k42 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k43 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k44 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k45 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k46 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k47 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k48 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k49 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k50 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k51 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k52 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k53 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k54 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k55 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
execute if score #k56 dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1
scoreboard players add #sb dz.data 1
execute if score #sb dz.data matches 2.. run scoreboard players set #sb dz.data 0
execute if score #sb dz.data matches 1 if score #ile_kr dz.data matches 1.. run scoreboard objectives setdisplay sidebar dz.ranking
execute unless score #sb dz.data matches 1 run scoreboard objectives setdisplay sidebar dz.sidebar
execute unless score #ile_kr dz.data matches 1.. run scoreboard objectives setdisplay sidebar dz.sidebar
