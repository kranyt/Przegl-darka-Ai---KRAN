package pl.kran.panstwa.market;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.block.data.Ageable;
import org.bukkit.block.data.BlockData;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.scheduler.BukkitTask;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.util.Items;
import pl.kran.panstwa.util.Msg;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;
import java.util.logging.Level;

public class MarketManager {
    /** Rosliny ktore zbieramy i sadzimy od nowa (Ageable). */
    private static final Set<Material> CROPS = EnumSet.of(Material.WHEAT, Material.CARROTS, Material.POTATOES,
            Material.BEETROOTS, Material.NETHER_WART, Material.COCOA, Material.SWEET_BERRY_BUSH);
    /** Owoce rosnace z lodyg. */
    private static final Set<Material> FRUITS = EnumSet.of(Material.MELON, Material.PUMPKIN);
    /** Rosliny rosnace w gore (zbieramy wszystko powyzej pierwszego bloku). */
    private static final Set<Material> TALL = EnumSet.of(Material.SUGAR_CANE, Material.CACTUS, Material.BAMBOO, Material.KELP_PLANT);
    /** Bloki ktore licza sie jako "farma". */
    private static final Set<Material> FARM = EnumSet.noneOf(Material.class);
    static {
        FARM.addAll(CROPS);
        FARM.addAll(FRUITS);
        FARM.addAll(TALL);
        FARM.add(Material.MELON_STEM);
        FARM.add(Material.PUMPKIN_STEM);
        FARM.add(Material.ATTACHED_MELON_STEM);
        FARM.add(Material.ATTACHED_PUMPKIN_STEM);
        FARM.add(Material.KELP);
        FARM.add(Material.BAMBOO_SAPLING);
    }

    private final PanstwaPlugin plugin;
    private final File file;
    private final Map<Integer, Share> shares = new LinkedHashMap<>();
    /** Bloki do posadzenia ponownie (lokalizacja -> dane bloku). */
    private final Map<Block, BlockData> replant = new HashMap<>();
    /** Gracz -> lista powiadomien o wygaslych akcjach. */
    private final Map<UUID, List<String>> notices = new HashMap<>();
    private int nextId = 1;
    private final List<BukkitTask> tasks = new ArrayList<>();

    public MarketManager(PanstwaPlugin plugin) {
        this.plugin = plugin;
        this.file = new File(plugin.getDataFolder(), "gielda.yml");
    }

    private FileConfiguration cfg() { return plugin.getConfig(); }

    public void start() {
        long harvest = cfg().getLong("gielda.zbior-co-sekund", 180) * 20L;
        long step = cfg().getLong("gielda.krok-cen-co-sekund", 180) * 20L;
        tasks.add(Bukkit.getScheduler().runTaskTimer(plugin, this::harvestAll, harvest, harvest));
        tasks.add(Bukkit.getScheduler().runTaskTimer(plugin, this::priceStep, step, step));
        tasks.add(Bukkit.getScheduler().runTaskTimer(plugin, this::checkUnsold, 1200L, 1200L));
    }

    public void shutdown() {
        tasks.forEach(BukkitTask::cancel);
        // posadz od razu wszystko co czeka, zeby nic nie zginelo przy restarcie
        for (Map.Entry<Block, BlockData> e : replant.entrySet()) {
            if (e.getKey().getType().isAir()) e.getKey().setBlockData(e.getValue(), false);
        }
        replant.clear();
        save();
    }

    public Collection<Share> all() { return shares.values(); }

    public Share get(int id) { return shares.get(id); }

    public List<Share> forSale() {
        List<Share> l = new ArrayList<>();
        for (Share s : shares.values()) if (s.forSale) l.add(s);
        return l;
    }

    public List<Share> ownedBy(UUID player) {
        List<Share> l = new ArrayList<>();
        for (Share s : shares.values()) if (player.equals(s.holder)) l.add(s);
        return l;
    }

    public Share at(String world, int x, int z) {
        for (Share s : shares.values()) if (s.world.equals(world) && s.x == x && s.z == z) return s;
        return null;
    }

