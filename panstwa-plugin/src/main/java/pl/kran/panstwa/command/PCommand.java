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
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class PCommand implements TabExecutor {
    private static final List<String> SUBS = List.of("fundament", "chunk", "wojna", "pokoj", "armia", "drony",
            "samolot", "jet", "gielda", "info", "tutaj", "chunki", "mapa", "wojny", "ranking", "gracz", "akcja",
            "nazwa", "lista", "pomoc", "zapros", "akceptuj", "odrzuc", "wyrzuc", "opusc", "czlonkowie", "oplata", "dom", "ustawdom");
    private final PanstwaPlugin plugin;
    private final InfoCommands info;
    /** Zaproszony gracz -> (wlasciciel panstwa, czas wygasniecia). */
    private final Map<UUID, Map.Entry<UUID, Long>> invites = new HashMap<>();

    public PCommand(PanstwaPlugin plugin) {
        this.plugin = plugin;
        this.info = new InfoCommands(plugin);
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (!(sender instanceof Player p)) {
            sender.sendMessage("Tylko dla graczy.");
            return true;
        }
        if (cmd.getName().equalsIgnoreCase("kraj")) {
            String[] a = new String[args.length + 1];
            a[0] = "info";
            System.arraycopy(args, 0, a, 1, args.length);
            args = a;
        }
        String sub = args.length == 0 ? "pomoc" : args[0].toLowerCase();
        Nation n = plugin.nations().of(p.getUniqueId());
        switch (sub) {
            case "fundament" -> {
                if (n != null) {
                    Msg.send(p, "&cNalezysz juz do panstwa &6" + n.getName() + "&c.");
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
            case "info", "kraj", "panstwo" -> info.nationInfo(p, args.length > 1 ? args[1] : null);
            case "tutaj", "chunkinfo" -> info.here(p);
            case "chunki" -> info.chunks(p, args.length > 1 ? args[1] : null);
            case "mapa" -> info.map(p);
            case "wojny" -> info.wars(p);
            case "ranking", "top" -> info.ranking(p);
            case "gracz" -> {
                if (args.length < 2) Msg.send(p, "&cUzycie: /p gracz <nick>");
                else info.player(p, args[1]);
            }
            case "akcja" -> {
                if (args.length < 2) Msg.send(p, "&cUzycie: /p akcja <id>");
                else info.share(p, args[1]);
            }
            case "admin" -> {
                if (!p.hasPermission("panstwa.admin")) {
                    Msg.send(p, "&cNie masz uprawnien.");
                    return true;
                }
                boolean on = plugin.toggleBypass(p);
                Msg.send(p, on ? "&aTryb admina WLACZONY - mozesz niszczyc/budowac na terenie wszystkich panstw."
                        : "&7Tryb admina wylaczony - ochrona panstw dziala tez na ciebie.");
            }
            case "dom", "home" -> plugin.homes().teleportHome(p);
            case "ustawdom", "sethome" -> plugin.homes().setHome(p);
            case "zapros" -> invite(p, n, args);
            case "akceptuj", "dolacz" -> accept(p, n);
            case "odrzuc" -> {
                if (invites.remove(p.getUniqueId()) != null) Msg.send(p, "&7Odrzuciles zaproszenie.");
                else Msg.send(p, "&cNie masz zadnego zaproszenia.");
            }
            case "wyrzuc" -> kick(p, n, args);
            case "opusc" -> leave(p, n);
            case "czlonkowie" -> members(p, args.length > 1 ? info.find(args[1]) : n, args.length > 1);
            case "oplata", "podatek" -> {
                if (needNation(p, n)) return true;
                plugin.menus().openUpkeep(p, n);
            }
            case "nazwa" -> {
                if (needOwner(p, n)) return true;
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

    private boolean needOwner(Player p, Nation n) {
        if (needNation(p, n)) return true;
        if (!n.isOwner(p.getUniqueId())) {
            Msg.send(p, "&cTylko wlasciciel panstwa moze to zrobic.");
            return true;
        }
        return false;
    }

    // ------------------------------------------------------------------ czlonkowie
    private void invite(Player p, Nation n, String[] args) {
        if (needOwner(p, n)) return;
        if (args.length < 2) {
            Msg.send(p, "&cUzycie: /p zapros <gracz>");
            return;
        }
        Player t = Bukkit.getPlayerExact(args[1]);
        if (t == null) {
            Msg.send(p, "&cGracz musi byc online.");
            return;
        }
        if (t == p) {
            Msg.send(p, "&cNie mozesz zaprosic siebie.");
            return;
        }
        if (plugin.nations().of(t.getUniqueId()) != null) {
            Msg.send(p, "&c" + t.getName() + " nalezy juz do panstwa.");
            return;
        }
        int max = plugin.getConfig().getInt("czlonkowie.max", 10);
        if (n.getMembers().size() >= max) {
            Msg.send(p, "&cTwoje panstwo ma juz maksymalnie " + max + " czlonkow.");
            return;
        }
        int sec = plugin.getConfig().getInt("czlonkowie.zaproszenie-wazne-sekundy", 120);
        invites.put(t.getUniqueId(), Map.entry(n.getOwner(), System.currentTimeMillis() + sec * 1000L));
        Msg.send(p, "&aZaproszono &f" + t.getName() + "&a do panstwa. Zaproszenie wazne " + sec + "s.");
        Msg.send(t, "&6" + p.getName() + " &azaprasza cie do panstwa &6" + n.getName() + "&a!");
        Msg.send(t, "&7Wpisz &a/p akceptuj &7aby dolaczyc albo &c/p odrzuc&7. (" + sec + "s)");
        t.playSound(t.getLocation(), "minecraft:entity.experience_orb.pickup", 1f, 1f);
    }

    private void accept(Player p, Nation current) {
        if (current != null) {
            Msg.send(p, "&cNalezysz juz do panstwa " + current.getName() + ". Najpierw je opusc: /p opusc");
            return;
        }
        Map.Entry<UUID, Long> inv = invites.remove(p.getUniqueId());
        if (inv == null || inv.getValue() < System.currentTimeMillis()) {
            Msg.send(p, "&cNie masz waznego zaproszenia.");
            return;
        }
        Nation n = plugin.nations().get(inv.getKey());
        if (n == null) {
            Msg.send(p, "&cTo panstwo juz nie istnieje.");
            return;
        }
        if (n.getMembers().size() >= plugin.getConfig().getInt("czlonkowie.max", 10)) {
            Msg.send(p, "&cTo panstwo jest juz pelne.");
            return;
        }
        plugin.nations().addMember(n, p.getUniqueId());
        for (Player o : n.online()) Msg.send(o, "&a" + p.getName() + " dolaczyl do panstwa &6" + n.getName() + "&a!");
    }

    private void kick(Player p, Nation n, String[] args) {
        if (needOwner(p, n)) return;
        if (args.length < 2) {
            Msg.send(p, "&cUzycie: /p wyrzuc <gracz>");
            return;
        }
        UUID target = null;
        for (UUID m : n.getMembers()) {
            if (plugin.menus().holderName(m).equalsIgnoreCase(args[1])) target = m;
        }
        if (target == null) {
            Msg.send(p, "&c" + args[1] + " nie jest czlonkiem twojego panstwa.");
            return;
        }
        plugin.nations().removeMember(n, target);
        Msg.send(p, "&aWyrzucono &f" + plugin.menus().holderName(target) + "&a z panstwa.");
        Player t = Bukkit.getPlayer(target);
        if (t != null) Msg.send(t, "&cZostales wyrzucony z panstwa " + n.getName() + ".");
    }

    private void leave(Player p, Nation n) {
        if (needNation(p, n)) return;
        if (n.isOwner(p.getUniqueId())) {
            Msg.send(p, "&cJestes wlascicielem. Aby usunac panstwo, zniszcz fundament.");
            return;
        }
        plugin.nations().removeMember(n, p.getUniqueId());
        Msg.send(p, "&7Opusciles panstwo &6" + n.getName() + "&7.");
        for (Player o : n.online()) Msg.send(o, "&e" + p.getName() + " opuscil panstwo.");
    }

    private void members(Player p, Nation n, boolean byArg) {
        if (n == null) {
            Msg.send(p, byArg ? "&cNie znaleziono panstwa." : "&cNie nalezysz do zadnego panstwa.");
            return;
        }
        Msg.send(p, "&6Czlonkowie panstwa " + n.getName() + " (" + (n.getMembers().size() + 1) + "):");
        for (UUID id : n.allPlayers()) {
            boolean online = Bukkit.getPlayer(id) != null;
            Msg.raw(p, " &8- " + (online ? "&a" : "&7") + plugin.menus().holderName(id)
                    + (n.isOwner(id) ? " &6(wlasciciel)" : "") + (online ? " &a●" : " &8●"));
        }
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
        for (Player dp : def.online()) {
            Msg.send(dp, "&c&lChunk " + pos + " twojego panstwa jest atakowany przez " + n.getName() + "! &7Bron go!");
            dp.playSound(dp.getLocation(), "minecraft:event.raid.horn", 1f, 1f);
        }
        for (Player ap : n.online()) {
            if (ap != p) Msg.send(ap, "&c" + p.getName() + " rozpoczal atak na chunk " + pos + " (" + def.getName() + ")! &7Dolacz do walki!");
        }
        p.playSound(p.getLocation(), "minecraft:event.raid.horn", 1f, 1f);
        plugin.wars().startWar(n, def, pos);
    }

    private void stock(Player p, Nation n) {
        if (needNation(p, n)) return;
        if (!n.isOwner(p.getUniqueId())) {
            Msg.send(p, "&cTylko wlasciciel panstwa moze wystawiac akcje.");
            return;
        }
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
        Msg.raw(p, "&e/p dom &7- teleport do swojego panstwa");
        Msg.raw(p, "&e/p ustawdom &7- ustaw dom panstwa (wlasciciel, na swoim terenie)");
        Msg.raw(p, "&6&l--- Czlonkowie i oplata ---");
        Msg.raw(p, "&e/p zapros <gracz> &7- zapros gracza (wlasciciel)");
        Msg.raw(p, "&e/p akceptuj &7| &e/p odrzuc &7- odpowiedz na zaproszenie");
        Msg.raw(p, "&e/p wyrzuc <gracz> &7- wyrzuc czlonka (wlasciciel)");
        Msg.raw(p, "&e/p opusc &7- opusc panstwo");
        Msg.raw(p, "&e/p czlonkowie [panstwo] &7- lista czlonkow");
        Msg.raw(p, "&e/p oplata &7- zaplac 64 diamenty (co 7 dni, inaczej panstwo wygasa!)");
        Msg.raw(p, "&6&l--- Informacje ---");
        Msg.raw(p, "&e/p info [panstwo|gracz] &7- informacje o panstwie");
        Msg.raw(p, "&e/p tutaj &7- do kogo nalezy chunk na ktorym stoisz");
        Msg.raw(p, "&e/p chunki [panstwo] &7- lista chunkow panstwa");
        Msg.raw(p, "&e/p mapa &7- mapa chunkow dookola");
        Msg.raw(p, "&e/p wojny &7- trwajace wojny");
        Msg.raw(p, "&e/p ranking &7- najlepsze panstwa");
        Msg.raw(p, "&e/p lista &7- wszystkie panstwa");
        Msg.raw(p, "&e/p gracz <nick> &7- informacje o graczu");
        Msg.raw(p, "&e/p akcja <id> &7- informacje o akcji");
        Msg.raw(p, "&e/p nazwa <nazwa> &7- zmien nazwe panstwa");
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command cmd, String label, String[] args) {
        if (cmd.getName().equalsIgnoreCase("kraj")) {
            String[] a = new String[args.length + 1];
            a[0] = "info";
            System.arraycopy(args, 0, a, 1, args.length);
            args = a;
        }
        List<String> out = new ArrayList<>();
        if (args.length == 1) {
            for (String s : SUBS) if (s.startsWith(args[0].toLowerCase())) out.add(s);
        } else if (args.length == 2) {
            String sub = args[0].toLowerCase();
            String pre = args[1].toLowerCase();
            if (sub.equals("info") || sub.equals("kraj") || sub.equals("panstwo") || sub.equals("chunki") || sub.equals("czlonkowie")) {
                for (Nation n : plugin.nations().all()) if (n.getName().toLowerCase().startsWith(pre)) out.add(n.getName());
            } else if (sub.equals("wyrzuc") && sender instanceof Player pl0) {
                Nation n = plugin.nations().of(pl0.getUniqueId());
                if (n != null) for (UUID m : n.getMembers()) {
                    String nm = plugin.menus().holderName(m);
                    if (nm.toLowerCase().startsWith(pre)) out.add(nm);
                }
            } else if (sub.equals("gracz") || sub.equals("zapros")) {
                for (Player pl : Bukkit.getOnlinePlayers()) if (pl.getName().toLowerCase().startsWith(pre)) out.add(pl.getName());
            } else if (sub.equals("akcja")) {
                plugin.market().all().forEach(sh -> {
                    String id = String.valueOf(sh.getId());
                    if (id.startsWith(pre)) out.add(id);
                });
            }
        }
        return out;
    }
}
