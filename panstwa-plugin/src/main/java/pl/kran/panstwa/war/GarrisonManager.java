package pl.kran.panstwa.war;

import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.entity.Mob;
import org.bukkit.scheduler.BukkitTask;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.model.Nation;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Garnizon: gdy nie ma wojny, armia panstwa jest widoczna w bazie -
 * zolnierze chodza wokol fundamentu, a drony / samoloty / jety kraza nad nim.
 * Jednostki garnizonu sa niesmiertelne (to tylko "wizualizacja" armii z magazynu).
 */
public class GarrisonManager {
    private static class GUnit {
        final UnitType type;
        final UnitBody unit;
        final Mob mob;
        double angle = ThreadLocalRandom.current().nextDouble(Math.PI * 2);
        int pathCooldown;

        GUnit(UnitType type, UnitBody unit) {
            this.type = type;
            this.unit = unit;
            this.mob = unit.body;
        }

        boolean alive() { return unit.alive(); }
    }

    private final PanstwaPlugin plugin;
    private final Map<UUID, List<GUnit>> garrisons = new HashMap<>();
    private final Map<UUID, Mob> byEntity = new HashMap<>();
    private BukkitTask moveTask;
    private BukkitTask syncTask;

    public GarrisonManager(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    public void start() {
        moveTask = Bukkit.getScheduler().runTaskTimer(plugin, this::move, 1L, 1L);
        syncTask = Bukkit.getScheduler().runTaskTimer(plugin, this::sync, 40L, 40L);
    }

    public void shutdown() {
        if (moveTask != null) moveTask.cancel();
        if (syncTask != null) syncTask.cancel();
        for (UUID id : new ArrayList<>(garrisons.keySet())) clear(id);
    }

    public boolean isGarrison(org.bukkit.entity.Entity e) {
        return byEntity.containsKey(e.getUniqueId());
    }

    private boolean enabled() {
        return plugin.getConfig().getBoolean("garnizon.wlaczony", true);
    }

    /** Usuwa garnizon panstwa (np. gdy zaczyna sie wojna albo panstwo znika). */
    public void clear(UUID nation) {
        List<GUnit> list = garrisons.remove(nation);
        if (list == null) return;
        for (GUnit g : list) forget(g);
    }

    private void forget(GUnit g) {
        byEntity.remove(g.mob.getUniqueId());
        if (g.unit.carrier != null) byEntity.remove(g.unit.carrier.getUniqueId());
        g.unit.remove();
    }

    // ------------------------------------------------------------------ dopasowanie liczby jednostek
    private void sync() {
        // usun garnizony panstw ktore juz nie istnieja
        for (UUID id : new ArrayList<>(garrisons.keySet())) {
            if (plugin.nations().get(id) == null) clear(id);
        }
        if (!enabled()) {
            for (UUID id : new ArrayList<>(garrisons.keySet())) clear(id);
            return;
        }
        int cap = plugin.getConfig().getInt("garnizon.max-na-typ", 6);
        for (Nation n : plugin.nations().all()) {
            Block fund = n.getFundamentBlock();
            boolean show = fund != null && !plugin.wars().inWar(n.getOwner())
                    && fund.getWorld().isChunkLoaded(fund.getX() >> 4, fund.getZ() >> 4)
                    && fund.getWorld().getDifficulty() != org.bukkit.Difficulty.PEACEFUL;
            if (!show) {
                clear(n.getOwner());
                continue;
            }
            List<GUnit> list = garrisons.computeIfAbsent(n.getOwner(), k -> new ArrayList<>());
            list.removeIf(g -> {
                if (g.alive()) return false;
                forget(g);
                return true;
            });
            Map<UnitType, Integer> have = new EnumMap<>(UnitType.class);
            for (GUnit g : list) have.merge(g.type, 1, Integer::sum);
            for (UnitType t : UnitType.values()) {
                int want = Math.min(n.getUnits(t), cap);
                int cur = have.getOrDefault(t, 0);
                for (int i = cur; i < want; i++) spawn(n, t, fund, list);
                if (cur > want) {
                    int toRemove = cur - want;
                    Iterator<GUnit> it = list.iterator();
                    while (it.hasNext() && toRemove > 0) {
                        GUnit g = it.next();
                        if (g.type != t) continue;
                        forget(g);
                        it.remove();
                        toRemove--;
                    }
                }
            }
        }
    }

    private void spawn(Nation n, UnitType t, Block fund, List<GUnit> list) {
        World w = fund.getWorld();
        ThreadLocalRandom r = ThreadLocalRandom.current();
        double x = fund.getX() + 0.5 + r.nextDouble(-4, 4);
        double z = fund.getZ() + 0.5 + r.nextDouble(-4, 4);
        double y = w.getHighestBlockYAt((int) Math.floor(x), (int) Math.floor(z)) + 1 + (t.flying() ? height(t) : 0);
        UnitBody body = plugin.wars().createUnit(t, n, "&a", new Location(w, x, y, z));
        body.body.setInvulnerable(true);
        GUnit g = new GUnit(t, body);
        list.add(g);
        byEntity.put(body.body.getUniqueId(), body.body);
        if (body.carrier != null) byEntity.put(body.carrier.getUniqueId(), body.carrier);
    }

    private double height(UnitType t) {
        return switch (t) {
            case DRONE -> 6;
            case PLANE -> 9;
            case JET -> 12;
            default -> 0;
        };
    }

    private double radius(UnitType t) {
        return switch (t) {
            case DRONE -> 6;
            case PLANE -> 10;
            case JET -> 14;
            default -> 8;
        };
    }

    // ------------------------------------------------------------------ ruch
    private void move() {
        for (Map.Entry<UUID, List<GUnit>> e : garrisons.entrySet()) {
            Nation n = plugin.nations().get(e.getKey());
            if (n == null) continue;
            Block fund = n.getFundamentBlock();
            if (fund == null) continue;
            Location center = fund.getLocation().add(0.5, 0, 0.5);
            List<GUnit> list = e.getValue();
            for (GUnit g : list) {
                if (!g.alive()) continue;
                if (g.type.flying()) moveFlyer(g, center, list); else moveSoldier(g, center);
            }
        }
    }

    /** Krazenie nad baza - predkoscia (velocity), bez teleportu, z odstepami miedzy jednostkami. */
    private void moveFlyer(GUnit g, Location center, List<GUnit> all) {
        World w = center.getWorld();
        double r = radius(g.type);
        // spokojne krazenie - ok. 40% normalnej predkosci jednostki
        double bpt = UnitType.PLAYER_WALK_BPS * g.type.speed(plugin.getConfig()) / 20.0 * 0.4;
        g.angle += bpt / r;
        double x = center.getX() + Math.cos(g.angle) * r;
        double z = center.getZ() + Math.sin(g.angle) * r;
        if (!w.isChunkLoaded(((int) Math.floor(x)) >> 4, ((int) Math.floor(z)) >> 4)) {
            g.unit.mover().setVelocity(new org.bukkit.util.Vector());
            return;
        }
        double y = Math.max(center.getY() + height(g.type),
                w.getHighestBlockYAt((int) Math.floor(x), (int) Math.floor(z)) + 2);
        Location me = g.unit.loc();
        org.bukkit.util.Vector push = new org.bukkit.util.Vector();
        for (GUnit o : all) {
            if (o == g || !o.alive() || !o.type.flying()) continue;
            double min = (WarManager.spacing(g.type) + WarManager.spacing(o.type)) / 2.0;
            org.bukkit.util.Vector diff = me.toVector().subtract(o.unit.loc().toVector());
            double d = diff.length();
            if (d >= min || d < 0.001) continue;
            push.add(diff.normalize().multiply((min - d) / min * bpt * 2));
        }
        // troche szybciej niz krazenie, zeby dogonic swoj punkt na okregu
        g.unit.flyTowards(new Location(w, x, y, z), bpt * 2.5, push.lengthSquared() > 0 ? push : null);
    }

    private void moveSoldier(GUnit g, Location center) {
        if (g.pathCooldown-- > 0) return;
        ThreadLocalRandom r = ThreadLocalRandom.current();
        g.pathCooldown = r.nextInt(60, 140);
        Location cur = g.mob.getLocation();
        World w = center.getWorld();
        double rad = radius(g.type);
        Location target;
        if (cur.getWorld() != w || cur.distance(center) > rad * 2.5) {
            target = center.clone();
        } else {
            double a = r.nextDouble(Math.PI * 2);
            double d = r.nextDouble(2, rad);
            target = center.clone().add(Math.cos(a) * d, 0, Math.sin(a) * d);
        }
        if (!w.isChunkLoaded(target.getBlockX() >> 4, target.getBlockZ() >> 4)) return;
        target.setY(w.getHighestBlockYAt(target) + 1);
        g.mob.getPathfinder().moveTo(target, 0.7);
    }
}
