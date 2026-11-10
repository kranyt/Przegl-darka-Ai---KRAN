package pl.kran.panstwa.war;

import com.destroystokyo.paper.entity.Pathfinder;
import net.kyori.adventure.bossbar.BossBar;
import org.bukkit.Bukkit;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.Particle;
import org.bukkit.World;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Mob;
import org.bukkit.entity.Phantom;
import org.bukkit.entity.Player;
import org.bukkit.entity.Vex;
import org.bukkit.entity.Zombie;
import org.bukkit.inventory.EntityEquipment;
import org.bukkit.inventory.ItemStack;
import org.bukkit.persistence.PersistentDataType;
import org.bukkit.scheduler.BukkitTask;
import org.bukkit.util.Vector;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.model.Nation;
import pl.kran.panstwa.util.Attr;
import pl.kran.panstwa.util.ChunkPos;
import pl.kran.panstwa.util.Msg;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

public class WarManager {
    private final PanstwaPlugin plugin;
    private final NamespacedKey unitKey;
    private final List<War> wars = new ArrayList<>();
    private final Map<UUID, WarUnit> unitsByEntity = new HashMap<>();
    private final Map<ChunkPos, Integer> tickets = new HashMap<>();
    private BukkitTask task;
    private long tickCounter;

    public WarManager(PanstwaPlugin plugin) {
        this.plugin = plugin;
        this.unitKey = new NamespacedKey(plugin, "jednostka");
    }

    public void start() {
        task = Bukkit.getScheduler().runTaskTimer(plugin, this::tick, 1L, 1L);
    }

    public void shutdown() {
        if (task != null) task.cancel();
        for (War w : new ArrayList<>(wars)) end(w, false, "Serwer zostal wylaczony - wojna przerwana.");
    }

    private FileConfiguration cfg() { return plugin.getConfig(); }

    public List<War> getWars() { return wars; }

    public War warAt(ChunkPos pos) {
        for (War w : wars) if (w.target.equals(pos)) return w;
        return null;
    }

    public War attackingWar(UUID nation) {
        for (War w : wars) if (w.attacker.equals(nation)) return w;
        return null;
    }

    public WarUnit getUnit(Entity e) {
        return unitsByEntity.get(e.getUniqueId());
    }

    public boolean isTaggedUnit(Entity e) {
        return e.getPersistentDataContainer().has(unitKey, PersistentDataType.STRING);
    }

    // =====================================================================
    //  START WOJNY
    // =====================================================================

    public War startWar(Nation attacker, Nation defender, ChunkPos target) {
        War w = new War(attacker.getOwner(), defender.getOwner(), target);
        wars.add(w);
        World tw = target.bukkitWorld();
        if (tw != null && tw.getDifficulty() == org.bukkit.Difficulty.PEACEFUL) {
            String warn = "&c&lUwaga: &cna poziomie trudnosci PEACEFUL serwer usuwa jednostki (zolnierzy, drony...)! "
                    + "Ustaw: /difficulty easy";
            for (Player p : attacker.online()) Msg.send(p, warn);
            for (Player p : defender.online()) Msg.send(p, warn);
            plugin.getLogger().warning("Swiat " + tw.getName() + " ma difficulty PEACEFUL - jednostki wojskowe beda znikac.");
        }
        addTicket(target);
        w.bar = BossBar.bossBar(Msg.c("&cWojna"), 0f, BossBar.Color.RED, BossBar.Overlay.NOTCHED_10);
        plugin.garrison().clear(attacker.getOwner());
        plugin.garrison().clear(defender.getOwner());
        deploy(w, attacker, true);
        deploy(w, defender, false);
        plugin.nations().save();
        updateBar(w);
        return w;
    }

