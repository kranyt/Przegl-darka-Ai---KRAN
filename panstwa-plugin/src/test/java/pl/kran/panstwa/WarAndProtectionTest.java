package pl.kran.panstwa;

import be.seeseemelk.mockbukkit.MockBukkit;
import be.seeseemelk.mockbukkit.ServerMock;
import be.seeseemelk.mockbukkit.WorldMock;
import be.seeseemelk.mockbukkit.entity.PlayerMock;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.block.Block;
import org.bukkit.event.block.BlockBreakEvent;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import pl.kran.panstwa.model.Nation;
import pl.kran.panstwa.util.ChunkPos;

import static org.junit.jupiter.api.Assertions.*;

class WarAndProtectionTest {
    private ServerMock server;
    private PanstwaPlugin plugin;
    private WorldMock world;

    @BeforeEach
    void setUp() {
        server = MockBukkit.mock();
        // MockBukkit nie ma chunk ticketow - w tescie nic nie robia
        world = new WorldMock(Material.DIRT, 4) {
            @Override
            public boolean addPluginChunkTicket(int x, int z, org.bukkit.plugin.Plugin plugin) { return true; }

            @Override
            public boolean removePluginChunkTicket(int x, int z, org.bukkit.plugin.Plugin plugin) { return true; }
        };
        world.setName("world");
        server.addWorld(world);
        plugin = MockBukkit.load(PanstwaPlugin.class);
    }

    @AfterEach
    void tearDown() {
        MockBukkit.unmock();
    }

    private Nation nation(PlayerMock owner, int chunkX, int chunkZ) {
        Location fund = new Location(world, (chunkX << 4) + 8, 5, (chunkZ << 4) + 8);
        fund.getBlock().setType(Material.BEACON);
        return plugin.nations().create(owner.getUniqueId(), owner.getName(), fund);
    }

    @Test
    void opCannotBreakForeignBlocksUnlessAdminMode() {
        PlayerMock owner = server.addPlayer("Wlasciciel");
        PlayerMock op = server.addPlayer("Op");
        op.setOp(true);
        nation(owner, 0, 0);
        Block b = world.getBlockAt(3, 4, 3);
        b.setType(Material.STONE);

        BlockBreakEvent e = new BlockBreakEvent(b, op);
        server.getPluginManager().callEvent(e);
        assertTrue(e.isCancelled(), "OP bez /p admin nie moze niszczyc w cudzym panstwie");

        op.performCommand("p admin");
        BlockBreakEvent e2 = new BlockBreakEvent(b, op);
        server.getPluginManager().callEvent(e2);
        assertFalse(e2.isCancelled(), "OP w trybie /p admin moze niszczyc");
    }

    @Test
    void memberCanBuildStrangerCannot() {
        PlayerMock owner = server.addPlayer("Wlasciciel");
        PlayerMock member = server.addPlayer("Czlonek");
        PlayerMock stranger = server.addPlayer("Obcy");
        Nation n = nation(owner, 0, 0);
        plugin.nations().addMember(n, member.getUniqueId());
        Block b = world.getBlockAt(3, 4, 3);
        b.setType(Material.STONE);

        BlockBreakEvent e = new BlockBreakEvent(b, member);
        server.getPluginManager().callEvent(e);
        assertFalse(e.isCancelled());
        BlockBreakEvent e2 = new BlockBreakEvent(b, stranger);
        server.getPluginManager().callEvent(e2);
        assertTrue(e2.isCancelled());
    }

    @Test
    void attackerCapturesChunkAfter10SecondsEvenInCreative() {
        PlayerMock att = server.addPlayer("Atakujacy");
        PlayerMock def = server.addPlayer("Obronca");
        Nation a = nation(att, 0, 0);
        Nation d = nation(def, 5, 0);
        ChunkPos target = new ChunkPos("world", 6, 0);
        plugin.nations().claim(d, target);
        def.teleport(new Location(world, 5 * 16 + 8, 5, 8)); // obronca u siebie, poza celem

        att.setGameMode(GameMode.CREATIVE);
        att.teleport(new Location(world, 6 * 16 + 8, 5, 8));
        assertTrue(att.performCommand("p wojna"));
        assertNotNull(plugin.wars().warAt(target), "wojna powinna sie zaczac");

        server.getScheduler().performTicks(20 * 12);

        assertSame(a, plugin.nations().getAt(target), "chunk powinien nalezec do atakujacego");
        assertNull(plugin.wars().warAt(target), "wojna powinna sie skonczyc");

        // po wojnie ochrona dalej dziala: obronca nie moze niszczyc w podbitym chunku
        Block b = world.getBlockAt(6 * 16 + 3, 4, 3);
        b.setType(Material.STONE);
        BlockBreakEvent e = new BlockBreakEvent(b, def);
        server.getPluginManager().callEvent(e);
        assertTrue(e.isCancelled(), "po wojnie ochrona musi dalej dzialac");
        // a w swoim fundamencie dalej tez
        Block own = world.getBlockAt(3, 4, 3);
        own.setType(Material.STONE);
        BlockBreakEvent e2 = new BlockBreakEvent(own, def);
        server.getPluginManager().callEvent(e2);
        assertTrue(e2.isCancelled());
    }

    @Test
    void defenderPresenceBlocksCapture() {
        PlayerMock att = server.addPlayer("Atakujacy");
        PlayerMock def = server.addPlayer("Obronca");
        nation(att, 0, 0);
        Nation d = nation(def, 5, 0);
        ChunkPos target = new ChunkPos("world", 6, 0);
        plugin.nations().claim(d, target);
        att.teleport(new Location(world, 6 * 16 + 8, 5, 8));
        def.teleport(new Location(world, 6 * 16 + 4, 5, 4));
        att.performCommand("p wojna");
        server.getScheduler().performTicks(20 * 12);
        assertSame(d, plugin.nations().getAt(target));
        assertNotNull(plugin.wars().warAt(target));
    }

    @Test
    void homeTeleportsMemberToNation() {
        PlayerMock owner = server.addPlayer("Wlasciciel");
        PlayerMock member = server.addPlayer("Czlonek");
        Nation n = nation(owner, 0, 0);
        plugin.nations().addMember(n, member.getUniqueId());
        member.teleport(new Location(world, 500, 5, 500));

        member.performCommand("p dom");
        server.getScheduler().performTicks(20 * 4);
        assertEquals(new ChunkPos("world", 0, 0), ChunkPos.of(member.getLocation()), "gracz powinien byc w panstwie");

        // ruch przerywa odliczanie
        member.teleport(new Location(world, 500, 5, 500));
        server.getScheduler().performTicks(20 * 31); // cooldown
        member.performCommand("p dom");
        member.simulatePlayerMove(new Location(world, 505, 5, 500));
        server.getScheduler().performTicks(20 * 4);
        assertNotEquals(new ChunkPos("world", 0, 0), ChunkPos.of(member.getLocation()));
    }

    @Test
    void setHomeOnlyInOwnTerritory() {
        PlayerMock owner = server.addPlayer("Wlasciciel");
        Nation n = nation(owner, 0, 0);
        owner.teleport(new Location(world, 200, 5, 200));
        owner.performCommand("p ustawdom");
        assertNull(n.getRawHome());
        owner.teleport(new Location(world, 3, 5, 3));
        owner.performCommand("p ustawdom");
        assertNotNull(n.getRawHome());
        assertEquals(3, n.getHome().getBlockX());
    }
}
