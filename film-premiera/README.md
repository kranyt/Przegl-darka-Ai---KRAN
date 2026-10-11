# Dziob.6mc.PL – film na premierę serwera

`Dziob-6mc-PL-premiera.mp4` – 47 s, 1920×1080, 30 fps, H.264 + AAC.

Sceny:
1. **0–6,6 s** – nocny pikselowy świat, „6MC.PL przedstawia…”
2. **6,6–14,8 s** – logo DZIOB budowane ze spadających bloków złota i trawy, promienie światła, fajerwerki
3. **14,8–25,4 s** – „Co czeka na serwerze?” – karty w stylu GUI Minecrafta + toast „Osiągnięcie zdobyte!”
4. **25,4–33 s** – odliczanie 3‑2‑1 przy migającym TNT, wybuch, „24 GRUDNIA! Wtedy ruszamy!”
5. **33–47 s** – wpis z listy serwerów, `IP: DZIOB.6MC.PL`, „PREMIERA 24 GRUDNIA”, splash „Wesołych Świąt!”, fajerwerki, plansza końcowa „PREMIERA 24.12”

Dźwięk: dostarczony lektor (ElevenLabs) + wygenerowana muzyka (pad, bas, perkusja, arpeggio, dzwoneczki sań i melodia „Jingle Bells” na dzwonkach) z automatycznym ściszaniem pod głos oraz efekty (uderzenia bloków, narastanie, wybuch TNT, fajerwerki). W tle przez cały film pada śnieg.

## Ponowne renderowanie
Skrypty w `zrodla/` (Python 3, numpy, Pillow, ffmpeg; czcionki pikselowe Press Start 2P / Pixelify Sans z paczek @fontsource w katalogu `../fonts`):
```
python3 music.py <katalog_build> voice.mp3   # -> mix.wav, mix.npy
python3 video.py wynik.mp4
```
Teksty kart funkcji są w `CARDS` w `video.py`.

---

# Wersja 2 – bez dźwięku

`Dziob-6mc-PL-premiera-24-grudnia-v2-bez-dzwieku.mp4` – 34 s, 1920×1080, 30 fps, bez ścieżki audio. Wszystkie animacje nowe:
1. **0–5 s** – ekran „Ładowanie świata” w stylu Minecrafta (pasek postępu, „Sypanie śniegu…”, „Ubieranie choinki…”)
2. **5–11 s** – izometryczna, zaśnieżona latająca wyspa budująca się blok po bloku, choinka ze świecącą gwiazdą, prezenty
3. **11–19 s** – „Co znajdziesz pod choinką?” – cztery prezenty spadają i otwierają się, odsłaniając atrakcje serwera
4. **19–26 s** – kalendarz adwentowy: okienka 1–23 otwierają się falą, zbliżenie na złote okienko 24 → „24 GRUDNIA – Wigilia • Premiera serwera”
5. **26–34 s** – zorza polarna, lampki choinkowe, logo DZIOB ze śnieżnych bloków złota, „PREMIERA 24.12”, czat Minecrafta „<Mikołaj> Ho ho ho! Widzimy się 24 grudnia! / IP: dziob.6mc.pl”, „Wesołych Świąt!”

Przejścia między scenami: „blokowe” zasłanianie ekranu rosnącymi kwadratami. Skrypt: `zrodla/video2.py` (korzysta z funkcji z `video.py`).

---

# Wersja 3 – bez dźwięku

`Dziob-6mc-PL-premiera-24-grudnia-v3-bez-dzwieku.mp4` – 36 s, 1920×1080, 30 fps, bez ścieżki audio. Nowe animacje:
1. **0–6,5 s** – sanie Mikołaja z reniferami lecą nad zaśnieżonym miasteczkiem i zostawiają złoty ślad, który „pisze” na niebie DZIOB.6MC.PL
2. **6,5–12,5 s** – świąteczny portal: rama z obsydianu buduje się blok po bloku, zapala się lodowo-fioletowy wir, kamera wlatuje do środka (efekt warp)
3. **12,5–19,5 s** – kula śnieżna z logo DZIOB spada na stół, trzęsie się, w środku wiruje śnieg; podstawka z tabliczką „24.12”
4. **19,5–27 s** – złota maszyna losująca: bębny kręcą się i zatrzymują na 2‑4 . 1‑2, deszcz złota i „JACKPOT! PREMIERA 24 GRUDNIA”
5. **27–36 s** – rosnąca choinka z bloków, bombki, migające lampki, spadająca gwiazda; obok logo, „PREMIERA 24 GRUDNIA • WIGILIA 2026”, „Wesołych Świąt!”

Przejścia: pikselowa „tęczówka” (koło) ze świecącą obwódką. Skrypt: `zrodla/video3.py`.

---

# Wersja 4 – „Dlaczego anarchia.gg ma tyle graczy…?” (z dźwiękiem)