    /** Wysyla armie panstwa na wojne. Zwraca opis wyslanych jednostek. */
    private void deploy(War w, Nation n, boolean attacker) {
        int dist = n.distanceTo(w.target);
        ChunkPos from = n.nearestChunk(w.target);
        if (from == null || dist == Integer.MAX_VALUE) return;
        int range = cfg().getInt("armia.zasieg-zolnierzy-chunki", 16);
        int cap = cfg().getInt("armia.max-jednostek-na-wojne", 30);
        StringBuilder sent = new StringBuilder();
        for (UnitType t : UnitType.values()) {
            if (!t.flying() && dist > range) continue;
            int count = Math.min(n.getUnits(t), cap);
            if (count <= 0) continue;
            n.addUnits(t, -count);
            for (int i = 0; i < count; i++) {
                Location base = from.surfaceCenter(t.flying() ? 6 : 0);
                if (base == null) break;
                ThreadLocalRandom r = ThreadLocalRandom.current();
                Location loc = base.add(r.nextDouble(-5, 5), 0, r.nextDouble(-5, 5));
                loc.setY(loc.getWorld().getHighestBlockYAt(loc) + 1 + (t.flying() ? 6 : 0));
                spawnUnit(w, t, n, attacker, loc);
            }
            if (sent.length() > 0) sent.append(", ");
            sent.append(count).append("x ").append(t.display());
        }
        for (Player p : n.online()) {
            if (sent.length() == 0) {
                Msg.send(p, attacker ? "&eNie wyslales zadnych jednostek - walczysz sam!"
                        : "&eNie masz jednostek ktore moga bronic chunka " + w.target + " - bron sie sam!");
            } else {
                Msg.send(p, (attacker ? "&aWyslano do ataku: &f" : "&aWyslano do obrony: &f") + sent);
            }
            if (!attacker || dist <= range) continue;
            if (n.getUnits(UnitType.SOLDIER) > 0) {
                Msg.send(p, "&eCel jest dalej niz " + range + " chunkow - zolnierze nie dosiegaja. Kup drony: &f/p drony");
            }
        }
    }

    private void spawnUnit(War w, UnitType t, Nation n, boolean attacker, Location loc) {
        UnitBody body = createUnit(t, n, attacker ? "&c" : "&9", loc);
        WarUnit u = new WarUnit(w, t, n.getOwner(), body);
        u.lastPos = body.loc();
        u.ticket = ChunkPos.of(body.loc());
        addTicket(u.ticket);
        w.units.add(u);
        unitsByEntity.put(body.body.getUniqueId(), u);
        if (body.carrier != null) unitsByEntity.put(body.carrier.getUniqueId(), u);
    }

    /**
     * Tworzy jednostke: zolnierz = zombie, dron = vex,
     * samolot / jet = phantom niesiony przez niewidzialnego vexa. Uzywane tez przez garnizon.
     * Latajace jednostki maja wlaczone AI (bez celow), zeby dzialala predkosc (velocity).
     */
    public UnitBody createUnit(UnitType t, Nation n, String color, Location loc) {
        World world = loc.getWorld();
        double hp = t.hp(cfg());
        switch (t) {
            case SOLDIER -> {
                Zombie z = world.spawn(loc, Zombie.class, e -> {
                    e.setAdult();
                    e.setShouldBurnInDay(false);
                    EntityEquipment eq = e.getEquipment();
                    eq.setHelmet(new ItemStack(Material.IRON_HELMET));
                    eq.setChestplate(new ItemStack(Material.IRON_CHESTPLATE));
                    eq.setLeggings(new ItemStack(Material.IRON_LEGGINGS));
                    eq.setBoots(new ItemStack(Material.IRON_BOOTS));
                    eq.setItemInMainHand(new ItemStack(Material.IRON_SWORD));
                    Attr.set(e, "spawn_reinforcements", 0);
                    // ~ predkosc chodzenia gracza
                    Attr.set(e, "movement_speed", 0.25 * t.speed(cfg()));
                    Attr.set(e, "follow_range", 48);
                    prepare(e, t, hp, color, n);
                });
                Bukkit.getMobGoals().removeAllGoals(z);
                return new UnitBody(t, z, null);
            }
            case DRONE -> {
                Vex v = world.spawn(loc, Vex.class, e -> {
                    e.setLimitedLifetime(false);
                    prepare(e, t, hp, color, n);
                });
                flyerSetup(v);
                v.setGlowing(true);
                return new UnitBody(t, v, null);
            }
            default -> {
                Vex carrier = world.spawn(loc, Vex.class, e -> {
                    e.setLimitedLifetime(false);
                    e.setInvisible(true);
                    e.setInvulnerable(true);
                    e.setSilent(true);
                    e.setPersistent(true);
                    e.setRemoveWhenFarAway(false);
                    e.setCanPickupItems(false);
                    e.getEquipment().clear();
                    e.getPersistentDataContainer().set(unitKey, PersistentDataType.STRING, n.getOwner().toString());
                });
                flyerSetup(carrier);
                Phantom ph = world.spawn(loc, Phantom.class, e -> {
                    e.setSize(t == UnitType.JET ? 6 : 2);
                    e.setShouldBurnInDay(false);
                    prepare(e, t, hp, color, n);
                });
                ph.setAI(false);
                ph.setGravity(false);
                ph.setGlowing(true);
                carrier.addPassenger(ph);
                return new UnitBody(t, ph, carrier);
            }
        }
    }

