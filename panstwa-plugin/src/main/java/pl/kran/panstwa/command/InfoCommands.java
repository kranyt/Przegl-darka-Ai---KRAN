package pl.kran.panstwa.command;

import org.bukkit.Bukkit;
import org.bukkit.OfflinePlayer;
import org.bukkit.entity.Player;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.market.Share;
import pl.kran.panstwa.model.Nation;
import pl.kran.panstwa.util.ChunkPos;
import pl.kran.panstwa.util.Msg;
import pl.kran.panstwa.war.UnitType;
import pl.kran.panstwa.war.War;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/** Komendy informacyjne: /p info, /p tutaj, /p chunki, /p mapa, /p wojny, /p ranking, /p gracz, /p akcja. */
public class InfoCommands {
    private static final String[] COLORS = {"&c", "&9", "&d", "&6", "&b", "&e", "&5", "&3", "&4", "&1"};
    private final PanstwaPlugin plugin;

    public InfoCommands(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    private String name(UUID id) {
        return plugin.menus().holderName(id);
    }

    /** Szuka panstwa po nazwie panstwa albo nicku wlasciciela. */
    public Nation find(String arg) {
        Nation n = plugin.nations().getByName(arg);
        if (n != null) return n;
        for (Nation x : plugin.nations().all()) {
            if (name(x.getOwner()).equalsIgnoreCase(arg)) return x;
        }
        return null;
    }

    /** Wartosc armii w diamentach (do rankingu). */
    public int armyValue(Nation n) {
        int v = n.getUnits(UnitType.SOLDIER) * plugin.getConfig().getInt("armia.zolnierz-koszt", 5);
        for (UnitType t : UnitType.values()) if (t.flying()) v += n.getUnits(t) * t.cost(plugin.getConfig());
        return v;
    }

    public int position(Nation n) {
        List<Nation> sorted = ranking();
        return sorted.indexOf(n) + 1;
    }

    private List<Nation> ranking() {
        List<Nation> list = new ArrayList<>(plugin.nations().all());
        list.sort(Comparator.comparingInt((Nation x) -> x.getChunks().size()).reversed()
                .thenComparing(Comparator.comparingInt(this::armyValue).reversed()));
        return list;
    }

    // ------------------------------------------------------------------ /p info [panstwo|gracz]
    public void nationInfo(Player p, String arg) {
        Nation n;
        if (arg == null) {
            n = plugin.nations().get(p.getUniqueId());
            if (n == null) {
                Msg.send(p, "&7Nie masz panstwa. Zaloz je: &f/p fundament &7lub sprawdz inne: &f/p info <nazwa>");
                return;
            }
        } else {
            n = find(arg);
            if (n == null) {
                Msg.send(p, "&cNie znaleziono panstwa ani gracza z panstwem: &f" + arg);
                return;
            }
        }
        boolean own = n.getOwner().equals(p.getUniqueId());
        OfflinePlayer owner = Bukkit.getOfflinePlayer(n.getOwner());
        Msg.raw(p, "&8&m                                        ");
        Msg.raw(p, "&6&l" + n.getName() + " &7(#" + position(n) + " w rankingu)");
        Msg.raw(p, " &7Wlasciciel: &f" + name(n.getOwner()) + (owner.isOnline() ? " &a(online)" : " &c(offline)"));
        if (owner.getFirstPlayed() > 0 && !owner.isOnline() && owner.getLastSeen() > 0) {
            Msg.raw(p, " &7Ostatnio online: &f" + new SimpleDateFormat("dd.MM.yyyy HH:mm").format(new Date(owner.getLastSeen())));
        }
        Msg.raw(p, " &7Chunki: &f" + n.getChunks().size());
        Msg.raw(p, " &7Fundament: &f" + n.getFundX() + ", " + n.getFundY() + ", " + n.getFundZ()
                + " &7(" + n.getFundWorld() + ", chunk " + n.getCapital() + ")");
        StringBuilder army = new StringBuilder(" &7Armia: ");
        for (UnitType t : UnitType.values()) army.append("&f").append(n.getUnits(t)).append(" &7").append(t.plural()).append("  ");
        Msg.raw(p, army.toString());
        Msg.raw(p, " &7Sila armii: &b" + armyValue(n) + " diamentow");
        long shares = plugin.market().all().stream().filter(s -> s.getIssuer().equals(n.getOwner())).count();
        Msg.raw(p, " &7Wystawione akcje: &f" + shares);
        List<String> wars = new ArrayList<>();
        for (War w : plugin.wars().getWars()) {
            if (!w.involves(n.getOwner())) continue;
            boolean att = w.getAttacker().equals(n.getOwner());
            Nation other = plugin.nations().get(att ? w.getDefender() : w.getAttacker());
            wars.add((att ? "&catakuje &6" : "&9broni sie przed &6") + (other == null ? "?" : other.getName())
                    + " &7(chunk " + w.getTarget() + ")");
        }
        Msg.raw(p, " &7Wojny: " + (wars.isEmpty() ? "&aspokoj" : String.join("&7, ", wars)));
        if (own && !n.isStarterPackBought()) Msg.raw(p, " &eWskazowka: kup pakiet startowy armii - &f/p armia");
        Msg.raw(p, "&8&m                                        ");
    }

    // ------------------------------------------------------------------ /p tutaj
    public void here(Player p) {
        ChunkPos pos = ChunkPos.of(p.getLocation());
        Nation n = plugin.nations().getAt(pos);
        Msg.send(p, "&7Chunk &f" + pos + " &7(" + pos.world() + ")");
        if (n == null) {
            Msg.raw(p, " &7Wlasciciel: &aniczyj &7- mozesz go kupic: &f/p chunk");
        } else {
            Msg.raw(p, " &7Panstwo: &6" + n.getName() + " &7(wlasciciel: &f" + name(n.getOwner()) + "&7)");
            if (n.getCapital().equals(pos)) Msg.raw(p, " &eTo chunk z fundamentem - nie do zniszczenia i nie do podbicia.");
            else if (n.getChunks().size() <= 1) Msg.raw(p, " &7Panstwo ma 1 chunk - nie mozna go podbic.");
            else if (!n.getOwner().equals(p.getUniqueId())) Msg.raw(p, " &cMozna go podbic: &f/p wojna");
        }
        War w = plugin.wars().warAt(pos);
        if (w != null) {
            Nation a = plugin.nations().get(w.getAttacker());
            Msg.raw(p, " &4&lTrwa tu wojna! &7Atakuje: &6" + (a == null ? "?" : a.getName()));
        }
        Nation mine = plugin.nations().get(p.getUniqueId());
        if (mine != null && n != mine) {
            int d = mine.distanceTo(pos);
            int range = plugin.getConfig().getInt("armia.zasieg-zolnierzy-chunki", 16);
            Msg.raw(p, " &7Odleglosc od twojego panstwa: &f" + (d == Integer.MAX_VALUE ? "inny swiat" : d + " chunkow")
                    + (d > range ? " &c(zolnierze nie dosiegna - potrzebne lotnictwo)" : " &a(w zasiegu zolnierzy)"));
        }
        int x = p.getLocation().getBlockX(), z = p.getLocation().getBlockZ();
        Share s = plugin.market().at(p.getWorld().getName(), x, z);
        if (s != null) Msg.raw(p, " &7Ta kolumna to &eakcja #" + s.getId() + " &7(cena &b" + s.getPrice() + "&7)");
    }

    // ------------------------------------------------------------------ /p chunki [panstwo]
    public void chunks(Player p, String arg) {
        Nation n = arg == null ? plugin.nations().get(p.getUniqueId()) : find(arg);
        if (n == null) {
            Msg.send(p, arg == null ? "&cNie masz panstwa." : "&cNie znaleziono panstwa: " + arg);
            return;
        }
        Msg.send(p, "&6Chunki panstwa " + n.getName() + " (" + n.getChunks().size() + "):");
        for (ChunkPos c : n.getChunks()) {
            String extra = c.equals(n.getCapital()) ? " &e(fundament)" : "";
            if (plugin.wars().warAt(c) != null) extra += " &4(wojna!)";
            Msg.raw(p, " &8- &f" + c + " &7bloki " + (c.x() << 4) + ", " + (c.z() << 4) + " &8(" + c.world() + ")" + extra);
        }
    }

    // ------------------------------------------------------------------ /p mapa
    public void map(Player p) {
        ChunkPos center = ChunkPos.of(p.getLocation());
        int rx = 10, rz = 5;
        Map<UUID, String> colors = new LinkedHashMap<>();
        Nation mine = plugin.nations().get(p.getUniqueId());
        Msg.raw(p, "&8&m          &6 Mapa chunkow &8(polnoc w gore) &8&m          ");
        for (int dz = -rz; dz <= rz; dz++) {
            StringBuilder row = new StringBuilder(" ");
            for (int dx = -rx; dx <= rx; dx++) {
                ChunkPos c = new ChunkPos(center.world(), center.x() + dx, center.z() + dz);
                Nation n = plugin.nations().getAt(c);
                String sym;
                if (dx == 0 && dz == 0) sym = "&e&l+";
                else if (plugin.wars().warAt(c) != null) sym = "&4⚔";
                else if (n == null) sym = "&7-";
                else {
                    String col = n == mine ? "&a" : colors.computeIfAbsent(n.getOwner(),
                            k -> COLORS[Math.floorMod(k.hashCode(), COLORS.length)]);
                    if (n == mine) colors.putIfAbsent(n.getOwner(), "&a");
                    sym = col + (c.equals(n.getCapital()) ? "★" : "■");
                }
                row.append(sym).append("&r");
            }
            Msg.raw(p, row.toString());
        }
        StringBuilder legend = new StringBuilder(" &e+ &7ty  &7- niczyje  &4⚔ &7wojna  ★ fundament");
        Msg.raw(p, legend.toString());
        if (!colors.isEmpty()) {
            StringBuilder l = new StringBuilder(" ");
            for (Map.Entry<UUID, String> e : colors.entrySet()) {
                Nation n = plugin.nations().get(e.getKey());
                if (n != null) l.append(e.getValue()).append("■ ").append(n.getName()).append("  ");
            }
            Msg.raw(p, l.toString());
        }
    }

    // ------------------------------------------------------------------ /p wojny
    public void wars(Player p) {
        List<War> wars = plugin.wars().getWars();
        if (wars.isEmpty()) {
            Msg.send(p, "&aObecnie nie trwa zadna wojna.");
            return;
        }
        Msg.send(p, "&4Trwajace wojny (" + wars.size() + "):");
        for (War w : wars) {
            Nation a = plugin.nations().get(w.getAttacker());
            Nation d = plugin.nations().get(w.getDefender());
            StringBuilder au = new StringBuilder(), du = new StringBuilder();
            for (UnitType t : UnitType.values()) {
                long ac = w.aliveCount(w.getAttacker(), t), dc = w.aliveCount(w.getDefender(), t);
                if (ac > 0) au.append(ac).append(" ").append(t.plural().toLowerCase()).append(" ");
                if (dc > 0) du.append(dc).append(" ").append(t.plural().toLowerCase()).append(" ");
            }
            Msg.raw(p, " &8- &c" + (a == null ? "?" : a.getName()) + " &7vs &9" + (d == null ? "?" : d.getName())
                    + " &7o chunk &f" + w.getTarget() + " &7(bloki " + (w.getTarget().x() << 4) + ", " + (w.getTarget().z() << 4) + ")");
            Msg.raw(p, "    &7Atak: &f" + (au.length() == 0 ? "brak jednostek" : au.toString().trim())
                    + " &8| &7Obrona: &f" + (du.length() == 0 ? "brak jednostek" : du.toString().trim()));
        }
    }

    // ------------------------------------------------------------------ /p ranking
    public void ranking(Player p) {
        List<Nation> list = ranking();
        if (list.isEmpty()) {
            Msg.send(p, "&7Nie ma jeszcze zadnych panstw.");
            return;
        }
        Msg.send(p, "&6&lRanking panstw &7(chunki, potem sila armii):");
        for (int i = 0; i < Math.min(10, list.size()); i++) {
            Nation n = list.get(i);
            String medal = i == 0 ? "&6" : i == 1 ? "&f" : i == 2 ? "&c" : "&7";
            Msg.raw(p, " " + medal + "#" + (i + 1) + " &6" + n.getName() + " &7- &f" + n.getChunks().size()
                    + " &7chunkow, armia &b" + armyValue(n) + " &7diam. &8(" + name(n.getOwner()) + ")");
        }
        Nation mine = plugin.nations().get(p.getUniqueId());
        if (mine != null && list.indexOf(mine) >= 10) {
            Msg.raw(p, " &7Twoje panstwo: &e#" + (list.indexOf(mine) + 1) + " &6" + mine.getName());
        }
    }

    // ------------------------------------------------------------------ /p gracz <nick>
    public void player(Player p, String arg) {
        @SuppressWarnings("deprecation")
        OfflinePlayer op = Bukkit.getOfflinePlayer(arg);
        Nation n = plugin.nations().get(op.getUniqueId());
        Msg.send(p, "&7Gracz &f" + (op.getName() == null ? arg : op.getName()) + (op.isOnline() ? " &a(online)" : " &c(offline)"));
        Msg.raw(p, " &7Panstwo: " + (n == null ? "&7brak" : "&6" + n.getName() + " &7(" + n.getChunks().size() + " chunkow)"));
        List<Share> shares = plugin.market().ownedBy(op.getUniqueId());
        Msg.raw(p, " &7Akcje: &f" + shares.size() + " &7(warte &b" + shares.stream().mapToInt(Share::getPrice).sum() + " diamentow&7)");
    }

    // ------------------------------------------------------------------ /p akcja <id>
    public void share(Player p, String arg) {
        Share s;
        try {
            s = plugin.market().get(Integer.parseInt(arg.replace("#", "")));
        } catch (NumberFormatException e) {
            s = null;
        }
        if (s == null) {
            Msg.send(p, "&cNie ma takiej akcji (mogla zniknac na gieldzie).");
            return;
        }
        Nation n = plugin.nations().get(s.getIssuer());
        Msg.send(p, "&eAkcja #" + s.getId());
        Msg.raw(p, " &7Cena: &b" + s.getPrice() + " diamentow");
        Msg.raw(p, " &7Panstwo: &6" + (n == null ? "-" : n.getName()) + " &7(wystawil: &f" + name(s.getIssuer()) + "&7)");
        Msg.raw(p, " &7Posiadacz: &f" + name(s.getHolder()) + (s.isForSale() ? " &a(na sprzedaz - /akcje)" : ""));
        Msg.raw(p, " &7Kolumna: &f" + s.getX() + ", " + s.getZ() + " &7(" + s.getWorld() + ")");
        Msg.raw(p, " &7Uprawa: &f" + s.getIcon().name().toLowerCase().replace('_', ' '));
    }
}
