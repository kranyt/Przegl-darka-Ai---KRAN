package pl.kran.panstwa.listener;

import org.bukkit.entity.Entity;
import org.bukkit.entity.Player;
import org.bukkit.entity.Projectile;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityCombustEvent;
import org.bukkit.event.entity.EntityDamageByEntityEvent;
import org.bukkit.event.entity.EntityDamageEvent;
import org.bukkit.event.entity.EntityDeathEvent;
import org.bukkit.event.entity.EntityPortalEvent;
import org.bukkit.event.entity.EntityTargetEvent;
import org.bukkit.event.entity.EntityTransformEvent;
import org.bukkit.event.world.EntitiesLoadEvent;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.war.WarUnit;

import java.util.UUID;

/** Zachowanie jednostek wojskowych. */
public class UnitListener implements Listener {
    private final PanstwaPlugin plugin;

    public UnitListener(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    private boolean isUnit(Entity e) {
        return plugin.wars().getUnit(e) != null || plugin.wars().isTaggedUnit(e);
    }

    @EventHandler
    public void onCombust(EntityCombustEvent e) {
        if (isUnit(e.getEntity())) e.setCancelled(true);
    }

    @EventHandler
    public void onTarget(EntityTargetEvent e) {
        if (isUnit(e.getEntity())) e.setCancelled(true);
    }

    @EventHandler
    public void onTransform(EntityTransformEvent e) {
        if (isUnit(e.getEntity())) e.setCancelled(true);
    }

    @EventHandler
    public void onPortal(EntityPortalEvent e) {
        if (isUnit(e.getEntity())) e.setCancelled(true);
    }

    @EventHandler(ignoreCancelled = true)
    public void onEnvDamage(EntityDamageEvent e) {
        if (!isUnit(e.getEntity())) return;
        switch (e.getCause()) {
            case SUFFOCATION, FALL, DROWNING, FLY_INTO_WALL, CRAMMING -> e.setCancelled(true);
            default -> { }
        }
    }

    /** Brak friendly fire: jednostki nie bija swoich i wlasciciel nie bije swoich jednostek. */
    @EventHandler(priority = EventPriority.HIGH, ignoreCancelled = true)
    public void onDamage(EntityDamageByEntityEvent e) {
        Entity damager = e.getDamager();
        if (damager instanceof Projectile pr && pr.getShooter() instanceof Entity shooter) damager = shooter;
        UUID attackerSide = sideOf(damager);
        UUID victimSide = sideOf(e.getEntity());
        if (attackerSide != null && attackerSide.equals(victimSide)) e.setCancelled(true);
    }

    private UUID sideOf(Entity e) {
        WarUnit u = plugin.wars().getUnit(e);
        if (u != null) return u.getSide();
        if (e instanceof Player p && plugin.nations().get(p.getUniqueId()) != null) return p.getUniqueId();
        return null;
    }

    @EventHandler
    public void onDeath(EntityDeathEvent e) {
        if (!isUnit(e.getEntity())) return;
        e.getDrops().clear();
        e.setDroppedExp(0);
    }

    /** Jednostki ktore zostaly po restarcie serwera (wojna juz nie istnieje) - usun. */
    @EventHandler
    public void onLoad(EntitiesLoadEvent e) {
        for (Entity en : e.getEntities()) {
            if (plugin.wars().isTaggedUnit(en) && plugin.wars().getUnit(en) == null) en.remove();
        }
    }
}