    private void flyerSetup(Mob m) {
        Bukkit.getMobGoals().removeAllGoals(m);
        m.setAI(true);
        m.setGravity(false);
        m.setSilent(true);
    }

    private void prepare(Mob m, UnitType t, double hp, String color, Nation n) {
        m.setPersistent(true);
        m.setRemoveWhenFarAway(false);
        m.setCanPickupItems(false);
        m.setSilent(t.flying());
        EntityEquipment eq = m.getEquipment();
        if (eq != null) {
            eq.setHelmetDropChance(0f);
            eq.setChestplateDropChance(0f);
            eq.setLeggingsDropChance(0f);
            eq.setBootsDropChance(0f);
            eq.setItemInMainHandDropChance(0f);
            eq.setItemInOffHandDropChance(0f);
        }
        Attr.setMaxHealth(m, hp);
        m.getPersistentDataContainer().set(unitKey, PersistentDataType.STRING, n.getOwner().toString());
        m.customName(Msg.c(color + "[" + n.getName() + "] &f" + t.display()));
        m.setCustomNameVisible(true);
    }

    // =====================================================================
    //  TICK
    // =====================================================================

    private void tick() {
        tickCounter++;
        for (War w : new ArrayList<>(wars)) {
            Iterator<WarUnit> it = w.units.iterator();
            while (it.hasNext()) {
                WarUnit u = it.next();
                if (!u.alive()) {
                    removeTicket(u.ticket);
                    removeTicket(u.aheadTicket);
                    unitsByEntity.remove(u.unit.body.getUniqueId());
                    if (u.unit.carrier != null) unitsByEntity.remove(u.unit.carrier.getUniqueId());
                    u.unit.remove();
                    it.remove();
                    // zginela - odrodzi sie po chwili w bazie
                    if (cfg().getBoolean("wojna.odradzanie", true)) {
                        int ticks = cfg().getInt("wojna.odradzanie-sekundy", 20) * 20;
                        w.respawns.add(new War.Respawn(u.type, u.side, ticks));
                    } else {
                        // bez odradzania jednostka przepada
                    }
                    continue;
                }
                try {
                    if (u.type.flying()) tickFlyer(u); else tickSoldier(u);
                    updateTicket(u);
                } catch (Exception ex) {
                    plugin.getLogger().warning("Blad jednostki: " + ex);
                }
            }
            tickRespawns(w);
            if (tickCounter % 20 == 0) {
                try {
                    secondTick(w);
                } catch (Exception ex) {
                    plugin.getLogger().log(java.util.logging.Level.SEVERE, "Blad wojny - wojna przerwana", ex);
                    end(w, false, "Wojna przerwana z powodu bledu.");
                }
            }
        }
    }

    private void tickRespawns(War w) {
        if (w.respawns.isEmpty() || !wars.contains(w)) return;
        Iterator<War.Respawn> it = w.respawns.iterator();
        while (it.hasNext()) {
            War.Respawn r = it.next();
            if (--r.ticks > 0) continue;
            it.remove();
            Nation n = plugin.nations().get(r.side);
            if (n == null) continue;
            Location loc = respawnPoint(w, n, r.type);
            if (loc == null) continue;
            spawnUnit(w, r.type, n, r.side.equals(w.attacker), loc);
        }
    }

    /** Atakujacy odradzaja sie na swoim najblizszym chunku, obroncy przy fundamencie. */
    private Location respawnPoint(War w, Nation n, UnitType t) {
        ChunkPos from = respawnChunk(w, n);
        if (from == null) return null;
        Location base = from.surfaceCenter(0);
        if (base == null) return null;
        ThreadLocalRandom r = ThreadLocalRandom.current();
        Location loc = base.add(r.nextDouble(-5, 5), 0, r.nextDouble(-5, 5));
        loc.setY(loc.getWorld().getHighestBlockYAt(loc) + 1 + (t.flying() ? cfg().getDouble("wojna.wysokosc-lotu", 5) : 0));
        return loc;
    }

