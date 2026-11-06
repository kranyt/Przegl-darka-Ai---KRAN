package pl.kran.panstwa.command;

import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabExecutor;
import org.bukkit.entity.Player;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.model.Nation;
import pl.kran.panstwa.util.ChunkPos;
import pl.kran.panstwa.util.Msg;
import pl.kran.panstwa.war.UnitType;
import pl.kran.panstwa.war.War;

import java.util.ArrayList;
import java.util.List;

public class PCommand implements TabExecutor {
    private static final List<String> SUBS = List.of("fundament", "chunk", "wojna", "pokoj", "armia", "drony",
            "samolot", "jet", "gielda", "info", "nazwa", "lista", "pomoc");
    private final PanstwaPlugin plugin;

    public PCommand(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (!(sender instanceof Player p)) {
            sender.sendMessage("Tylko dla graczy.");
            return true;
        }
        String sub = args.length == 0 ? "pomoc" : args[0].toLowerCase();
        Nation n = plugin.nations().get(p.getUniqueId());
        switch (sub) {
            case "fundament" -> {
                if (n != null) {
                    Msg.send(p, "&cMasz juz panstwo &6" + n.getName() + "&c.");
                    return true;
                }
                plugin.menus().openFundament(p);
            }
            case "chunk" -> {
                if (needNation(p, n)) return true;
                plugin.menus().openChunk(p);
            }
            case "wojna" -> war(p, n);
            case "pokoj" -> {
                if (needNation(p, n)) return true;
                War w = plugin.wars().attackingWar(n.getOwner());
                if (w == null) {
                    Msg.send(p, "&cNie prowadzisz zadnego ataku.");
                    return true;
                }
                plugin.wars().end(w, false, n.getName() + " wycofalo sie z wojny o chunk " + w.getTarget() + ".");
            }
            case "armia" -> {
                if (needNation(p, n)) return true;
                plugin.menus().openArmy(p, n);
            }
            case "drony", "dron" -> unitShop(p, n, UnitType.DRONE);
            case "samolot", "samoloty" -> unitShop(p, n, UnitType.PLANE);
            case "jet", "jety" -> unitShop(p, n, UnitType.JET);
            case "gielda" -> stock(p, n);
            case "info" -> info(p);
            case "nazwa" -> {
                if (needNation(p, n)) return true;
                if (args.length < 2 || !args[1].matches("[A-Za-z0-9_ĄĆĘŁŃÓŚŹŻąćęłńóśźż]{3,16}")) {
                    Msg.send(p, "&cUzycie: /p nazwa <nazwa> &7(3-16 znakow, litery/cyfry/_)");
                    return true;
                }
                Nation other = plugin.nations().getByName(args[1]);
                if (other != null && other != n) {
                    Msg.send(p, "&cTaka nazwa jest juz zajeta.");
                    return true;
                }
                n.setName(args[1]);
                plugin.nations().save();
                Msg.send(p, "&aNazwa panstwa zmieniona na &6" + n.getName() + "&a.");
            }
            case "lista" -> {
                Msg.send(p, "&6Panstwa (" + plugin.nations().all().size() + "):");
                for (Nation x : plugin.nations().all()) {
                    Msg.raw(p, " &8- &6" + x.getName() + " &7wlasciciel: &f" + plugin.menus().holderName(x.getOwner())
                            + " &7chunki: &f" + x.getChunks().size());
                }
            }
            default -> help(p);
        }
        return true;
    }

    private boolean needNation(Player p, Nation n) {
        if (n == null) {
            Msg.send(p, "&cNie masz panstwa! Zaloz je: &f/p fundament");
            return true;
        }
        return false;
    }

    private void unitShop(Player p, Nation n, UnitType t) {
        if (needNation(p, n)) return;
        plugin.menus().openUnitShop(p, n, t);
    }

