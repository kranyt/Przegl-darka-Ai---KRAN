package pl.kran.panstwa.gui;

import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;

import java.util.HashMap;
import java.util.Map;

/** Holder ktory oznacza nasze menu i trzyma jego stan. */
public class MenuHolder implements InventoryHolder {
    public enum Type { FUNDAMENT, DELETE, CHUNK, ARMY, UNIT_SHOP, STOCK_CREATE, MARKET, SELL_SHARES, UPKEEP }

    final Type type;
    Inventory inventory;
    /** Dodatkowe dane menu (np. typ jednostki, cena, strona). */
    final Map<String, Object> data = new HashMap<>();
    /** Slot -> id akcji (dla menu z akcjami). */
    final Map<Integer, Integer> slotShares = new HashMap<>();

    MenuHolder(Type type) {
        this.type = type;
    }

    public Type getType() { return type; }

    @Override
    public Inventory getInventory() { return inventory; }

    @SuppressWarnings("unchecked")
    <T> T get(String key) { return (T) data.get(key); }
}