`Dziob-6mc-PL-dlaczego-anarchia.mp4` – 43,5 s, 1920×1080, 30 fps, AAC. Memowy, autoironiczny film; dźwięk w całości syntezowany (bez nagrania lektora):
1. **0–5,5 s** – pytanie pisane na maszynie: „Dlaczego anarchia.gg ma tyle graczy… a my nawet filmu o premierze nie możemy zrobić?” + dramatyczne uderzenia i trzęsienie kamery
2. **5,5–12 s** – podzielony ekran: tłum skaczących graczy i szybki czat vs. samotny gracz z głową ptaka na Dziob.6mc.PL, przetaczający się krzak, świerszcze, „halo? / jest ktoś?”, „HMMM…”
3. **12–19,9 s** – montażownia: „Próba nr 1” – render staje na 99%, okno „BŁĄD: Komputer się poddał.” + smutna trąbka; „Próba nr 2” – tandetny slajd „PREMIERA!!!”
4. **19,9–25,5 s** – zgrzyt płyty, „ALE CHWILA…”, miniatury trzech poprzednich filmów: „Zrobiliśmy już 3 filmy o premierze! (ten jest czwarty)”
5. **25,5–34 s** – wchodzi chiptune: „Dlaczego warto wbić na Dziob.6mc.PL?” – lista z odhaczanymi punktami
6. **34–43,5 s** – „Każdy wielki serwer zaczynał od zera. Teraz nasza kolej.” – rosnący wykres graczy 1→2→5→20→100→???, logo, IP, „Premiera 24.12”, „Bądź jednym z pierwszych!”

Skrypt (obraz + dźwięk): `zrodla/video4.py`.

---

# Wersja 5 – „0 zł vs 20 zł” (pionowy, TikTok/Shorts/Reels, z dźwiękiem)

`Dziob-6mc-PL-0zl-vs-20zl-pionowy.mp4` – 32 s, **1080×1920 (9:16)**, 30 fps, AAC. Młodzieżowy, szybki montaż: napisy wyskakujące słowo po słowie, „uderzenia” zoomem na bit, białe błyski na cięciach, pasek postępu u góry, syntezowany bit trap (808, klaskanie, hi-haty) + efekty (kasa fiskalna, zatrzymanie płyty, boing, syrena).

1. **0–1,5 s** – hak: „CZEKAJ.” + oczy + „TO CIĘ ZASKOCZY”
2. **1,5–5 s** – „Żeby mieć chociaż 1000$ na anarchia.gg…” (saldo $0)
3. **5–8,5 s** – „…musisz wydać 20 zł*” – banknot wylatuje z portfela, saldo $1000, „-20 zł”
4. **8,5–12,5 s** – „A na Dziob.6mc.PL?” → „0 ZŁ. ZERO. NIC.” + deszcz monet, „nawet grosza”
5. **12,5–15,5 s** – beat staje: „no dobra… musisz opłacić PRĄD” + migająca żarówka, rachunek „płatne: rodzice :)”
6. **15,5–18,5 s** – „ALE NA ANARCHIA.GG TEŻ MUSISZ.” – żarówka = żarówka, „PRĄD: 1 : 1”
7. **18,5–22,5 s** – „Czyli: 20 zł + prąd vs 0 zł + prąd” → puchar, „DZIOB WYGRYWA O 20 ZŁ”, „20 zł = 1 kebab ;)”, konfetti
8. **22,5–27 s** – „Wszystko co musisz wiedzieć”: serwer, IP dziob.6mc.pl, premiera 24 grudnia (Wigilia), cena 0 zł, start od zera, Minecraft
9. **27–32 s** – logo, „WBIJAJ 24.12”, IP, „Wyślij to ziomkowi, który wydaje kasę na serwery”

Dopisek na ekranie (5–22,5 s): „*kwota wg ekipy Dziob.6mc.PL (10.2026)” – kwota dot. anarchia.gg pochodzi od ekipy serwera, nie była weryfikowana.

Skrypt (obraz + dźwięk): `zrodla/video5.py`.

---

# Wersja 6 – „Czat ekipy” (pionowy, z dźwiękiem)

`Dziob-6mc-PL-czat-ekipy-pionowy.mp4` – 34 s, **1080×1920 (9:16)**, 30 fps, AAC. Format „POV” + fałszywy czat grupowy + tier list. Syntezowany bit w stylu jersey club, dźwięki powiadomień i pisania.

1. **0–2,2 s** – „POV: twoja ekipa szuka serwera na święta” (pisane na żywo)
2. **2,2–20,5 s** – telefon z czatem „EKIPA NA ŚWIĘTA”: Kuba, Ola, Mati i Ty ustalają, gdzie grać w Wigilię → dziob.6mc.pl, premiera 24.12, start od zera, „ile kosztuje?” – „0 zł” – „CO” – „nawet twoja babcia” – „WBIJAMY!!!”, naklejka z ptakiem, „kto nie wbije ten stawia karpia”; wskaźnik pisania, serduszka-reakcje
3. **20,5–28 s** – TIER LIST „plany na Wigilię”: D kłótnia przy stole, C Kevin sam w domu po raz 30., B 12 potraw, A prezenty, **S PREMIERA DZIOB.6MC.PL** + konfetti
4. **28–34 s** – logo, „24.12”, „IP: dziob.6mc.pl”, „oznacz ekipę, z którą wbijasz”, „Minecraft • 0 zł • start od zera”

Skrypt (obraz + dźwięk): `zrodla/video6.py`.
