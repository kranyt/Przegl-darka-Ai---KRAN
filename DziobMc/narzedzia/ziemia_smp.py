"""Earth SMP: państwa, władcy, skarbce, wojny, stolice, teleporty po mapie Ziemi (świat minecraft:ziemia)."""
from wspolne import NS, J, t, sc, sel, tellraw, fn, jfile, snbt_text, firework_cmd, cooldown
from rdzen import RANGI, prefix

SWIAT = "minecraft:ziemia"
STREFA = 64          # promień chronionej strefy stolicy (kratki)

# id, nazwa, kod, kolor, stolica, szer., dł., kontynent
KRAJE = [
    (1, "Polska", "POL", "red", "Warszawa", 52.23, 21.01, "Europa"),
    (2, "Niemcy", "GER", "dark_gray", "Berlin", 52.52, 13.40, "Europa"),
    (3, "Francja", "FRA", "blue", "Paryż", 48.86, 2.35, "Europa"),
    (4, "Wielka Brytania", "GBR", "dark_blue", "Londyn", 51.51, -0.13, "Europa"),
    (5, "Hiszpania", "ESP", "gold", "Madryt", 40.42, -3.70, "Europa"),
    (6, "Włochy", "ITA", "green", "Rzym", 41.90, 12.50, "Europa"),
    (7, "Ukraina", "UKR", "yellow", "Kijów", 50.45, 30.52, "Europa"),
    (8, "Rosja", "RUS", "white", "Moskwa", 55.76, 37.62, "Europa"),
    (9, "Szwecja", "SWE", "aqua", "Sztokholm", 59.33, 18.07, "Europa"),
    (10, "Norwegia", "NOR", "dark_red", "Oslo", 59.91, 10.75, "Europa"),
    (11, "Finlandia", "FIN", "white", "Helsinki", 60.17, 24.94, "Europa"),
    (12, "Czechy", "CZE", "blue", "Praga", 50.08, 14.44, "Europa"),
    (13, "Słowacja", "SVK", "blue", "Bratysława", 48.15, 17.11, "Europa"),
    (14, "Litwa", "LTU", "yellow", "Wilno", 54.69, 25.28, "Europa"),
    (15, "Austria", "AUT", "red", "Wiedeń", 48.21, 16.37, "Europa"),
    (16, "Szwajcaria", "CHE", "red", "Berno", 46.95, 7.45, "Europa"),
    (17, "Holandia", "NLD", "gold", "Amsterdam", 52.37, 4.90, "Europa"),
    (18, "Węgry", "HUN", "dark_green", "Budapeszt", 47.50, 19.04, "Europa"),
    (19, "Rumunia", "ROU", "yellow", "Bukareszt", 44.43, 26.10, "Europa"),
    (20, "Grecja", "GRC", "aqua", "Ateny", 37.98, 23.73, "Europa"),
    (21, "Portugalia", "PRT", "dark_green", "Lizbona", 38.72, -9.14, "Europa"),
    (22, "Turcja", "TUR", "red", "Ankara", 39.93, 32.86, "Azja"),
    (23, "Islandia", "ISL", "blue", "Reykjavik", 64.15, -21.94, "Europa"),
    (24, "Dania", "DNK", "red", "Kopenhaga", 55.68, 12.57, "Europa"),
    (25, "USA", "USA", "blue", "Waszyngton", 38.90, -77.04, "Ameryka Płn."),
    (26, "Kanada", "CAN", "red", "Ottawa", 45.42, -75.70, "Ameryka Płn."),
    (27, "Meksyk", "MEX", "dark_green", "Meksyk", 19.43, -99.13, "Ameryka Płn."),
    (28, "Kuba", "CUB", "blue", "Hawana", 23.11, -82.37, "Ameryka Płn."),
    (29, "Brazylia", "BRA", "green", "Brasília", -15.79, -47.88, "Ameryka Płd."),
    (30, "Argentyna", "ARG", "aqua", "Buenos Aires", -34.60, -58.38, "Ameryka Płd."),
    (31, "Chile", "CHL", "red", "Santiago", -33.45, -70.67, "Ameryka Płd."),
    (32, "Peru", "PER", "dark_red", "Lima", -12.05, -77.04, "Ameryka Płd."),
    (33, "Kolumbia", "COL", "yellow", "Bogota", 4.71, -74.07, "Ameryka Płd."),
    (34, "Wenezuela", "VEN", "gold", "Caracas", 10.48, -66.90, "Ameryka Płd."),
    (35, "Egipt", "EGY", "gold", "Kair", 30.04, 31.24, "Afryka"),
    (36, "Maroko", "MAR", "dark_red", "Rabat", 34.02, -6.84, "Afryka"),
    (37, "Algieria", "DZA", "dark_green", "Algier", 36.75, 3.06, "Afryka"),
    (38, "Nigeria", "NGA", "green", "Abudża", 9.06, 7.49, "Afryka"),
    (39, "Kenia", "KEN", "dark_red", "Nairobi", -1.29, 36.82, "Afryka"),
    (40, "Etiopia", "ETH", "yellow", "Addis Abeba", 9.03, 38.74, "Afryka"),
    (41, "RPA", "ZAF", "dark_green", "Pretoria", -25.75, 28.19, "Afryka"),
    (42, "Madagaskar", "MDG", "red", "Antananarywa", -18.88, 47.51, "Afryka"),
    (43, "Arabia Saudyjska", "SAU", "dark_green", "Rijad", 24.71, 46.68, "Azja"),
    (44, "Iran", "IRN", "green", "Teheran", 35.69, 51.39, "Azja"),
    (45, "Indie", "IND", "gold", "Nowe Delhi", 28.61, 77.21, "Azja"),
    (46, "Chiny", "CHN", "red", "Pekin", 39.90, 116.41, "Azja"),
    (47, "Japonia", "JPN", "white", "Tokio", 35.68, 139.69, "Azja"),
    (48, "Korea Płd.", "KOR", "blue", "Seul", 37.57, 126.98, "Azja"),
    (49, "Mongolia", "MNG", "red", "Ułan Bator", 47.89, 106.91, "Azja"),
    (50, "Kazachstan", "KAZ", "aqua", "Astana", 51.17, 71.45, "Azja"),
    (51, "Indonezja", "IDN", "red", "Dżakarta", -6.21, 106.85, "Azja"),
    (52, "Tajlandia", "THA", "blue", "Bangkok", 13.76, 100.50, "Azja"),
    (53, "Wietnam", "VNM", "red", "Hanoi", 21.03, 105.85, "Azja"),
    (54, "Filipiny", "PHL", "blue", "Manila", 14.60, 120.98, "Azja"),
    (55, "Australia", "AUS", "dark_blue", "Canberra", -35.28, 149.13, "Oceania"),
    (56, "Nowa Zelandia", "NZL", "dark_aqua", "Wellington", -41.29, 174.78, "Oceania"),
]
N = len(KRAJE)
KONTYNENTY = ["Europa", "Azja", "Afryka", "Ameryka Płn.", "Ameryka Płd.", "Oceania"]

TRIGGERY_ZIEMIA = ["panstwo", "stolica", "skarbiec", "wojna", "przyjmij", "ziemia", "gdzie"]
OBIEKTY = ["dz.kraj", "dz.id", "dz.prosba", "dz.rid", "dz.mojwrog", "dz.k_czl", "dz.k_skarb", "dz.k_wl",
           "dz.k_zamk", "dz.k_wrog", "dz.k_pkt", "dz.k_wczas", "dz.k_wygr", "dz.k_pokoj", "dz.cd_stol", "dz.kc"]


