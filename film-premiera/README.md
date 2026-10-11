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
