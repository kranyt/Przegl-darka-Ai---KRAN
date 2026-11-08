package pl.kran.panstwa.model;

import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.scheduler.BukkitTask;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.util.Items;
import pl.kran.panstwa.util.Msg;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/** Oplata za panstwo: 64 diamenty co 7 dni, inaczej panstwo wygasa. */
public class UpkeepManager {
    private final PanstwaPlugin plugin;
    private BukkitTask task;
    /** Ostatnie ostrzezenie (godziny do konca) wyslane danemu panstwu. */
    private final Map<UUID, Long> lastWarn = new HashMap<>();

    public UpkeepManager(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    public void start() {
        task = Bukkit.getScheduler().runTaskTimer(plugin, this::check, 200L, 1200L);
    }

    public void shutdown() {
        if (task != null) task.cancel();
    }

    public int cost() { return plugin.getConfig().getInt("oplata.koszt-diamenty", 64); }

    public long period() { return plugin.upkeepPeriodMs(); }

    public int maxAhead() { return plugin.getConfig().getInt("oplata.max-okresow-z-gory", 4); }

    public long timeLeft(Nation n) { return n.getPaidUntil() - System.currentTimeMillis(); }

    public static String timeText(long ms) {
        if (ms <= 0) return "0min";
        long min = ms / 60000;
        long d = min / 1440, h = (min % 1440) / 60, m = min % 60;
        if (d > 0) return d + "d " + h + "h";
        if (h > 0) return h + "h " + m + "min";
        return m + "min";
    }

    /** Zaplata za kolejny okres. Zwraca blad albo null. */
    public String pay(Player p, Nation n) {
        long now = System.currentTimeMillis();
        long base = Math.max(now, n.getPaidUntil());
        if (base + period() - now > period() * (long) maxAhead()) {
            return "Panstwo jest juz oplacone na " + maxAhead() + " okresy z gory.";
        }
        if (!Items.takeDiamonds(p, cost())) return "Potrzebujesz " + cost() + " diamentow!";
        n.setPaidUntil(base + period());
        lastWarn.remove(n.getOwner());
        plugin.nations().save();
        for (Player o : n.online()) {
            Msg.send(o, "&a" + p.getName() + " oplacil panstwo! Oplacone jeszcze na &f" + timeText(timeLeft(n)) + "&a.");
        }
        return null;
    }

    private void check() {
        long now = System.currentTimeMillis();
        for (Nation n : new ArrayList<>(plugin.nations().all())) {
            long left = n.getPaidUntil() - now;
            if (left <= 0) {
                plugin.disband(n, "&cPanstwo &6" + n.getName() + " &cwygaslo - nie zaplacono " + cost() + " diamentow.");
                lastWarn.remove(n.getOwner());
                continue;
            }
            // ostrzezenia: 24h, 6h, 1h, 10min przed koncem
            for (long mark : new long[]{24 * 60, 6 * 60, 60, 10}) {
                long markMs = mark * 60_000L;
                if (left <= markMs && lastWarn.getOrDefault(n.getOwner(), Long.MAX_VALUE) > mark) {
                    lastWarn.put(n.getOwner(), mark);
                    warn(n);
                    break;
                }
            }
        }
    }

    public void warn(Nation n) {
        for (Player p : n.online()) warn(p, n);
    }

    public void warn(Player p, Nation n) {
        Msg.send(p, "&c&lUwaga! &cTwoje panstwo wygasnie za &f" + timeText(timeLeft(n))
                + "&c! Zaplac &b" + cost() + " diamentow&c: &f/p oplata");
        p.playSound(p.getLocation(), "minecraft:block.note_block.pling", 1f, 0.6f);
    }
}