def nazwa(k, bold=True):
    return t(k[1], k[3], bold=bold)


def tag_kraju(k):
    return [t("[", "dark_gray"), t(k[2], k[3], bold=True), t("] ", "dark_gray")]


def build():
    # ---------------------------------------------------------------- obiekty i dane
    dz = ["# Earth SMP – inicjalizacja"]
    dz += [f"scoreboard objectives add {o} dummy" for o in OBIEKTY]
    dz += [f"scoreboard objectives add {tr} trigger" for tr in TRIGGERY_ZIEMIA]
    dz += ["scoreboard objectives add dz.ranking dummy " + J([t("🌍 ", "aqua"), t("Potęga państw", "gold", bold=True)]).replace("🌍", "✪")]
    dz += ["execute unless score #skala dz.data matches 1.. run scoreboard players set #skala dz.data 2000",
           "scoreboard players set #11132 dz.data 11132", "scoreboard players set #m11132 dz.data -11132",
           "scoreboard players set #1113 dz.data 1113", "scoreboard players set #111320 dz.data 111320",
           "scoreboard players set #40075200 dz.data 40075200", "scoreboard players set #30 dz.data 30",
           "scoreboard players set #500 dz.data 500", "scoreboard players set #1000 dz.data 1000",
           "scoreboard players set #m1 dz.data -1"]
    for k in KRAJE:
        dz.append(f"scoreboard players add #k{k[0]} dz.k_czl 0")
        for o in ["dz.k_skarb", "dz.k_wl", "dz.k_zamk", "dz.k_wrog", "dz.k_pkt", "dz.k_wczas", "dz.k_wygr", "dz.k_pokoj"]:
            dz.append(f"scoreboard players add #k{k[0]} {o} 0")
        dz.append(f"data modify storage dziobmc:kraje n.k{k[0]} set value {snbt_text(nazwa(k))}")
        dz.append(f"scoreboard players display name k{k[2]} dz.ranking {J([t(k[2] + ' ', 'dark_gray'), nazwa(k, False)])}")
    dz += [f"function {NS}:ziemia/przelicz", f"function {NS}:ziemia/druzyny"]
    fn("ziemia/init", "\n".join(dz))

    # współrzędne stolic dla bieżącej skali
    pr = ["# Liczy współrzędne stolic i granicę świata dla skali #skala (1 kratka = #skala m)",
          "scoreboard players operation #s10 dz.data = #skala dz.data",
          "scoreboard players operation #s10 dz.data *= #10 dz.data"]
    for k in KRAJE:
        i, lat, lon = k[0], round(k[5] * 100), round(k[6] * 100)
        pr += [f"scoreboard players set #x dz.data {lon}",
               "scoreboard players operation #x dz.data *= #11132 dz.data",
               "scoreboard players operation #x dz.data /= #s10 dz.data",
               f"scoreboard players set #z dz.data {lat}",
               "scoreboard players operation #z dz.data *= #m11132 dz.data",
               "scoreboard players operation #z dz.data /= #s10 dz.data",
               f"execute store result storage dziobmc:kraje s.k{i}.x int 1 run scoreboard players get #x dz.data",
               f"execute store result storage dziobmc:kraje s.k{i}.z int 1 run scoreboard players get #z dz.data",
               f"scoreboard players remove #x dz.data {STREFA}", f"scoreboard players remove #z dz.data {STREFA}",
               f"execute store result storage dziobmc:kraje s.k{i}.x0 int 1 run scoreboard players get #x dz.data",
               f"execute store result storage dziobmc:kraje s.k{i}.z0 int 1 run scoreboard players get #z dz.data",
               f"data modify storage dziobmc:kraje s.k{i}.i set value {i}",
               f"scoreboard players operation #sx{i} dz.data = #x dz.data",
               f"scoreboard players add #sx{i} dz.data {STREFA}",
               f"scoreboard players operation #sz{i} dz.data = #z dz.data",
               f"scoreboard players add #sz{i} dz.data {STREFA}"]
    pr += ["scoreboard players operation #wb dz.data = #40075200 dz.data",
           "scoreboard players operation #wb dz.data /= #skala dz.data",
           "execute store result storage dziobmc:tmp g.wb int 1 run scoreboard players get #wb dz.data",
           f"function {NS}:ziemia/granica with storage dziobmc:tmp g"]
    fn("ziemia/przelicz", "\n".join(pr))
    fn("ziemia/granica", f"""
        execute in {SWIAT} run worldborder center 0 0
        $execute in {SWIAT} run worldborder set $(wb)
    """)
    for s in [1000, 2000, 4000, 8000]:
        fn(f"ziemia/skala/{s}", f"""
            # Ustaw tę samą skalę co w plugins/DziobEarth/config.yml
            scoreboard players set #skala dz.data {s}
            function {NS}:ziemia/przelicz
            {tellraw("@s", t(f"✔ Skala mapy Ziemi ustawiona na 1:{s}", "green", bold=True))}
        """)

    # ---------------------------------------------------------------- drużyny: ranga × państwo (prefiksy w TAB i czacie)
    dr = ["# Drużyny r<ranga>k<państwo> – kolejność w TAB: najpierw ranga"]
    for ri, (rid, team, lvl, pre, col, staff) in enumerate(RANGI):
        for k in [None] + KRAJE:
            kid = 0 if k is None else k[0]
            name = f"r{ri}k{kid}"
            px = prefix(pre) + ([] if k is None else tag_kraju(k))
            dr += [f"team add {name}", f"team modify {name} prefix {J(px)}", f"team modify {name} color {col}",
                   f"team modify {name} collisionRule never", f"team modify {name} friendlyFire true"]
    # migracja ze starych drużyn rang
    for ri, (rid, team, *_r) in enumerate(RANGI):
        dr.append(f"scoreboard players set @a[team={team}] dz.rid {ri}")
        dr.append(f"team remove {team}")
    fn("ziemia/druzyny", "\n".join(dr))
    fn("gracz/druzyna", f"""
        # Wpisuje gracza do drużyny r<ranga>k<państwo>
        execute unless score @s dz.rid matches 0.. run scoreboard players set @s dz.rid {len(RANGI) - 1}
        scoreboard players add @s dz.kraj 0
        execute store result storage dziobmc:tmp d.r int 1 run scoreboard players get @s dz.rid
        execute store result storage dziobmc:tmp d.k int 1 run scoreboard players get @s dz.kraj
        function {NS}:gracz/druzyna_m with storage dziobmc:tmp d
    """)
    fn("gracz/druzyna_m", "$team join r$(r)k$(k) @s")

    # ---------------------------------------------------------------- ID gracza (do próśb o dołączenie)
    fn("gracz/nadaj_id", """
        scoreboard players add #nast_id dz.data 1
        scoreboard players operation @s dz.id = #nast_id dz.data
    """)

    # ---------------------------------------------------------------- menu /trigger panstwo
    LIN = t("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "aqua", bold=True)
    menu_brak = [tellraw("@s", LIN), tellraw("@s", t("   ✪ ", "aqua"), t("WYBIERZ PAŃSTWO", "gold", bold=True), t("  (kliknij nazwę, aby dołączyć)", "gray")), tellraw("@s", LIN)]
    for kont in KONTYNENTY:
        czesci = [t(f" {kont}: ", "yellow", bold=True)]
        for k in [k for k in KRAJE if k[7] == kont]:
            czesci += [t(k[1], k[3], run=f"/trigger panstwo set {100 + k[0]}",
                         hover=[t(k[1], k[3], bold=True), t(f"\nStolica: {k[4]}\nKliknij, aby dołączyć", "gray")]), t(" • ", "dark_gray")]
        menu_brak.append(tellraw("@s", *czesci[:-1]))
    menu_brak += [tellraw("@s", t(" Pierwszy gracz w państwie zostaje jego ", "gray"), t("WŁADCĄ", "gold", bold=True), t("!", "gray")),
                  tellraw("@s", t(" ➤ ", "dark_gray"), t("[RANKING PAŃSTW]", "yellow", bold=True, run="/trigger panstwo set 2"), t("  "),
                          t("[LOSOWY TP NA ZIEMI]", "green", bold=True, run="/trigger ziemia set 11")),
                  tellraw("@s", LIN)]
    fn("kraje/menu_wybor", "\n".join(menu_brak))

    for k in KRAJE:
        i = k[0]
        fn(f"kraje/info/{i}", "\n".join([
            tellraw("@s", LIN),
            tellraw("@s", t("   ✪ ", "aqua"), nazwa(k), t(f"  •  stolica: {k4(k)}", "gray")),
            tellraw("@s", LIN),
            tellraw("@s", t(" Mieszkańcy: ", "gray"), sc(f"#k{i}", "dz.k_czl", "white", True), t("   Skarbiec: ", "gray"), sc(f"#k{i}", "dz.k_skarb", "gold", True), t(" ⛃   Wygrane wojny: ", "gray"), sc(f"#k{i}", "dz.k_wygr", "red", True)),
            f"execute if score #k{i} dz.k_wrog matches 1.. run " + tellraw("@s", t(" ⚔ WOJNA! ", "dark_red", bold=True), t("Punkty: ", "gray"), sc(f"#k{i}", "dz.k_pkt", "yellow", True), t("  (do 15)   Zostało: ", "gray"), sc(f"#k{i}", "dz.k_wczas", "white"), t(" s", "gray")),
            f"execute if score #k{i} dz.k_zamk matches 1 run " + tellraw("@s", t(" Granice: ", "gray"), t("ZAMKNIĘTE", "red", bold=True), t(" (nowi wysyłają prośby)", "gray")),
            f"execute unless score #k{i} dz.k_zamk matches 1 run " + tellraw("@s", t(" Granice: ", "gray"), t("OTWARTE", "green", bold=True)),
            tellraw("@s", t(" ➤ ", "dark_gray"), t("[STOLICA]", "green", bold=True, run="/trigger stolica set 1", hover=t("Teleport do stolicy")), t(" "),
                    t("[WPŁAĆ 100]", "gold", bold=True, run="/trigger skarbiec set 100"), t(" "),
                    t("[WPŁAĆ 1000]", "gold", bold=True, run="/trigger skarbiec set 1000"), t(" "),
                    t("[RANKING]", "yellow", bold=True, run="/trigger panstwo set 2"), t(" "),
                    t("[OPUŚĆ]", "red", run="/trigger panstwo set 999", hover=t("Opuść państwo", "red"))),
            "execute if entity @s[tag=dz.wladca] run " + tellraw("@s", t(" ♛ Władca: ", "gold", bold=True),
                                                                  t("[GRANICE OTWÓRZ/ZAMKNIJ]", "aqua", run="/trigger panstwo set 997"), t(" "),
                                                                  t("[WOJNA]", "dark_red", bold=True, run="/trigger wojna set 1"), t(" "),
                                                                  t("[WYPŁAĆ 500]", "yellow", run="/trigger skarbiec set -500"), t(" "),
                                                                  t("[KAPITULACJA]", "gray", run="/trigger wojna set 999")),
            f"execute if score #k{i} dz.k_wl matches 0 run " + tellraw("@s", t(" Tron jest wolny! ", "gold"), t("[PRZEJMIJ WŁADZĘ]", "gold", bold=True, run="/trigger panstwo set 998")),
            tellraw("@s", LIN),
        ]))

    rank_menu = [tellraw("@s", LIN), tellraw("@s", t("   ✪ ", "aqua"), t("RANKING PAŃSTW", "gold", bold=True), t("  (mieszkańcy / skarbiec / wygrane wojny)", "gray")), tellraw("@s", LIN)]
    for k in KRAJE:
        i = k[0]
        rank_menu.append(f"execute if score #k{i} dz.k_czl matches 1.. run " + tellraw("@s", t(" • ", "dark_gray"), nazwa(k), t("  👥 ", "gray"), sc(f"#k{i}", "dz.k_czl", "white"), t("  ⛃ ", "gold"), sc(f"#k{i}", "dz.k_skarb", "yellow"), t("  ⚔ ", "red"), sc(f"#k{i}", "dz.k_wygr", "white")).replace("👥", "☺"))
    rank_menu += [tellraw("@s", t(" Ranking potęgi pokazuje się też co chwilę na scoreboardzie.", "gray", italic=True)), tellraw("@s", LIN)]
    fn("kraje/ranking", "\n".join(rank_menu))

    pan = ["# /trigger panstwo",
           f"execute if score @s panstwo matches 2 run function {NS}:kraje/ranking",
           f"execute if score @s panstwo matches 1 unless score @s dz.kraj matches 1.. run function {NS}:kraje/menu_wybor",
           f"execute if score @s panstwo matches 997 if entity @s[tag=dz.wladca] run function {NS}:kraje/granice",
           f"execute if score @s panstwo matches 998 if score @s dz.kraj matches 1.. run function {NS}:kraje/przejmij",
           f"execute if score @s panstwo matches 999 if score @s dz.kraj matches 1.. run function {NS}:kraje/opusc"]
    for k in KRAJE:
        i = k[0]
        pan.append(f"execute if score @s panstwo matches 1 if score @s dz.kraj matches {i} run function {NS}:kraje/info/{i}")
        pan.append(f"execute if score @s panstwo matches {100 + i} run function {NS}:kraje/dolacz/{i}")
    pan.append("scoreboard players set @s panstwo 0")
    fn("komendy/panstwo", "\n".join(pan))

    # ---------------------------------------------------------------- dołączanie / opuszczanie (per państwo)
    disp_wejdz, disp_wyjdz, disp_przejmij, disp_granice, disp_wplata, disp_wyplata = [], [], [], [], [], []
    for k in KRAJE:
        i = k[0]
        fn(f"kraje/dolacz/{i}", f"""
            execute if score @s dz.kraj matches 1.. run return run {tellraw("@s", t("✖ Najpierw opuść swoje państwo: ", "red"), t("[OPUŚĆ]", "red", bold=True, run="/trigger panstwo set 999"))}
            execute if score #k{i} dz.k_zamk matches 1 if score #k{i} dz.k_wl matches 1 run return run function {NS}:kraje/prosba/{i}
            function {NS}:kraje/wejdz/{i}
        """)
        fn(f"kraje/wejdz/{i}", f"""
            scoreboard players set @s dz.kraj {i}
            scoreboard players set @s dz.prosba 0
            scoreboard players add #k{i} dz.k_czl 1
            execute unless score #k{i} dz.k_wl matches 1 run return run function {NS}:kraje/wladca/{i}
            {tellraw("@a", t("✪ ", "aqua"), sel("@s"), t(" dołączył do państwa ", "gray"), nazwa(k), t("!", "gray"))}
            function {NS}:gracz/druzyna
            playsound minecraft:block.note_block.chime master @s ~ ~ ~ 1 1.4
            function {NS}:kraje/info/{i}
        """)
        fn(f"kraje/wladca/{i}", f"""
            scoreboard players set #k{i} dz.k_wl 1
            tag @s add dz.wladca
            function {NS}:gracz/druzyna
            title @a times 10 60 20
            title @a title {J(nazwa(k))}
            title @a subtitle {J([sel("@s"), t(" zostaje władcą!", "gold")])}
            {tellraw("@a", t("♛ ", "gold"), sel("@s"), t(" zakłada państwo ", "yellow"), nazwa(k), t(" i zostaje jego ", "yellow"), t("WŁADCĄ", "gold", bold=True), t("!", "yellow"))}
            execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.7 1
            {firework_cmd()}
            function {NS}:kraje/info/{i}
        """)
        fn(f"kraje/prosba/{i}", f"""
            scoreboard players set @s dz.prosba {i}
            execute unless score @s dz.id matches 1.. run function {NS}:gracz/nadaj_id
            {tellraw("@s", t("✉ Granice państwa ", "gray"), nazwa(k), t(" są zamknięte – wysłano prośbę do władcy.", "gray"))}
            execute store result storage dziobmc:tmp p.id int 1 run scoreboard players get @s dz.id
            data modify storage dziobmc:tmp p.k set value {i}
            function {NS}:kraje/prosba_m with storage dziobmc:tmp p
        """)
        disp_wejdz.append(f"execute if score @s dz.prosba matches {i} run function {NS}:kraje/wejdz/{i}")
        fn(f"kraje/wyjdz/{i}", f"""
            scoreboard players remove #k{i} dz.k_czl 1
            execute if score #k{i} dz.k_czl matches ..-1 run scoreboard players set #k{i} dz.k_czl 0
            {tellraw("@a", t("✪ ", "aqua"), sel("@s"), t(" opuścił państwo ", "gray"), nazwa(k))}
            execute if entity @s[tag=dz.wladca] run scoreboard players set #k{i} dz.k_wl 0
            execute if entity @s[tag=dz.wladca] run {tellraw("@a", t("♛ Tron państwa ", "gold"), nazwa(k), t(" jest wolny! Mieszkańcy mogą go przejąć.", "gold"))}
        """)
        disp_wyjdz.append(f"execute if score @s dz.kraj matches {i} run function {NS}:kraje/wyjdz/{i}")
        fn(f"kraje/przejmij/{i}", f"""
            execute if score #k{i} dz.k_wl matches 1 run return run {tellraw("@s", t("✖ To państwo ma już władcę.", "red"))}
            function {NS}:kraje/wladca/{i}
        """)
        disp_przejmij.append(f"execute if score @s dz.kraj matches {i} run function {NS}:kraje/przejmij/{i}")
        fn(f"kraje/granice/{i}", f"""
            execute if score #k{i} dz.k_zamk matches 1 run return run function {NS}:kraje/granice_otworz/{i}
            scoreboard players set #k{i} dz.k_zamk 1
            {tellraw("@s", t("✔ Granice państwa zamknięte – nowi gracze muszą wysłać prośbę.", "yellow"))}
        """)
        fn(f"kraje/granice_otworz/{i}", f"""
            scoreboard players set #k{i} dz.k_zamk 0
            {tellraw("@s", t("✔ Granice państwa otwarte – każdy może dołączyć.", "green"))}
        """)
        disp_granice.append(f"execute if score @s dz.kraj matches {i} run function {NS}:kraje/granice/{i}")
        fn(f"kraje/wplata/{i}", f"""
            scoreboard players operation @s dz.coins -= #v dz.data
            scoreboard players operation #k{i} dz.k_skarb += #v dz.data
            {tellraw("@a[scores={dz.kraj=" + str(i) + "}]", t("⛃ ", "gold"), sel("@s"), t(" wpłacił ", "gray"), sc("#v", "dz.data", "gold", True), t(" monet do skarbca. Stan: ", "gray"), sc(f"#k{i}", "dz.k_skarb", "yellow", True))}
        """)
        disp_wplata.append(f"execute if score @s dz.kraj matches {i} run function {NS}:kraje/wplata/{i}")
        fn(f"kraje/wyplata/{i}", f"""
            execute if score #k{i} dz.k_skarb < #v dz.data run return run {tellraw("@s", t("✖ W skarbcu jest za mało monet.", "red"))}
            scoreboard players operation #k{i} dz.k_skarb -= #v dz.data
            scoreboard players operation @s dz.coins += #v dz.data
            {tellraw("@a[scores={dz.kraj=" + str(i) + "}]", t("⛃ Władca ", "gold"), sel("@s"), t(" wypłacił ", "gray"), sc("#v", "dz.data", "gold", True), t(" monet ze skarbca.", "gray"))}
        """)
        disp_wyplata.append(f"execute if score @s dz.kraj matches {i} run function {NS}:kraje/wyplata/{i}")

    fn("kraje/prosba_m", f"""
        $tellraw @a[tag=dz.wladca,scores={{dz.kraj=$(k)}}] [{{"text":"✉ ","color":"aqua"}},{{"selector":"@s"}},{{"text":" prosi o dołączenie do państwa. ","color":"gray"}},{{"text":"[PRZYJMIJ]","color":"green","bold":true,"clickEvent":{{"action":"run_command","value":"/trigger przyjmij set $(id)"}}}}]
        $execute as @a[tag=dz.wladca,scores={{dz.kraj=$(k)}}] at @s run playsound minecraft:block.note_block.bell master @s ~ ~ ~ 1 1.2
    """)
    fn("kraje/opusc", "\n".join(disp_wyjdz + [
        "tag @s remove dz.wladca", "scoreboard players set @s dz.kraj 0", f"function {NS}:gracz/druzyna"]))
    fn("kraje/przejmij", "\n".join(disp_przejmij))
    fn("kraje/granice", "\n".join(disp_granice))
    fn("kraje/wejdz_prosba", "\n".join(disp_wejdz))
    fn("komendy/przyjmij", f"""
        # Władca przyjmuje gracza o podanym ID
        execute unless entity @s[tag=dz.wladca] run return run function {NS}:komendy/przyjmij_reset
        scoreboard players operation #v dz.data = @s przyjmij
        scoreboard players operation #lk dz.data = @s dz.kraj
        execute as @a[scores={{dz.prosba=1..}}] if score @s dz.id = #v dz.data if score @s dz.prosba = #lk dz.data at @s run function {NS}:kraje/wejdz_prosba
        scoreboard players set @s przyjmij 0
    """)
    fn("komendy/przyjmij_reset", "scoreboard players set @s przyjmij 0")
    fn("komendy/skarbiec", f"""
        scoreboard players operation #v dz.data = @s skarbiec
        scoreboard players set @s skarbiec 0
        execute unless score @s dz.kraj matches 1.. run return run {tellraw("@s", t("✖ Nie należysz do żadnego państwa.", "red"))}
        execute if score #v dz.data matches 2.. unless score @s dz.coins >= #v dz.data run return run {tellraw("@s", t("✖ Masz za mało monet.", "red"))}
        execute if score #v dz.data matches 2.. run return run function {NS}:kraje/skarbiec_wplata
        execute if score #v dz.data matches ..-1 unless entity @s[tag=dz.wladca] run return run {tellraw("@s", t("✖ Tylko władca może wypłacać ze skarbca.", "red"))}
        execute if score #v dz.data matches ..-1 run scoreboard players operation #v dz.data *= #m1 dz.data
        execute if score #v dz.data matches 1.. run function {NS}:kraje/skarbiec_wyplata
    """)
    fn("kraje/skarbiec_wplata", "\n".join(disp_wplata))
    fn("kraje/skarbiec_wyplata", "\n".join(disp_wyplata))

    # ---------------------------------------------------------------- stolice i teleporty
    st = ["# /trigger stolica: 1 = własna stolica (lub lista), 100+N = stolica państwa N",
          f"execute if score @s stolica matches 1 unless score @s dz.kraj matches 1.. run function {NS}:kraje/menu_stolice"]
    for k in KRAJE:
        i = k[0]
        st.append(f"execute if score @s stolica matches 1 if score @s dz.kraj matches {i} run function {NS}:kraje/tp/{i}")
        st.append(f"execute if score @s stolica matches {100 + i} run function {NS}:kraje/tp/{i}")
        fn(f"kraje/tp/{i}", f"""
            {cooldown("dz.cd_stol", 600)}
            {tellraw("@s", t("✈ Lecisz do stolicy: ", "aqua"), t(k[4], k[3], bold=True), t(" (", "gray"), nazwa(k, False), t(")", "gray"))}
            function {NS}:ziemia/tp_m with storage dziobmc:kraje s.k{i}
        """)
    st.append("scoreboard players set @s stolica 0")
    fn("komendy/stolica", "\n".join(st))
    ms = [tellraw("@s", LIN), tellraw("@s", t("   ✈ ", "aqua"), t("STOLICE ŚWIATA", "gold", bold=True), t("  (kliknij, aby polecieć)", "gray")), tellraw("@s", LIN)]
    for kont in KONTYNENTY:
        cz = [t(f" {kont}: ", "yellow", bold=True)]
        for k in [k for k in KRAJE if k[7] == kont]:
            cz += [t(k[4], k[3], run=f"/trigger stolica set {100 + k[0]}", hover=t(k[1], k[3])), t(" • ", "dark_gray")]
        ms.append(tellraw("@s", *cz[:-1]))
    ms.append(tellraw("@s", LIN))
    fn("kraje/menu_stolice", "\n".join(ms))
    fn("ziemia/tp_m", f"""
        $execute in {SWIAT} run spreadplayers $(x) $(z) 0 10 false @s
        function {NS}:ziemia/po_tp
    """)
    fn("ziemia/po_tp", f"""
        execute at @s unless dimension {SWIAT} run return run {tellraw("@s", t("✖ Świat 'ziemia' nie istnieje. Zainstaluj plugin DziobEarth (patrz instrukcja).", "red"))}
        tag @s remove dz.lobby
        gamemode survival @s[gamemode=adventure,tag=!dz.build]
        effect give @s minecraft:resistance 5 4 true
        effect give @s minecraft:slow_falling 6 0 true
        execute at @s run playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 0.8
        title @s times 5 40 10
        title @s title {J(t("✈ Ziemia", "aqua", bold=True))}
        title @s subtitle {J(t("/trigger gdzie – sprawdź gdzie jesteś", "gray"))}
    """)

    # losowy teleport na ląd
    fn("ziemia/rtp", f"""
        {cooldown("dz.cd_rtp", 1200)}
        scoreboard players set #proby_rtp dz.data 0
        {tellraw("@s", t("✈ Szukam lądu na mapie Ziemi...", "aqua"))}
        function {NS}:ziemia/rtp_proba
    """)
    fn("ziemia/rtp_proba", f"""
        scoreboard players add #proby_rtp dz.data 1
        execute if score #proby_rtp dz.data matches 9.. run return run function {NS}:ziemia/rtp_stolica
        execute store result score #x dz.data run random value -170..170
        execute store result score #z dz.data run random value -60..55
        scoreboard players operation #x dz.data *= #111320 dz.data
        scoreboard players operation #x dz.data /= #skala dz.data
        scoreboard players operation #z dz.data *= #111320 dz.data
        scoreboard players operation #z dz.data /= #skala dz.data
        execute store result storage dziobmc:tmp r.x int 1 run scoreboard players get #x dz.data
        execute store result storage dziobmc:tmp r.z int 1 run scoreboard players get #z dz.data
        function {NS}:ziemia/rtp_m with storage dziobmc:tmp r
        execute at @s if dimension {SWIAT} if block ~ ~-1 ~ minecraft:water run return run function {NS}:ziemia/rtp_proba
        execute at @s if dimension {SWIAT} if block ~ ~-1 ~ minecraft:ice run return run function {NS}:ziemia/rtp_proba
        function {NS}:ziemia/po_tp
    """)
    fn("ziemia/rtp_m", f"$execute in {SWIAT} run spreadplayers $(x) $(z) 0 150 false @s")
    rs = ["execute store result score #r dz.data run random value 1.." + str(N)]
    for k in KRAJE:
        rs.append(f"execute if score #r dz.data matches {k[0]} run function {NS}:ziemia/tp_m with storage dziobmc:kraje s.k{k[0]}")
    fn("ziemia/rtp_stolica", "\n".join(rs))

    # ---------------------------------------------------------------- /trigger gdzie
    gd = [f"execute at @s unless dimension {SWIAT} run return run " + tellraw("@s", t("✖ Komenda działa na mapie Ziemi. ", "red"), t("[LECĘ]", "green", bold=True, run="/trigger ziemia set 11")),
          "execute store result score #px dz.data run data get entity @s Pos[0]",
          "execute store result score #pz dz.data run data get entity @s Pos[2]",
          "scoreboard players operation #lon dz.data = #px dz.data",
          "scoreboard players operation #lon dz.data *= #skala dz.data",
          "scoreboard players operation #lon dz.data /= #1113 dz.data",
          "scoreboard players operation #lat dz.data = #pz dz.data",
          "scoreboard players operation #lat dz.data *= #skala dz.data",
          "scoreboard players operation #lat dz.data /= #1113 dz.data",
          "scoreboard players operation #lat dz.data *= #m1 dz.data",
          f"function {NS}:ziemia/gdzie_format",
          "scoreboard players set #min dz.data 2147483647", "scoreboard players set #najbl dz.data 0"]
    for k in KRAJE:
        i = k[0]
        gd += [f"scoreboard players operation #dx dz.data = #sx{i} dz.data", "scoreboard players operation #dx dz.data -= #px dz.data",
               f"scoreboard players operation #dz dz.data = #sz{i} dz.data", "scoreboard players operation #dz dz.data -= #pz dz.data",
               "scoreboard players operation #dx dz.data /= #10 dz.data", "scoreboard players operation #dz dz.data /= #10 dz.data",
               "scoreboard players operation #dx dz.data *= #dx dz.data", "scoreboard players operation #dz dz.data *= #dz dz.data",
               "scoreboard players operation #dx dz.data += #dz dz.data",
               f"execute if score #dx dz.data < #min dz.data run scoreboard players set #najbl dz.data {i}",
               "scoreboard players operation #min dz.data < #dx dz.data"]
    gd += ["scoreboard players operation #sq dz.data = #min dz.data", f"function {NS}:util/sqrt",
           "scoreboard players operation #sq dz.data *= #10 dz.data"]
    for k in KRAJE:
        gd.append(f"execute if score #najbl dz.data matches {k[0]} run " + tellraw("@s", t(" Najbliższa stolica: ", "gray"), t(k[4], k[3], bold=True), t(" (", "gray"), nazwa(k, False), t(") ~", "gray"), sc("#sq", "dz.data", "white", True), t(" kratek", "gray")))
    gd.append("scoreboard players set @s gdzie 0")
    fn("komendy/gdzie", "\n".join(gd))
    fn("ziemia/gdzie_format", f"""
        scoreboard players set #ns dz.data 1
        execute if score #lat dz.data matches ..-1 run scoreboard players set #ns dz.data -1
        execute if score #lat dz.data matches ..-1 run scoreboard players operation #lat dz.data *= #m1 dz.data
        scoreboard players set #ew dz.data 1
        execute if score #lon dz.data matches ..-1 run scoreboard players set #ew dz.data -1
        execute if score #lon dz.data matches ..-1 run scoreboard players operation #lon dz.data *= #m1 dz.data
        scoreboard players operation #lat_c dz.data = #lat dz.data
        scoreboard players operation #lat_c dz.data /= #100 dz.data
        scoreboard players operation #lat_u dz.data = #lat dz.data
        scoreboard players operation #lat_u dz.data %= #100 dz.data
        scoreboard players operation #lon_c dz.data = #lon dz.data
        scoreboard players operation #lon_c dz.data /= #100 dz.data
        scoreboard players operation #lon_u dz.data = #lon dz.data
        scoreboard players operation #lon_u dz.data %= #100 dz.data
        {tellraw("@s", t("━━━━━━━━━━━ ✪ GDZIE JESTEM ✪ ━━━━━━━━━━━", "aqua", bold=True))}
        execute if score #lat_u dz.data matches 10.. if score #ns dz.data matches 1 run {tellraw("@s", t(" Szerokość: ", "gray"), sc("#lat_c", "dz.data", "white", True), t(".", "white", bold=True), sc("#lat_u", "dz.data", "white", True), t("° N", "yellow", bold=True))}
        execute if score #lat_u dz.data matches ..9 if score #ns dz.data matches 1 run {tellraw("@s", t(" Szerokość: ", "gray"), sc("#lat_c", "dz.data", "white", True), t(".0", "white", bold=True), sc("#lat_u", "dz.data", "white", True), t("° N", "yellow", bold=True))}
        execute if score #lat_u dz.data matches 10.. if score #ns dz.data matches -1 run {tellraw("@s", t(" Szerokość: ", "gray"), sc("#lat_c", "dz.data", "white", True), t(".", "white", bold=True), sc("#lat_u", "dz.data", "white", True), t("° S", "yellow", bold=True))}
        execute if score #lat_u dz.data matches ..9 if score #ns dz.data matches -1 run {tellraw("@s", t(" Szerokość: ", "gray"), sc("#lat_c", "dz.data", "white", True), t(".0", "white", bold=True), sc("#lat_u", "dz.data", "white", True), t("° S", "yellow", bold=True))}
        execute if score #lon_u dz.data matches 10.. if score #ew dz.data matches 1 run {tellraw("@s", t(" Długość:    ", "gray"), sc("#lon_c", "dz.data", "white", True), t(".", "white", bold=True), sc("#lon_u", "dz.data", "white", True), t("° E", "yellow", bold=True))}
        execute if score #lon_u dz.data matches ..9 if score #ew dz.data matches 1 run {tellraw("@s", t(" Długość:    ", "gray"), sc("#lon_c", "dz.data", "white", True), t(".0", "white", bold=True), sc("#lon_u", "dz.data", "white", True), t("° E", "yellow", bold=True))}
        execute if score #lon_u dz.data matches 10.. if score #ew dz.data matches -1 run {tellraw("@s", t(" Długość:    ", "gray"), sc("#lon_c", "dz.data", "white", True), t(".", "white", bold=True), sc("#lon_u", "dz.data", "white", True), t("° W", "yellow", bold=True))}
        execute if score #lon_u dz.data matches ..9 if score #ew dz.data matches -1 run {tellraw("@s", t(" Długość:    ", "gray"), sc("#lon_c", "dz.data", "white", True), t(".0", "white", bold=True), sc("#lon_u", "dz.data", "white", True), t("° W", "yellow", bold=True))}
    """)
    fn("util/sqrt", """
        # Pierwiastek całkowity z #sq (metoda Newtona) -> #sq
        execute if score #sq dz.data matches ..0 run return run scoreboard players set #sq dz.data 0
        scoreboard players operation #n dz.data = #sq dz.data
        scoreboard players set #r dz.data 1000
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        function dziobmc:util/sqrt_krok
        scoreboard players operation #sq dz.data = #r dz.data
    """)
    fn("util/sqrt_krok", """
        scoreboard players operation #q dz.data = #n dz.data
        scoreboard players operation #q dz.data /= #r dz.data
        scoreboard players operation #r dz.data += #q dz.data
        scoreboard players operation #r dz.data /= #2 dz.data
        execute if score #r dz.data matches ..0 run scoreboard players set #r dz.data 1
    """)

    # ---------------------------------------------------------------- /trigger ziemia (menu)
    fn("komendy/ziemia", f"""
        execute if score @s ziemia matches 11 run function {NS}:ziemia/rtp
        execute if score @s ziemia matches 12 run scoreboard players set @s stolica 1
        execute if score @s ziemia matches 13 run scoreboard players set @s panstwo 1
        execute if score @s ziemia matches 14 run scoreboard players set @s gdzie 1
        execute if score @s ziemia matches 1 run function {NS}:ziemia/menu
        scoreboard players set @s ziemia 0
    """)
    fn("ziemia/menu", "\n".join([
        tellraw("@s", LIN),
        tellraw("@s", t("   ✪ ", "aqua"), t("EARTH SMP", "gold", bold=True), t(" – mapa Ziemi w Minecraft", "gray")),
        tellraw("@s", LIN),
        tellraw("@s", t(" ➤ ", "dark_gray"), t("[LOSOWY LĄD]", "green", bold=True, run="/trigger ziemia set 11"), t(" teleport w losowe miejsce na lądzie", "gray")),
        tellraw("@s", t(" ➤ ", "dark_gray"), t("[MOJA STOLICA]", "aqua", bold=True, run="/trigger ziemia set 12"), t(" stolica twojego państwa", "gray")),
        tellraw("@s", t(" ➤ ", "dark_gray"), t("[PAŃSTWA]", "gold", bold=True, run="/trigger ziemia set 13"), t(" dołącz / zarządzaj państwem", "gray")),
        tellraw("@s", t(" ➤ ", "dark_gray"), t("[STOLICE ŚWIATA]", "yellow", bold=True, run=f"/trigger stolica set 1"), t(" lot do dowolnej stolicy", "gray")),
        tellraw("@s", t(" ➤ ", "dark_gray"), t("[GDZIE JESTEM]", "white", bold=True, run="/trigger ziemia set 14"), t(" szerokość/długość i najbliższa stolica", "gray")),
        tellraw("@s", t(" ➤ ", "dark_gray"), t("[WOJNY]", "dark_red", bold=True, run="/trigger wojna set 1"), t(" wojny między państwami (dla władców)", "gray")),
        tellraw("@s", LIN),
    ]))

    # ---------------------------------------------------------------- wojny
    wm = [f"execute unless entity @s[tag=dz.wladca] run return run " + tellraw("@s", t("✖ Tylko władca państwa może wypowiadać wojny.", "red")),
          tellraw("@s", LIN), tellraw("@s", t("   ⚔ ", "dark_red"), t("WYPOWIEDZ WOJNĘ", "red", bold=True), t("  (tylko państwom z mieszkańcami)", "gray")), tellraw("@s", LIN),
          tellraw("@s", t(" Wojna trwa 30 min. Punkt = zabicie wroga. Do 15 pkt. Zwycięzca bierze 30% skarbca wroga!", "gray"))]
    for k in KRAJE:
        i = k[0]
        wm.append(f"execute if score #k{i} dz.k_czl matches 1.. unless score @s dz.kraj matches {i} run " + tellraw("@s", t(" ⚔ ", "dark_red"), nazwa(k), t("  👥 ".replace("👥", "☺"), "gray"), sc(f"#k{i}", "dz.k_czl", "white"), t("  "), t("[WYPOWIEDZ WOJNĘ]", "red", bold=True, run=f"/trigger wojna set {100 + i}")))
    wm.append(tellraw("@s", LIN))
    fn("wojna/menu", "\n".join(wm))
    wd = [f"execute if score @s wojna matches 1 run function {NS}:wojna/menu",
          f"execute if score @s wojna matches 999 if entity @s[tag=dz.wladca] run function {NS}:wojna/kapitulacja"]
    for k in KRAJE:
        wd.append(f"execute if score @s wojna matches {100 + k[0]} if entity @s[tag=dz.wladca] run function {NS}:wojna/wypowiedz_b {{b:{k[0]}}}")
    wd.append("scoreboard players set @s wojna 0")
    fn("komendy/wojna", "\n".join(wd))
    fn("wojna/wypowiedz_b", f"""
        $data modify storage dziobmc:tmp w.b set value $(b)
        execute store result storage dziobmc:tmp w.a int 1 run scoreboard players get @s dz.kraj
        function {NS}:wojna/nazwy with storage dziobmc:tmp w
        function {NS}:wojna/wypowiedz with storage dziobmc:tmp w
    """)
    fn("wojna/nazwy", """
        $data modify storage dziobmc:tmp w.na set from storage dziobmc:kraje n.k$(a)
        $data modify storage dziobmc:tmp w.nb set from storage dziobmc:kraje n.k$(b)
    """)
    fn("wojna/wypowiedz", f"""
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
    # punkty za zabicie wroga – advancement per państwo ofiary
    for k in KRAJE:
        i = k[0]
        jfile(f"data/{NS}/advancement/wojna/zab{i}.json", {
            "criteria": {"zabicie": {"trigger": "minecraft:player_killed_entity", "conditions": {"entity": [
                {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": "minecraft:player"}},
                {"condition": "minecraft:entity_scores", "entity": "this", "scores": {"dz.kraj": i}}]}}},
            "rewards": {"function": f"{NS}:wojna/zab/{i}"}})
        fn(f"wojna/zab/{i}", f"""
            advancement revoke @s only {NS}:wojna/zab{i}
            execute unless score @s dz.kraj matches 1.. run return 0
            execute store result storage dziobmc:tmp z.a int 1 run scoreboard players get @s dz.kraj
            data modify storage dziobmc:tmp z.b set value {i}
            function {NS}:wojna/punkt with storage dziobmc:tmp z
        """)
    fn("wojna/punkt", f"""
        $execute unless score #k$(a) dz.k_wrog matches $(b) run return 0
        $scoreboard players add #k$(a) dz.k_pkt 1
        $tellraw @a[scores={{dz.kraj=$(a)}}] [{{"text":"⚔ +1 punkt wojenny! Wynik: ","color":"gold"}},{{"score":{{"name":"#k$(a)","objective":"dz.k_pkt"}},"color":"green","bold":true}},{{"text":" : ","color":"gray"}},{{"score":{{"name":"#k$(b)","objective":"dz.k_pkt"}},"color":"red","bold":true}}]
        $tellraw @a[scores={{dz.kraj=$(b)}}] [{{"text":"⚔ Wróg zdobywa punkt! Wynik: ","color":"red"}},{{"score":{{"name":"#k$(b)","objective":"dz.k_pkt"}},"color":"green","bold":true}},{{"text":" : ","color":"gray"}},{{"score":{{"name":"#k$(a)","objective":"dz.k_pkt"}},"color":"red","bold":true}}]
        $execute if score #k$(a) dz.k_pkt matches 15.. run function {NS}:wojna/koniec {{a:$(a),b:$(b)}}
    """)
    # zegar wojny
    tk = []
    for k in KRAJE:
        i = k[0]
        tk.append(f"execute if score #k{i} dz.k_wrog matches 1.. run function {NS}:wojna/tik/{i}")
        tk.append(f"execute if score #k{i} dz.k_pokoj matches 1.. run scoreboard players remove #k{i} dz.k_pokoj 1")
        fn(f"wojna/tik/{i}", f"""
            scoreboard players remove #k{i} dz.k_wczas 1
            execute if score #k{i} dz.k_wczas matches ..0 store result storage dziobmc:tmp k.b int 1 run scoreboard players get #k{i} dz.k_wrog
            execute if score #k{i} dz.k_wczas matches ..0 run data modify storage dziobmc:tmp k.a set value {i}
            execute if score #k{i} dz.k_wczas matches ..0 run function {NS}:wojna/koniec with storage dziobmc:tmp k
        """)
    fn("wojna/sekunda", "\n".join(tk))
    fn("wojna/koniec", f"""
        # a, b – państwa w wojnie. Zwycięża to z większą liczbą punktów.
        $execute store result score #pa dz.data run scoreboard players get #k$(a) dz.k_pkt
        $execute store result score #pb dz.data run scoreboard players get #k$(b) dz.k_pkt
        $data modify storage dziobmc:tmp e1 set value {{w:$(a),l:$(b)}}
        $data modify storage dziobmc:tmp e2 set value {{w:$(b),l:$(a)}}
        function {NS}:wojna/e_nazwy
        execute if score #pa dz.data > #pb dz.data run function {NS}:wojna/wygrana with storage dziobmc:tmp e1
        execute if score #pb dz.data > #pa dz.data run function {NS}:wojna/wygrana with storage dziobmc:tmp e2
        execute if score #pa dz.data = #pb dz.data run function {NS}:wojna/remis with storage dziobmc:tmp e1
        $function {NS}:wojna/reset {{a:$(a),b:$(b)}}
    """)
    fn("wojna/e_nazwy", f"""
        function {NS}:wojna/e_nazwy_m with storage dziobmc:tmp e1
    """)
    fn("wojna/e_nazwy_m", """
        $data modify storage dziobmc:tmp e1.nw set from storage dziobmc:kraje n.k$(w)
        $data modify storage dziobmc:tmp e1.nl set from storage dziobmc:kraje n.k$(l)
        $data modify storage dziobmc:tmp e2.nw set from storage dziobmc:kraje n.k$(l)
        $data modify storage dziobmc:tmp e2.nl set from storage dziobmc:kraje n.k$(w)
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
        $execute as @a[scores={{dz.kraj=$(w)}}] at @s run {firework_cmd()}
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
        execute store result storage dziobmc:tmp c.l int 1 run scoreboard players get @s dz.kraj
        function {NS}:wojna/kapitulacja_m with storage dziobmc:tmp c
    """)
    fn("wojna/kapitulacja_m", f"""
        $execute unless score #k$(l) dz.k_wrog matches 1.. run return run tellraw @s {{"text":"✖ Twoje państwo nie prowadzi wojny.","color":"red"}}
        $execute store result storage dziobmc:tmp c.w int 1 run scoreboard players get #k$(l) dz.k_wrog
        tellraw @a [{{"text":"🏳 ","color":"white"}},{{"text":"Państwo kapituluje!","color":"gray"}}]
        function {NS}:wojna/kapitulacja_m2 with storage dziobmc:tmp c
    """.replace("🏳", "⚑"))
    fn("wojna/kapitulacja_m2", f"""
        $scoreboard players set #k$(w) dz.k_pkt 15
        $scoreboard players set #k$(l) dz.k_pkt 0
        $function {NS}:wojna/koniec {{a:$(w),b:$(l)}}
    """)

    # ---------------------------------------------------------------- strefy stolic (co sekundę)
    sf = ["# Kto należy do jakiej wojny",
          "scoreboard players set @a dz.mojwrog 0"]
    for k in KRAJE:
        sf.append(f"execute as @a[scores={{dz.kraj={k[0]}}}] run scoreboard players operation @s dz.mojwrog = #k{k[0]} dz.k_wrog")
    sf += ["tag @a remove dz.strefa_obca"]
    for k in KRAJE:
        sf.append(f"function {NS}:ziemia/strefa_m with storage dziobmc:kraje s.k{k[0]}")
    sf += ["gamemode adventure @a[tag=dz.strefa_obca,gamemode=survival,tag=!dz.build]",
           "execute as @a[tag=dz.strefa_obca,tag=!dz.strefa_bylo] run " + tellraw("@s", t("⛨ Wchodzisz do chronionej stolicy obcego państwa – nie możesz tu niszczyć bloków.", "gold")),
           "tag @a[tag=dz.strefa_obca] add dz.strefa_bylo",
           "gamemode survival @a[tag=!dz.strefa_obca,tag=dz.strefa_bylo,tag=!dz.lobby,gamemode=adventure,tag=!dz.build]",
           "tag @a[tag=!dz.strefa_obca] remove dz.strefa_bylo"]
    fn("ziemia/strefy", "\n".join(sf))
    fn("ziemia/strefa_m", f"""
        $execute in {SWIAT} as @a[x=$(x0),y=-64,z=$(z0),dx={2 * STREFA},dy=400,dz={2 * STREFA}] unless score @s dz.kraj matches $(i) unless score @s dz.mojwrog matches $(i) run tag @s add dz.strefa_obca
    """)

    # ---------------------------------------------------------------- ranking (sidebar) co 10 s
    rk = []
    for k in KRAJE:
        i = k[0]
        rk += [f"scoreboard players operation #p dz.data = #k{i} dz.k_czl", "scoreboard players operation #p dz.data *= #100 dz.data",
               f"scoreboard players operation #q dz.data = #k{i} dz.k_skarb", "scoreboard players operation #q dz.data /= #10 dz.data",
               "scoreboard players operation #p dz.data += #q dz.data",
               f"scoreboard players operation #q dz.data = #k{i} dz.k_wygr", "scoreboard players operation #q dz.data *= #500 dz.data",
               "scoreboard players operation #p dz.data += #q dz.data",
               f"execute if score #k{i} dz.k_czl matches 1.. run scoreboard players operation k{k[2]} dz.ranking = #p dz.data",
               f"execute if score #k{i} dz.k_czl matches 1.. run scoreboard players display name k{k[2]} dz.ranking {J([t(k[2] + ' ', 'dark_gray'), nazwa(k, False)])}",
               f"execute unless score #k{i} dz.k_czl matches 1.. run scoreboard players reset k{k[2]} dz.ranking"]
    rk += ["scoreboard players set #ile_kr dz.data 0"]
    for k in KRAJE:
        rk.append(f"execute if score #k{k[0]} dz.k_czl matches 1.. run scoreboard players add #ile_kr dz.data 1")
    rk += ["scoreboard players add #sb dz.data 1",
           "execute if score #sb dz.data matches 2.. run scoreboard players set #sb dz.data 0",
           "execute if score #sb dz.data matches 1 if score #ile_kr dz.data matches 1.. run scoreboard objectives setdisplay sidebar dz.ranking",
           "execute unless score #sb dz.data matches 1 run scoreboard objectives setdisplay sidebar dz.sidebar",
           "execute unless score #ile_kr dz.data matches 1.. run scoreboard objectives setdisplay sidebar dz.sidebar"]
    fn("ziemia/ranking", "\n".join(rk))

    # ---------------------------------------------------------------- pętla Earth SMP (co sekundę)
    fn("ziemia/sekunda", f"""
        function {NS}:wojna/sekunda
        scoreboard players operation #t15 dz.data = #sek dz.data
        scoreboard players operation #t15 dz.data %= #15 dz.data
        execute if score #t15 dz.data matches 0 run function {NS}:ziemia/ranking
        scoreboard players operation #t15 dz.data = #sek dz.data
        scoreboard players operation #t15 dz.data %= #60 dz.data
        execute if score #t15 dz.data matches 0 run function {NS}:ziemia/granica with storage dziobmc:tmp g
        execute as @a[scores={{dz.prosba=1..,dz.kraj=1..}}] run scoreboard players set @s dz.prosba 0
    """)

    # ---------------------------------------------------------------- NPC "Państwa" w lobby
    jfile(f"data/{NS}/advancement/npc/panstwa.json", {
        "criteria": {"klik": {"trigger": "minecraft:player_interacted_with_entity", "conditions": {
            "entity": [{"condition": "minecraft:entity_properties", "entity": "this",
                        "predicate": {"type": "minecraft:interaction", "nbt": "{Tags:[\"dz.int.panstwa\"]}"}}]}}},
        "rewards": {"function": f"{NS}:npc/panstwa"}})
    fn("npc/panstwa", f"""
        advancement revoke @s only {NS}:npc/panstwa
        playsound minecraft:entity.villager.ambient master @s ~ ~ ~ 1 1
        function {NS}:ziemia/menu
    """)


def build_tick():
    tk = [f"execute as @a[scores={{{tr}=1..}}] at @s run function {NS}:komendy/{tr}" for tr in TRIGGERY_ZIEMIA]
    tk.append(f"execute as @a[scores={{skarbiec=..-1}}] at @s run function {NS}:komendy/skarbiec")
    tk += [f"scoreboard players enable @a {tr}" for tr in TRIGGERY_ZIEMIA]
    fn("ziemia/tick", "\n".join(tk))


def k4(k):
    return k[4]
