# 🐦 DziobSi – Dziob Inteligence

Aplikacja AI na telefon (PWA + APK) ze słownikiem **5 000 000 słów**.

## Wersja
Aktualna wersja: **2.3.0** (widoczna w aplikacji: ekran startowy i Ustawienia → Wersja aplikacji).

## Co potrafi
- **Pamięć** (`memory.js`) – DziobSi zapamiętuje fakty o użytkowniku (imię, wiek, miasto, co lubi
  i czego nie, zwierzęta, rodzeństwo, „zapamiętaj…”), także po zamknięciu aplikacji. Mózg AI dostaje
  je w instrukcji, a rozmowa (ostatnie wymiany) też jest zapamiętywana. „Co o mnie wiesz?” wypisuje
  pamięć, „zapomnij wszystko” ją czyści; podgląd i usuwanie w Ustawieniach → Pamięć.
- **Rozmowa zamiast „znam to słowo”** – DziobSi nie komentuje słów, tylko rozmawia. Słownik działa w tle
  (poprawianie literówek) i w zakładce Słownik. Dopóki Mózg AI nie jest pobrany, w czacie widać baner
  „Włącz pełny Mózg AI”, a pod odpowiedziami znacznik „⚡ Tryb podstawowy” / „🧠 Mózg AI”.
- **Mózg AI w telefonie** (`llm.js`) – polski model językowy **Bielik 1.5B** (SpeakLeash, Q4_K_M ~973 MB)
  uruchamiany lokalnie przez [wllama](https://github.com/ngxson/wllama) (llama.cpp w WebAssembly).
  Czyta wiadomość i sam układa odpowiedź; gdy użytkownik nie pyta – po prostu rozmawia.
  Pobiera się raz (Ustawienia → Mózg AI), potem działa bez internetu. Słownik 5 000 000 słów
  podpowiada modelowi poprawki literówek użytkownika i poprawia pisownię odpowiedzi modelu. Bez pobranego modelu działa mózg na regułach.
- Każda odpowiedź kończy się: *„Jeśli masz jeszcze jakieś zapytanie, pytaj – jestem otwarty na wszystko! 🐦”*
- **Wygląd** – ciepły, spokojny styl (kremowy / grafitowy, szeryfowa czcionka odpowiedzi)
  z efektem **Liquid Glass** (szklane, rozmyte panele i pływający pasek zakładek);
  motyw jasny, ciemny lub automatyczny.
- **Krótkie odpowiedzi** – DziobSi odpowiada zwięźle.
- **Rozmowa** (`talk.js`) – odpowiada na pytania o siebie („lubisz mnie?” → „Tak, bardzo cię lubię! 💛”),
  pytania tak/nie z odmianą czasownika (lubisz → lubię, możesz → mogę), uczucia, ulubione rzeczy,
  stolice, ciekawostki, krótkie definicje; zapamiętuje imię użytkownika.
- **DziobSi Code** – opisz, co zbudować („gra”, „kalkulator”, „lista zadań”, „zegar”, „strona”…),
  a DziobSi wstawi kod do edytora z podglądem na żywo. W czacie: „napisz pętlę w python”,
  „zrób grę” – kod z przyciskami *Kopiuj* i *Otwórz w Code*.
- **Samodzielne AI** – odpowiada wyłącznie własny „mózg” DziobSi, bez internetu
  i bez wspomagania innymi AI.
- **Analiza słów** – każde słowo, nawet spoza słownika, DziobSi krótko rozbiera:
  część mowy, przedrostki, złożenia, podobne słowa, możliwa literówka.
- **Blokada wulgaryzmów** – na wiadomości z niecenzuralnymi słowami DziobSi nie odpowiada
  (wykrywa też zapisy typu `k.u.r.w.a`, `chuuuj`, `kórwa`); słownik jest z nich oczyszczony.
- **5 000 000 słów** (`data/slownik.bin`, ~22 MB) – polskie słowa ze wszystkimi odmianami
  i angielskie; zapisane posortowane, z kodowaniem przedrostkowym w blokach po 32 słowa
  (`bigdict.js`): w pamięci zostają spakowane, a sprawdzenie słowa to wyszukiwanie binarne
  i rozpakowanie jednego bloku (ułamek milisekundy).
- **500 000 najczęstszych słów** (`data/slowa.txt`) – ranking popularności, rymy, losowanie:
  sprawdzanie pisowni i podpowiedzi poprawek, rymy, słowa na / kończące się na…,
  losowe słowa.
- **Słownik** – wyszukiwarka po 5 000 000 słowach (także wzorce `kot*`, `k?t`); najpierw popularne.
- Kalkulator, godzina, data.
- Działa **offline** i instaluje się na ekranie głównym telefonu (Android i iPhone).

## APK (Android)
Workflow `.github/workflows/apk.yml` buduje **DziobSi.apk** przy każdym pushu
(projekt Capacitor w `android/`). Plik pobierzesz z zakładki **Releases**
(albo z artefaktów w zakładce Actions). Na telefonie: pobierz → otwórz → zainstaluj
(zezwól na instalację z nieznanych źródeł).

Lokalnie (z Android SDK): `npm ci && npm run build && npx cap sync android && cd android && ./gradlew assembleDebug`.

## Wersja przeglądarkowa (PWA)
1. Włącz GitHub Pages: *Settings → Pages → Source: GitHub Actions*.
   Workflow `.github/workflows/pages.yml` opublikuje aplikację.
2. Otwórz adres strony na telefonie
   (np. `https://<twoj-login>.github.io/<nazwa-repo>/`).
3. Android/Chrome: „Zainstaluj aplikację”. iPhone/Safari: Udostępnij → „Do ekranu początkowego”.

## Uruchomienie lokalnie
```
python3 -m http.server 8000
```
i otwórz http://localhost:8000

## Źródła słów (5 000 000)
| Źródło | Słów | Licencja |
|---|---:|---|
| [SJP.pl – słownik do gier](https://sjp.pl/sl/growy/) (przez [kamilmielnik/scrabble-dictionaries](https://github.com/kamilmielnik/scrabble-dictionaries)) – polski z odmianami | 3 219 043 | GPL 2 / LGPL 2.1 / CC BY 4.0 / MPL 1.1 / Apache 2.0 |
| [FrequencyWords](https://github.com/hermitdave/FrequencyWords) (OpenSubtitles) – polski 2018 + 2016 | 826 286 | CC BY-SA 4.0 |
| [dwyl/english-words](https://github.com/dwyl/english-words) – angielski | 312 919 | Unlicense |
| FrequencyWords – angielski | 641 752 | CC BY-SA 4.0 |

Wulgaryzmy (polskie i angielskie) są usunięte. Słowa z list częstości pochodzą z napisów
filmowych – są tam też imiona, nazwy i rzadkie formy potoczne.
Skrypt budujący: kolejność SJP → polskie listy częstości → angielski słownik → angielska lista częstości, aż do 5 000 000.
