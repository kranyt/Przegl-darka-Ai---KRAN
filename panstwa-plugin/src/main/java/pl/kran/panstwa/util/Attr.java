package pl.kran.panstwa.util;

import org.bukkit.NamespacedKey;
import org.bukkit.Registry;
import org.bukkit.attribute.Attribute;
import org.bukkit.attribute.AttributeInstance;
import org.bukkit.entity.LivingEntity;

/**
 * Atrybuty pobierane po kluczu, zeby plugin dzialal na kazdej wersji 1.21.x
 * (w 1.21.2+ zmieniono nazwy z "generic.max_health" na "max_health").
 */
public final class Attr {
    private Attr() {}

    public static Attribute find(String name) {
        for (String prefix : new String[]{"", "generic.", "zombie."}) {
            Attribute a = Registry.ATTRIBUTE.get(NamespacedKey.minecraft(prefix + name));
            if (a != null) return a;
        }
        return null;
    }

    public static void set(LivingEntity e, String name, double value) {
        Attribute a = find(name);
        if (a == null) return;
        AttributeInstance inst = e.getAttribute(a);
        if (inst != null) inst.setBaseValue(value);
    }

    public static void setMaxHealth(LivingEntity e, double hp) {
        set(e, "max_health", hp);
        e.setHealth(hp);
    }
}
