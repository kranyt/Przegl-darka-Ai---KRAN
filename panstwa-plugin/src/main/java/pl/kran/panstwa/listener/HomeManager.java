package pl.kran.panstwa.listener;

import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDamageEvent;
import org.bukkit.event.player.PlayerMoveEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.event.player.PlayerRespawnEvent;
import org.bukkit.scheduler.BukkitTask;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.model.Nation;
import pl.kran.panstwa.util.ChunkPos;
import pl.kran.panstwa.util.Msg;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/** /p dom, /p ustawdom i odradzanie po smierci w swoim panstwie. */
public class HomeManager implements Listener {
    private final PanstwaPlugin plugin;
    private final Map<UUID, BukkitTask> pending = new HashMap<>();
    private final Map<UUID, Long> cooldowns = new HashMap<>();

    public HomeManager(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    private int warmup() { return plugin.getConfig().getInt("dom.odliczanie-sekundy", 3); }

    private int cooldown() { return plugin.getConfig().getInt("dom.cooldown-sekundy", 30); }

    public void teleportHome(Player p) {
        Nation n = plugin.nations().of(p.getUniqueId());
        if (n == null) {
            Msg.send(p, "&cNie masz panstwa! Zaloz je: &f/p fundament");
            return;
        }
        Location home = n.getHome();
        if (home == null) {
            Msg.send(p, "&cSwiat twojego panstwa nie jest zaladowany.");
            return;
        }
        long left = cooldowns.getOrDefault(p.getUniqueId(), 0L) - System.currentTimeMillis();
        if (left > 0 && !p.hasPermission("panstwa.admin")) {
            Msg.send(p, "&cMusisz poczekac jeszcze &f" + (left / 1000 + 1) + "s&c.");
            return;
        }
        cancel(p.getUniqueId());
        int sec = warmup();
        if (sec <= 0) {
            doTeleport(p);
            return;
        }
        Msg.send(p, "&aTeleportacja do panstwa &6" + n.getName() + " &aza &f" + sec + "s&a. Nie ruszaj sie!");
        final int[] count = {sec};
        BukkitTask task = Bukkit.getScheduler().runTaskTimer(plugin, () -> {
            if (!p.isOnline()) { cancel(p.getUniqueId()); return; }
            if (count[0] <= 0) {
                cancel(p.getUniqueId());
                doTeleport(p);
                return;
            }
            p.sendActionBar(Msg.c("&eTeleportacja do domu za &f" + count[0] + "s&e..."));
            count[0]--;
        }, 0L, 20L);
        pending.put(p.getUniqueId(), task);
    }

    private void doTeleport(Player p) {
        Nation n = plugin.nations().of(p.getUniqueId());
        if (n == null) return;
        Location home = n.getHome();
        if (home == null) return;
        home.getWorld().getChunkAt(home); // zaladuj chunk
        if (p.teleport(home)) {
            Msg.send(p, "&aJestes w domu - &6" + n.getName() + "&a.");
            p.playSound(home, "minecraft:entity.enderman.teleport", 1f, 1.2f);
            cooldowns.put(p.getUniqueId(), System.currentTimeMillis() + cooldown() * 1000L);
        }
    }

    private boolean cancel(UUID id) {
        BukkitTask t = pending.remove(id);
        if (t != null) t.cancel();
        return t != null;
    }

    public void setHome(Player p) {
        Nation n = plugin.nations().of(p.getUniqueId());
        if (n == null) {
            Msg.send(p, "&cNie masz panstwa.");
            return;
        }
        if (!n.isOwner(p.getUniqueId())) {
            Msg.send(p, "&cTylko wlasciciel moze ustawic dom panstwa.");
            return;
        }
        if (!n.getChunks().contains(ChunkPos.of(p.getLocation()))) {
            Msg.send(p, "&cDom mozna ustawic tylko na terenie swojego panstwa.");
            return;
        }
        n.setHome(p.getLocation());
        plugin.nations().save();
        Msg.send(p, "&aUstawiono dom panstwa tutaj. Teleport: &f/p dom");
    }

    // ------------------------------------------------------------------ anulowanie odliczania
    @EventHandler(ignoreCancelled = true)
    public void onMove(PlayerMoveEvent e) {
        if (!pending.containsKey(e.getPlayer().getUniqueId())) return;
        Location f = e.getFrom(), t = e.getTo();
        if (f.getBlockX() == t.getBlockX() && f.getBlockY() == t.getBlockY() && f.getBlockZ() == t.getBlockZ()) return;
        if (cancel(e.getPlayer().getUniqueId())) Msg.send(e.getPlayer(), "&cTeleportacja anulowana - ruszyles sie.");
    }

    @EventHandler(ignoreCancelled = true)
    public void onDamage(EntityDamageEvent e) {
        if (e.getEntity() instanceof Player p && cancel(p.getUniqueId())) {
            Msg.send(p, "&cTeleportacja anulowana - otrzymales obrazenia.");
        }
    }

    @EventHandler
    public void onQuit(PlayerQuitEvent e) {
        cancel(e.getPlayer().getUniqueId());
    }

    // ------------------------------------------------------------------ odradzanie po smierci
    @EventHandler(priority = EventPriority.HIGH)
    public void onRespawn(PlayerRespawnEvent e) {
        if (!plugin.getConfig().getBoolean("dom.odradzanie-w-panstwie", true)) return;
        if (e.isBedSpawn() || e.isAnchorSpawn()) return; // lozko / kotwica maja pierwszenstwo
        Nation n = plugin.nations().of(e.getPlayer().getUniqueId());
        if (n == null) return;
        Location home = n.getHome();
        if (home != null) e.setRespawnLocation(home);
    }
}
