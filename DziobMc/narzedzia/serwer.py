"""Pliki serwera: server.properties, skrypty startowe, ikona, konfiguracje pluginów."""
from pathlib import Path


def esc(s):
    """Escapowanie do server.properties (ISO-8859-1 + \\uXXXX)."""
    out = []
    for ch in s:
        if ord(ch) > 126:
            out.append("\\u%04X" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)


S = "§"
MOTD = (f"{S}6{S}l✦ DziobMc ✦ {S}r{S}e1.16.4-1.21+ {S}8| {S}fDziob.fun\\n"
        f"{S}a⚔ Custom Moby {S}8• {S}cEventy {S}8• {S}dRangi {S}8• {S}6Sklep")

PROPERTIES = f"""#DziobMc - Dziob.fun
motd={esc(MOTD)}
level-name=DziobMc
server-port=25565
max-players=100
gamemode=survival
difficulty=normal
pvp=true
online-mode=true
enable-command-block=true
spawn-protection=0
allow-flight=true
view-distance=10
simulation-distance=8
spawn-monsters=true
spawn-animals=true
white-list=false
enforce-secure-profile=false
"""

START_SH = """#!/bin/bash
# DziobMc - start serwera (Linux / macOS)
# Wrzuć tu plik server.jar = Paper 1.21.4 (wymaga Java 21)
cd "$(dirname "$0")"
while true; do
  java -Xms2G -Xmx4G -XX:+UseG1GC -jar server.jar nogui
  echo "Serwer wyłączony. Restart za 5 sekund (Ctrl+C aby anulować)..."
  sleep 5
done
"""

START_BAT = """@echo off
title DziobMc - Dziob.fun
REM Wrzuc tu plik server.jar = Paper 1.21.4 (wymaga Java 21)
:start
java -Xms2G -Xmx4G -XX:+UseG1GC -jar server.jar nogui
echo Serwer wylaczony. Restart za 5 sekund...
timeout /t 5
goto start
"""

TAB_YML = """# ==========================================================
#  DziobMc – fragment konfiguracji pluginu TAB (NEZNAMY)
#  Skopiuj sekcje do plugins/TAB/config.yml (zastąp istniejące)
#  https://github.com/NEZNAMY/TAB
# ==========================================================
header-footer:
  enabled: true
  header:
  - ""
  - "&6&l✦ &e&lD&6&lz&e&li&6&lo&e&lb&6&lM&e&lc &6&l✦"
  - "&7Najbardziej epicki serwer survival!"
  - "&8&m                                        "
  - ""
  footer:
  - ""
  - "&8&m                                        "
  - "&7Online: &a%online%&7/&a%maxplayers%  &8|  &7Ping: &a%ping%ms"
  - "&7Ranga: %luckperms-prefix%"
  - "&6⛃ &eSklep z rangami: &6&lDziob.fun"
  - "&9Discord: &bdiscord.gg/TWOJ-LINK"
  - ""

# Prefiksy rang w TAB i nad głową – bierze je z LuckPerms
scoreboard-teams:
  enabled: true
  sorting-types:
  - "GROUPS:wlasciciel,admin,moderator,helper,youtuber,legenda,mvp,vip,default"
  - "PLACEHOLDER_A_TO_Z:%player%"

tablist-name-formatting:
  enabled: true
"""

TAB_GROUPS = """# DziobMc – plugins/TAB/groups.yml
_DEFAULT_:
  tabprefix: "&8[&7GRACZ&8] &7"
  tagprefix: "&8[&7GRACZ&8] &7"
wlasciciel:
  tabprefix: "&8[&4&lWŁAŚCICIEL&8] &c"
  tagprefix: "&8[&4&lWŁAŚCICIEL&8] &c"
admin:
  tabprefix: "&8[&c&lADMIN&8] &c"
  tagprefix: "&8[&c&lADMIN&8] &c"
moderator:
  tabprefix: "&8[&2&lMOD&8] &a"
  tagprefix: "&8[&2&lMOD&8] &a"
helper:
  tabprefix: "&8[&b&lHELPER&8] &b"
  tagprefix: "&8[&b&lHELPER&8] &b"
youtuber:
  tabprefix: "&8[&f&lY&c&lT&8] &f"
  tagprefix: "&8[&f&lY&c&lT&8] &f"
legenda:
  tabprefix: "&8[&d&lLEGENDA&8] &d"
  tagprefix: "&8[&d&lLEGENDA&8] &d"
mvp:
  tabprefix: "&8[&6&lMVP&8] &6"
  tagprefix: "&8[&6&lMVP&8] &6"
vip:
  tabprefix: "&8[&e&lVIP&8] &e"
  tagprefix: "&8[&e&lVIP&8] &e"
"""

