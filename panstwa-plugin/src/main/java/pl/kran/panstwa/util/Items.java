package pl.kran.panstwa.util;

import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemFlag;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public final class Items {
    private Items() {}

    public static ItemStack icon(Material mat, int amount, String name, String... lore) {
        ItemStack it = new ItemStack(mat, Math.max(1, Math.min(amount, mat.getMaxStackSize())));
        ItemMeta meta = it.getItemMeta();
        meta.displayName(Msg.item(name));
        List<net.kyori.adventure.text.Component> l = new ArrayList<>();
        for (String s : lore) l.add(Msg.item(s));
        meta.lore(l);
        meta.addItemFlags(ItemFlag.values());
        it.setItemMeta(meta);
        return it;
    }

    public static ItemStack icon(Material mat, String name, String... lore) {
        return icon(mat, 1, name, lore);
    }

    public static ItemStack icon(Material mat, int amount, String name, List<String> lore) {
        return icon(mat, amount, name, lore.toArray(new String[0]));
    }

    public static int count(Player p, Material mat) {
        int n = 0;
        for (ItemStack it : p.getInventory().getStorageContents()) {
            if (it != null && it.getType() == mat && !it.hasItemMeta()) n += it.getAmount();
        }
        return n;
    }

    public static boolean has(Player p, Map<Material, Integer> cost) {
        for (Map.Entry<Material, Integer> e : cost.entrySet()) {
            if (count(p, e.getKey()) < e.getValue()) return false;
        }
        return true;
    }

    /** Zabiera przedmioty (tylko "czyste", bez zmienionej nazwy). Zwraca false jesli brakuje. */
    public static boolean take(Player p, Map<Material, Integer> cost) {
        if (!has(p, cost)) return false;
        for (Map.Entry<Material, Integer> e : cost.entrySet()) {
            int left = e.getValue();
            ItemStack[] contents = p.getInventory().getStorageContents();
            for (int i = 0; i < contents.length && left > 0; i++) {
                ItemStack it = contents[i];
                if (it == null || it.getType() != e.getKey() || it.hasItemMeta()) continue;
                int t = Math.min(left, it.getAmount());
                it.setAmount(it.getAmount() - t);
                left -= t;
                contents[i] = it.getAmount() <= 0 ? null : it;
            }
            p.getInventory().setStorageContents(contents);
        }
        return true;
    }

    public static boolean takeDiamonds(Player p, int amount) {
        return take(p, Map.of(Material.DIAMOND, amount));
    }

    /** Daje przedmioty, nadmiar wyrzuca pod nogi. */
    public static void give(Player p, ItemStack... items) {
        Location loc = p.getLocation();
        for (ItemStack rest : p.getInventory().addItem(items).values()) {
            loc.getWorld().dropItemNaturally(loc, rest);
        }
    }

    /** Dzieli duza ilosc na stacki. */
    public static List<ItemStack> stacks(Material mat, int amount) {
        List<ItemStack> list = new ArrayList<>();
        while (amount > 0) {
            int s = Math.min(amount, mat.getMaxStackSize());
            list.add(new ItemStack(mat, s));
            amount -= s;
        }
        return list;
    }

    public static String stacksText(int amount) {
        if (amount <= 64) return amount + "x";
        int full = amount / 64;
        int rest = amount % 64;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < full; i++) sb.append(i == 0 ? "" : " + ").append("64x");
        if (rest > 0) sb.append(" + ").append(rest).append("x");
        return sb.toString() + " (" + amount + ")";
    }
}
