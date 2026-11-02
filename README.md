# 🐦 DziobSi – Dziob Inteligence

Aplikacja AI na telefon (PWA) ze słownikiem **500 000 polskich słów**.

## Co potrafi
- **Czat AI** – offline odpowiada wbudowany „mózg” DziobSi; po dodaniu klucza
  Gemini (⚙️ Ustawienia) odpowiada na każde pytanie jak pełne AI (Gemini).
- **500 000 słów** (`data/slowa.txt`) – posortowane od najczęściej używanych:
  sprawdzanie pisowni i podpowiedzi poprawek, rymy, słowa na / kończące się na…,
  losowe słowa.
- **Słownik** – wyszukiwarka po 500 000 słowach (także wzorce `kot*`, `*ość`).
- Kalkulator, godzina, data.
- Działa **offline** i instaluje się na ekranie głównym telefonu (Android i iPhone).

## Jak zainstalować na telefonie
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
