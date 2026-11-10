package pl.kran.panstwa.war;

import org.bukkit.Location;
import org.bukkit.entity.Mob;
import org.bukkit.util.Vector;
import pl.kran.panstwa.util.ChunkPos;

import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

/** Jedna jednostka (zolnierz / dron / samolot / jet) bioraca udzial w wojnie. */
public class WarUnit {
    final War war;
    final UnitType type;
    final UUID side;
    final UnitBody unit;
    /** Widoczna encja (do celowania / obrazen). */
    final Mob entity;
    int attackCooldown;
    int pathCooldown;
    Location lastPos;
    int stuckTicks;
    ChunkPos ticket;
    /** Chunk do ktorego zolnierz zaraz wejdzie (ladowany z wyprzedzeniem). */
    ChunkPos aheadTicket;
    double orbitAngle = Math.random() * Math.PI * 2;
    /** Wlasne miejsce w szyku - kazda jednostka idzie w troche inne miejsce, zeby nie wchodzily w siebie. */
    final Vector formation;

    WarUnit(War war, UnitType type, UUID side, UnitBody unit) {
        this.war = war;
        this.type = type;
        this.side = side;
        this.unit = unit;
        this.entity = unit.body;
        ThreadLocalRandom r = ThreadLocalRandom.current();
        double a = r.nextDouble(Math.PI * 2);
        double d = r.nextDouble(1.5, 6.5);
        this.formation = new Vector(Math.cos(a) * d, 0, Math.sin(a) * d);
    }

    public War getWar() { return war; }
    public UnitType getType() { return type; }
    public UUID getSide() { return side; }
    public Mob getEntity() { return entity; }

    boolean alive() {
        return unit.alive();
    }
}
