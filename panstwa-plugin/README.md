# Państwa – plugin Paper 1.21.x

Państwa, chunki, wojny z armią/dronami/samolotami/jetami oraz giełda akcji farm.

## Instalacja
1. Wrzuć `Panstwa-1.4.0.jar` do folderu `plugins/` serwera Paper 1.21 – 1.21.x (Java 21).
2. Uruchom serwer. Konfiguracja: `plugins/Panstwa/config.yml` (koszty, HP, prędkości, szanse giełdy).
3. Dane zapisują się w `plugins/Panstwa/panstwa.yml` i `plugins/Panstwa/gielda.yml`.

Budowanie ze źródeł: `mvn package` → `target/Panstwa-1.4.0.jar`.

## Komendy
| Komenda | Opis |
|---|---|
| `/p fundament` | Menu: 64x Dirt + 64x Drewno dębowe → dostajesz **Fundament** (beacon). Postawienie go zakłada państwo i daje chunk, którego nikt nie może zniszczyć. |
| *(zniszczenie fundamentu)* | Właściciel dostaje menu „Czy chcesz usunąć państwo?” – zielona wełna = TAK, czerwona = NIE. Inni nie mogą go zniszczyć. |
| `/p chunk` | Menu: 32x diament → kupujesz chunk, na którym stoisz. |
| `/p wojna` | Atak na cudzy chunk, na którym stoisz (państwo musi mieć >1 chunk; chunk z fundamentem jest nie do podbicia). |
| `/p pokoj` | Wycofanie się z ataku. |
| `/p armia` | Pierwszy zakup: 5 diamentów = 5 żołnierzy, potem 5 diamentów = 1 żołnierz. Żołnierz: 24 HP (12 serc), prędkość jak gracz. |
| `/p drony` | 1 dron = 64x + 64x diamentów (128). 68 HP, prędkość 3. |
| `/p samolot` | 1 samolot = 4x 64 diamenty (256). 120 HP, prędkość 4. |
| `/p jet` | 1 jet = 8x 64 diamenty (512). 256 HP, prędkość 8. |
| `/p gielda` | Wystaw akcje farmy (patrz niżej). |
| `/akcje` | Rynek – kupowanie akcji. |
| `/sprzedajakcje [id]` | Sprzedaj akcję serwerowi po aktualnej cenie (bez id otwiera menu). |
| `/mojeakcje` | Lista twoich akcji z cenami. |
| `/p nazwa <nazwa>`, `/p pomoc` | Zmiana nazwy państwa, pomoc. |

### Komendy informacyjne
| Komenda | Opis |
|---|---|
| `/p info [państwo\|gracz]` lub `/kraj [państwo\|gracz]` | Informacje o państwie: właściciel (online/offline), miejsce w rankingu, chunki, fundament, armia, siła armii, akcje, wojny. Bez argumentu – twoje państwo. |
| `/p tutaj` | Do kogo należy chunk, na którym stoisz, czy można go podbić, odległość od twojego państwa (czy żołnierze dosięgną), czy trwa tu wojna, czy kolumna jest akcją. |
| `/p chunki [państwo]` | Lista chunków państwa z koordynatami. |
| `/p mapa` | Mapa chunków dookoła w czacie (twoje na zielono, inne państwa w kolorach, ★ fundament, ⚔ wojna). |
| `/p wojny` | Wszystkie trwające wojny i ile jednostek zostało każdej stronie. |
| `/p ranking` (`/p top`) | Top 10 państw (chunki, potem siła armii). |
| `/p lista` | Wszystkie państwa. |
| `/p gracz <nick>` | Państwo i akcje gracza. |
| `/p akcja <id>` | Szczegóły akcji (cena, posiadacz, kolumna, uprawa). |

## Członkowie
| Komenda | Opis |
|---|---|
| `/p zapros <gracz>` | Właściciel zaprasza gracza (online) – zaproszenie ważne 2 minuty. |
| `/p akceptuj` / `/p odrzuc` | Przyjęcie / odrzucenie zaproszenia. |
| `/p wyrzuc <gracz>` | Właściciel wyrzuca członka. |
| `/p opusc` | Członek opuszcza państwo. |
| `/p czlonkowie [państwo]` | Lista członków (online/offline). |

Gracz może należeć tylko do jednego państwa (max 10 członków + właściciel, do zmiany w configu).
Członkowie mogą budować i otwierać skrzynie na terenie państwa, kupować chunki i jednostki dla państwa, rozpoczynać wojny (`/p wojna`, `/p pokoj`), płacić za państwo i walczyć – liczą się przy przejmowaniu i obronie chunka, a jednostki wroga ich atakują.
Tylko właściciel może: zapraszać/wyrzucać, zmieniać nazwę, wystawiać akcje (`/p gielda`) i usunąć państwo (zniszczenie fundamentu).

## Opłata za państwo
- Państwo trzeba opłacać **64 diamentami co 7 dni** – komenda `/p oplata` (menu z czasem do końca i przyciskiem zapłaty). Płacić może każdy członek, można zapłacić do 4 okresów z góry.
- Nowe państwo jest opłacone na pierwsze 7 dni.
- Ostrzeżenia na czacie 24h, 6h, 1h i 10 min przed końcem oraz przy wejściu na serwer, gdy zostało mniej niż 24h.
- Jeśli nikt nie zapłaci, państwo **wygasa**: zostaje usunięte razem z fundamentem, chunkami i armią, a trwające wojny się kończą.
- Czas opłaty widać też w `/p info`.

