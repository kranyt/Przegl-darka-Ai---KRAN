package pl.kran.panstwa.war;

import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.entity.Mob;
import org.bukkit.util.Vector;

/**
 * Cialo jednostki. Zolnierz = zombie, dron = vex.
 * Samolot / jet = phantom (wyglad + hitbox) niesiony przez niewidzialnego vexa (naped),
 * bo phantom bez AI nie przyjmuje predkosci, a z AI sam leci gdzie chce.
 * Wszystko lata przez nadawanie PREDKOSCI (velocity) - bez teleportowania.
 */
public class UnitBody {
    final UnitType type;
    /** Widoczna jednostka - ja sie atakuje i ona atakuje. */
    final Mob body;
    /** Niewidzialny "naped" dla samolotu / jetu (null dla zolnierza i drona). */
    final Mob carrier;

    UnitBody(UnitType type, Mob body, Mob carrier) {
        this.type = type;
        this.body = body;
        this.carrier = carrier;
    }

    public Mob body() { return body; }
    public Mob carrier() { return carrier; }

    /** Encja ktorej nadajemy predkosc. */
    Mob mover() { return carrier != null ? carrier : body; }

    Location loc() { return body.getLocation(); }

    boolean alive() {
        return body.isValid() && !body.isDead() && (carrier == null || carrier.isValid());
    }

    void remove() {
        if (carrier != null && carrier.isValid()) carrier.remove();
        if (body.isValid()) body.remove();
    }

    /** Czy jakis gracz jest na tyle blisko, ze widzi jednostke (i serwer ja aktywnie tickuje). */
    static boolean watched(Location loc) {
        for (org.bukkit.entity.Player p : loc.getWorld().getPlayers()) {
            if (p.getLocation().distanceSquared(loc) < 30 * 30) return true;
        }
        return false;
    }

    /**
     * Ruch gdy NIKT nie patrzy: Paper usypia moby daleko od graczy (nie dzialaja wtedy
     * predkosc ani pathfinding), wiec przesuwamy jednostke o maly krok po trasie.
     * Nikt tego nie widzi, a przy graczach jednostka znow leci / idzie normalnie.
     */
    void stepUnseen(Location next) {
        mover().setVelocity(new Vector());
        mover().teleport(next, io.papermc.paper.entity.TeleportFlag.EntityState.RETAIN_PASSENGERS);
    }

    /**
     * Ustawia predkosc w strone celu (max {@code maxSpeed} blokow na tick) plus odpychanie {@code push}.
     * Zwraca przewidywana pozycje w nastepnym ticku.
     */
    Location flyTowards(Location goal, double maxSpeed, Vector push) {
        Mob m = mover();
        Location cur = m.getLocation();
        Vector v = goal.toVector().subtract(cur.toVector());
        double len = v.length();
        if (len > maxSpeed) v.multiply(maxSpeed / len);
        if (push != null) v.add(push);
        double l2 = v.length();
        if (l2 > maxSpeed) v.multiply(maxSpeed / l2);
        // nie w ziemie
        World w = cur.getWorld();
        Location next = cur.clone().add(v);
        int ground = w.getHighestBlockYAt(next.getBlockX(), next.getBlockZ());
        if (next.getY() < ground + 1.2) v.setY(Math.max(v.getY(), Math.min(maxSpeed, ground + 1.2 - cur.getY())));
        m.setVelocity(v);
        if (v.lengthSquared() > 0.0004) {
            Location look = cur.clone().setDirection(v);
            m.setRotation(look.getYaw(), look.getPitch());
            if (carrier != null) body.setRotation(look.getYaw(), look.getPitch());
        }
        return cur.clone().add(v);
    }
}