    // ---------------------------------------------------------------
    //  Farma w kolumnie
    // ---------------------------------------------------------------

    /** Czy w kolumnie (od gory do dolu) jest jakas farma. Zwraca ikone rosliny albo null. */
    public Material farmIn(World w, int x, int z) {
        for (int y = w.getMaxHeight() - 1; y >= w.getMinHeight(); y--) {
            Material m = w.getBlockAt(x, y, z).getType();
            if (FARM.contains(m)) return iconFor(m);
        }
        return null;
    }

    private Material iconFor(Material m) {
        return switch (m) {
            case WHEAT -> Material.WHEAT;
            case CARROTS -> Material.CARROT;
            case POTATOES -> Material.POTATO;
            case BEETROOTS -> Material.BEETROOT;
            case NETHER_WART -> Material.NETHER_WART;
            case COCOA -> Material.COCOA_BEANS;
            case SWEET_BERRY_BUSH -> Material.SWEET_BERRIES;
            case MELON, MELON_STEM, ATTACHED_MELON_STEM -> Material.MELON_SLICE;
            case PUMPKIN, PUMPKIN_STEM, ATTACHED_PUMPKIN_STEM -> Material.PUMPKIN;
            case SUGAR_CANE -> Material.SUGAR_CANE;
            case CACTUS -> Material.CACTUS;
            case BAMBOO, BAMBOO_SAPLING -> Material.BAMBOO;
            case KELP, KELP_PLANT -> Material.KELP;
            default -> Material.WHEAT;
        };
    }

    // ---------------------------------------------------------------
    //  Wystawianie / kupno / sprzedaz
    // ---------------------------------------------------------------

    /** Ile czasu (ms) zostalo zanim niesprzedana akcja wygasnie. */
    public long timeLeft(Share s) {
        long max = cfg().getLong("gielda.wygasanie-niesprzedanej-godziny", 24) * 3600_000L;
        return Math.max(0, s.listedAt + max - System.currentTimeMillis());
    }

    public Share create(String world, int x, int z, UUID issuer, int price, Material icon) {
        double med = median();
        Share s = new Share(nextId++, world, x, z, issuer);
        s.holder = issuer;
        s.forSale = true;
        s.exact = Math.max(1, price);
        s.listedAt = System.currentTimeMillis();
        s.icon = icon;
        // wystawiona taniej niz wiekszosc akcji -> od razu zaczyna drozec
        if (s.exact < med) {
            double pct = upPercent();
            s.trendTarget = s.exact * (1 + pct);
            s.trendPct = (int) Math.round(pct * 100);
        }
        shares.put(s.id, s);
        save();
        return s;
    }

    /** Kupno akcji z rynku. Zwraca komunikat bledu albo null gdy OK. */
    public String buy(Player buyer, Share s) {
        if (!shares.containsKey(s.id) || !s.forSale) return "Ta akcja nie jest juz na sprzedaz.";
        if (buyer.getUniqueId().equals(s.holder)) return "Nie mozesz kupic wlasnej akcji.";
        int price = s.getPrice();
        if (!Items.takeDiamonds(buyer, price)) return "Potrzebujesz " + price + " diamentow.";
        UUID seller = s.holder;
        if (seller != null) {
            List<ItemStack> pay = Items.stacks(Material.DIAMOND, price);
            Player sp = Bukkit.getPlayer(seller);
            if (sp != null) {
                Items.give(sp, pay.toArray(new ItemStack[0]));
                Msg.send(sp, "&a" + buyer.getName() + " kupil twoja akcje #" + s.id + " za &b" + price + " diamentow&a!");
            } else {
                plugin.nations().addPending(seller, pay);
            }
        }
        s.holder = buyer.getUniqueId();
        s.forSale = false;
        save();
        return null;
    }

    /** Sprzedaz akcji serwerowi po aktualnej cenie. Akcja wraca na rynek. */
    public String sellToServer(Player p, Share s) {
        if (!shares.containsKey(s.id) || !p.getUniqueId().equals(s.holder) || s.forSale) {
            return "Nie masz tej akcji.";
        }
        Items.give(p, Items.stacks(Material.DIAMOND, s.getPrice()).toArray(new ItemStack[0]));
        s.holder = null;
        s.forSale = true;
        s.listedAt = System.currentTimeMillis();
        save();
        return null;
    }

