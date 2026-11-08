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
        addTicket(target);
        w.bar = BossBar.bossBar(Msg.c("&cWojna"), 0f, BossBar.Color.RED, BossBar.Overlay.NOTCHED_10);
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
        World world = loc.getWorld();
        String color = attacker ? "&c" : "&9";
        double hp = t.hp(cfg());
        Mob mob;
        switch (t) {
            case SOLDIER -> mob = world.spawn(loc, Zombie.class, z -> {
                z.setAdult();
                z.setShouldBurnInDay(false);
                EntityEquipment eq = z.getEquipment();
                eq.setHelmet(new ItemStack(Material.IRON_HELMET));
                eq.setChestplate(new ItemStack(Material.IRON_CHESTPLATE));
                eq.setLeggings(new ItemStack(Material.IRON_LEGGINGS));
                eq.setBoots(new ItemStack(Material.IRON_BOOTS));
                eq.setItemInMainHand(new ItemStack(Material.IRON_SWORD));
                Attr.set(z, "spawn_reinforcements", 0);
                // ~ predkosc chodzenia gracza
                Attr.set(z, "movement_speed", 0.25 * t.speed(cfg()));
                Attr.set(z, "follow_range", 48);
                prepare(z, w, t, hp, color, n);
            });
            case DRONE -> mob = world.spawn(loc, Vex.class, v -> {
                v.setLimitedLifetime(false);
                prepare(v, w, t, hp, color, n);
            });
            default -> mob = world.spawn(loc, Phantom.class, ph -> {
                ph.setSize(t == UnitType.JET ? 6 : 2);
                ph.setShouldBurnInDay(false);
                prepare(ph, w, t, hp, color, n);
            });
        }
        if (t.flying()) {
            mob.setAI(false);
            mob.setGravity(false);
        } else {
            Bukkit.getMobGoals().removeAllGoals(mob);
        }
        WarUnit u = new WarUnit(w, t, n.getOwner(), mob);
        u.lastPos = mob.getLocation();
        u.ticket = ChunkPos.of(mob.getLocation());
        addTicket(u.ticket);
        w.units.add(u);
        unitsByEntity.put(mob.getUniqueId(), u);
    }

    private void prepare(Mob m, War w, UnitType t, double hp, String color, Nation n) {
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
                    unitsByEntity.remove(u.entity.getUniqueId());
                    it.remove();
                    continue;
                }
                try {
                    if (u.type.flying()) tickFlyer(u); else tickSoldier(u);
                    updateTicket(u);
                } catch (Exception ex) {
                    plugin.getLogger().warning("Blad jednostki: " + ex);
                }
            }
            if (tickCounter % 20 == 0) secondTick(w);
        }
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

        // stuck detection
        Location cur = m.getLocation();
        if (u.lastPos != null && u.lastPos.getWorld() == cur.getWorld() && u.lastPos.distanceSquared(cur) < 1) {
            u.stuckTicks += 20;
        } else {
            u.stuckTicks = 0;
        }
        u.lastPos = cur;

        Location dest = destinationFor(u);
        if (dest == null) return;
        if (u.war.target.contains(cur) && cur.distance(dest) < 6) {
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
        boolean ok = pf.moveTo(wp, 1.0);
        if ((!ok || u.stuckTicks >= 60) && len > 0.1) {
            // zablokowany - lekki skok w kierunku celu (nie teleport)
            Vector push = dir.normalize().multiply(0.35);
            push.setY(m.isOnGround() ? 0.45 : m.getVelocity().getY());
            m.setVelocity(push);
        }
    }

    private void tickFlyer(WarUnit u) {
        Mob m = u.entity;
        if (u.attackCooldown > 0) u.attackCooldown--;
        Location cur = m.getLocation();
        World world = cur.getWorld();
        double speed = UnitType.PLAYER_WALK_BPS * u.type.speed(cfg()) / 20.0; // bloki na tick
        LivingEntity enemy = findEnemy(u, cfg().getDouble("wojna.zasieg-wykrywania", 16) + 8);

        Location goal;
        if (enemy != null) {
            goal = enemy.getLocation().add(0, enemy.getHeight() * 0.6, 0);
        } else {
            Location dest = destinationFor(u);
            if (dest == null) return;
            if (u.war.target.contains(cur) || cur.distance(dest) < 12) {
                // kraza nad celem
                u.orbitAngle += speed / 8.0;
                goal = dest.clone().add(Math.cos(u.orbitAngle) * 6, 6, Math.sin(u.orbitAngle) * 6);
            } else {
                goal = dest.clone().add(0, 10, 0);
            }
        }

        Vector delta = goal.toVector().subtract(cur.toVector());
        double dist = delta.length();
        Location next;
        if (dist <= speed || dist < 0.01) {
            next = goal.clone();
        } else {
            next = cur.clone().add(delta.clone().normalize().multiply(speed));
        }
        // nie wlatuj w ziemie
        int ground = world.getHighestBlockYAt(next.getBlockX(), next.getBlockZ());
        double minY = ground + (enemy != null ? 1.0 : 4.0);
        if (next.getY() < minY) next.setY(Math.min(minY, next.getY() + speed + 0.5));
        if (dist > 0.01) next.setDirection(delta);
        m.teleport(next);

        if (enemy != null && next.distance(enemy.getLocation().add(0, enemy.getHeight() * 0.5, 0)) <= 2.5) {
            tryAttack(u, enemy);
        }
        if (tickCounter % 4 == 0) {
            world.spawnParticle(Particle.SMOKE, next, 2, 0.1, 0.1, 0.1, 0.01);
        }
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
        return !p.isDead() && (p.getGameMode() == GameMode.SURVIVAL || p.getGameMode() == GameMode.ADVENTURE);
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

    public void end(War w, boolean attackerWon, String reason) {
        if (!wars.remove(w)) return;
        for (WarUnit u : w.units) {
            unitsByEntity.remove(u.entity.getUniqueId());
            removeTicket(u.ticket);
            if (u.alive()) {
                Nation n = plugin.nations().get(u.side);
                if (n != null) n.addUnits(u.type, 1); // ocalale jednostki wracaja do armii
                u.entity.remove();
            }
        }
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
