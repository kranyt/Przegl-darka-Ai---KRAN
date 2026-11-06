package pl.kran.panstwa.gui;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.OfflinePlayer;
import org.bukkit.entity.Player;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.market.Share;
import pl.kran.panstwa.model.Nation;
import pl.kran.panstwa.util.Items;
import pl.kran.panstwa.util.Msg;
import pl.kran.panstwa.war.UnitType;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/** Budowanie wszystkich menu. Klikniecia obsluguje MenuListener. */
public class Menus {
    private final PanstwaPlugin plugin;

    public Menus(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    private Inventory create(MenuHolder h, int size, String title) {
        Inventory inv = Bukkit.createInventory(h, size, Msg.c(title));
        h.inventory = inv;
        ItemStack filler = Items.icon(Material.GRAY_STAINED_GLASS_PANE, " ");
        for (int i = 0; i < size; i++) inv.setItem(i, filler);
        return inv;
    }

    private String status(boolean ok) {
        return ok ? "&a✔ Masz wystarczajaco" : "&c✘ Brakuje ci";
    }

    // ------------------------------------------------------------------ /p fundament
    public void openFundament(Player p) {
        MenuHolder h = new MenuHolder(MenuHolder.Type.FUNDAMENT);
        Inventory inv = create(h, 27, "&6&lFundament Państwa");
        Map<Material, Integer> cost = plugin.fundamentCost();
        int slot = 10;
        for (Map.Entry<Material, Integer> e : cost.entrySet()) {
            boolean ok = Items.count(p, e.getKey()) >= e.getValue();
            inv.setItem(slot, Items.icon(e.getKey(), e.getValue(), "&e" + e.getValue() + "x " + pretty(e.getKey()),
                    "&7Potrzebne do fundamentu", "&7Masz: &f" + Items.count(p, e.getKey()), status(ok)));
            slot += 1;
        }
        inv.setItem(13, Items.icon(Material.BEACON, "&6&lFundament",
                "&7Postaw go, aby zalozyc panstwo.", "&7Dostajesz chunk ktorego", "&7nikt nie moze zniszczyc."));
        inv.setItem(16, Items.icon(Material.LIME_CONCRETE, "&a&lKup Fundament",
                "&7Kliknij aby wymienic surowce", "&7na Fundament Panstwa."));
        p.openInventory(inv);
    }

    // ------------------------------------------------------------------ usuwanie panstwa
    public void openDelete(Player p) {
        MenuHolder h = new MenuHolder(MenuHolder.Type.DELETE);
        Inventory inv = create(h, 27, "&4Czy chcesz usunąć państwo?");
        inv.setItem(4, Items.icon(Material.PAPER, "&c&lCzy chcesz usunąć państwo?",
                "&7Stracisz wszystkie chunki", "&7i cala armie!"));
        inv.setItem(11, Items.icon(Material.LIME_WOOL, "&a&lTAK", "&7Usun panstwo"));
        inv.setItem(15, Items.icon(Material.RED_WOOL, "&c&lNIE", "&7Anuluj"));
        p.openInventory(inv);
    }

    // ------------------------------------------------------------------ /p chunk
    public void openChunk(Player p) {
        int cost = plugin.getConfig().getInt("chunk.koszt-diamenty", 32);
        MenuHolder h = new MenuHolder(MenuHolder.Type.CHUNK);
        Inventory inv = create(h, 27, "&b&lKup Chunk");
        boolean ok = Items.count(p, Material.DIAMOND) >= cost;
        inv.setItem(11, Items.icon(Material.DIAMOND, cost, "&b" + cost + "x Diament",
                "&7Koszt nowego chunka", "&7Masz: &f" + Items.count(p, Material.DIAMOND), status(ok)));
        inv.setItem(13, Items.icon(Material.GRASS_BLOCK, "&aChunk na ktorym stoisz",
                "&7X: &f" + (p.getLocation().getBlockX() >> 4) + " &7Z: &f" + (p.getLocation().getBlockZ() >> 4),
                "&7Chunki poza fundamentem", "&7moga zostac podbite na wojnie!"));
        inv.setItem(15, Items.icon(Material.LIME_CONCRETE, "&a&lKup Chunk", "&7Kliknij aby kupic ten chunk."));
        p.openInventory(inv);
    }

    // ------------------------------------------------------------------ /p armia
    public void openArmy(Player p, Nation n) {
        MenuHolder h = new MenuHolder(MenuHolder.Type.ARMY);
        Inventory inv = create(h, 27, "&c&lArmia &8- &7" + n.getName());
        int first = plugin.getConfig().getInt("armia.pierwszy-pakiet-koszt", 5);
        int firstAmount = plugin.getConfig().getInt("armia.pierwszy-pakiet-ilosc", 5);
        int next = plugin.getConfig().getInt("armia.zolnierz-koszt", 5);
        double hp = UnitType.SOLDIER.hp(plugin.getConfig());
        if (!n.isStarterPackBought()) {
            inv.setItem(11, Items.icon(Material.IRON_SWORD, firstAmount, "&a&lKup " + firstAmount + " zolnierzy",
                    "&7Koszt: &b" + first + "x Diament", "&7Pierwszy zakup - pakiet startowy!",
                    "&7HP: &c" + (int) hp + " (" + (hp / 2) + " serc)"));
        } else {
            inv.setItem(11, Items.icon(Material.IRON_SWORD, "&a&lKup 1 zolnierza",
                    "&7Koszt: &b" + next + "x Diament", "&7HP: &c" + (int) hp + " (" + (hp / 2) + " serc)"));
        }
        inv.setItem(13, armyInfo(n));
        inv.setItem(15, Items.icon(Material.PHANTOM_MEMBRANE, "&b&lLotnictwo",
                "&7Drony: &f/p drony", "&7Samoloty: &f/p samolot", "&7Jety: &f/p jet",
                "&7Lotnictwo doleci wszedzie,", "&7takze dalej niz 16 chunkow."));
        p.openInventory(inv);
    }

    private ItemStack armyInfo(Nation n) {
        List<String> lore = new ArrayList<>();
        for (UnitType t : UnitType.values()) lore.add("&7" + t.plural() + ": &f" + n.getUnits(t));
        return Items.icon(Material.SHIELD, 1, "&6&lTwoja armia", lore);
    }

    // ------------------------------------------------------------------ /p drony /p samolot /p jet
    public void openUnitShop(Player p, Nation n, UnitType t) {
        MenuHolder h = new MenuHolder(MenuHolder.Type.UNIT_SHOP);
        h.data.put("unit", t);
        int cost = t.cost(plugin.getConfig());
        Inventory inv = create(h, 27, "&b&lKup: " + t.display());
        boolean ok = Items.count(p, Material.DIAMOND) >= cost;
        inv.setItem(11, Items.icon(Material.DIAMOND, Math.min(cost, 64), "&bKoszt: " + Items.stacksText(cost) + " Diament",
                "&7Masz: &f" + Items.count(p, Material.DIAMOND), status(ok)));
        inv.setItem(13, Items.icon(t.icon(), "&f&l" + t.display(),
                "&7HP: &c" + (int) t.hp(plugin.getConfig()),
                "&7Predkosc: &f" + t.speed(plugin.getConfig()),
                "&7Obrazenia: &f" + (int) t.damage(plugin.getConfig()),
                "&7Leci - doleci wszedzie.",
                "&7Posiadasz: &f" + n.getUnits(t)));
        inv.setItem(15, Items.icon(Material.LIME_CONCRETE, "&a&lKup 1x " + t.display(), "&7Kliknij aby kupic."));
        p.openInventory(inv);
    }

    // ------------------------------------------------------------------ /p gielda
    public void openStockCreate(Player p, int price, int count) {
        MenuHolder h = new MenuHolder(MenuHolder.Type.STOCK_CREATE);
        h.data.put("price", price);
        h.data.put("count", count);
        h.data.put("world", p.getWorld().getName());
        h.data.put("x", p.getLocation().getBlockX());
        h.data.put("z", p.getLocation().getBlockZ());
        Inventory inv = create(h, 36, "&e&lGiełda &8- wystaw akcje");
        renderStock(h);
        p.openInventory(inv);
    }

    void renderStock(MenuHolder h) {
        Inventory inv = h.inventory;
        int price = h.get("price");
        int count = h.get("count");
        inv.setItem(10, Items.icon(Material.RED_STAINED_GLASS_PANE, "&c-10 diamentow"));
        inv.setItem(11, Items.icon(Material.PINK_STAINED_GLASS_PANE, "&c-1 diament"));
        inv.setItem(13, Items.icon(Material.DIAMOND, Math.min(price, 64), "&bCena 1 akcji: &f" + price + " diamentow",
                "&7Ty jako wlasciciel panstwa", "&7ustalasz pierwsza cene."));
        inv.setItem(15, Items.icon(Material.LIME_STAINED_GLASS_PANE, "&a+1 diament"));
        inv.setItem(16, Items.icon(Material.GREEN_STAINED_GLASS_PANE, "&a+10 diamentow"));
        inv.setItem(20, Items.icon(Material.PINK_STAINED_GLASS_PANE, "&c-1 akcja"));
        inv.setItem(22, Items.icon(Material.WHEAT, count, "&eIlosc akcji: &f" + count,
                "&71 akcja = 1 kolumna blokow", "&7(od samej gory do samego dolu)", "&7z farma, zaczynajac od tej",
                "&7na ktorej stoisz.", "&7Posiadacz akcji dostaje plony", "&7co 3 minuty."));
        inv.setItem(24, Items.icon(Material.LIME_STAINED_GLASS_PANE, "&a+1 akcja"));
        inv.setItem(31, Items.icon(Material.LIME_CONCRETE, "&a&lWystaw akcje", "&7" + count + "x po " + price + " diamentow"));
    }

    // ------------------------------------------------------------------ /akcje
    public void openMarket(Player p, int page) {
        MenuHolder h = new MenuHolder(MenuHolder.Type.MARKET);
        h.data.put("page", page);
        Inventory inv = create(h, 54, "&a&lRynek akcji &8(strona " + (page + 1) + ")");
        List<Share> list = plugin.market().forSale();
        fillShares(h, list, page, true);
        p.openInventory(inv);
    }

    // ------------------------------------------------------------------ /sprzedajakcje
    public void openSell(Player p, int page) {
        MenuHolder h = new MenuHolder(MenuHolder.Type.SELL_SHARES);
        h.data.put("page", page);
        Inventory inv = create(h, 54, "&c&lSprzedaj akcje &8(strona " + (page + 1) + ")");
        List<Share> list = new ArrayList<>();
        for (Share s : plugin.market().ownedBy(p.getUniqueId())) if (!s.isForSale()) list.add(s);
        fillShares(h, list, page, false);
        p.openInventory(inv);
    }

    private void fillShares(MenuHolder h, List<Share> list, int page, boolean buying) {
        Inventory inv = h.inventory;
        for (int i = 0; i < 45; i++) inv.setItem(i, null);
        int start = page * 45;
        for (int i = 0; i < 45 && start + i < list.size(); i++) {
            Share s = list.get(start + i);
            Nation n = plugin.nations().get(s.getIssuer());
            List<String> lore = new ArrayList<>();
            lore.add("&7Cena: &b" + s.getPrice() + " diamentow");
            lore.add("&7Panstwo: &f" + (n == null ? "-" : n.getName()));
            lore.add("&7Kolumna: &f" + s.getX() + ", " + s.getZ() + " &7(" + s.getWorld() + ")");
            lore.add("&7Sprzedawca: &f" + holderName(s.getHolder()));
            lore.add("");
            lore.add(buying ? "&aKliknij aby kupic" : "&cKliknij aby sprzedac serwerowi za " + s.getPrice());
            inv.setItem(i, Items.icon(s.getIcon(), 1, "&eAkcja #" + s.getId(), lore));
            h.slotShares.put(i, s.getId());
        }
        if (list.isEmpty()) {
            inv.setItem(22, Items.icon(Material.BARRIER, buying ? "&cBrak akcji na sprzedaz" : "&cNie masz zadnych akcji"));
        }
        if (page > 0) inv.setItem(45, Items.icon(Material.ARROW, "&ePoprzednia strona"));
        if (start + 45 < list.size()) inv.setItem(53, Items.icon(Material.ARROW, "&eNastepna strona"));
        inv.setItem(49, Items.icon(Material.BOOK, "&6Gielda",
                "&7Ceny zmieniaja sie co 5 minut:", "&a35% &7- drozeje o 15-110%",
                "&c35% &7- tanieje o 30-70%", "&430% &7- akcja znika!"));
    }

    public String holderName(UUID id) {
        if (id == null) return "Serwer";
        OfflinePlayer op = Bukkit.getOfflinePlayer(id);
        return op.getName() == null ? "?" : op.getName();
    }

    public static String pretty(Material m) {
        return switch (m) {
            case DIRT -> "Ziemia (Dirt)";
            case OAK_LOG -> "Drewno debowe";
            case DIAMOND -> "Diament";
            default -> m.name().toLowerCase().replace('_', ' ');
        };
    }
}
