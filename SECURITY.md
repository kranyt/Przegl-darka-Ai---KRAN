# Bezpieczeństwo strony DziobHost.PL

## Co jest zabezpieczone w `index.html`
- **Content-Security-Policy** (hashe SHA-256 + `strict-dynamic`): wykonują się tylko nasze 3 skrypty
  i to, co one doładują (AdSense). Blokowane: wstrzyknięty kod (XSS), `eval`, `onerror=` itp.,
  wtyczki (`object-src 'none'`), podmiana `<base>`, wysyłanie formularzy na obce adresy.
- **Ochrona przed clickjackingiem**: strona ukrywa się, gdy ktoś osadzi ją w ramce.
- **Referrer-Policy**, wymuszanie HTTPS dla zasobów (`upgrade-insecure-requests`).
- Dane wpisywane przez użytkownika są wstawiane wyłącznie jako tekst (`textContent`), pola mają limity długości,
  adres serwera jest sprawdzany ponownie tuż przed utworzeniem.

## WAŻNE: po każdej zmianie w `<script>` uruchom
```
python3 tools/update-csp.py
```
Inaczej przeglądarka zablokuje zmieniony skrypt (inny hash). Zmiana ID reklam w atrybutach
`data-slot` / `data-seconds` przy `#adModal` oraz `data-ad-slot` reklam bocznych NIE wymaga tego kroku.

## Hosting (nagłówki HTTP - silniejsze niż `<meta>`)
- **Netlify / Cloudflare Pages**: plik `_headers` działa automatycznie.
- **Apache**: plik `.htaccess` (HTTPS, HSTS, blokada `.git`, `tools/`, plików ukrytych, listowania katalogów).
- **Nginx**: przepisz nagłówki z `_headers` do `add_header ... always;`.
- **GitHub Pages**: nie pozwala ustawiać nagłówków - działa tylko ochrona z `<meta>` i skryptu.

## Czego strona sama nie załatwi
- **Konta**: włącz 2FA na hostingu, domenie (rejestratorze), GitHubie, Google AdSense i Cloudflare.
- **Prawdziwy backend**: kreator i panel są teraz tylko podglądem w przeglądarce. Gdy powstanie prawdziwe
  tworzenie serwerów/logowanie, cała walidacja, limity i uprawnienia muszą być po stronie serwera
  (frontend da się zawsze obejść).
- **Domena**: włącz blokadę transferu i DNSSEC u rejestratora.
