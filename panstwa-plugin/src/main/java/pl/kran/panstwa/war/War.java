package pl.kran.panstwa.war;

import net.kyori.adventure.bossbar.BossBar;
import pl.kran.panstwa.util.ChunkPos;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class War {
    final UUID attacker;
    final UUID defender;
    final ChunkPos target;
    final List<WarUnit> units = new ArrayList<>();
    final long startMillis = System.currentTimeMillis();
    int captureSeconds;
    BossBar bar;

    War(UUID attacker, UUID defender, ChunkPos target) {
        this.attacker = attacker;
        this.defender = defender;
        this.target = target;
    }

    public UUID getAttacker() { return attacker; }
    public UUID getDefender() { return defender; }
    public ChunkPos getTarget() { return target; }

    public boolean involves(UUID nation) {
        return attacker.equals(nation) || defender.equals(nation);
    }

    public long aliveCount(UUID side, UnitType type) {
        return units.stream().filter(u -> u.side.equals(side) && u.type == type && u.alive()).count();
    }
}