    private ChunkPos respawnChunk(War w, Nation n) {
        if (n.getOwner().equals(w.defender)) return n.getCapital();
        return n.nearestChunk(w.target);
    }

    private void updateTicket(WarUnit u) {
        ChunkPos now = ChunkPos.of(u.entity.getLocation());
        if (!now.equals(u.ticket)) {
            addTicket(now);
            removeTicket(u.ticket);
            u.ticket = now;
        }
    }

    private void tickSoldier(WarUnit u) {
        Mob m = u.entity;
        if (u.attackCooldown > 0) u.attackCooldown--;
        if (u.pathCooldown > 0) u.pathCooldown--;
        Pathfinder pf = m.getPathfinder();
        LivingEntity enemy = findEnemy(u, cfg().getDouble("wojna.zasieg-wykrywania", 16));
        if (enemy != null) {
            m.lookAt(enemy);
            double d = m.getLocation().distance(enemy.getLocation());
            if (d <= 2.3) {
                tryAttack(u, enemy);
            }
            if (u.pathCooldown <= 0) {
                pf.moveTo(enemy, 1.0);
                u.pathCooldown = 10;
            }
            return;
        }
        if (u.pathCooldown > 0) return;
        u.pathCooldown = 20;

        Location cur = m.getLocation();
        if (!UnitBody.watched(cur)) {
            walkUnseen(u, cur);
            return;
        }
        // stuck detection
        if (u.lastPos != null && u.lastPos.getWorld() == cur.getWorld() && u.lastPos.distanceSquared(cur) < 1) {
            u.stuckTicks += 20;
        } else {
            u.stuckTicks = 0;
        }
        u.lastPos = cur;

        Location dest = destinationFor(u);
        if (dest == null) return;
        dest.add(u.formation); // kazdy zolnierz ma swoje miejsce - nie wchodza w siebie
        dest.setY(dest.getWorld().getHighestBlockYAt(dest) + 1);
        if (u.war.target.contains(cur) && cur.distance(dest) < 1.5) {
            pf.stopPathfinding();
            return;
        }
        Vector dir = dest.toVector().subtract(cur.toVector()).setY(0);
        double len = dir.length();
        Location wp;
        if (len > 20) {
            Vector step = dir.normalize().multiply(20);
            wp = cur.clone().add(step);
            wp.setY(wp.getWorld().getHighestBlockYAt(wp) + 1);
        } else {
            wp = dest;
        }
        // zaladuj chunk punktu docelowego, zeby pathfinding dzialal i zolnierz nie zniknal
        ChunkPos ahead = ChunkPos.of(wp);
        if (!ahead.equals(u.aheadTicket)) {
            addTicket(ahead);
            wp.getWorld().getChunkAt(ahead.x(), ahead.z());
            removeTicket(u.aheadTicket);
            u.aheadTicket = ahead;
        }
        boolean ok = pf.moveTo(wp, 1.0);
        if ((!ok || u.stuckTicks >= 60) && len > 0.1) {
            // zablokowany - lekki skok w kierunku celu (nie teleport)
            Vector push = dir.normalize().multiply(0.35);
            push.setY(m.isOnGround() ? 0.45 : m.getVelocity().getY());
            m.setVelocity(push);
        }
    }

    /** Zolnierz daleko od graczy (serwer go uspil) - przesuwa sie po ziemi tempem chodu. */
    private void walkUnseen(WarUnit u, Location cur) {
        Location dest = destinationFor(u);
        if (dest == null) return;
        dest.add(u.formation);
        Vector dir = dest.toVector().subtract(cur.toVector()).setY(0);
        double len = dir.length();
        if (len < 1) return;
        double step = UnitType.PLAYER_WALK_BPS * u.type.speed(cfg()); // co 20 tickow = 1 sekunda chodu
        Location next = cur.clone().add(dir.normalize().multiply(Math.min(step, len)));
        next.setY(next.getWorld().getHighestBlockYAt(next) + 1);
        next.setDirection(dir);
        prepareChunk(u, next);
        u.unit.stepUnseen(next);
    }

