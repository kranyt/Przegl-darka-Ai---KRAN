# Państwa – plugin Paper 1.21.x

Państwa, chunki, wojny z armią/dronami/samolotami/jetami oraz giełda akcji farm.

## Instalacja
1. Wrzuć `Panstwa-1.0.0.jar` do folderu `plugins/` serwera Paper 1.21 – 1.21.x (Java 21).
2. Uruchom serwer. Konfiguracja: `plugins/Panstwa/config.yml` (koszty, HP, prędkości, szanse giełdy).
3. Dane zapisują się w `plugins/Panstwa/panstwa.yml` i `plugins/Panstwa/gielda.yml`.

Budowanie ze źródeł: `mvn package` → `target/Panstwa-1.0.0.jar`.

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

## Wojna
- Wpisujesz `/p wojna` stojąc na chunku wroga. Cała twoja armia (max 30 jednostek danego typu, do zmiany w configu) wyrusza z twojego najbliższego chunka, a armia obrońcy z jego najbliższego chunka.
- Jednostki **nie teleportują się** – żołnierze idą (pathfinding), drony/samoloty/jety lecą nad terenem z prędkością = wielokrotność prędkości chodu gracza.
- Jeśli cel jest dalej niż **16 chunków**, żołnierze nie dosięgają – lecą tylko drony, samoloty i jety.
- Jednostki walczą z jednostkami przeciwnika i z wrogim graczem. Gracz nie musi mieć armii – może walczyć sam.
- Chunk zostaje przejęty, gdy atakujący (gracz albo jego jednostki) jest na nim **10 sekund** bez żadnego obrońcy. Postęp widać na pasku bossbar.
- Po zakończeniu wojny ocalałe jednostki wracają do armii, zabite przepadają. Wojna kończy się porażką atakującego po 10 minutach.

## Giełda
- Akcja = jedna kolumna bloków (od samej góry do samego dołu) w chunku twojego państwa, w której jest farma (pszenica, marchew, ziemniaki, buraki, brodawki, kakao, jagody, melon/dynia, trzcina, kaktus, bambus, kelp).
- `/p gielda` stojąc na takiej kolumnie: wybierasz cenę (jako właściciel państwa ustalasz pierwszą cenę) i liczbę akcji (kolejne kolumny z farmą w tym chunku, od najbliższej).
- Kupujący płaci sprzedającemu diamentami (gracze offline dostaną je po wejściu na serwer).
- Posiadacz akcji co **3 minuty** dostaje plony z tej kolumny; po **2 minutach** rośliny same się sadzą od nowa.
- Co **5 minut** serwer zmienia ceny: 30% – akcja znika, 35% – tanieje o 30-70%, 35% – drożeje o 15-110%.

## Ochrona
Na chunkach państwa tylko właściciel może niszczyć i stawiać bloki, otwierać skrzynie itp. Wybuchy, ogień i tłoki nie niszczą chunków państw. Uprawnienie `panstwa.admin` (domyślnie OP) pozwala ominąć ochronę.
