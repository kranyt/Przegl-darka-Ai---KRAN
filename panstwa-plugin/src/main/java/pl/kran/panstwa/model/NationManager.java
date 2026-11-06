package pl.kran.panstwa.model;

import org.bukkit.Location;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.inventory.ItemStack;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.util.ChunkPos;
import pl.kran.panstwa.war.UnitType;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.logging.Level;

public class NationManager {
    private final PanstwaPlugin plugin;
    private final File file;
    private final Map<UUID, Nation> nations = new HashMap<>();
    private final Map<ChunkPos, UUID> chunkOwners = new HashMap<>();
    /** Przedmioty czekajace na graczy offline (diamenty z gieldy, plony). */
    private final Map<UUID, List<ItemStack>> pending = new HashMap<>();

    public NationManager(PanstwaPlugin plugin) {
        this.plugin = plugin;
        this.file = new File(plugin.getDataFolder(), "panstwa.yml");
    }

    public Collection<Nation> all() { return nations.values(); }

    public Nation get(UUID owner) { return nations.get(owner); }

    public Nation getAt(ChunkPos pos) {
        UUID o = chunkOwners.get(pos);
        return o == null ? null : nations.get(o);
    }

    public Nation getAt(Location loc) { return getAt(ChunkPos.of(loc)); }

    public Nation getByName(String name) {
        for (Nation n : nations.values()) if (n.getName().equalsIgnoreCase(name)) return n;
        return null;
    }

    public Nation getByFundament(Location loc) {
        Nation n = getAt(loc);
        return n != null && n.isFundament(loc) ? n : null;
    }

    public Nation create(UUID owner, String name, Location fundament) {
        Nation n = new Nation(owner, name, fundament.getWorld().getName(),
                fundament.getBlockX(), fundament.getBlockY(), fundament.getBlockZ());
        nations.put(owner, n);
        claim(n, ChunkPos.of(fundament));
        save();
        return n;
    }

    public void claim(Nation n, ChunkPos pos) {
        n.getChunks().add(pos);
        chunkOwners.put(pos, n.getOwner());
    }

    public void transfer(ChunkPos pos, Nation from, Nation to) {
        if (from != null) from.getChunks().remove(pos);
        claim(to, pos);
        save();
    }

    public void delete(Nation n) {
        for (ChunkPos c : n.getChunks()) chunkOwners.remove(c);
        nations.remove(n.getOwner());
        save();
    }

    // ---------- oczekujace przedmioty ----------

    public void addPending(UUID player, List<ItemStack> items) {
        pending.computeIfAbsent(player, k -> new ArrayList<>()).addAll(items);
        save();
    }

    public List<ItemStack> takePending(UUID player) {
        List<ItemStack> l = pending.remove(player);
        if (l != null) save();
        return l;
    }

    // ---------- zapis / odczyt ----------

    public void load() {
        nations.clear();
        chunkOwners.clear();
        pending.clear();
        if (!file.exists()) return;
        YamlConfiguration y = YamlConfiguration.loadConfiguration(file);
        ConfigurationSection sec = y.getConfigurationSection("panstwa");
        if (sec != null) {
            for (String key : sec.getKeys(false)) {
                try {
                    ConfigurationSection s = sec.getConfigurationSection(key);
                    UUID owner = UUID.fromString(key);
                    Nation n = new Nation(owner, s.getString("nazwa"), s.getString("fundament.swiat"),
                            s.getInt("fundament.x"), s.getInt("fundament.y"), s.getInt("fundament.z"));
                    n.setStarterPackBought(s.getBoolean("pierwszy-pakiet"));
                    for (UnitType t : UnitType.values()) n.setUnits(t, s.getInt("armia." + t.key()));
                    nations.put(owner, n);
                    for (String c : s.getStringList("chunki")) claim(n, ChunkPos.parse(c));
                } catch (Exception e) {
                    plugin.getLogger().log(Level.WARNING, "Nie udalo sie wczytac panstwa " + key, e);
                }
            }
        }
        ConfigurationSection ps = y.getConfigurationSection("oczekujace");
        if (ps != null) {
            for (String key : ps.getKeys(false)) {
                List<ItemStack> items = new ArrayList<>();
                for (Object o : ps.getList(key, List.of())) if (o instanceof ItemStack it) items.add(it);
                pending.put(UUID.fromString(key), items);
            }
        }
    }

    public void save() {
        YamlConfiguration y = new YamlConfiguration();
        for (Nation n : nations.values()) {
            String p = "panstwa." + n.getOwner() + ".";
            y.set(p + "nazwa", n.getName());
            y.set(p + "fundament.swiat", n.getFundWorld());
            y.set(p + "fundament.x", n.getFundX());
            y.set(p + "fundament.y", n.getFundY());
            y.set(p + "fundament.z", n.getFundZ());
            y.set(p + "pierwszy-pakiet", n.isStarterPackBought());
            for (UnitType t : UnitType.values()) y.set(p + "armia." + t.key(), n.getUnits(t));
            List<String> ch = new ArrayList<>();
            for (ChunkPos c : n.getChunks()) ch.add(c.serialize());
            y.set(p + "chunki", ch);
        }
        for (Map.Entry<UUID, List<ItemStack>> e : pending.entrySet()) {
            y.set("oczekujace." + e.getKey(), e.getValue());
        }
        try {
            plugin.getDataFolder().mkdirs();
            y.save(file);
        } catch (IOException e) {
            plugin.getLogger().log(Level.SEVERE, "Nie udalo sie zapisac panstw", e);
        }
    }
}