    private void war(Player p, Nation n) {
        if (needNation(p, n)) return;
        ChunkPos pos = ChunkPos.of(p.getLocation());
        Nation def = plugin.nations().getAt(pos);
        if (def == null) {
            Msg.send(p, "&cTen chunk nie nalezy do zadnego panstwa. Mozesz go kupic: &f/p chunk");
            return;
        }
        if (def == n) {
            Msg.send(p, "&cTo twoj chunk!");
            return;
        }
        if (def.getChunks().size() <= 1) {
            Msg.send(p, "&cPanstwo " + def.getName() + " ma tylko 1 chunk - nie mozna go podbic.");
            return;
        }
        if (def.getCapital().equals(pos)) {
            Msg.send(p, "&cTo chunk z fundamentem - nikt nie moze go zniszczyc ani podbic!");
            return;
        }
        if (plugin.wars().warAt(pos) != null) {
            Msg.send(p, "&cO ten chunk juz toczy sie wojna.");
            return;
        }
        if (plugin.wars().attackingWar(n.getOwner()) != null) {
            Msg.send(p, "&cJuz atakujesz inny chunk! Wycofaj sie: &f/p pokoj");
            return;
        }
        int dist = n.distanceTo(pos);
        int range = plugin.getConfig().getInt("armia.zasieg-zolnierzy-chunki", 16);
        int capture = plugin.getConfig().getInt("wojna.czas-przejecia-sekundy", 10);
        Bukkit.broadcast(Msg.c(Msg.PREFIX + "&4&lWOJNA! &6" + n.getName() + " &catakuje chunk &f" + pos
                + " &cpanstwa &6" + def.getName() + "&c!"));
        if (dist > range) {
            Msg.send(p, "&eCel jest &f" + (dist == Integer.MAX_VALUE ? "w innym swiecie" : dist + " chunkow")
                    + "&e od twojego panstwa - zolnierze nie dosiegaja, leci tylko lotnictwo (&f/p drony&e).");
        }
        Msg.send(p, "&7Zostan na chunku (ty lub twoja armia) przez &f" + capture
                + "s&7 bez obroncow, aby go przejac. Wycofanie: &f/p pokoj");
        Player dp = Bukkit.getPlayer(def.getOwner());
        if (dp != null) {
            Msg.send(dp, "&c&lTwoj chunk " + pos + " jest atakowany przez " + n.getName() + "! &7Bron go!");
            dp.playSound(dp.getLocation(), "minecraft:event.raid.horn", 1f, 1f);
        }
        p.playSound(p.getLocation(), "minecraft:event.raid.horn", 1f, 1f);
        plugin.wars().startWar(n, def, pos);
    }

    private void stock(Player p, Nation n) {
        if (needNation(p, n)) return;
        ChunkPos pos = ChunkPos.of(p.getLocation());
        if (plugin.nations().getAt(pos) != n) {
            Msg.send(p, "&cMusisz stac na chunku swojego panstwa.");
            return;
        }
        int x = p.getLocation().getBlockX();
        int z = p.getLocation().getBlockZ();
        if (plugin.market().at(p.getWorld().getName(), x, z) != null) {
            Msg.send(p, "&cKolumna na ktorej stoisz jest juz akcja.");
            return;
        }
        if (plugin.market().farmIn(p.getWorld(), x, z) == null) {
            Msg.send(p, "&cW kolumnie na ktorej stoisz (od samej gory do samego dolu) musi byc farma!");
            Msg.send(p, "&7Np. pszenica, marchew, ziemniaki, buraki, trzcina, melon, dynia, brodawki...");
            return;
        }
        plugin.menus().openStockCreate(p, 10, 1);
    }

    private void info(Player p) {
        ChunkPos pos = ChunkPos.of(p.getLocation());
        Nation here = plugin.nations().getAt(pos);
        Msg.send(p, "&7Chunk &f" + pos + "&7: " + (here == null ? "&aniczyj" : "&6" + here.getName()
                + (here.getCapital().equals(pos) ? " &e(fundament)" : "")));
        Nation n = plugin.nations().get(p.getUniqueId());
        if (n == null) {
            Msg.send(p, "&7Nie masz panstwa. Zaloz je: &f/p fundament");
            return;
        }
        Msg.raw(p, "&6&l" + n.getName());
        Msg.raw(p, " &7Chunki: &f" + n.getChunks().size() + " &7Fundament: &f" + n.getFundX() + ", " + n.getFundY() + ", " + n.getFundZ());
        StringBuilder sb = new StringBuilder(" &7Armia: ");
        for (UnitType t : UnitType.values()) sb.append("&f").append(n.getUnits(t)).append(" &7").append(t.plural()).append("  ");
        Msg.raw(p, sb.toString());
    }

    private void help(Player p) {
        Msg.raw(p, "&6&l=== Panstwa ===");
        Msg.raw(p, "&e/p fundament &7- zaloz panstwo (64 dirt + 64 drewna debowego)");
        Msg.raw(p, "&e/p chunk &7- kup chunk na ktorym stoisz (32 diamenty)");
        Msg.raw(p, "&e/p wojna &7- zaatakuj chunk na ktorym stoisz");
        Msg.raw(p, "&e/p pokoj &7- wycofaj sie z ataku");
        Msg.raw(p, "&e/p armia &7- kup zolnierzy");
        Msg.raw(p, "&e/p drony &7| &e/p samolot &7| &e/p jet &7- lotnictwo");
        Msg.raw(p, "&e/p gielda &7- wystaw akcje farmy");
        Msg.raw(p, "&e/akcje &7| &e/sprzedajakcje &7| &e/mojeakcje &7- gielda akcji");
        Msg.raw(p, "&e/p info &7| &e/p nazwa <nazwa> &7| &e/p lista");
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command cmd, String label, String[] args) {
        List<String> out = new ArrayList<>();
        if (args.length == 1) {
            for (String s : SUBS) if (s.startsWith(args[0].toLowerCase())) out.add(s);
        }
        return out;
    }
}
