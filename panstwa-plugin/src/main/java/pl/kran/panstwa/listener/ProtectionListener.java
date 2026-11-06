package pl.kran.panstwa.listener;

import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.block.Block;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.block.BlockBreakEvent;
import org.bukkit.event.block.BlockBurnEvent;
import org.bukkit.event.block.BlockExplodeEvent;
import org.bukkit.event.block.BlockPistonExtendEvent;
import org.bukkit.event.block.BlockPistonRetractEvent;
import org.bukkit.event.block.BlockPlaceEvent;
import org.bukkit.event.entity.EntityChangeBlockEvent;
import org.bukkit.event.entity.EntityExplodeEvent;
import org.bukkit.event.player.PlayerBucketEmptyEvent;
import org.bukkit.event.player.PlayerBucketFillEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.inventory.ItemStack;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.model.Nation;
import pl.kran.panstwa.util.ChunkPos;
import pl.kran.panstwa.util.Items;
import pl.kran.panstwa.util.Msg;

import java.util.List;

/** Fundament + ochrona chunkow panstw. */
public class ProtectionListener implements Listener {
    private final PanstwaPlugin plugin;

    public ProtectionListener(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    private boolean canBuild(Player p, Block b) {
        Nation n = plugin.nations().getAt(b.getLocation());
        if (n == null) return true;
        if (n.getOwner().equals(p.getUniqueId())) return true;
        return p.hasPermission("panstwa.admin");
    }

    // ------------------------------------------------------------- stawianie fundamentu
    @EventHandler(priority = EventPriority.HIGH, ignoreCancelled = true)
    public void onPlace(BlockPlaceEvent e) {
        Player p = e.getPlayer();
        Block b = e.getBlockPlaced();
        if (plugin.isFundamentItem(e.getItemInHand())) {
            if (plugin.nations().get(p.getUniqueId()) != null) {
                e.setCancelled(true);
                Msg.send(p, "&cMasz juz panstwo! Jedno panstwo na gracza.");
                return;
            }
            Nation owner = plugin.nations().getAt(b.getLocation());
            if (owner != null) {
                e.setCancelled(true);
                Msg.send(p, "&cTen chunk nalezy juz do panstwa " + owner.getName() + ".");
                return;
            }
            String name = p.getName();
            if (plugin.nations().getByName(name) != null) name = name + "_" + (System.currentTimeMillis() % 1000);
            Nation n = plugin.nations().create(p.getUniqueId(), name, b.getLocation());
            p.playSound(p.getLocation(), "minecraft:block.beacon.activate", 1f, 1f);
            Bukkit.broadcast(Msg.c(Msg.PREFIX + "&aPowstalo nowe panstwo: &6" + n.getName() + "&a!"));
            Msg.send(p, "&aTwoje panstwo zostalo zalozone na chunku &f" + ChunkPos.of(b.getLocation())
                    + "&a. Nikt nie moze go zniszczyc. Zmien nazwe: &f/p nazwa <nazwa>");
            return;
        }
        if (!canBuild(p, b)) {
            e.setCancelled(true);
            Msg.send(p, "&cTen teren nalezy do panstwa " + plugin.nations().getAt(b.getLocation()).getName() + ".");
        }
    }

    // ------------------------------------------------------------- niszczenie
    @EventHandler(priority = EventPriority.HIGH, ignoreCancelled = true)
    public void onBreak(BlockBreakEvent e) {
        Player p = e.getPlayer();
        Block b = e.getBlock();
        Nation fund = plugin.nations().getByFundament(b.getLocation());
        if (fund != null) {
            e.setCancelled(true);
            if (fund.getOwner().equals(p.getUniqueId())) {
                Bukkit.getScheduler().runTask(plugin, () -> plugin.menus().openDelete(p));
            } else {
                Msg.send(p, "&cNie mozesz zniszczyc fundamentu panstwa " + fund.getName() + "!");
            }
            return;
        }
        if (!canBuild(p, b)) {
            e.setCancelled(true);
            Msg.send(p, "&cTen teren nalezy do panstwa " + plugin.nations().getAt(b.getLocation()).getName() + ".");
        }
    }

    @EventHandler(ignoreCancelled = true)
    public void onBucket(PlayerBucketEmptyEvent e) {
        if (!canBuild(e.getPlayer(), e.getBlockClicked().getRelative(e.getBlockFace()))) e.setCancelled(true);
    }

    @EventHandler(ignoreCancelled = true)
    public void onBucketFill(PlayerBucketFillEvent e) {
        if (!canBuild(e.getPlayer(), e.getBlockClicked())) e.setCancelled(true);
    }

    @EventHandler(ignoreCancelled = true)
    public void onInteract(PlayerInteractEvent e) {
        if (e.getClickedBlock() == null) return;
        Block b = e.getClickedBlock();
        if (e.getAction() == Action.PHYSICAL || (e.getAction() == Action.RIGHT_CLICK_BLOCK && isProtectedInteract(b.getType()))) {
            if (!canBuild(e.getPlayer(), b)) {
                e.setCancelled(true);
                if (e.getAction() != Action.PHYSICAL) Msg.send(e.getPlayer(), "&cNie mozesz tego uzywac na terenie cudzego panstwa.");
            }
        }
    }

    private boolean isProtectedInteract(Material m) {
        String n = m.name();
        return n.endsWith("CHEST") || n.endsWith("SHULKER_BOX") || n.endsWith("BARREL") || n.endsWith("FURNACE")
                || n.endsWith("DOOR") || n.endsWith("GATE") || n.endsWith("HOPPER") || n.endsWith("DISPENSER")
                || n.endsWith("DROPPER") || n.equals("BEACON") || n.endsWith("ANVIL") || n.endsWith("BUTTON")
                || n.equals("LEVER") || n.equals("FARMLAND") || n.endsWith("_BED") || n.equals("SMOKER")
                || n.equals("BREWING_STAND") || n.equals("REPEATER") || n.equals("COMPARATOR");
    }

    // ------------------------------------------------------------- wybuchy, ogien, tloki
    @EventHandler(ignoreCancelled = true)
    public void onEntityExplode(EntityExplodeEvent e) {
        filter(e.blockList());
    }

    @EventHandler(ignoreCancelled = true)
    public void onBlockExplode(BlockExplodeEvent e) {
        filter(e.blockList());
    }

    private void filter(List<Block> blocks) {
        blocks.removeIf(b -> plugin.nations().getAt(b.getLocation()) != null);
    }

    @EventHandler(ignoreCancelled = true)
    public void onBurn(BlockBurnEvent e) {
        if (plugin.nations().getAt(e.getBlock().getLocation()) != null) e.setCancelled(true);
    }

    @EventHandler(ignoreCancelled = true)
    public void onEntityChange(EntityChangeBlockEvent e) {
        if (e.getEntity() instanceof Player) return;
        if (plugin.nations().getByFundament(e.getBlock().getLocation()) != null) e.setCancelled(true);
        else if (plugin.nations().getAt(e.getBlock().getLocation()) != null
                && e.getEntity().getType().name().matches("ENDERMAN|WITHER|ENDER_DRAGON|RAVAGER|ZOMBIE")) e.setCancelled(true);
    }

    @EventHandler(ignoreCancelled = true)
    public void onPistonExtend(BlockPistonExtendEvent e) {
        Nation from = plugin.nations().getAt(e.getBlock().getLocation());
        for (Block b : e.getBlocks()) {
            Block to = b.getRelative(e.getDirection());
            if (crosses(from, b) || crosses(from, to)) { e.setCancelled(true); return; }
        }
    }

    @EventHandler(ignoreCancelled = true)
    public void onPistonRetract(BlockPistonRetractEvent e) {
        Nation from = plugin.nations().getAt(e.getBlock().getLocation());
        for (Block b : e.getBlocks()) if (crosses(from, b)) { e.setCancelled(true); return; }
    }

    private boolean crosses(Nation from, Block b) {
        Nation n = plugin.nations().getAt(b.getLocation());
        return n != null && n != from;
    }

    // ------------------------------------------------------------- odbior zaleglych przedmiotow
    @EventHandler
    public void onJoin(PlayerJoinEvent e) {
        Player p = e.getPlayer();
        Bukkit.getScheduler().runTaskLater(plugin, () -> {
            if (!p.isOnline()) return;
            List<ItemStack> items = plugin.nations().takePending(p.getUniqueId());
            if (items == null || items.isEmpty()) return;
            Items.give(p, items.toArray(new ItemStack[0]));
            Msg.send(p, "&aOdebrales przedmioty z gieldy ktore przyszly gdy byles offline ("
                    + items.stream().mapToInt(ItemStack::getAmount).sum() + ").");
        }, 40L);
    }
}