LUCKPERMS = """# ==========================================================
#  DziobMc – rangi w LuckPerms (opcjonalnie, dla Paper/Spigot)
#  Wklej te komendy po kolei w konsoli serwera.
#  UWAGA: datapack ma własne rangi (drużyny) – działają też bez pluginów.
# ==========================================================
lp creategroup vip
lp creategroup mvp
lp creategroup legenda
lp creategroup youtuber
lp creategroup helper
lp creategroup moderator
lp creategroup admin
lp creategroup wlasciciel

lp group vip parent add default
lp group mvp parent add vip
lp group legenda parent add mvp
lp group youtuber parent add mvp
lp group helper parent add default
lp group moderator parent add helper
lp group admin parent add moderator
lp group wlasciciel parent add admin

lp group default meta setprefix 10 "&8[&7GRACZ&8] &7"
lp group vip meta setprefix 20 "&8[&e&lVIP&8] &e"
lp group mvp meta setprefix 30 "&8[&6&lMVP&8] &6"
lp group legenda meta setprefix 40 "&8[&d&lLEGENDA&8] &d"
lp group youtuber meta setprefix 40 "&8[&f&lY&c&lT&8] &f"
lp group helper meta setprefix 50 "&8[&b&lHELPER&8] &b"
lp group moderator meta setprefix 60 "&8[&2&lMOD&8] &a"
lp group admin meta setprefix 70 "&8[&c&lADMIN&8] &c"
lp group wlasciciel meta setprefix 80 "&8[&4&lWŁAŚCICIEL&8] &c"

# Uprawnienia przykładowe
lp group helper permission set minecraft.command.kick true
lp group moderator permission set minecraft.command.ban true
lp group admin permission set minecraft.command.gamemode true
lp group admin permission set minecraft.command.function true
lp group wlasciciel permission set * true

# Nadanie rangi graczowi (plugin + datapack):
#   lp user NICK parent set vip
#   execute as NICK run function dziobmc:rangi/ustaw/vip
"""


PLUGINY_TXT = """==========================================================
  WRZUĆ TUTAJ PLUGINY (pliki .jar)
==========================================================

OBOWIĄZKOWE – dzięki nim wejdą gracze od 1.16.4 do najnowszej wersji:

  1. ViaVersion    -> https://modrinth.com/plugin/viaversion
                      (wpuszcza NOWSZE wersje niż serwer, np. 1.21.5, 1.21.10...)
  2. ViaBackwards  -> https://modrinth.com/plugin/viabackwards
                      (wpuszcza STARSZE wersje: 1.16.4 ... 1.21.3)

  Pobierz najnowszą wersję każdego (plik .jar, wersja dla Paper)
  i wrzuć oba pliki .jar DO TEGO FOLDERU.

OPCJONALNE (ładniejszy TAB i rangi z uprawnieniami):

  3. TAB           -> https://modrinth.com/plugin/tab-was-taken
  4. LuckPerms     -> https://luckperms.net/download

  Konfiguracja do nich jest w folderze: dodatki-pluginy/

Po wrzuceniu pluginów zrestartuj serwer.
Aktualizuj ViaVersion/ViaBackwards, gdy wyjdzie nowa wersja Minecrafta –
wtedy gracze z tą wersją też wejdą.
"""