    // ---------------------------------------------------------------
    //  Zbior plonow co 3 minuty
    // ---------------------------------------------------------------

    private void harvestAll() {
        for (Share s : shares.values()) {
            if (s.forSale || s.holder == null) continue;
            World w = Bukkit.getWorld(s.world);
            if (w == null) continue;
            List<ItemStack> drops = harvestColumn(w, s.x, s.z);
            if (drops.isEmpty()) continue;
            Player p = Bukkit.getPlayer(s.holder);
            if (p != null) {
                Items.give(p, drops.toArray(new ItemStack[0]));
                Msg.send(p, "&aZebrano plony z akcji &f#" + s.id + "&a (" + drops.stream().mapToInt(ItemStack::getAmount).sum() + " przedmiotow).");
            } else {
                plugin.nations().addPending(s.holder, drops);
            }
        }
    }

    private List<ItemStack> harvestColumn(World w, int x, int z) {
        List<ItemStack> drops = new ArrayList<>();
        w.getChunkAt(x >> 4, z >> 4); // zaladuj chunk
        long delay = cfg().getLong("gielda.sadzenie-po-sekundach", 120) * 20L;
        for (int y = w.getMaxHeight() - 1; y >= w.getMinHeight(); y--) {
            Block b = w.getBlockAt(x, y, z);
            Material m = b.getType();
            if (CROPS.contains(m) && b.getBlockData() instanceof Ageable age) {
                if (age.getAge() < age.getMaximumAge()) continue;
                drops.addAll(b.getDrops());
                if (m == Material.SWEET_BERRY_BUSH) {
                    age.setAge(1);
                    b.setBlockData(age, false);
                    continue;
                }
                Ageable seed = (Ageable) age.clone();
                seed.setAge(0);
                b.setType(Material.AIR, false);
                scheduleReplant(b, seed, delay);
            } else if (FRUITS.contains(m)) {
                drops.addAll(b.getDrops());
                b.setType(Material.AIR, false);
            } else if (TALL.contains(m) || m == Material.KELP) {
                Material below = b.getRelative(0, -1, 0).getType();
                boolean sameBelow = below == m || (m == Material.KELP && below == Material.KELP_PLANT)
                        || (m == Material.KELP_PLANT && below == Material.KELP_PLANT);
                if (!sameBelow) continue;
                drops.addAll(b.getDrops());
                BlockData orig = b.getBlockData();
                b.setType(m == Material.KELP || m == Material.KELP_PLANT ? Material.WATER : Material.AIR, false);
                if (m == Material.KELP || m == Material.KELP_PLANT) continue;
                scheduleReplant(b, orig, delay);
            }
        }
        return drops;
    }

    private void scheduleReplant(Block b, BlockData data, long delay) {
        replant.put(b, data);
        Bukkit.getScheduler().runTaskLater(plugin, () -> {
            BlockData d = replant.remove(b);
            if (d != null && b.getType().isAir()) {
                b.setBlockData(d, false);
            }
        }, delay);
    }

    // ---------------------------------------------------------------
    //  Zmiana cen - stopniowo, krok co 3 minuty
    // ---------------------------------------------------------------

    /** Mediana cen wszystkich akcji - ponizej niej akcja jest "tania". */
    private double median() {
        List<Double> prices = new ArrayList<>();
        for (Share s : shares.values()) prices.add(s.exact);
        if (prices.isEmpty()) return 0;
        prices.sort(Double::compare);
        int n = prices.size();
        return n % 2 == 1 ? prices.get(n / 2) : (prices.get(n / 2 - 1) + prices.get(n / 2)) / 2.0;
    }

    public boolean isCheap(Share s) {
        return s.exact < median();
    }

    private double range(double min, double max) {
        return (min + ThreadLocalRandom.current().nextDouble() * (max - min)) / 100.0;
    }

