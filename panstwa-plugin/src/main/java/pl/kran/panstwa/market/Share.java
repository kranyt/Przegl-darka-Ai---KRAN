package pl.kran.panstwa.market;

import org.bukkit.Material;

import java.util.UUID;

/**
 * Akcja = jedna kolumna blokow (od samej gory do samego dolu) z farma.
 * holder - kto ma akcje (null = serwer). forSale - czy wystawiona na /akcje.
 */
public class Share {
    final int id;
    final String world;
    final int x, z;
    final UUID issuer;      // wlasciciel panstwa ktory wystawil akcje jako pierwszy
    UUID holder;            // aktualny posiadacz (null = serwer)
    boolean forSale;
    /** Dokladna cena - zmienia sie stopniowo o male procenty. */
    double exact;
    /** Kiedy akcja zostala wystawiona na sprzedaz (wygasa po 24h bez sprzedazy). */
    long listedAt;
    /** Aktualny trend: cena do ktorej akcja stopniowo dazy (0 = brak trendu). */
    double trendTarget;
    /** Calkowita zmiana trendu w procentach (do wyswietlania, + / -). */
    int trendPct;
    Material icon;

    Share(int id, String world, int x, int z, UUID issuer) {
        this.id = id;
        this.world = world;
        this.x = x;
        this.z = z;
        this.issuer = issuer;
    }

    public int getId() { return id; }
    public String getWorld() { return world; }
    public int getX() { return x; }
    public int getZ() { return z; }
    public UUID getIssuer() { return issuer; }
    public UUID getHolder() { return holder; }
    public boolean isForSale() { return forSale; }
    public long getListedAt() { return listedAt; }
    public int getPrice() { return (int) Math.max(1, Math.round(exact)); }
    public boolean hasTrend() { return trendTarget > 0; }
    public int getTrendPct() { return trendPct; }
    public Material getIcon() { return icon == null ? Material.WHEAT : icon; }

    /** Opis trendu do GUI / czatu. */
    public String trendText() {
        if (!hasTrend()) return "&7stabilna";
        return trendTarget > exact ? "&a▲ rosnie &7(trend +" + trendPct + "%)" : "&c▼ spada &7(trend " + trendPct + "%)";
    }
}
