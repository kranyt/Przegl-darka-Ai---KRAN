package pl.kran.panstwa.listener;

import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.block.BlockFace;
import org.bukkit.block.BlockState;
import org.bukkit.block.Container;
import org.bukkit.block.data.BlockData;
import org.bukkit.block.data.Bisected;
import org.bukkit.block.data.type.Bed;
import org.bukkit.block.data.type.Stairs;
import org.bukkit.block.data.type.TrapDoor;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.BlockBreakEvent;
import org.bukkit.event.block.BlockPlaceEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.scheduler.BukkitTask;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.util.Msg;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.logging.Level;

/** Bloki postawione poza panstwem znikaja po 10 minutach. */
public class TempBlockManager implements Listener {
    private record Entry(Material type, long expireAt) {}

    private final PanstwaPlugin plugin;
    private final File file;
    /** "swiat;x;y;z" -> blok i czas znikniecia. */
    private final Map<String, Entry> blocks = new HashMap<>();
    private BukkitTask task;
    private BukkitTask saveTask;

    public TempBlockManager(PanstwaPlugin plugin) {
        this.plugin = plugin;
        this.file = new File(plugin.getDataFolder(), "znikajace-bloki.yml");
    }

    private boolean enabled() {
        return plugin.getConfig().getBoolean("znikajace-bloki.wlaczone", true);
    }

    private long delayMs() {
        return plugin.getConfig().getLong("znikajace-bloki.czas-minuty", 10) * 60_000L;
    }

    private static String key(Block b) {
        return b.getWorld().getName() + ";" + b.getX() + ";" + b.getY() + ";" + b.getZ();
    }

    public void start() {
        load();
        task = Bukkit.getScheduler().runTaskTimer(plugin, this::tick, 40L, 40L);
        saveTask = Bukkit.getScheduler().runTaskTimer(plugin, this::save, 6000L, 6000L);
    }

    public void shutdown() {
        if (task != null) task.cancel();
        if (saveTask != null) saveTask.cancel();
        save();
    }

    // ------------------------------------------------------------------ eventy
    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onPlace(BlockPlaceEvent e) {
        if (!enabled()) return;
        Player p = e.getPlayer();
        Block b = e.getBlockPlaced();
        if (p.hasPermission("panstwa.trwalebloki")) return;
        if (plugin.nations().getAt(b.getLocation()) != null) return;
        long delay = delayMs();
        blocks.put(key(b), new Entry(b.getType(), System.currentTimeMillis() + delay));
        p.sendActionBar(Msg.c("&e⚠ Ten blok zniknie za &c" + (delay / 60_000L)
                + " minut &e- postawiles go poza panstwem!"));
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onBreak(BlockBreakEvent e) {
        blocks.remove(key(e.getBlock()));
    }

    // ------------------------------------------------------------------ usuwanie
    private void tick() {
        if (blocks.isEmpty()) return;
        long now = System.currentTimeMillis();
        int done = 0;
        Iterator<Map.Entry<String, Entry>> it = blocks.entrySet().iterator();
        while (it.hasNext() && done < 300) {
            Map.Entry<String, Entry> en = it.next();
            if (en.getValue().expireAt() > now) continue;
            String[] k = en.getKey().split(";");
            World w = Bukkit.getWorld(k[0]);
            if (w == null) { it.remove(); continue; }
            int x = Integer.parseInt(k[1]), y = Integer.parseInt(k[2]), z = Integer.parseInt(k[3]);
            if (!w.isChunkLoaded(x >> 4, z >> 4)) continue; // usunie sie gdy chunk bedzie zaladowany
            it.remove();
            done++;
            Block b = w.getBlockAt(x, y, z);
            if (b.getType() != en.getValue().type()) continue;          // blok juz zmieniony
            if (plugin.nations().getAt(b.getLocation()) != null) continue; // teren stal sie panstwem
            remove(b);
        }
    }

    private void remove(Block b) {
        BlockState state = b.getState();
        if (state instanceof Container c) {
            Location loc = b.getLocation().add(0.5, 0.5, 0.5);
            for (ItemStack it : c.getInventory().getContents()) {
                if (it != null && !it.getType().isAir()) b.getWorld().dropItemNaturally(loc, it);
            }
            c.getInventory().clear();
        }
        BlockData data = b.getBlockData();
        Block other = null;
        if (data instanceof Bed bed) {
            BlockFace f = bed.getPart() == Bed.Part.FOOT ? bed.getFacing() : bed.getFacing().getOppositeFace();
            other = b.getRelative(f);
        } else if (data instanceof Bisected bi && !(data instanceof Stairs) && !(data instanceof TrapDoor)) {
            // drzwi, wysokie kwiaty itp. - dwa bloki
            other = bi.getHalf() == Bisected.Half.BOTTOM ? b.getRelative(BlockFace.UP) : b.getRelative(BlockFace.DOWN);
        }
        if (other != null && other.getType() == b.getType()) other.setType(Material.AIR, false);
        b.setType(Material.AIR, other == null);
        b.getWorld().spawnParticle(org.bukkit.Particle.CLOUD, b.getLocation().add(0.5, 0.5, 0.5), 4, 0.2, 0.2, 0.2, 0.01);
    }

    // ------------------------------------------------------------------ zapis
    private void load() {
        blocks.clear();
        if (!file.exists()) return;
        YamlConfiguration y = YamlConfiguration.loadConfiguration(file);
        ConfigurationSection s = y.getConfigurationSection("bloki");
        if (s == null) return;
        for (String k : s.getKeys(false)) {
            Material m = Material.matchMaterial(s.getString(k + ".typ", ""));
            if (m == null) continue;
            blocks.put(k.replace('|', ';'), new Entry(m, s.getLong(k + ".znika")));
        }
    }

    private void save() {
        YamlConfiguration y = new YamlConfiguration();
        for (Map.Entry<String, Entry> e : blocks.entrySet()) {
            String k = "bloki." + e.getKey().replace(';', '|').replace('.', '_');
            y.set(k + ".typ", e.getValue().type().name());
            y.set(k + ".znika", e.getValue().expireAt());
        }
        try {
            plugin.getDataFolder().mkdirs();
            y.save(file);
        } catch (IOException ex) {
            plugin.getLogger().log(Level.SEVERE, "Nie udalo sie zapisac znikajacych blokow", ex);
        }
    }
}
