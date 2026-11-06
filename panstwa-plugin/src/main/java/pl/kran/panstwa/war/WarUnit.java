package pl.kran.panstwa.war;

import org.bukkit.Location;
import org.bukkit.entity.Mob;
import pl.kran.panstwa.util.ChunkPos;

import java.util.UUID;

/** Jedna jednostka (zolnierz / dron / samolot / jet) bioraca udzial w wojnie. */
public class WarUnit {
    final War war;
    final UnitType type;
    final UUID side;
    final Mob entity;
    int attackCooldown;
    int pathCooldown;
    Location lastPos;
    int stuckTicks;
    ChunkPos ticket;
    double orbitAngle = Math.random() * Math.PI * 2;

    WarUnit(War war, UnitType type, UUID side, Mob entity) {
        this.war = war;
        this.type = type;
        this.side = side;
        this.entity = entity;
    }

    public War getWar() { return war; }
    public UnitType getType() { return type; }
    public UUID getSide() { return side; }
    public Mob getEntity() { return entity; }

    boolean alive() {
        return entity.isValid() && !entity.isDead();
    }
}
