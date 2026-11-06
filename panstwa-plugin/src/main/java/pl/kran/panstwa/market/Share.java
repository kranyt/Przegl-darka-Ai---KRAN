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
    int price;
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
    public int getPrice() { return price; }
    public Material getIcon() { return icon == null ? Material.WHEAT : icon; }
}
