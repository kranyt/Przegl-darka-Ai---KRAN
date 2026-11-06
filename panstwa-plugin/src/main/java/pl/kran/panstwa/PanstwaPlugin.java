package pl.kran.panstwa;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.World;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.entity.Entity;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.plugin.java.JavaPlugin;
import pl.kran.panstwa.command.PCommand;
import pl.kran.panstwa.command.StockCommands;
import pl.kran.panstwa.gui.MenuListener;
import pl.kran.panstwa.gui.Menus;
import pl.kran.panstwa.listener.ProtectionListener;
import pl.kran.panstwa.listener.UnitListener;
import pl.kran.panstwa.market.MarketManager;
import pl.kran.panstwa.model.NationManager;
import pl.kran.panstwa.util.Msg;
import pl.kran.panstwa.war.WarManager;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class PanstwaPlugin extends JavaPlugin {
    private NationManager nations;
    private WarManager wars;
    private MarketManager market;
    private Menus menus;
    private NamespacedKey fundamentKey;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        fundamentKey = new NamespacedKey(this, "fundament");
        nations = new NationManager(this);
        nations.load();
        market = new MarketManager(this);
        market.load();
        wars = new WarManager(this);
        menus = new Menus(this);

        Bukkit.getPluginManager().registerEvents(new MenuListener(this), this);
        Bukkit.getPluginManager().registerEvents(new ProtectionListener(this), this);
        Bukkit.getPluginManager().registerEvents(new UnitListener(this), this);

        PCommand p = new PCommand(this);
        getCommand("p").setExecutor(p);
        getCommand("p").setTabCompleter(p);
        getCommand("kraj").setExecutor(p);
        getCommand("kraj").setTabCompleter(p);
        StockCommands sc = new StockCommands(this);
        for (String c : List.of("akcje", "sprzedajakcje", "mojeakcje")) {
            getCommand(c).setExecutor(sc);
            getCommand(c).setTabCompleter(sc);
        }

        // usun jednostki ktore zostaly po poprzednim uruchomieniu
        for (World w : Bukkit.getWorlds()) {
            for (Entity e : w.getEntities()) if (wars.isTaggedUnit(e)) e.remove();
        }

        wars.start();
        market.start();
        getLogger().info("Panstwa wlaczone! Panstw: " + nations.all().size() + ", akcji: " + market.all().size());
    }

    @Override
    public void onDisable() {
        if (wars != null) wars.shutdown();
        if (market != null) market.shutdown();
        if (nations != null) nations.save();
    }

    public NationManager nations() { return nations; }
    public WarManager wars() { return wars; }
    public MarketManager market() { return market; }
    public Menus menus() { return menus; }

    /** Koszt fundamentu z configu (domyslnie 64 dirt + 64 oak log). */
    public Map<Material, Integer> fundamentCost() {
        Map<Material, Integer> cost = new LinkedHashMap<>();
        ConfigurationSection s = getConfig().getConfigurationSection("fundament.koszt");
        if (s != null) {
            for (String k : s.getKeys(false)) {
                Material m = Material.matchMaterial(k);
                if (m != null) cost.put(m, s.getInt(k));
            }
        }
        if (cost.isEmpty()) {
            cost.put(Material.DIRT, 64);
            cost.put(Material.OAK_LOG, 64);
        }
        return cost;
    }

    public ItemStack fundamentItem() {
        ItemStack it = new ItemStack(Material.BEACON);
        ItemMeta meta = it.getItemMeta();
        meta.displayName(Msg.item("&6&lFundament Państwa"));
        meta.lore(List.of(Msg.item("&7Postaw ten blok, aby zalozyc panstwo."),
                Msg.item("&7Chunk z fundamentem jest nie do zniszczenia.")));
        meta.getPersistentDataContainer().set(fundamentKey, PersistentDataType.BYTE, (byte) 1);
        it.setItemMeta(meta);
        return it;
    }

    public boolean isFundamentItem(ItemStack it) {
        return it != null && it.getType() == Material.BEACON && it.hasItemMeta()
                && it.getItemMeta().getPersistentDataContainer().has(fundamentKey, PersistentDataType.BYTE);
    }
}
