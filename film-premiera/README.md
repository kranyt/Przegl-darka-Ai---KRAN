# Dziob.6mc.PL – film na premierę serwera

`Dziob-6mc-PL-premiera.mp4` – 47 s, 1920×1080, 30 fps, H.264 + AAC.

Sceny:
1. **0–6,6 s** – nocny pikselowy świat, „6MC.PL przedstawia…”
2. **6,6–14,8 s** – logo DZIOB budowane ze spadających bloków złota i trawy, promienie światła, fajerwerki
3. **14,8–25,4 s** – „Co czeka na serwerze?” – karty w stylu GUI Minecrafta + toast „Osiągnięcie zdobyte!”
4. **25,4–33 s** – odliczanie 3‑2‑1 przy migającym TNT, wybuch, „START! Serwer już działa!”
5. **33–47 s** – wpis z listy serwerów, `IP: DZIOB.6MC.PL`, żółty splash „Premiera!”, fajerwerki, plansza końcowa

Dźwięk: dostarczony lektor (ElevenLabs) + wygenerowana muzyka (pad, bas, perkusja, arpeggio) z automatycznym ściszaniem pod głos oraz efekty (uderzenia bloków, narastanie, wybuch TNT, fajerwerki).

## Ponowne renderowanie
Skrypty w `zrodla/` (Python 3, numpy, Pillow, ffmpeg; czcionki pikselowe Press Start 2P / Pixelify Sans z paczek @fontsource w katalogu `../fonts`):
```
python3 music.py <katalog_build> voice.mp3   # -> mix.wav, mix.npy
python3 video.py wynik.mp4
```
Teksty kart funkcji są w `CARDS` w `video.py`.