    /** O ile procent akcja ma podrozec: najczesciej 5-16%, rzadko 17-60%. */
    private double upPercent() {
        double r = ThreadLocalRandom.current().nextDouble(100);
        if (r < cfg().getDouble("gielda.drozenie.czesto-szansa", 85)) {
            return range(cfg().getDouble("gielda.drozenie.czesto-min", 5), cfg().getDouble("gielda.drozenie.czesto-max", 16));
        }
        return range(cfg().getDouble("gielda.drozenie.rzadko-min", 17), cfg().getDouble("gielda.drozenie.rzadko-max", 60));
    }

    /** O ile procent akcja ma stanie: czesto 5-15%, rzadko 16-30%, bardzo rzadko 31-80%. */
    private double downPercent() {
        double r = ThreadLocalRandom.current().nextDouble(100);
        double often = cfg().getDouble("gielda.tanienie.czesto-szansa", 80);
        double rare = cfg().getDouble("gielda.tanienie.rzadko-szansa", 18);
        if (r < often) {
            return range(cfg().getDouble("gielda.tanienie.czesto-min", 5), cfg().getDouble("gielda.tanienie.czesto-max", 15));
        }
        if (r < often + rare) {
            return range(cfg().getDouble("gielda.tanienie.rzadko-min", 16), cfg().getDouble("gielda.tanienie.rzadko-max", 30));
        }
        return range(cfg().getDouble("gielda.tanienie.bardzo-rzadko-min", 31), cfg().getDouble("gielda.tanienie.bardzo-rzadko-max", 80));
    }

    /**
     * Co 3 minuty: akcja bez trendu losuje nowy (wygasa / tanieje / drozeje),
     * a potem cena przesuwa sie w strone celu malymi krokami (max ~3% na krok),
     * zeby nie bylo nagle +40%.
     */
    private void priceStep() {
        if (shares.isEmpty()) return;
        ThreadLocalRandom r = ThreadLocalRandom.current();
        double med = median();
        double maxStep = cfg().getDouble("gielda.max-krok-procent", 3);
        double minStep = cfg().getDouble("gielda.min-krok-procent", 1);
        boolean changed = false;

        for (Share s : new ArrayList<>(shares.values())) {
            if (!s.hasTrend()) {
                boolean cheap = s.exact < med;
                String k = cheap ? "gielda.tania." : "gielda.droga.";
                double pGone = cfg().getDouble(k + "szansa-wygasniecia", cheap ? 5 : 15);
                double pDown = cfg().getDouble(k + "szansa-stanienia", cheap ? 20 : 35);
                double roll = r.nextDouble(100);
                if (roll < pGone) {
                    expire(s, "wygasla na gieldzie");
                    changed = true;
                    continue;
                }
                double pct = roll < pGone + pDown ? -downPercent() : upPercent();
                s.trendTarget = Math.max(1.0, s.exact * (1 + pct));
                s.trendPct = (int) Math.round(pct * 100);
            }
            // jeden maly krok w strone celu
            double step = range(minStep, maxStep);
            if (s.trendTarget > s.exact) {
                s.exact = Math.min(s.trendTarget, s.exact * (1 + step));
            } else {
                s.exact = Math.max(s.trendTarget, Math.max(1.0, s.exact * (1 - step)));
            }
            if (Math.abs(s.exact - s.trendTarget) < 0.0001 || (s.exact <= 1.0 && s.trendTarget <= 1.0)) {
                s.trendTarget = 0;
                s.trendPct = 0;
            }
            changed = true;
        }
        if (changed) save();
    }

    /** Akcje ktore nie sprzedaly sie przez 24h wygasaja. */
    private void checkUnsold() {
        long max = cfg().getLong("gielda.wygasanie-niesprzedanej-godziny", 24) * 3600_000L;
        long now = System.currentTimeMillis();
        boolean changed = false;
        for (Share s : new ArrayList<>(shares.values())) {
            if (s.forSale && now - s.listedAt >= max) {
                expire(s, "nie sprzedala sie przez " + (max / 3600_000L) + "h");
                changed = true;
            }
        }
        if (changed) save();
    }

