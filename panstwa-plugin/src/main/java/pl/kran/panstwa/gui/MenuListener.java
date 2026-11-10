package pl.kran.panstwa.gui;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.inventory.Inventory;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.market.Share;
import pl.kran.panstwa.model.Nation;
import pl.kran.panstwa.util.ChunkPos;
import pl.kran.panstwa.util.Items;
import pl.kran.panstwa.util.Msg;
import pl.kran.panstwa.war.UnitType;

import java.util.ArrayList;
import java.util.List;

public class MenuListener implements Listener {
    private final PanstwaPlugin plugin;

    public MenuListener(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler
    public void onDrag(InventoryDragEvent e) {
        if (e.getView().getTopInventory().getHolder() instanceof MenuHolder) e.setCancelled(true);
    }

    @EventHandler
    public void onClick(InventoryClickEvent e) {
        Inventory top = e.getView().getTopInventory();
        if (!(top.getHolder() instanceof MenuHolder h)) return;
        e.setCancelled(true);
        if (!(e.getWhoClicked() instanceof Player p)) return;
        if (e.getClickedInventory() != top) return;
        int slot = e.getRawSlot();
        switch (h.type) {
            case FUNDAMENT -> clickFundament(p, slot);
            case DELETE -> clickDelete(p, slot);
            case CHUNK -> clickChunk(p, slot);
            case ARMY -> clickArmy(p, slot);
            case UNIT_SHOP -> clickUnitShop(p, h, slot);
            case STOCK_CREATE -> clickStock(p, h, slot);
            case MARKET -> clickMarket(p, h, slot);
            case SELL_SHARES -> clickSell(p, h, slot);
            case UPKEEP -> clickUpkeep(p, slot);
        }
    }

    private void click(Player p) {
        p.playSound(p.getLocation(), "minecraft:ui.button.click", 0.6f, 1f);
    }

    private void success(Player p) {
        p.playSound(p.getLocation(), "minecraft:entity.player.levelup", 0.7f, 1.4f);
    }

    private void fail(Player p, String msg) {
        p.playSound(p.getLocation(), "minecraft:entity.villager.no", 0.7f, 1f);
        Msg.send(p, "&c" + msg);
    }

    // ------------------------------------------------------------------
    private void clickFundament(Player p, int slot) {
        if (slot != 16) return;
        if (plugin.nations().of(p.getUniqueId()) != null) {
            fail(p, "Nalezysz juz do panstwa!");
            return;
        }
        if (!Items.take(p, plugin.fundamentCost())) {
            fail(p, "Nie masz wymaganych surowcow!");
            return;
        }
        Items.give(p, plugin.fundamentItem());
        success(p);
        p.closeInventory();
        Msg.send(p, "&aOtrzymales &6Fundament Panstwa&a! Postaw go tam, gdzie ma powstac twoje panstwo.");
    }

    private void clickDelete(Player p, int slot) {
        if (slot == 15) {
            click(p);
            p.closeInventory();
            Msg.send(p, "&7Anulowano. Panstwo nie zostalo usuniete.");
            return;
        }
        if (slot != 11) return;
        Nation n = plugin.nations().get(p.getUniqueId());
        p.closeInventory();
        if (n == null) {
            fail(p, "Nie masz panstwa.");
            return;
        }
        plugin.disband(n, "&cPanstwo &6" + n.getName() + " &czostalo usuniete.");
    }

    private void clickChunk(Player p, int slot) {
        if (slot != 15) return;
        p.closeInventory();
        Nation n = plugin.nations().of(p.getUniqueId());
        if (n == null) {
            fail(p, "Najpierw zaloz panstwo: /p fundament");
            return;
        }
        ChunkPos pos = ChunkPos.of(p.getLocation());
        Nation owner = plugin.nations().getAt(pos);
        if (owner != null) {
            fail(p, owner == n ? "Ten chunk juz nalezy do twojego panstwa." : "Ten chunk nalezy do panstwa " + owner.getName() + ". Mozesz go podbic: /p wojna");
            return;
        }
        int cost = plugin.getConfig().getInt("chunk.koszt-diamenty", 32);
        if (!Items.takeDiamonds(p, cost)) {
            fail(p, "Potrzebujesz " + cost + " diamentow!");
            return;
        }
        plugin.nations().claim(n, pos);
        plugin.nations().save();
        success(p);
        Msg.send(p, "&aKupiles chunk &f" + pos + "&a! Twoje panstwo ma teraz &f" + n.getChunks().size() + "&a chunkow.");
    }

    private void clickArmy(Player p, int slot) {
        if (slot != 11) return;
        Nation n = plugin.nations().of(p.getUniqueId());
        if (n == null) {
            p.closeInventory();
            fail(p, "Nie masz panstwa.");
            return;
        }
        int cost;
        int amount;
        if (!n.isStarterPackBought()) {
            cost = plugin.getConfig().getInt("armia.pierwszy-pakiet-koszt", 5);
            amount = plugin.getConfig().getInt("armia.pierwszy-pakiet-ilosc", 5);
        } else {
            cost = plugin.getConfig().getInt("armia.zolnierz-koszt", 5);
            amount = 1;
        }
        if (!Items.takeDiamonds(p, cost)) {
            fail(p, "Potrzebujesz " + cost + " diamentow!");
            return;
        }
        n.setStarterPackBought(true);
        n.addUnits(UnitType.SOLDIER, amount);
        plugin.nations().save();
        success(p);
        Msg.send(p, "&aKupiles &f" + amount + "&a zolnierzy. Masz ich teraz &f" + n.getUnits(UnitType.SOLDIER) + "&a.");
        plugin.menus().openArmy(p, n);
    }

    private void clickUnitShop(Player p, MenuHolder h, int slot) {
        if (slot != 15) return;
        UnitType t = h.get("unit");
        Nation n = plugin.nations().of(p.getUniqueId());
        if (n == null) {
            p.closeInventory();
            fail(p, "Nie masz panstwa.");
            return;
        }
        int cost = t.cost(plugin.getConfig());
        if (!Items.takeDiamonds(p, cost)) {
            fail(p, "Potrzebujesz " + cost + " diamentow!");
            return;
        }
        n.addUnits(t, 1);
        plugin.nations().save();
        success(p);
        Msg.send(p, "&aKupiles 1x &f" + t.display() + "&a. Masz teraz &f" + n.getUnits(t) + "&a.");
        plugin.menus().openUnitShop(p, n, t);
    }

    private void clickStock(Player p, MenuHolder h, int slot) {
        int price = h.get("price");
        int count = h.get("count");
        switch (slot) {
            case 10 -> price -= 10;
            case 11 -> price -= 1;
            case 15 -> price += 1;
            case 16 -> price += 10;
            case 20 -> count -= 1;
            case 24 -> count += 1;
            case 31 -> {
                createShares(p, h, price, count);
                return;
            }
            default -> { return; }
        }
        h.data.put("price", Math.max(1, Math.min(100000, price)));
        h.data.put("count", Math.max(1, Math.min(64, count)));
        click(p);
        plugin.menus().renderStock(h);
    }

    private void createShares(Player p, MenuHolder h, int price, int count) {
        p.closeInventory();
        Nation n = plugin.nations().get(p.getUniqueId());
        String worldName = h.get("world");
        World w = Bukkit.getWorld(worldName);
        int sx = h.get("x");
        int sz = h.get("z");
        if (n == null || w == null) {
            fail(p, "Nie masz panstwa.");
            return;
        }
        ChunkPos pos = new ChunkPos(worldName, sx >> 4, sz >> 4);
        if (plugin.nations().getAt(pos) != n) {
            fail(p, "Musisz stac na chunku swojego panstwa.");
            return;
        }
        // kolumny z farma w tym chunku, posortowane od najblizszej do miejsca gdzie stoisz
        List<int[]> columns = new ArrayList<>();
        for (int dx = 0; dx < 16; dx++) {
            for (int dz = 0; dz < 16; dz++) {
                int x = (pos.x() << 4) + dx;
                int z = (pos.z() << 4) + dz;
                if (plugin.market().at(worldName, x, z) != null) continue;
                if (plugin.market().farmIn(w, x, z) == null) continue;
                columns.add(new int[]{x, z});
            }
        }
        columns.sort((a, b) -> Integer.compare(
                (a[0] - sx) * (a[0] - sx) + (a[1] - sz) * (a[1] - sz),
                (b[0] - sx) * (b[0] - sx) + (b[1] - sz) * (b[1] - sz)));
        boolean standingOk = columns.stream().anyMatch(c -> c[0] == sx && c[1] == sz);
        if (!standingOk) {
            fail(p, "W kolumnie na ktorej stoisz (od gory do dolu) musi byc farma, ktora nie jest jeszcze akcja!");
            return;
        }
        int made = 0;
        for (int[] c : columns) {
            if (made >= count) break;
            Material icon = plugin.market().farmIn(w, c[0], c[1]);
            Share s = plugin.market().create(worldName, c[0], c[1], p.getUniqueId(), price, icon);
            made++;
            Msg.raw(p, " &8- &eAkcja #" + s.getId() + " &7kolumna &f" + c[0] + ", " + c[1]);
        }
        success(p);
        Msg.send(p, "&aWystawiono &f" + made + "&a akcji po &b" + price + " diamentow&a na rynku (/akcje).");
        if (made < count) {
            Msg.send(p, "&eW tym chunku bylo tylko " + made + " wolnych kolumn z farma.");
        }
    }

    private void clickUpkeep(Player p, int slot) {
        if (slot != 15) return;
        Nation n = plugin.nations().of(p.getUniqueId());
        if (n == null) {
            p.closeInventory();
            fail(p, "Nie nalezysz do zadnego panstwa.");
            return;
        }
        String err = plugin.upkeep().pay(p, n);
        if (err != null) {
            fail(p, err);
            return;
        }
        success(p);
        plugin.menus().openUpkeep(p, n);
    }

    private void clickMarket(Player p, MenuHolder h, int slot) {
        int page = h.get("page");
        if (slot == 45 && page > 0) { plugin.menus().openMarket(p, page - 1); return; }
        if (slot == 53) { plugin.menus().openMarket(p, page + 1); return; }
        Integer id = h.slotShares.get(slot);
        if (id == null) return;
        Share s = plugin.market().get(id);
        if (s == null) {
            fail(p, "Ta akcja juz nie istnieje.");
            plugin.menus().openMarket(p, page);
            return;
        }
        String err = plugin.market().buy(p, s);
        if (err != null) {
            fail(p, err);
            return;
        }
        success(p);
        Msg.send(p, "&aKupiles akcje &f#" + s.getId() + "&a za &b" + s.getPrice()
                + " diamentow&a! Co 3 minuty dostaniesz plony z tej farmy.");
        plugin.menus().openMarket(p, page);
    }

    private void clickSell(Player p, MenuHolder h, int slot) {
        int page = h.get("page");
        if (slot == 45 && page > 0) { plugin.menus().openSell(p, page - 1); return; }
        if (slot == 53) { plugin.menus().openSell(p, page + 1); return; }
        Integer id = h.slotShares.get(slot);
        if (id == null) return;
        Share s = plugin.market().get(id);
        if (s == null) {
            fail(p, "Ta akcja juz nie istnieje.");
            plugin.menus().openSell(p, page);
            return;
        }
        int price = s.getPrice();
        String err = plugin.market().sellToServer(p, s);
        if (err != null) {
            fail(p, err);
            return;
        }
        success(p);
        Msg.send(p, "&aSprzedales akcje &f#" + id + "&a serwerowi za &b" + price + " diamentow&a.");
        plugin.menus().openSell(p, page);
    }

}
