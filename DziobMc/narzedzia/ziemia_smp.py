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


LIN = t("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "aqua", bold=True)


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
    dz += [f"function {NS}:kraje/init", f"function {NS}:ziemia/przelicz"]
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

    # ---------------------------------------------------------------- ID gracza (do próśb o dołączenie)
    fn("gracz/nadaj_id", """
        scoreboard players add #nast_id dz.data 1
        scoreboard players operation @s dz.id = #nast_id dz.data
    """)

    # ---------------------------------------------------------------- stolice i teleporty
    st = ["# /trigger stolica: 1 = własna stolica (lub lista), 100+N = stolica państwa N",
          f"execute if score @s stolica matches 1 unless score @s dz.kid matches 1.. run function {NS}:kraje/menu_stolice",
          f"execute if score @s stolica matches 1 if score @s dz.kid matches 1.. run function {NS}:kraje/tp_wlasna"]
    for k in KRAJE:
        i = k[0]
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
