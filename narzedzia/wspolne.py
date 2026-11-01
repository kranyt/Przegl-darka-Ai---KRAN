"""Wspólne narzędzia generatora paczki DziobMc."""
import json
import textwrap

NS = "dziobmc"
SPAWN = "0 151 18 180 0"          # x y z yaw pitch – punkt spawnu w lobby
ARENA = "0 151 -75"               # środek areny bossa
PARKOUR_START = "-29 151 0 90 0"  # start parkouru (patrzy na zachód)

FILES = {}  # ścieżka względna w datapacku -> zawartość


def J(obj):
    """Kompaktowy JSON (polskie znaki bez escapowania)."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def snbt_text(obj):
    """Komponent tekstowy jako string SNBT: '{"text":...}'."""
    s = J(obj)
    assert "'" not in s, s
    return "'" + s + "'"


def t(text, color=None, bold=None, italic=None, run=None, suggest=None,
      url=None, hover=None, underlined=None):
    d = {"text": text}
    if color:
        d["color"] = color
    if bold is not None:
        d["bold"] = bold
    if italic is not None:
        d["italic"] = italic
    if underlined is not None:
        d["underlined"] = underlined
    if run:
        d["clickEvent"] = {"action": "run_command", "value": run}
    if suggest:
        d["clickEvent"] = {"action": "suggest_command", "value": suggest}
    if url:
        d["clickEvent"] = {"action": "open_url", "value": url}
    if hover is not None:
        d["hoverEvent"] = {"action": "show_text", "contents": hover}
    return d


def sc(name, objective, color=None, bold=None):
    d = {"score": {"name": name, "objective": objective}}
    if color:
        d["color"] = color
    if bold is not None:
        d["bold"] = bold
    return d


def sel(selector, color=None):
    d = {"selector": selector}
    if color:
        d["color"] = color
    return d


def tellraw(target, *parts):
    return f"tellraw {target} {J(list(parts) if len(parts) != 1 else parts[0])}"


def _clean(text):
    lines = [ln.strip() for ln in textwrap.dedent(text).split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines) + "\n"


def fn(name, text):
    """Dodaj funkcję dziobmc:<name>."""
    FILES[f"data/{NS}/function/{name}.mcfunction"] = _clean(text)


def raw(path, text):
    FILES[path] = _clean(text)


def jfile(path, obj):
    FILES[path] = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


# --- przedmioty -------------------------------------------------------------

def item(iid, name=None, color="gold", ench=None, lore=None, glint=False,
         unbreakable=False, dye=None):
    """Przedmiot w składni komponentów 1.21 (do /give)."""
    comps = []
    if ench:
        lv = ",".join(f'"minecraft:{k}":{v}' for k, v in ench.items())
        comps.append(f"enchantments={{levels:{{{lv}}}}}")
    if name:
        comps.append("custom_name=" + snbt_text(
            {"text": name, "color": color, "italic": False, "bold": True}))
    if lore:
        comps.append("lore=[" + ",".join(
            snbt_text({"text": ln, "color": "gray", "italic": False})
            for ln in lore) + "]")
    if glint:
        comps.append("enchantment_glint_override=true")
    if unbreakable:
        comps.append("unbreakable={}")
    if dye is not None:
        comps.append(f"dyed_color={{rgb:{dye}}}")
    s = f"minecraft:{iid}"
    if comps:
        s += "[" + ",".join(comps) + "]"
    return s


def nbt_item(iid, ench=None, dye=None):
    """Przedmiot w NBT encji (HandItems/ArmorItems) – format 1.21."""
    comps = []
    if ench:
        lv = ",".join(f'"minecraft:{k}":{v}' for k, v in ench.items())
        comps.append(f'"minecraft:enchantments":{{levels:{{{lv}}}}}')
    if dye is not None:
        comps.append(f'"minecraft:dyed_color":{{rgb:{dye}}}')
    s = f'{{id:"minecraft:{iid}",count:1'
    if comps:
        s += ",components:{" + ",".join(comps) + "}"
    return s + "}"


def cooldown(objective, ticks):
    """Linie sprawdzające cooldown (gametime). Po nich cooldown jest ustawiony."""
    return f"""scoreboard players add @s {objective} 0
scoreboard players set #cd dz.data {ticks}
execute store result score #teraz dz.data run time query gametime
scoreboard players operation #roznica dz.data = #teraz dz.data
scoreboard players operation #roznica dz.data -= @s {objective}
execute if score #roznica dz.data < #cd dz.data run return run function {NS}:util/cooldown_info
scoreboard players operation @s {objective} = #teraz dz.data"""


def firework_cmd(pos="~ ~1 ~", colors=(16766720, 16744192), shape="large_ball"):
    cols = ",".join(str(c) for c in colors)
    return ("summon minecraft:firework_rocket " + pos +
            ' {LifeTime:18,FireworksItem:{id:"minecraft:firework_rocket",count:1,'
            'components:{"minecraft:fireworks":{flight_duration:1b,explosions:[{shape:"'
            + shape + '",colors:[I;' + cols + '],has_trail:true,has_twinkle:true}]}}}}')