    private void tickFlyer(WarUnit u) {
        if (u.attackCooldown > 0) u.attackCooldown--;
        Location cur = u.unit.loc();
        World world = cur.getWorld();
        double speed = UnitType.PLAYER_WALK_BPS * u.type.speed(cfg()) / 20.0; // bloki na tick
        LivingEntity enemy = findEnemy(u, cfg().getDouble("wojna.zasieg-wykrywania", 16) + 8);
        double cruise = cfg().getDouble("wojna.wysokosc-lotu", 5);

        Location goal;
        if (enemy != null) {
            // atak - leci na wroga
            goal = enemy.getLocation().add(0, enemy.getHeight() * 0.6, 0);
        } else {
            Location dest = destinationFor(u);
            if (dest == null) return;
            if (u.war.target.contains(cur) || horizontal(cur, dest) < 10) {
                // kraza nisko nad celem, kazda jednostka po swoim okregu
                double radius = 4 + u.formation.length();
                u.orbitAngle += Math.min(0.12, speed / radius);
                goal = dest.clone().add(Math.cos(u.orbitAngle) * radius, 0, Math.sin(u.orbitAngle) * radius);
            } else {
                goal = dest.clone().add(u.formation);
            }
            // wysokosc trzymana nisko nad ziemia (zeby bylo je widac)
            Location ahead = cur.clone().add(goal.toVector().subtract(cur.toVector()).setY(0).normalize().multiply(Math.max(speed * 4, 2)));
            if (!Double.isFinite(ahead.getX())) ahead = cur.clone();
            double groundAhead = Math.max(world.getHighestBlockYAt(ahead.getBlockX(), ahead.getBlockZ()),
                    world.getHighestBlockYAt(cur.getBlockX(), cur.getBlockZ()));
            goal.setY(groundAhead + 1 + cruise);
        }

        // nie wchodza w siebie - odpychanie od innych jednostek
        Vector push = separation(u, speed);
        Location next;
        if (UnitBody.watched(cur)) {
            next = u.unit.flyTowards(goal, speed, push); // prawdziwa predkosc - bez teleportu
        } else {
            Vector v = goal.toVector().subtract(cur.toVector());
            if (v.length() > speed) v.normalize().multiply(speed);
            next = cur.clone().add(v);
            int g = world.getHighestBlockYAt(next.getBlockX(), next.getBlockZ());
            if (next.getY() < g + 1.2) next.setY(g + 1.2);
            next.setDirection(v.lengthSquared() > 1e-6 ? v : cur.getDirection());
            prepareChunk(u, next);
            u.unit.stepUnseen(next);
        }

        // zaladuj chunk do ktorego leci ZANIM tam wleci - inaczej jednostka znika
        prepareChunk(u, next);

        if (enemy != null && u.unit.loc().distance(enemy.getLocation().add(0, enemy.getHeight() * 0.5, 0)) <= attackRange(u.type)) {
            tryAttack(u, enemy);
        }
        if (tickCounter % 4 == 0) {
            world.spawnParticle(Particle.SMOKE, cur, 2, 0.1, 0.1, 0.1, 0.01);
        }
    }

    private double attackRange(UnitType t) {
        return switch (t) {
            case PLANE -> 3.5;
            case JET -> 5.5;
            default -> 2.5;
        };
    }

    /** Minimalny odstep miedzy jednostkami (zalezy od wielkosci). */
    static double spacing(UnitType t) {
        return switch (t) {
            case SOLDIER -> 1.2;
            case DRONE -> 2.0;
            case PLANE -> 3.5;
            case JET -> 6.0;
        };
    }

    /** Wektor odpychania od jednostek tej samej strony, ktore sa za blisko. */
    private Vector separation(WarUnit u, double speed) {
        Location me = u.unit.loc();
        Vector push = new Vector();
        for (WarUnit o : u.war.units) {
            if (o == u || !o.side.equals(u.side) || !o.alive() || o.entity.getWorld() != me.getWorld()) continue;
            double min = (spacing(u.type) + spacing(o.type)) / 2.0;
            Vector diff = me.toVector().subtract(o.unit.loc().toVector());
            double d = diff.length();
            if (d >= min) continue;
            if (d < 0.01) diff = new Vector(Math.random() - 0.5, 0, Math.random() - 0.5);
            push.add(diff.normalize().multiply((min - d) / min));
        }
        if (push.lengthSquared() < 1e-6) return null;
        return push.multiply(speed);
    }

