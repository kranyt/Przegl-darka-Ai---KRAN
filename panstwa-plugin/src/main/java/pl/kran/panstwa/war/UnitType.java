package pl.kran.panstwa.war;

import org.bukkit.Material;
import org.bukkit.configuration.file.FileConfiguration;

public enum UnitType {
    SOLDIER("zolnierz", "Żołnierz", "Żołnierze", false, Material.IRON_SWORD),
    DRONE("dron", "Dron", "Drony", true, Material.PHANTOM_MEMBRANE),
    PLANE("samolot", "Samolot", "Samoloty", true, Material.ELYTRA),
    JET("jet", "Jet", "Jety", true, Material.FIREWORK_ROCKET);

    /** Predkosc chodzenia gracza w blokach na sekunde. */
    public static final double PLAYER_WALK_BPS = 4.317;

    private final String key;
    private final String display;
    private final String plural;
    private final boolean flying;
    private final Material icon;

    UnitType(String key, String display, String plural, boolean flying, Material icon) {
        this.key = key;
        this.display = display;
        this.plural = plural;
        this.flying = flying;
        this.icon = icon;
    }

    public String key() { return key; }
    public String display() { return display; }
    public String plural() { return plural; }
    public boolean flying() { return flying; }
    public Material icon() { return icon; }

    public double hp(FileConfiguration c) { return c.getDouble("jednostki." + key + ".hp"); }
    public double speed(FileConfiguration c) { return c.getDouble("jednostki." + key + ".predkosc", 1.0); }
    public double damage(FileConfiguration c) { return c.getDouble("jednostki." + key + ".obrazenia", 4); }
    public int cost(FileConfiguration c) { return c.getInt("jednostki." + key + ".koszt-diamenty"); }

    public static UnitType byKey(String k) {
        for (UnitType t : values()) if (t.key.equalsIgnoreCase(k)) return t;
        return null;
    }
}
