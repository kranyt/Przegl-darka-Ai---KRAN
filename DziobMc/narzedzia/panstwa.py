"""Państwa bez limitu: każdy kraj z listy może mieć wiele państw (Polska, Polska2, Polska3...).

Państwo (egzemplarz) ma id = kraj*1000 + numer. Dane trzymane są w:
  * storage dziobmc:kraje lista[] – {id,k,n,nn,nj,tj,kod,kol,x,z,x0,z0}
  * fake playerach #k<id> – dz.k_czl, dz.k_skarb, dz.k_wl, dz.k_zamk, dz.k_wrog, dz.k_pkt, dz.k_wczas, dz.k_wygr, dz.k_pokoj
Gracz: dz.kraj (kraj bazowy), dz.kid (id państwa), dz.prosba (id państwa, do którego prosi).
"""
from wspolne import NS, J, t, sc, sel, tellraw, fn, jfile, snbt_text, firework_cmd, cooldown
from rdzen import RANGI, prefix
from ziemia_smp import KRAJE, KONTYNENTY, SWIAT, STREFA

LIN = t("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "aqua", bold=True)
OB_K = ["dz.k_czl", "dz.k_skarb", "dz.k_wl", "dz.k_zamk", "dz.k_wrog", "dz.k_pkt", "dz.k_wczas", "dz.k_wygr", "dz.k_pokoj"]


def build():
    # ---------------------------------------------------------------- init
    ini = ["scoreboard objectives add dz.kid dummy", "scoreboard objectives add dz.cd_przen dummy",
           "scoreboard players set #160 dz.data 160",
           "execute unless data storage dziobmc:kraje lista run data modify storage dziobmc:kraje lista set value []"]
    for k in KRAJE:
        ini.append(f"data modify storage dziobmc:kraje b.k{k[0]} set value {{k:{k[0]},nazwa:\"{k[1]}\",kod:\"{k[2]}\",kol:\"{k[3]}\",stol:\"{k[4]}\"}}")
    for ri, (rid, team, lvl, pre, col, staff) in enumerate(RANGI):
        ini.append(f"data modify storage dziobmc:kraje rp.r{ri} set value {{rp:{snbt_text(prefix(pre))},rkol:\"{col}\"}}")
    # sprzątanie po starej wersji (stałe drużyny)
    for ri in range(len(RANGI)):
        for kid in range(0, len(KRAJE) + 1):
            ini.append(f"team remove r{ri}k{kid}")
    fn("kraje/init", "\n".join(ini))

    # ---------------------------------------------------------------- drużyny (tworzone w locie)
    fn("gracz/druzyna", f"""
        # Wpisuje gracza do drużyny r<ranga>i<id państwa> (tworzy ją, jeśli trzeba)
        execute unless score @s dz.rid matches 0.. run scoreboard players set @s dz.rid {len(RANGI) - 1}
        scoreboard players add @s dz.kid 0
        execute store result storage dziobmc:tmp d.r int 1 run scoreboard players get @s dz.rid
        execute store result storage dziobmc:tmp d.id int 1 run scoreboard players get @s dz.kid
        function {NS}:gracz/druzyna_spr with storage dziobmc:tmp d
    """)
    fn("gracz/druzyna_spr", f"""
        # państwo mogło zostać rozwiązane
        $execute if score @s dz.kid matches 1.. unless data storage dziobmc:kraje lista[{{id:$(id)}}] run function {NS}:kraje/wyczysc_gracza
        $data modify storage dziobmc:tmp d merge from storage dziobmc:kraje rp.r$(r)
        execute if score @s dz.kid matches 1.. run function {NS}:gracz/druzyna_tj with storage dziobmc:tmp d
        execute unless score @s dz.kid matches 1.. run function {NS}:gracz/druzyna_bez with storage dziobmc:tmp d
        execute if score @s dz.kid matches 1.. run function {NS}:gracz/druzyna_z with storage dziobmc:tmp d
    """)
    fn("gracz/druzyna_tj", "$data modify storage dziobmc:tmp d.tj set from storage dziobmc:kraje lista[{id:$(id)}].tj")
    fn("gracz/druzyna_bez", """
        $team add r$(r)i0
        $team modify r$(r)i0 prefix $(rp)
        $team modify r$(r)i0 color $(rkol)
        $team modify r$(r)i0 collisionRule never
        $team join r$(r)i0 @s
    """)
    fn("gracz/druzyna_z", """
        $team add r$(r)i$(id)
        $team modify r$(r)i$(id) prefix [$(rp),{"text":"[","color":"dark_gray"},$(tj),{"text":"] ","color":"dark_gray"}]
        $team modify r$(r)i$(id) color $(rkol)
        $team modify r$(r)i$(id) collisionRule never
        $team join r$(r)i$(id) @s
    """)
    fn("kraje/wyczysc_gracza", """
        scoreboard players set @s dz.kid 0
        scoreboard players set @s dz.kraj 0
        tag @s remove dz.wladca
        scoreboard players set #zero dz.data 0
        execute store result storage dziobmc:tmp d.id int 1 run scoreboard players get #zero dz.data
    """)

    # ---------------------------------------------------------------- iterator po liście państw
    fn("kraje/iter", f"""
        # Wywołuje funkcję z #iter_tryb dla każdego państwa: 1 = sekunda, 2 = ranking, 3 = lista dla gracza, 4 = menu wojny
        data modify storage dziobmc:tmp it set from storage dziobmc:kraje lista
        function {NS}:kraje/iter_krok
    """)
    fn("kraje/iter_krok", f"""
        execute unless data storage dziobmc:tmp it[0] run return 0
        execute if score #iter_tryb dz.data matches 1 run function {NS}:kraje/na_sekunde with storage dziobmc:tmp it[0]
        execute if score #iter_tryb dz.data matches 2 run function {NS}:kraje/na_ranking with storage dziobmc:tmp it[0]
        execute if score #iter_tryb dz.data matches 3 run function {NS}:kraje/na_liste with storage dziobmc:tmp it[0]
        execute if score #iter_tryb dz.data matches 4 run function {NS}:kraje/na_wojne with storage dziobmc:tmp it[0]
        data remove storage dziobmc:tmp it[0]
        function {NS}:kraje/iter_krok
    """)

    # ---------------------------------------------------------------- menu /trigger panstwo
    menu = [tellraw("@s", LIN), tellraw("@s", t("   ✪ ", "aqua"), t("WYBIERZ KRAJ", "gold", bold=True), t("  (kliknij nazwę)", "gray")), tellraw("@s", LIN)]
    for kont in KONTYNENTY:
        cz = [t(f" {kont}: ", "yellow", bold=True)]
        for k in [k for k in KRAJE if k[7] == kont]:
            cz += [t(k[1], k[3], run=f"/trigger panstwo set {100 + k[0]}", hover=[t(k[1], k[3], bold=True), t(f"\nStolica: {k[4]}\nZobacz państwa / załóż nowe", "gray")]), t(" • ", "dark_gray")]
        menu.append(tellraw("@s", *cz[:-1]))
    menu += [tellraw("@s", t(" Każdy kraj może mieć wiele państw: ", "gray"), t("Polska, Polska2, Polska3...", "red", bold=True)),
             tellraw("@s", t(" Kto zakłada państwo, zostaje jego ", "gray"), t("WŁADCĄ", "gold", bold=True), t("!", "gray")),
             tellraw("@s", t(" ➤ ", "dark_gray"), t("[RANKING PAŃSTW]", "yellow", bold=True, run="/trigger panstwo set 2"), t("  "),
                     t("[LOSOWY TP NA ZIEMI]", "green", bold=True, run="/trigger ziemia set 11")),
             tellraw("@s", LIN)]
    fn("kraje/menu_wybor", "\n".join(menu))

    # lista państw danego kraju + przycisk "załóż nowe"
    for k in KRAJE:
        fn(f"kraje/kraj/{k[0]}", "\n".join([
            tellraw("@s", LIN),
            tellraw("@s", t("   ✪ ", "aqua"), t(f"PAŃSTWA: {k[1].upper()}", k[3], bold=True)),
            tellraw("@s", LIN),
            "scoreboard players set #lista_ile dz.data 0",
            f"scoreboard players set #fk dz.data {k[0]}",
            "scoreboard players set #iter_tryb dz.data 3",
            f"function {NS}:kraje/iter",
            "execute if score #lista_ile dz.data matches 0 run " + tellraw("@s", t(" Nikt jeszcze nie założył tu państwa!", "gray", italic=True)),
            f"scoreboard players set #k dz.data {k[0]}",
            f"function {NS}:kraje/wolny_n",
            f"function {NS}:kraje/przycisk_zaloz with storage dziobmc:tmp wn",
            tellraw("@s", LIN),
        ]))
    fn("kraje/na_liste", f"""
        $execute unless score #fk dz.data matches $(k) run return 0
        scoreboard players add #lista_ile dz.data 1
        $tellraw @s [{{"text":" • ","color":"dark_gray"}},$(nj),{{"text":"  ☺ ","color":"gray"}},{{"score":{{"name":"#k$(id)","objective":"dz.k_czl"}},"color":"white"}},{{"text":"  ⛃ ","color":"gold"}},{{"score":{{"name":"#k$(id)","objective":"dz.k_skarb"}},"color":"yellow"}},{{"text":"  "}},{{"text":"[DOŁĄCZ]","color":"green","bold":true,"clickEvent":{{"action":"run_command","value":"/trigger panstwo set $(id)"}}}}]
    """)
    fn("kraje/wolny_n", f"""
        # Szuka najniższego wolnego numeru państwa dla kraju #k -> storage tmp wn {{k,n,id,nn,...}}
        scoreboard players set #n dz.data 0
        function {NS}:kraje/wolny_n_krok
    """)
    fn("kraje/wolny_n_krok", f"""
        scoreboard players add #n dz.data 1
        scoreboard players operation #id dz.data = #k dz.data
        scoreboard players operation #id dz.data *= #1000 dz.data
        scoreboard players operation #id dz.data += #n dz.data
        execute store result storage dziobmc:tmp wn.id int 1 run scoreboard players get #id dz.data
        execute store result storage dziobmc:tmp wn.k int 1 run scoreboard players get #k dz.data
        execute store result storage dziobmc:tmp wn.n int 1 run scoreboard players get #n dz.data
        scoreboard players set #zal dz.data 200000
        scoreboard players operation #zal dz.data += #k dz.data
        execute store result storage dziobmc:tmp wn.zal int 1 run scoreboard players get #zal dz.data
        execute if score #n dz.data matches 999.. run return 0
        function {NS}:kraje/wolny_n_spr with storage dziobmc:tmp wn
    """)
    fn("kraje/wolny_n_spr", f"""
        $execute if data storage dziobmc:kraje lista[{{id:$(id)}}] run function {NS}:kraje/wolny_n_krok
        $data modify storage dziobmc:tmp wn merge from storage dziobmc:kraje b.k$(k)
        execute if score #n dz.data matches 1 run data modify storage dziobmc:tmp wn.nn set value ""
        execute unless score #n dz.data matches 1 store result storage dziobmc:tmp wn.nn int 1 run scoreboard players get #n dz.data
    """)
    fn("kraje/przycisk_zaloz", """
        $tellraw @s [{"text":" ➤ ","color":"dark_gray"},{"text":"[ZAŁÓŻ PAŃSTWO: $(nazwa)$(nn)]","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/trigger panstwo set $(zal)"},"hoverEvent":{"action":"show_text","contents":"Zostaniesz władcą nowego państwa!"}}]
    """)

    # zakładanie
    fn("kraje/zaloz", f"""
        # #k = kraj bazowy; zakłada państwo o najniższym wolnym numerze i robi gracza władcą
        execute if score @s dz.kid matches 1.. run return run {tellraw("@s", t("✖ Najpierw opuść swoje państwo: ", "red"), t("[OPUŚĆ]", "red", bold=True, run="/trigger panstwo set 999"))}
        function {NS}:kraje/wolny_n
        execute if score #n dz.data matches 999.. run return run {tellraw("@s", t("✖ Za dużo państw tego kraju.", "red"))}
        function {NS}:kraje/zaloz_m with storage dziobmc:tmp wn
    """)
    fn("kraje/zaloz_m", f"""
        $data modify storage dziobmc:tmp wn.nj set value '{{"text":"$(nazwa)$(nn)","color":"$(kol)","bold":true}}'
        $data modify storage dziobmc:tmp wn.tj set value '{{"text":"$(kod)$(nn)","color":"$(kol)","bold":true}}'
        # stolica: pierwsze państwo = prawdziwa stolica, kolejne = miejsce założenia (na mapie Ziemi)
        $data modify storage dziobmc:tmp wn.x set from storage dziobmc:kraje s.k$(k).x
        $data modify storage dziobmc:tmp wn.z set from storage dziobmc:kraje s.k$(k).z
        execute unless score #n dz.data matches 1 at @s if dimension {SWIAT} run function {NS}:kraje/stolica_tutaj_wn
        execute unless score #n dz.data matches 1 at @s unless dimension {SWIAT} run function {NS}:kraje/stolica_przesun_wn
        function {NS}:kraje/x0z0_wn
        data modify storage dziobmc:kraje lista append from storage dziobmc:tmp wn
        function {NS}:kraje/zaloz_m2 with storage dziobmc:tmp wn
    """)
    fn("kraje/zaloz_m2", f"""
        $scoreboard players set #k$(id) dz.k_czl 0
        $scoreboard players set #k$(id) dz.k_skarb 0
        $scoreboard players set #k$(id) dz.k_wl 0
        $scoreboard players set #k$(id) dz.k_zamk 0
        $scoreboard players set #k$(id) dz.k_wrog 0
        $scoreboard players set #k$(id) dz.k_pkt 0
        $scoreboard players set #k$(id) dz.k_wczas 0
        $scoreboard players set #k$(id) dz.k_wygr 0
        $scoreboard players set #k$(id) dz.k_pokoj 0
        $tellraw @a [{{"text":"✪ ","color":"aqua"}},{{"selector":"@s"}},{{"text":" zakłada nowe państwo ","color":"yellow"}},$(nj),{{"text":"!","color":"yellow"}}]
        $function {NS}:kraje/wejdz {{id:$(id)}}
    """)
    fn("kraje/stolica_tutaj_wn", """
        execute store result storage dziobmc:tmp wn.x int 1 run data get entity @s Pos[0]
        execute store result storage dziobmc:tmp wn.z int 1 run data get entity @s Pos[2]
    """)
    fn("kraje/stolica_przesun_wn", """
        # gracz poza mapą Ziemi: stolica obok prawdziwej, przesunięta o 160 kratek na numer
        execute store result score #x dz.data run data get storage dziobmc:tmp wn.x
        scoreboard players operation #q dz.data = #n dz.data
        scoreboard players remove #q dz.data 1
        scoreboard players operation #q dz.data *= #160 dz.data
        scoreboard players operation #x dz.data += #q dz.data
        execute store result storage dziobmc:tmp wn.x int 1 run scoreboard players get #x dz.data
    """)
    fn("kraje/x0z0_wn", f"""
        execute store result score #x dz.data run data get storage dziobmc:tmp wn.x
        execute store result score #z dz.data run data get storage dziobmc:tmp wn.z
        scoreboard players remove #x dz.data {STREFA}
        scoreboard players remove #z dz.data {STREFA}
        execute store result storage dziobmc:tmp wn.x0 int 1 run scoreboard players get #x dz.data
        execute store result storage dziobmc:tmp wn.z0 int 1 run scoreboard players get #z dz.data
    """)

    # dołączanie
    fn("kraje/dolacz", f"""
        # #v = id państwa
        execute if score @s dz.kid matches 1.. run return run {tellraw("@s", t("✖ Najpierw opuść swoje państwo: ", "red"), t("[OPUŚĆ]", "red", bold=True, run="/trigger panstwo set 999"))}
        execute store result storage dziobmc:tmp j.id int 1 run scoreboard players get #v dz.data
        function {NS}:kraje/dolacz_m with storage dziobmc:tmp j
    """)
    fn("kraje/dolacz_m", f"""
        $execute unless data storage dziobmc:kraje lista[{{id:$(id)}}] run return run tellraw @s {{"text":"✖ To państwo już nie istnieje.","color":"red"}}
        $execute if score #k$(id) dz.k_zamk matches 1 if score #k$(id) dz.k_wl matches 1 run return run function {NS}:kraje/prosba {{id:$(id)}}
        $function {NS}:kraje/wejdz {{id:$(id)}}
    """)
    # wejdz: nazwa przez osobne makro (lista j)
    fn("kraje/wejdz", f"""
        $scoreboard players set @s dz.kid $(id)
        $scoreboard players set #q dz.data $(id)
        scoreboard players operation #q dz.data /= #1000 dz.data
        scoreboard players operation @s dz.kraj = #q dz.data
        scoreboard players set @s dz.prosba 0
        $scoreboard players add #k$(id) dz.k_czl 1
        $data modify storage dziobmc:tmp j set from storage dziobmc:kraje lista[{{id:$(id)}}]
        $execute unless score #k$(id) dz.k_wl matches 1 run return run function {NS}:kraje/wladca with storage dziobmc:tmp j
        function {NS}:kraje/wejdz_ogloszenie with storage dziobmc:tmp j
        function {NS}:gracz/druzyna
        playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.4
        function {NS}:kraje/info
    """)
    fn("kraje/wejdz_ogloszenie", """
        $tellraw @a [{"text":"✪ ","color":"aqua"},{"selector":"@s"},{"text":" dołączył do państwa ","color":"gray"},$(nj),{"text":"!","color":"gray"}]
    """)
    fn("kraje/wladca", f"""
        $scoreboard players set #k$(id) dz.k_wl 1
        tag @s add dz.wladca
        function {NS}:gracz/druzyna
        title @a times 10 60 20
        $title @a title [$(nj)]
        title @a subtitle [{{"selector":"@s"}},{{"text":" zostaje władcą!","color":"gold"}}]
        $tellraw @a [{{"text":"♛ ","color":"gold"}},{{"selector":"@s"}},{{"text":" zostaje WŁADCĄ państwa ","color":"yellow"}},$(nj),{{"text":"!","color":"yellow"}}]
        execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.7 1
        {firework_cmd()}
        function {NS}:kraje/info
    """)
    fn("kraje/prosba", f"""
        $scoreboard players set @s dz.prosba $(id)
        execute unless score @s dz.id matches 1.. run function {NS}:gracz/nadaj_id
        {tellraw("@s", t("✉ Granice tego państwa są zamknięte – wysłano prośbę do władcy.", "gray"))}
        execute store result storage dziobmc:tmp p.pid int 1 run scoreboard players get @s dz.id
        $data modify storage dziobmc:tmp p.id set value $(id)
        function {NS}:kraje/prosba_m with storage dziobmc:tmp p
    """)
    fn("kraje/prosba_m", """
        $tellraw @a[tag=dz.wladca,scores={dz.kid=$(id)}] [{"text":"✉ ","color":"aqua"},{"selector":"@s"},{"text":" prosi o dołączenie do państwa. ","color":"gray"},{"text":"[PRZYJMIJ]","color":"green","bold":true,"clickEvent":{"action":"run_command","value":"/trigger przyjmij set $(pid)"}}]
        $execute as @a[tag=dz.wladca,scores={dz.kid=$(id)}] at @s run playsound minecraft:block.note_block.bell master @s ~ ~ ~ 1 1.2
    """)
    fn("komendy/przyjmij", f"""
        execute unless entity @s[tag=dz.wladca] run return run scoreboard players set @s przyjmij 0
        scoreboard players operation #v dz.data = @s przyjmij
        scoreboard players operation #lk dz.data = @s dz.kid
        scoreboard players set @s przyjmij 0
        execute as @a[scores={{dz.prosba=1..}}] if score @s dz.id = #v dz.data if score @s dz.prosba = #lk dz.data at @s run function {NS}:kraje/wejdz_prosba
    """)
    fn("kraje/wejdz_prosba", f"""
        execute store result storage dziobmc:tmp j.id int 1 run scoreboard players get @s dz.prosba
        function {NS}:kraje/wejdz with storage dziobmc:tmp j
    """)

    # opuszczanie / rozwiązanie
    fn("kraje/opusc", f"""
        execute store result storage dziobmc:tmp o.id int 1 run scoreboard players get @s dz.kid
        function {NS}:kraje/opusc_m with storage dziobmc:tmp o
        tag @s remove dz.wladca
        scoreboard players set @s dz.kid 0
        scoreboard players set @s dz.kraj 0
        function {NS}:gracz/druzyna
    """)
    fn("kraje/opusc_m", f"""
        $data modify storage dziobmc:tmp o merge from storage dziobmc:kraje lista[{{id:$(id)}}]
        $scoreboard players remove #k$(id) dz.k_czl 1
        tellraw @a [{{"text":"✪ ","color":"aqua"}},{{"selector":"@s"}},{{"text":" opuścił państwo ","color":"gray"}},$(id_nj)]
        $execute if entity @s[tag=dz.wladca] run scoreboard players set #k$(id) dz.k_wl 0
        $execute if score #k$(id) dz.k_czl matches ..0 run return run function {NS}:kraje/rozwiaz with storage dziobmc:tmp o
        execute if entity @s[tag=dz.wladca] run tellraw @a [{{"text":"♛ Tron państwa ","color":"gold"}},$(id_nj),{{"text":" jest wolny! Mieszkańcy mogą go przejąć.","color":"gold"}}]
    """.replace("$(id_nj)", "{\"nbt\":\"o.nj\",\"storage\":\"dziobmc:tmp\",\"interpret\":true}"))
    fn("kraje/rozwiaz", f"""
        $tellraw @a [{{"text":"✖ Państwo ","color":"gray"}},$(nj),{{"text":" zostało rozwiązane (brak mieszkańców).","color":"gray"}}]
        $execute if score #k$(id) dz.k_wrog matches 1.. run function {NS}:kraje/rozwiaz_wojna {{id:$(id)}}
        $data remove storage dziobmc:kraje lista[{{id:$(id)}}]
        $scoreboard players reset #k$(id)
        $scoreboard players reset k$(kod)$(nn) dz.ranking
    """)
    fn("kraje/rozwiaz_wojna", """
        $execute store result storage dziobmc:tmp rw.w int 1 run scoreboard players get #k$(id) dz.k_wrog
        $data modify storage dziobmc:tmp rw.l set value $(id)
        function dziobmc:kraje/rozwiaz_wojna2 with storage dziobmc:tmp rw
    """)
    fn("kraje/rozwiaz_wojna2", """
        $scoreboard players set #k$(w) dz.k_wrog 0
        $scoreboard players set #k$(w) dz.k_wczas 0
        $scoreboard players add #k$(w) dz.k_wygr 1
    """)

    # przejęcie tronu, granice, przeniesienie stolicy, skarbiec
    fn("kraje/przejmij", f"""
        execute store result storage dziobmc:tmp o.id int 1 run scoreboard players get @s dz.kid
        function {NS}:kraje/przejmij_m with storage dziobmc:tmp o
    """)
    fn("kraje/przejmij_m", f"""
        $execute if score #k$(id) dz.k_wl matches 1 run return run tellraw @s {{"text":"✖ To państwo ma już władcę.","color":"red"}}
        $data modify storage dziobmc:tmp j set from storage dziobmc:kraje lista[{{id:$(id)}}]
        function {NS}:kraje/wladca with storage dziobmc:tmp j
    """)
    fn("kraje/granice", f"""
        execute store result storage dziobmc:tmp o.id int 1 run scoreboard players get @s dz.kid
        function {NS}:kraje/granice_m with storage dziobmc:tmp o
    """)
    fn("kraje/granice_m", """
        $execute if score #k$(id) dz.k_zamk matches 1 run return run function dziobmc:kraje/granice_otworz {id:$(id)}
        $scoreboard players set #k$(id) dz.k_zamk 1
        tellraw @s {"text":"✔ Granice zamknięte – nowi gracze muszą wysłać prośbę.","color":"yellow"}
    """)
    fn("kraje/granice_otworz", """
        $scoreboard players set #k$(id) dz.k_zamk 0
        tellraw @s {"text":"✔ Granice otwarte – każdy może dołączyć.","color":"green"}
    """)
    fn("kraje/przenies_stolice", f"""
        execute at @s unless dimension {SWIAT} run return run {tellraw("@s", t("✖ Stolicę można przenieść tylko na mapie Ziemi.", "red"))}
        {cooldown("dz.cd_przen", 72000)}
        execute store result storage dziobmc:tmp ps.id int 1 run scoreboard players get @s dz.kid
        execute store result storage dziobmc:tmp ps.x int 1 run data get entity @s Pos[0]
        execute store result storage dziobmc:tmp ps.z int 1 run data get entity @s Pos[2]
        execute store result score #x dz.data run data get entity @s Pos[0]
        execute store result score #z dz.data run data get entity @s Pos[2]
        scoreboard players remove #x dz.data {STREFA}
        scoreboard players remove #z dz.data {STREFA}
        execute store result storage dziobmc:tmp ps.x0 int 1 run scoreboard players get #x dz.data
        execute store result storage dziobmc:tmp ps.z0 int 1 run scoreboard players get #z dz.data
        function {NS}:kraje/przenies_m with storage dziobmc:tmp ps
        {tellraw("@s", t("✔ Stolica twojego państwa jest teraz tutaj! Strefa ochronna: 64 kratki.", "green", bold=True))}
        playsound minecraft:block.beacon.activate master @s ~ ~ ~ 1 1
    """)
    fn("kraje/przenies_m", """
        $data modify storage dziobmc:kraje lista[{id:$(id)}].x set value $(x)
        $data modify storage dziobmc:kraje lista[{id:$(id)}].z set value $(z)
        $data modify storage dziobmc:kraje lista[{id:$(id)}].x0 set value $(x0)
        $data modify storage dziobmc:kraje lista[{id:$(id)}].z0 set value $(z0)
    """)
    fn("komendy/skarbiec", f"""
        scoreboard players operation #v dz.data = @s skarbiec
        scoreboard players set @s skarbiec 0
        execute unless score @s dz.kid matches 1.. run return run {tellraw("@s", t("✖ Nie należysz do żadnego państwa.", "red"))}
        execute store result storage dziobmc:tmp s.id int 1 run scoreboard players get @s dz.kid
        execute if score #v dz.data matches 2.. unless score @s dz.coins >= #v dz.data run return run {tellraw("@s", t("✖ Masz za mało monet.", "red"))}
        execute if score #v dz.data matches 2.. run return run function {NS}:kraje/wplata with storage dziobmc:tmp s
        execute if score #v dz.data matches ..-1 unless entity @s[tag=dz.wladca] run return run {tellraw("@s", t("✖ Tylko władca może wypłacać ze skarbca.", "red"))}
        execute if score #v dz.data matches ..-1 run scoreboard players operation #v dz.data *= #m1 dz.data
        execute if score #v dz.data matches 1.. run function {NS}:kraje/wyplata with storage dziobmc:tmp s
    """)
    fn("kraje/wplata", """
        scoreboard players operation @s dz.coins -= #v dz.data
        $scoreboard players operation #k$(id) dz.k_skarb += #v dz.data
        $tellraw @a[scores={dz.kid=$(id)}] [{"text":"⛃ ","color":"gold"},{"selector":"@s"},{"text":" wpłacił ","color":"gray"},{"score":{"name":"#v","objective":"dz.data"},"color":"gold","bold":true},{"text":" monet do skarbca. Stan: ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_skarb"},"color":"yellow","bold":true}]
    """)
    fn("kraje/wyplata", """
        $execute if score #k$(id) dz.k_skarb < #v dz.data run return run tellraw @s {"text":"✖ W skarbcu jest za mało monet.","color":"red"}
        $scoreboard players operation #k$(id) dz.k_skarb -= #v dz.data
        scoreboard players operation @s dz.coins += #v dz.data
        $tellraw @a[scores={dz.kid=$(id)}] [{"text":"⛃ Władca ","color":"gold"},{"selector":"@s"},{"text":" wypłacił ","color":"gray"},{"score":{"name":"#v","objective":"dz.data"},"color":"gold","bold":true},{"text":" monet ze skarbca.","color":"gray"}]
    """)
    fn("kraje/do_skarbca", f"""
        # Dodaje #v monet do skarbca państwa gracza (@s)
        execute unless score @s dz.kid matches 1.. run return 0
        execute store result storage dziobmc:tmp s.id int 1 run scoreboard players get @s dz.kid
        function {NS}:kraje/do_skarbca_m with storage dziobmc:tmp s
    """)
    fn("kraje/do_skarbca_m", "$scoreboard players operation #k$(id) dz.k_skarb += #v dz.data")

    # info o własnym państwie
    fn("kraje/info", f"""
        execute store result storage dziobmc:tmp i.id int 1 run scoreboard players get @s dz.kid
        function {NS}:kraje/info_m with storage dziobmc:tmp i
    """)
    fn("kraje/info_m", f"""
        $data modify storage dziobmc:tmp i merge from storage dziobmc:kraje lista[{{id:$(id)}}]
        function {NS}:kraje/info_m2 with storage dziobmc:tmp i
    """)
    fn("kraje/info_m2", "\n".join([
        tellraw("@s", LIN),
        '$tellraw @s [{"text":"   ✪ ","color":"aqua"},$(nj),{"text":"   stolica: ","color":"gray"},{"text":"$(x) / $(z)","color":"white"}]',
        tellraw("@s", LIN),
        '$tellraw @s [{"text":" Mieszkańcy: ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_czl"},"color":"white","bold":true},{"text":"   Skarbiec: ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_skarb"},"color":"gold","bold":true},{"text":" ⛃   Wygrane wojny: ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_wygr"},"color":"red","bold":true}]',
        '$execute if score #k$(id) dz.k_wrog matches 1.. run tellraw @s [{"text":" ⚔ WOJNA! ","color":"dark_red","bold":true},{"text":"Punkty: ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_pkt"},"color":"yellow","bold":true},{"text":" (do 15)  Zostało: ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_wczas"},"color":"white"},{"text":" s","color":"gray"}]',
        '$execute if score #k$(id) dz.k_zamk matches 1 run tellraw @s [{"text":" Granice: ","color":"gray"},{"text":"ZAMKNIĘTE","color":"red","bold":true}]',
        '$execute unless score #k$(id) dz.k_zamk matches 1 run tellraw @s [{"text":" Granice: ","color":"gray"},{"text":"OTWARTE","color":"green","bold":true}]',
        tellraw("@s", t(" ➤ ", "dark_gray"), t("[STOLICA]", "green", bold=True, run="/trigger stolica set 1", hover=t("Teleport do stolicy")), t(" "),
                t("[WPŁAĆ 100]", "gold", bold=True, run="/trigger skarbiec set 100"), t(" "),
                t("[WPŁAĆ 1000]", "gold", bold=True, run="/trigger skarbiec set 1000"), t(" "),
                t("[RANKING]", "yellow", bold=True, run="/trigger panstwo set 2"), t(" "),
                t("[OPUŚĆ]", "red", run="/trigger panstwo set 999", hover=t("Opuść państwo", "red"))),
        "execute if entity @s[tag=dz.wladca] run " + tellraw("@s", t(" ♛ Władca: ", "gold", bold=True),
                                                              t("[GRANICE]", "aqua", run="/trigger panstwo set 997", hover=t("Otwórz/zamknij granice")), t(" "),
                                                              t("[STOLICA TUTAJ]", "green", run="/trigger panstwo set 996", hover=t("Przenieś stolicę w miejsce, w którym stoisz (co 1h)")), t(" "),
                                                              t("[WOJNA]", "dark_red", bold=True, run="/trigger wojna set 1"), t(" "),
                                                              t("[WYPŁAĆ 500]", "yellow", run="/trigger skarbiec set -500"), t(" "),
                                                              t("[KAPITULACJA]", "gray", run="/trigger wojna set 999")),
        '$execute if score #k$(id) dz.k_wl matches 0 run tellraw @s [{"text":" Tron jest wolny! ","color":"gold"},{"text":"[PRZEJMIJ WŁADZĘ]","color":"gold","bold":true,"clickEvent":{"action":"run_command","value":"/trigger panstwo set 998"}}]',
        tellraw("@s", LIN),
    ]))

    # ranking (lista na czacie + sidebar)
    fn("kraje/ranking", "\n".join([
        tellraw("@s", LIN), tellraw("@s", t("   ✪ ", "aqua"), t("RANKING PAŃSTW", "gold", bold=True), t("  (patrz też scoreboard)", "gray")), tellraw("@s", LIN),
        "scoreboard players set #lista_ile dz.data 0",
        "scoreboard players set #fk dz.data -1",
        "scoreboard players set #iter_tryb dz.data 5",
        f"function {NS}:kraje/iter_ranking",
        "execute if score #lista_ile dz.data matches 0 run " + tellraw("@s", t(" Nie ma jeszcze żadnych państw – załóż pierwsze!", "gray", italic=True)),
        tellraw("@s", LIN)]))
    fn("kraje/iter_ranking", f"""
        data modify storage dziobmc:tmp it set from storage dziobmc:kraje lista
        function {NS}:kraje/iter_ranking_krok
    """)
    fn("kraje/iter_ranking_krok", f"""
        execute unless data storage dziobmc:tmp it[0] run return 0
        function {NS}:kraje/wiersz_rankingu with storage dziobmc:tmp it[0]
        data remove storage dziobmc:tmp it[0]
        function {NS}:kraje/iter_ranking_krok
    """)
    fn("kraje/wiersz_rankingu", """
        scoreboard players add #lista_ile dz.data 1
        $tellraw @s [{"text":" • ","color":"dark_gray"},$(nj),{"text":"  ☺ ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_czl"},"color":"white"},{"text":"  ⛃ ","color":"gold"},{"score":{"name":"#k$(id)","objective":"dz.k_skarb"},"color":"yellow"},{"text":"  ⚔ ","color":"red"},{"score":{"name":"#k$(id)","objective":"dz.k_wygr"},"color":"white"}]
    """)
    fn("kraje/na_ranking", """
        $scoreboard players operation #p dz.data = #k$(id) dz.k_czl
        scoreboard players operation #p dz.data *= #100 dz.data
        $scoreboard players operation #q dz.data = #k$(id) dz.k_skarb
        scoreboard players operation #q dz.data /= #10 dz.data
        scoreboard players operation #p dz.data += #q dz.data
        $scoreboard players operation #q dz.data = #k$(id) dz.k_wygr
        scoreboard players operation #q dz.data *= #500 dz.data
        scoreboard players operation #p dz.data += #q dz.data
        $scoreboard players operation k$(kod)$(nn) dz.ranking = #p dz.data
        $scoreboard players display name k$(kod)$(nn) dz.ranking $(nj)
        scoreboard players add #ile_kr dz.data 1
    """)
    fn("ziemia/ranking", f"""
        scoreboard players set #ile_kr dz.data 0
        scoreboard players set #iter_tryb dz.data 2
        function {NS}:kraje/iter
        scoreboard players add #sb dz.data 1
        execute if score #sb dz.data matches 2.. run scoreboard players set #sb dz.data 0
        execute if score #sb dz.data matches 1 if score #ile_kr dz.data matches 1.. run scoreboard objectives setdisplay sidebar dz.ranking
        execute unless score #sb dz.data matches 1 run scoreboard objectives setdisplay sidebar dz.sidebar
        execute unless score #ile_kr dz.data matches 1.. run scoreboard objectives setdisplay sidebar dz.sidebar
    """)

    # ---------------------------------------------------------------- /trigger panstwo – rozdzielnik
    pan = ["# /trigger panstwo: 1 menu, 2 ranking, 100+K kraj K, 20000K załóż państwo kraju K, ID>=1001 dołącz, 996 stolica tutaj, 997 granice, 998 tron, 999 opuść",
           "scoreboard players operation #v dz.data = @s panstwo",
           "scoreboard players set @s panstwo 0",
           f"execute if score #v dz.data matches 1 if score @s dz.kid matches 1.. run function {NS}:kraje/info",
           f"execute if score #v dz.data matches 1 unless score @s dz.kid matches 1.. run function {NS}:kraje/menu_wybor",
           f"execute if score #v dz.data matches 2 run function {NS}:kraje/ranking",
           f"execute if score #v dz.data matches 996 if entity @s[tag=dz.wladca] run function {NS}:kraje/przenies_stolice",
           f"execute if score #v dz.data matches 997 if entity @s[tag=dz.wladca] run function {NS}:kraje/granice",
           f"execute if score #v dz.data matches 998 if score @s dz.kid matches 1.. run function {NS}:kraje/przejmij",
           f"execute if score #v dz.data matches 999 if score @s dz.kid matches 1.. run function {NS}:kraje/opusc",
           f"execute if score #v dz.data matches 1001..99999 run function {NS}:kraje/dolacz"]
    for k in KRAJE:
        pan.append(f"execute if score #v dz.data matches {100 + k[0]} run function {NS}:kraje/kraj/{k[0]}")
        pan.append(f"execute if score #v dz.data matches {200000 + k[0]} run scoreboard players set #k dz.data {k[0]}")
    pan.append(f"execute if score #v dz.data matches 200001..200999 run function {NS}:kraje/zaloz")
    fn("komendy/panstwo", "\n".join(pan))

    # ---------------------------------------------------------------- stolica własnego państwa
    fn("kraje/tp_wlasna", f"""
        {cooldown("dz.cd_stol", 600)}
        execute store result storage dziobmc:tmp t.id int 1 run scoreboard players get @s dz.kid
        function {NS}:kraje/tp_wlasna_m with storage dziobmc:tmp t
    """)
    fn("kraje/tp_wlasna_m", f"""
        $data modify storage dziobmc:tmp t merge from storage dziobmc:kraje lista[{{id:$(id)}}]
        function {NS}:kraje/tp_wlasna_m2 with storage dziobmc:tmp t
    """)
    fn("kraje/tp_wlasna_m2", f"""
        $tellraw @s [{{"text":"✈ Lecisz do stolicy państwa ","color":"aqua"}},$(nj)]
        $function {NS}:ziemia/tp_m {{x:$(x),z:$(z)}}
    """)

    # ---------------------------------------------------------------- co sekundę: strefy stolic + wojny
    fn("ziemia/strefy", f"""
        tag @a remove dz.strefa_obca
        scoreboard players set @a dz.mojwrog 0
        execute as @a[scores={{dz.kid=1..}}] run function {NS}:kraje/mojwrog
        scoreboard players set #iter_tryb dz.data 1
        function {NS}:kraje/iter
        gamemode adventure @a[tag=dz.strefa_obca,gamemode=survival,tag=!dz.build]
        execute as @a[tag=dz.strefa_obca,tag=!dz.strefa_bylo] run {tellraw("@s", t("⛨ Wchodzisz do chronionej stolicy obcego państwa – nie możesz tu niszczyć bloków.", "gold"))}
        tag @a[tag=dz.strefa_obca] add dz.strefa_bylo
        gamemode survival @a[tag=!dz.strefa_obca,tag=dz.strefa_bylo,tag=!dz.lobby,gamemode=adventure,tag=!dz.build]
        tag @a[tag=!dz.strefa_obca] remove dz.strefa_bylo
    """)
    fn("kraje/mojwrog", f"""
        execute store result storage dziobmc:tmp mw.id int 1 run scoreboard players get @s dz.kid
        function {NS}:kraje/mojwrog_m with storage dziobmc:tmp mw
    """)
    fn("kraje/mojwrog_m", "$scoreboard players operation @s dz.mojwrog = #k$(id) dz.k_wrog")
    fn("kraje/na_sekunde", f"""
        $execute in {SWIAT} as @a[x=$(x0),y=-64,z=$(z0),dx={2 * STREFA},dy=400,dz={2 * STREFA}] unless score @s dz.kid matches $(id) unless score @s dz.mojwrog matches $(id) run tag @s add dz.strefa_obca
        $execute if score #k$(id) dz.k_pokoj matches 1.. run scoreboard players remove #k$(id) dz.k_pokoj 1
        $execute if score #k$(id) dz.k_wrog matches 1.. run function {NS}:wojna/tik {{id:$(id)}}
    """)
    fn("wojna/sekunda", "# wojny liczone są w kraje/na_sekunde (iterator)")

    # ---------------------------------------------------------------- wojny
    fn("wojna/menu", "\n".join([
        f"execute unless entity @s[tag=dz.wladca] run return run " + tellraw("@s", t("✖ Tylko władca państwa może wypowiadać wojny.", "red")),
        tellraw("@s", LIN), tellraw("@s", t("   ⚔ ", "dark_red"), t("WYPOWIEDZ WOJNĘ", "red", bold=True)), tellraw("@s", LIN),
        tellraw("@s", t(" Wojna trwa 30 min. Punkt = zabicie wroga. Do 15 pkt. Zwycięzca bierze 30% skarbca wroga!", "gray")),
        "scoreboard players operation #fk dz.data = @s dz.kid",
        "scoreboard players set #iter_tryb dz.data 4",
        f"function {NS}:kraje/iter",
        tellraw("@s", LIN)]))
    fn("kraje/na_wojne", """
        $execute if score #fk dz.data matches $(id) run return 0
        $tellraw @s [{"text":" ⚔ ","color":"dark_red"},$(nj),{"text":"  ☺ ","color":"gray"},{"score":{"name":"#k$(id)","objective":"dz.k_czl"},"color":"white"},{"text":"  "},{"text":"[WYPOWIEDZ WOJNĘ]","color":"red","bold":true,"clickEvent":{"action":"run_command","value":"/trigger wojna set $(id)"}}]
    """)
    fn("komendy/wojna", f"""
        scoreboard players operation #v dz.data = @s wojna
        scoreboard players set @s wojna 0
        execute if score #v dz.data matches 1 run function {NS}:wojna/menu
        execute if score #v dz.data matches 999 if entity @s[tag=dz.wladca] run function {NS}:wojna/kapitulacja
        execute if score #v dz.data matches 1001.. if entity @s[tag=dz.wladca] run function {NS}:wojna/wypowiedz_v
    """)
    fn("wojna/wypowiedz_v", f"""
        execute if score #v dz.data = @s dz.kid run return run {tellraw("@s", t("✖ Nie możesz wypowiedzieć wojny samemu sobie.", "red"))}
        execute store result storage dziobmc:tmp w.a int 1 run scoreboard players get @s dz.kid
        execute store result storage dziobmc:tmp w.b int 1 run scoreboard players get #v dz.data
        function {NS}:wojna/nazwy with storage dziobmc:tmp w
        function {NS}:wojna/wypowiedz with storage dziobmc:tmp w
    """)
    fn("wojna/nazwy", f"""
        $execute unless data storage dziobmc:kraje lista[{{id:$(b)}}] run return run tellraw @s {{"text":"✖ To państwo nie istnieje.","color":"red"}}
        $data modify storage dziobmc:tmp w.na set from storage dziobmc:kraje lista[{{id:$(a)}}].nj
        $data modify storage dziobmc:tmp w.nb set from storage dziobmc:kraje lista[{{id:$(b)}}].nj
    """)
    fn("wojna/wypowiedz", f"""
        $execute unless data storage dziobmc:kraje lista[{{id:$(b)}}] run return 0
        $execute if score #k$(a) dz.k_wrog matches 1.. run return run tellraw @s {{"text":"✖ Twoje państwo już prowadzi wojnę.","color":"red"}}
        $execute if score #k$(b) dz.k_wrog matches 1.. run return run tellraw @s {{"text":"✖ To państwo prowadzi już inną wojnę.","color":"red"}}
        $execute if score #k$(a) dz.k_pokoj matches 1.. run return run tellraw @s {{"text":"✖ Trwa rozejm po ostatniej wojnie (30 min).","color":"red"}}
        $execute unless score #k$(b) dz.k_czl matches 1.. run return run tellraw @s {{"text":"✖ To państwo nie ma mieszkańców.","color":"red"}}
        $scoreboard players set #k$(a) dz.k_wrog $(b)
        $scoreboard players set #k$(b) dz.k_wrog $(a)
        $scoreboard players set #k$(a) dz.k_pkt 0
        $scoreboard players set #k$(b) dz.k_pkt 0
        $scoreboard players set #k$(a) dz.k_wczas 1800
        $scoreboard players set #k$(b) dz.k_wczas 1800
        title @a times 10 70 20
        title @a title [{{"text":"⚔ WOJNA! ⚔","color":"dark_red","bold":true}}]
        $title @a subtitle [$(na),{{"text":" wypowiada wojnę ","color":"gray"}},$(nb)]
        $tellraw @a [{{"text":"⚔ ","color":"dark_red"}},$(na),{{"text":" wypowiada wojnę państwu ","color":"gray"}},$(nb),{{"text":"! 30 minut, do 15 punktów. Zwycięzca bierze 30% skarbca wroga!","color":"gray"}}]
        execute as @a at @s run playsound minecraft:event.raid.horn master @s ~ ~ ~ 1 1
    """)
    # punkty: jeden advancement – ofiarę rozpoznajemy po zdrowiu 0 w pobliżu
    jfile(f"data/{NS}/advancement/wojna/zabojstwo.json", {
        "criteria": {"zabicie": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "minecraft:player"}}]}}},
        "rewards": {"function": f"{NS}:wojna/zabojstwo"}})
    fn("wojna/zabojstwo", f"""
        advancement revoke @s only {NS}:wojna/zabojstwo
        execute unless score @s dz.kid matches 1.. run return 0
        scoreboard players set #ofiara dz.data 0
        execute as @a[distance=..96,nbt={{Health:0.0f}},sort=nearest,limit=1] run scoreboard players operation #ofiara dz.data = @s dz.kid
        execute unless score #ofiara dz.data matches 1.. run return 0
        execute store result storage dziobmc:tmp z.a int 1 run scoreboard players get @s dz.kid
        execute store result storage dziobmc:tmp z.b int 1 run scoreboard players get #ofiara dz.data
        function {NS}:wojna/punkt with storage dziobmc:tmp z
    """)
    fn("wojna/punkt", f"""
        $execute unless score #k$(a) dz.k_wrog matches $(b) run return 0
        $scoreboard players add #k$(a) dz.k_pkt 1
        $tellraw @a[scores={{dz.kid=$(a)}}] [{{"text":"⚔ +1 punkt wojenny! Wynik: ","color":"gold"}},{{"score":{{"name":"#k$(a)","objective":"dz.k_pkt"}},"color":"green","bold":true}},{{"text":" : ","color":"gray"}},{{"score":{{"name":"#k$(b)","objective":"dz.k_pkt"}},"color":"red","bold":true}}]
        $tellraw @a[scores={{dz.kid=$(b)}}] [{{"text":"⚔ Wróg zdobywa punkt! Wynik: ","color":"red"}},{{"score":{{"name":"#k$(b)","objective":"dz.k_pkt"}},"color":"green","bold":true}},{{"text":" : ","color":"gray"}},{{"score":{{"name":"#k$(a)","objective":"dz.k_pkt"}},"color":"red","bold":true}}]
        $execute if score #k$(a) dz.k_pkt matches 15.. run function {NS}:wojna/koniec {{a:$(a),b:$(b)}}
    """)
    fn("wojna/tik", f"""
        $scoreboard players remove #k$(id) dz.k_wczas 1
        $execute unless score #k$(id) dz.k_wczas matches ..0 run return 0
        $execute store result storage dziobmc:tmp k.b int 1 run scoreboard players get #k$(id) dz.k_wrog
        $data modify storage dziobmc:tmp k.a set value $(id)
        function {NS}:wojna/koniec with storage dziobmc:tmp k
    """)
    fn("wojna/koniec", f"""
        $execute store result score #pa dz.data run scoreboard players get #k$(a) dz.k_pkt
        $execute store result score #pb dz.data run scoreboard players get #k$(b) dz.k_pkt
        $data modify storage dziobmc:tmp e1 set value {{w:$(a),l:$(b)}}
        $data modify storage dziobmc:tmp e2 set value {{w:$(b),l:$(a)}}
        function {NS}:wojna/e_nazwy_m with storage dziobmc:tmp e1
        execute if score #pa dz.data > #pb dz.data run function {NS}:wojna/wygrana with storage dziobmc:tmp e1
        execute if score #pb dz.data > #pa dz.data run function {NS}:wojna/wygrana with storage dziobmc:tmp e2
        execute if score #pa dz.data = #pb dz.data run function {NS}:wojna/remis with storage dziobmc:tmp e1
        $function {NS}:wojna/reset {{a:$(a),b:$(b)}}
    """)
    fn("wojna/e_nazwy_m", """
        $data modify storage dziobmc:tmp e1.nw set from storage dziobmc:kraje lista[{id:$(w)}].nj
        $data modify storage dziobmc:tmp e1.nl set from storage dziobmc:kraje lista[{id:$(l)}].nj
        $data modify storage dziobmc:tmp e2.nw set from storage dziobmc:kraje lista[{id:$(l)}].nj
        $data modify storage dziobmc:tmp e2.nl set from storage dziobmc:kraje lista[{id:$(w)}].nj
    """)
    fn("wojna/wygrana", f"""
        $scoreboard players operation #lup dz.data = #k$(l) dz.k_skarb
        scoreboard players operation #lup dz.data *= #3 dz.data
        scoreboard players operation #lup dz.data /= #10 dz.data
        $scoreboard players operation #k$(l) dz.k_skarb -= #lup dz.data
        $scoreboard players operation #k$(w) dz.k_skarb += #lup dz.data
        $scoreboard players add #k$(w) dz.k_wygr 1
        title @a times 10 80 20
        $title @a title [$(nw)]
        $title @a subtitle [{{"text":"wygrywa wojnę z ","color":"gold"}},$(nl),{{"text":"!","color":"gold"}}]
        $tellraw @a [{{"text":"♛ ","color":"gold"}},$(nw),{{"text":" WYGRYWA WOJNĘ z ","color":"gold","bold":true}},$(nl),{{"text":" i zdobywa ","color":"gray"}},{{"score":{{"name":"#lup","objective":"dz.data"}},"color":"yellow","bold":true}},{{"text":" monet ze skarbca wroga!","color":"gray"}}]
        $execute as @a[scores={{dz.kid=$(w)}}] at @s run {firework_cmd()}
        execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
    """)
    fn("wojna/remis", """
        $tellraw @a [{"text":"⚔ Wojna ","color":"gray"},$(nw),{"text":" – ","color":"gray"},$(nl),{"text":" kończy się REMISEM.","color":"yellow","bold":true}]
    """)
    fn("wojna/reset", """
        $scoreboard players set #k$(a) dz.k_wrog 0
        $scoreboard players set #k$(b) dz.k_wrog 0
        $scoreboard players set #k$(a) dz.k_wczas 0
        $scoreboard players set #k$(b) dz.k_wczas 0
        $scoreboard players set #k$(a) dz.k_pokoj 1800
        $scoreboard players set #k$(b) dz.k_pokoj 1800
    """)
    fn("wojna/kapitulacja", f"""
        execute store result storage dziobmc:tmp c.l int 1 run scoreboard players get @s dz.kid
        function {NS}:wojna/kapitulacja_m with storage dziobmc:tmp c
    """)
    fn("wojna/kapitulacja_m", f"""
        $execute unless score #k$(l) dz.k_wrog matches 1.. run return run tellraw @s {{"text":"✖ Twoje państwo nie prowadzi wojny.","color":"red"}}
        $execute store result storage dziobmc:tmp c.w int 1 run scoreboard players get #k$(l) dz.k_wrog
        tellraw @a [{{"text":"⚑ ","color":"white"}},{{"text":"Państwo kapituluje!","color":"gray"}}]
        function {NS}:wojna/kapitulacja_m2 with storage dziobmc:tmp c
    """)
    fn("wojna/kapitulacja_m2", f"""
        $scoreboard players set #k$(w) dz.k_pkt 15
        $scoreboard players set #k$(l) dz.k_pkt 0
        $function {NS}:wojna/koniec {{a:$(w),b:$(l)}}
    """)