    private static double horizontal(Location a, Location b) {
        double dx = a.getX() - b.getX(), dz = a.getZ() - b.getZ();
        return Math.sqrt(dx * dx + dz * dz);
    }

    /** Dodaje ticket i laduje chunk zanim jednostka do niego wejdzie. */
    private void prepareChunk(WarUnit u, Location next) {
        ChunkPos np = ChunkPos.of(next);
        if (np.equals(u.ticket)) return;
        addTicket(np);
        next.getWorld().getChunkAt(np.x(), np.z());
        removeTicket(u.ticket);
        u.ticket = np;
    }

    private void tryAttack(WarUnit u, LivingEntity enemy) {
        if (u.attackCooldown > 0) return;
        u.attackCooldown = 20;
        u.entity.swingMainHand();
        enemy.damage(u.type.damage(cfg()), u.entity);
        if (u.type.flying()) {
            enemy.getWorld().spawnParticle(Particle.CRIT, enemy.getLocation().add(0, 1, 0), 8, 0.3, 0.3, 0.3, 0.1);
        }
    }

    private Location destinationFor(WarUnit u) {
        return u.war.target.surfaceCenter(0);
    }

    /** Najblizszy wrog: jednostka drugiej strony albo wrogi gracz (wlasciciel panstwa). */
    private LivingEntity findEnemy(WarUnit u, double range) {
        Location loc = u.entity.getLocation();
        double best = range * range;
        LivingEntity found = null;
        for (WarUnit o : u.war.units) {
            if (o.side.equals(u.side) || !o.alive() || o.entity.getWorld() != loc.getWorld()) continue;
            double d = o.entity.getLocation().distanceSquared(loc);
            if (d < best) { best = d; found = o.entity; }
        }
        UUID enemySide = u.side.equals(u.war.attacker) ? u.war.defender : u.war.attacker;
        Nation enemy = plugin.nations().get(enemySide);
        if (enemy == null) return found;
        for (Player p : enemy.online()) {
            if (!validFighter(p) || p.getWorld() != loc.getWorld()) continue;
            double d = p.getLocation().distanceSquared(loc);
            if (d < best) { best = d; found = p; }
        }
        return found;
    }

    private boolean validFighter(Player p) {
        // kreatywny tez sie liczy (wczesniej przez to nie dalo sie przejac chunka), obserwator nie
        return !p.isDead() && p.isValid() && p.getGameMode() != GameMode.SPECTATOR;
    }

    // =====================================================================
    //  PRZEJMOWANIE CHUNKA (co sekunde)
    // =====================================================================

    private void secondTick(War w) {
        Nation att = plugin.nations().get(w.attacker);
        Nation def = plugin.nations().get(w.defender);
        if (att == null || def == null || !def.getChunks().contains(w.target)) {
            end(w, false, "Wojna zakonczona - jedno z panstw juz nie istnieje lub chunk zmienil wlasciciela.");
            return;
        }
        boolean attackers = presence(w, w.attacker);
        boolean defenders = presence(w, w.defender);
        int need = cfg().getInt("wojna.czas-przejecia-sekundy", 10);
        if (attackers && !defenders) {
            w.captureSeconds++;
        } else {
            w.captureSeconds = 0;
        }
        if (w.captureSeconds >= need) {
            plugin.nations().transfer(w.target, def, att);
            Bukkit.broadcast(Msg.c(Msg.PREFIX + "&6" + att.getName() + " &7podbilo chunk &f" + w.target
                    + " &7panstwa &6" + def.getName() + "&7!"));
            end(w, true, null);
            return;
        }
        long maxSec = cfg().getLong("wojna.max-czas-sekundy", 600);
        if ((System.currentTimeMillis() - w.startMillis) / 1000 >= maxSec) {
            end(w, false, "Czas wojny minal - " + def.getName() + " obronilo chunk " + w.target + ".");
            return;
        }
        updateBar(w);
    }

    private boolean presence(War w, UUID side) {
        Nation n = plugin.nations().get(side);
        if (n != null) {
            for (Player p : n.online()) {
                if (validFighter(p) && w.target.contains(p.getLocation())) return true;
            }
        }
        for (WarUnit u : w.units) {
            if (u.side.equals(side) && u.alive() && w.target.contains(u.entity.getLocation())) return true;
        }
        return false;
    }

