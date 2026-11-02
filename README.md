# 🐦 DziobSi – Dziob Inteligence

Aplikacja AI na telefon (PWA) ze słownikiem **500 000 polskich słów**.

## Co potrafi
- **Samodzielne AI** – odpowiada wyłącznie własny „mózg” DziobSi, bez internetu
  i bez wspomagania innymi AI.
- **Analiza nieznanych słów** – część mowy, budowa, przedrostki, złożenia,
  rdzeń i rodzina wyrazów, podpowiedzi literówek, werdykt.
- **Blokada wulgaryzmów** – na wiadomości z niecenzuralnymi słowami DziobSi nie odpowiada
  (wykrywa też zapisy typu `k.u.r.w.a`, `chuuuj`, `kórwa`); słownik jest z nich oczyszczony.
- **500 000 słów** (`data/slowa.txt`) – posortowane od najczęściej używanych:
  sprawdzanie pisowni i podpowiedzi poprawek, rymy, słowa na / kończące się na…,
  losowe słowa.
- **Słownik** – wyszukiwarka po 500 000 słowach (także wzorce `kot*`, `*ość`).
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

Źródło listy słów: FrequencyWords (H. Dave, licencja CC BY-SA 4.0, na podstawie OpenSubtitles),
przefiltrowane do 500 000 słów złożonych z polskich liter.