    private void expire(Share s, String reason) {
        shares.remove(s.id);
        if (s.holder == null) return;
        String note = "&cAkcja #" + s.id + " &7(" + s.x + ", " + s.z + ", cena " + s.getPrice() + ") &c" + reason + "!";
        notices.computeIfAbsent(s.holder, k -> new ArrayList<>()).add(note);
        Player p = Bukkit.getPlayer(s.holder);
        if (p != null) {
            Msg.send(p, note);
            Msg.send(p, "&7Szczegoly zobaczysz w &f/mojeakcje&7.");
        }
    }

    // ---------------------------------------------------------------
    //  Powiadomienia o wygaslych akcjach (zostaja az gracz je zobaczy)
    // ---------------------------------------------------------------

    public int noticeCount(UUID player) {
        List<String> l = notices.get(player);
        return l == null ? 0 : l.size();
    }

    /** Zwraca i usuwa powiadomienia (gracz je wlasnie zobaczyl). */
    public List<String> takeNotices(UUID player) {
        List<String> l = notices.remove(player);
        if (l != null) save();
        return l == null ? List.of() : l;
    }

    // ---------------------------------------------------------------
    //  Zapis / odczyt
    // ---------------------------------------------------------------

    public void load() {
        shares.clear();
        notices.clear();
        if (!file.exists()) return;
        YamlConfiguration y = YamlConfiguration.loadConfiguration(file);
        nextId = y.getInt("nastepne-id", 1);
        ConfigurationSection ns = y.getConfigurationSection("powiadomienia");
        if (ns != null) {
            for (String key : ns.getKeys(false)) notices.put(UUID.fromString(key), new ArrayList<>(ns.getStringList(key)));
        }
        ConfigurationSection sec = y.getConfigurationSection("akcje");
        if (sec == null) return;
        for (String key : sec.getKeys(false)) {
            try {
                ConfigurationSection c = sec.getConfigurationSection(key);
                Share s = new Share(Integer.parseInt(key), c.getString("swiat"), c.getInt("x"), c.getInt("z"),
                        UUID.fromString(c.getString("wystawca")));
                String h = c.getString("posiadacz");
                s.holder = h == null || h.isEmpty() ? null : UUID.fromString(h);
                s.forSale = c.getBoolean("na-sprzedaz");
                s.exact = c.getDouble("cena");
                s.listedAt = c.getLong("wystawiona", System.currentTimeMillis());
                s.trendTarget = c.getDouble("trend-cel", 0);
                s.trendPct = c.getInt("trend-procent", 0);
                s.icon = Material.matchMaterial(c.getString("ikona", "WHEAT"));
                shares.put(s.id, s);
                nextId = Math.max(nextId, s.id + 1);
            } catch (Exception e) {
                plugin.getLogger().log(Level.WARNING, "Nie udalo sie wczytac akcji " + key, e);
            }
        }
    }

    public void save() {
        YamlConfiguration y = new YamlConfiguration();
        y.set("nastepne-id", nextId);
        for (Map.Entry<UUID, List<String>> e : notices.entrySet()) y.set("powiadomienia." + e.getKey(), e.getValue());
        for (Share s : shares.values()) {
            String p = "akcje." + s.id + ".";
            y.set(p + "swiat", s.world);
            y.set(p + "x", s.x);
            y.set(p + "z", s.z);
            y.set(p + "wystawca", s.issuer.toString());
            y.set(p + "posiadacz", s.holder == null ? "" : s.holder.toString());
            y.set(p + "na-sprzedaz", s.forSale);
            y.set(p + "cena", s.exact);
            y.set(p + "wystawiona", s.listedAt);
            y.set(p + "trend-cel", s.trendTarget);
            y.set(p + "trend-procent", s.trendPct);
            y.set(p + "ikona", s.getIcon().name());
        }
        try {
            plugin.getDataFolder().mkdirs();
            y.save(file);
        } catch (IOException e) {
            plugin.getLogger().log(Level.SEVERE, "Nie udalo sie zapisac gieldy", e);
        }
    }
}