    private void updateBar(War w) {
        Nation att = plugin.nations().get(w.attacker);
        Nation def = plugin.nations().get(w.defender);
        if (att == null || def == null) return;
        int need = cfg().getInt("wojna.czas-przejecia-sekundy", 10);
        long left = cfg().getLong("wojna.max-czas-sekundy", 600) - (System.currentTimeMillis() - w.startMillis) / 1000;
        int aU = (int) w.units.stream().filter(u -> u.side.equals(w.attacker) && u.alive()).count();
        int dU = (int) w.units.stream().filter(u -> u.side.equals(w.defender) && u.alive()).count();
        w.bar.name(Msg.c("&c" + att.getName() + " &7(" + aU + ") &fvs &9" + def.getName() + " &7(" + dU + ")"
                + " &8| &ePrzejmowanie " + w.captureSeconds + "/" + need + "s &8| &7" + Math.max(0, left) + "s"));
        w.bar.progress(Math.min(1f, w.captureSeconds / (float) need));
        for (Player p : att.online()) p.showBossBar(w.bar);
        for (Player p : def.online()) p.showBossBar(w.bar);
    }

    // =====================================================================
    //  KONIEC WOJNY
    // =====================================================================

    public boolean inWar(UUID nation) {
        for (War w : wars) if (w.involves(nation)) return true;
        return false;
    }

    public void end(War w, boolean attackerWon, String reason) {
        if (!wars.remove(w)) return;
        for (WarUnit u : w.units) {
            unitsByEntity.remove(u.unit.body.getUniqueId());
            if (u.unit.carrier != null) unitsByEntity.remove(u.unit.carrier.getUniqueId());
            removeTicket(u.ticket);
            removeTicket(u.aheadTicket);
            if (u.alive()) {
                Nation n = plugin.nations().get(u.side);
                if (n != null) n.addUnits(u.type, 1); // ocalale jednostki wracaja do armii
            }
            u.unit.remove();
        }
        // jednostki czekajace na odrodzenie tez wracaja
        for (War.Respawn r : w.respawns) {
            Nation n = plugin.nations().get(r.side);
            if (n != null) n.addUnits(r.type, 1);
        }
        w.respawns.clear();
        w.units.clear();
        removeTicket(w.target);
        for (Player p : Bukkit.getOnlinePlayers()) p.hideBossBar(w.bar);
        plugin.nations().save();

        List<Player> notify = new ArrayList<>();
        List<UUID> sides = new ArrayList<>();
        for (UUID id : new UUID[]{w.attacker, w.defender}) {
            Nation nn = plugin.nations().get(id);
            if (nn == null) continue;
            for (Player pl : nn.online()) { notify.add(pl); sides.add(id); }
        }
        for (int i = 0; i < notify.size(); i++) {
            Player p = notify.get(i);
            UUID id = sides.get(i);
            if (attackerWon) {
                Msg.send(p, id.equals(w.attacker) ? "&a&lZwyciestwo! &aChunk " + w.target + " jest teraz twoj."
                        : "&c&lPorazka! &cStraciles chunk " + w.target + ".");
            } else if (reason != null) {
                Msg.send(p, "&e" + reason);
            }
            if (attackerWon || reason != null) Msg.send(p, "&7Ocalale jednostki wrocily do armii.");
        }
    }

    /** Konczy wszystkie wojny w ktorych bierze udzial panstwo. */
    public void endAllFor(UUID nation, String reason) {
        for (War w : new ArrayList<>(wars)) if (w.involves(nation)) end(w, false, reason);
    }

    // =====================================================================
    //  CHUNK TICKETS - zeby jednostki nie znikaly w niezaladowanych chunkach
    // =====================================================================

    private void addTicket(ChunkPos c) {
        if (c == null) return;
        int n = tickets.merge(c, 1, Integer::sum);
        if (n == 1) {
            World w = c.bukkitWorld();
            if (w != null) w.addPluginChunkTicket(c.x(), c.z(), plugin);
        }
    }

    private void removeTicket(ChunkPos c) {
        if (c == null) return;
        Integer n = tickets.get(c);
        if (n == null) return;
        if (n <= 1) {
            tickets.remove(c);
            World w = c.bukkitWorld();
            if (w != null) w.removePluginChunkTicket(c.x(), c.z(), plugin);
        } else {
            tickets.put(c, n - 1);
        }
    }
}
