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
MOTD = (f"{S}6{S}l✦ DziobMc ✦ {S}r{S}e1.21 {S}8| {S}fDziob.fun\\n"
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
enforce-secure-profile=true
"""

START_SH = """#!/bin/bash
# DziobMc - start serwera (Linux / macOS)
# Wrzuć tu plik server.jar (Paper / Purpur / Vanilla 1.21 – 1.21.4)
cd "$(dirname "$0")"
while true; do
  java -Xms2G -Xmx4G -XX:+UseG1GC -jar server.jar nogui
  echo "Serwer wyłączony. Restart za 5 sekund (Ctrl+C aby anulować)..."
  sleep 5
done
"""

START_BAT = """@echo off
title DziobMc - Dziob.fun
REM Wrzuc tu plik server.jar (Paper / Purpur / Vanilla 1.21 - 1.21.4)
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
    pl = out / "plugins-konfiguracja"
    pl.mkdir(exist_ok=True)
    (pl / "TAB-config-fragment.yml").write_text(TAB_YML, encoding="utf-8")
    (pl / "TAB-groups.yml").write_text(TAB_GROUPS, encoding="utf-8")
    (pl / "LuckPerms-komendy.txt").write_text(LUCKPERMS, encoding="utf-8")
    ikona(out / "server-icon.png")