## Wojna
- Wpisujesz `/p wojna` stojąc na chunku wroga. Cała twoja armia (max 30 jednostek danego typu, do zmiany w configu) wyrusza z twojego najbliższego chunka, a armia obrońcy z jego najbliższego chunka.
- Jednostki **nie teleportują się** – żołnierze idą (pathfinding), drony/samoloty/jety lecą nad terenem z prędkością = wielokrotność prędkości chodu gracza.
- Jeśli cel jest dalej niż **16 chunków**, żołnierze nie dosięgają – lecą tylko drony, samoloty i jety.
- Jednostki walczą z jednostkami przeciwnika i z wrogim graczem. Gracz nie musi mieć armii – może walczyć sam.
- Drony, samoloty i jety lecą nisko (5 bloków nad ziemią, `wojna.wysokosc-lotu`) i świecą (glowing), żeby było je widać.
- Chunk zostaje przejęty, gdy atakujący (gracz albo jego jednostki) jest na nim **10 sekund** bez żadnego obrońcy. Postęp widać na pasku bossbar.
- Po zakończeniu wojny ocalałe jednostki wracają do armii, zabite przepadają. Wojna kończy się porażką atakującego po 10 minutach.

## Giełda
- Akcja = jedna kolumna bloków (od samej góry do samego dołu) w chunku twojego państwa, w której jest farma (pszenica, marchew, ziemniaki, buraki, brodawki, kakao, jagody, melon/dynia, trzcina, kaktus, bambus, kelp).
- `/p gielda` stojąc na takiej kolumnie: wybierasz cenę (jako właściciel państwa ustalasz pierwszą cenę) i liczbę akcji (kolejne kolumny z farmą w tym chunku, od najbliższej).
- Kupujący płaci sprzedającemu diamentami (gracze offline dostaną je po wejściu na serwer).
- Posiadacz akcji co **3 minuty** dostaje plony z tej kolumny; po **2 minutach** rośliny same się sadzą od nowa.

### Ceny akcji
- Ceny zmieniają się **stopniowo**: co **3 minuty** cena robi mały krok (1–3%) w stronę celu aktualnego trendu – nie ma nagłych skoków o 40%.
- Gdy trend się skończy, losowany jest nowy:
  - **tania** akcja (tańsza niż większość, czyli poniżej mediany): 5% wygasa, 20% tanieje, 75% drożeje,
  - **droga** akcja: 15% wygasa, 35% tanieje, 50% drożeje.
- Wielkość trendu: drożenie najczęściej o 5–16%, rzadko o 17–60%; tanienie często o 5–15%, rzadko o 16–30%, bardzo rzadko o 31–80%.
- **Najpopularniejsza farma** (rodzaj uprawy, którego akcje ma najwięcej różnych graczy, min. 2): szanse i wielkości są odwrócone –
  tania: 5% wygasa, **75% tanieje**, 20% drożeje; droga: 15% wygasa, **50% tanieje**, 35% drożeje;
  tanieje o 5–16% (rzadko 17–60%), a drożeje o 5–15% (rzadko 16–30%, bardzo rzadko 31–80%). W menu oznaczona ★.
- Jeśli właściciel państwa wystawi akcję taniej niż większość akcji, akcja od razu zaczyna drożeć.
- Akcja, której nikt nie kupi przez **24h**, wygasa.
- Gdy twoja akcja wygaśnie, informacja czeka na ciebie, dopóki jej nie zobaczysz – pokazuje się w `/mojeakcje`, `/akcje` i `/sprzedajakcje` (czerwona bariera + wiadomość), a po wejściu na serwer dostajesz przypomnienie.
- W menu każda akcja pokazuje trend (▲ rośnie / ▼ spada), czy jest tania czy droga i za ile wygaśnie.

## Znikające bloki
Bloki postawione **poza państwem** znikają po **10 minutach**. Po postawieniu takiego bloku na action barze pojawia się informacja, że blok zniknie za 10 minut. Zawartość skrzyń wypada na ziemię. Jeśli teren w międzyczasie stanie się częścią państwa, blok zostaje. Uprawnienie `panstwa.trwalebloki` wyłącza znikanie dla danego gracza; czas i włączenie – `znikajace-bloki` w configu.

## Garnizon
Gdy państwo nie walczy, jego armia jest widoczna w bazie: żołnierze chodzą wokół fundamentu, a drony, samoloty i jety krążą nad nim (max 6 widocznych każdego typu). Jednostki garnizonu są nieśmiertelne – to tylko pokaz armii. Gdy zaczyna się wojna, znikają z bazy i wyruszają do walki, a po wojnie ocalałe wracają. Ustawienia: `garnizon` w configu.

## Ochrona
Na chunkach państwa tylko właściciel i członkowie mogą niszczyć i stawiać bloki, otwierać skrzynie itp. Wybuchy, ogień i tłoki nie niszczą chunków państw.
Admin (uprawnienie `panstwa.admin`, domyślnie OP) może włączyć tryb omijania ochrony komendą `/p admin` – domyślnie jest wyłączony, więc OP gra normalnie.

**Uwaga:** na poziomie trudności *Peaceful* Minecraft usuwa jednostki (zombie/vex/phantom), więc wojsko nie działa – ustaw co najmniej `/difficulty easy`.