GDZIE_TXT = """==========================================================
   DziobMc – GDZIE CO DAĆ  (IP: Dziob.fun)
==========================================================

Folder serwera po rozpakowaniu DziobMc-Serwer.zip:

DziobMc-Serwer/
|
|-- server.jar            <-- [1] TY WRZUCASZ: Paper 1.21.4
|                              https://papermc.io/downloads/paper
|                              (wybierz 1.21.4, zmień nazwę pliku na server.jar)
|
|-- plugins/              <-- [2] TY WRZUCASZ: ViaVersion.jar + ViaBackwards.jar
|   `-- WRZUC-TUTAJ-PLUGINY.txt     (linki w środku)
|
|-- eula.txt              <-- [3] TY ZMIENIASZ: eula=false  ->  eula=true
|
|-- start.bat             <-- [4] Windows: kliknij 2x, żeby włączyć serwer
|-- start.sh              <--     Linux/Mac:  ./start.sh
|
|-- DziobMc/              <-- świat (mapa). NIE RUSZAJ.
|   `-- datapacks/
|       `-- DziobMc-Pack/      <-- cała paczka: moby, eventy, rangi, sklep...
|
|-- server.properties     <-- ustawienia (MOTD, sloty, port 25565) – gotowe
|-- server-icon.png       <-- ikonka serwera na liście – gotowa
`-- dodatki-pluginy/      <-- opcjonalnie: konfiguracja TAB i LuckPerms

----------------------------------------------------------
KROKI:
  1. Zainstaluj Java 21  -> https://adoptium.net
  2. Wrzuć server.jar (Paper 1.21.4)            [1]
  3. Wrzuć ViaVersion i ViaBackwards do plugins/ [2]
  4. eula=true                                   [3]
  5. Uruchom start.bat / start.sh                [4]
  6. Poczekaj ~10 s – mapa lobby zbuduje się sama.
  7. W konsoli serwera wpisz:
        op TwojNick
        execute as TwojNick run function dziobmc:rangi/ustaw/wlasciciel
  8. W grze: /function dziobmc:admin/panel   (panel admina)

DOMENA Dziob.fun:
  W panelu domeny dodaj rekord A:  Dziob.fun -> IP twojego serwera
  (jeśli port inny niż 25565, dodaj rekord SRV _minecraft._tcp).

WERSJE GRACZY: 1.16.4 -> najnowsza (dzięki ViaVersion + ViaBackwards).
Gracze na starszych wersjach (np. 1.16) mogą widzieć drobne różnice:
numerki w scoreboardzie, napisy-hologramy wyglądają trochę inaczej,
NPC trzeba zastąpić komendą /trigger (np. /trigger sklep).
"""


def ikona(path: Path):
    """64x64 ikona serwera – złoty dziób na ciemnym tle."""
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (64, 64), (20, 16, 30, 255))
    d = ImageDraw.Draw(img)
    for r in range(32, 0, -1):
        c = int(30 + (32 - r) * 2.2)
        d.ellipse([32 - r, 32 - r, 32 + r, 32 + r], fill=(c, int(c * 0.6), 20, 255))
    d.ellipse([6, 6, 58, 58], outline=(255, 200, 40, 255), width=3)
    d.polygon([(18, 22), (52, 32), (18, 42)], fill=(255, 170, 0, 255), outline=(120, 60, 0, 255))
    d.line([(18, 32), (46, 32)], fill=(150, 80, 0, 255), width=2)
    d.ellipse([12, 14, 22, 24], fill=(255, 255, 255, 255))
    d.ellipse([15, 17, 20, 22], fill=(0, 0, 0, 255))
    for x, y in [(50, 12), (54, 50), (10, 52)]:
        d.polygon([(x, y - 4), (x + 1, y - 1), (x + 4, y), (x + 1, y + 1), (x, y + 4), (x - 1, y + 1), (x - 4, y), (x - 1, y - 1)], fill=(255, 240, 120, 255))
    img.save(path)


def build(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    (out / "server.properties").write_text(PROPERTIES, encoding="latin-1")
    (out / "start.sh").write_text(START_SH, encoding="utf-8")
    (out / "start.sh").chmod(0o755)
    (out / "start.bat").write_text(START_BAT.replace("\n", "\r\n"), encoding="ascii")
    (out / "eula.txt").write_text(
        "# Przeczytaj https://aka.ms/MinecraftEULA i zmien na eula=true jesli akceptujesz.\neula=false\n",
        encoding="ascii")
    pl = out / "dodatki-pluginy"
    pl.mkdir(exist_ok=True)
    (pl / "TAB-config-fragment.yml").write_text(TAB_YML, encoding="utf-8")
    (pl / "TAB-groups.yml").write_text(TAB_GROUPS, encoding="utf-8")
    (pl / "LuckPerms-komendy.txt").write_text(LUCKPERMS, encoding="utf-8")
    ikona(out / "server-icon.png")
    (out / "plugins").mkdir(exist_ok=True)
    (out / "plugins" / "WRZUC-TUTAJ-PLUGINY.txt").write_text(PLUGINY_TXT, encoding="utf-8")
    (out / "GDZIE-CO-DAC.txt").write_text(GDZIE_TXT, encoding="utf-8")
