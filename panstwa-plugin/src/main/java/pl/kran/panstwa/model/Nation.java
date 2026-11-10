package pl.kran.panstwa.model;

import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.entity.Player;
import pl.kran.panstwa.util.ChunkPos;
import pl.kran.panstwa.war.UnitType;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

public class Nation {
    private final UUID owner;
    private String name;
    private final String fundWorld;
    private final int fundX, fundY, fundZ;
    private final Set<ChunkPos> chunks = new LinkedHashSet<>();
    private final Map<UnitType, Integer> army = new EnumMap<>(UnitType.class);
    private boolean starterPackBought;
    private final Set<UUID> members = new LinkedHashSet<>();
    /** Do kiedy oplacone jest panstwo (64 diamenty co 7 dni). */
    private long paidUntil;

    public Nation(UUID owner, String name, String fundWorld, int fundX, int fundY, int fundZ) {
        this.owner = owner;
        this.name = name;
        this.fundWorld = fundWorld;
        this.fundX = fundX;
        this.fundY = fundY;
        this.fundZ = fundZ;
    }

    public UUID getOwner() { return owner; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getFundWorld() { return fundWorld; }
    public int getFundX() { return fundX; }
    public int getFundY() { return fundY; }
    public int getFundZ() { return fundZ; }
    public Set<ChunkPos> getChunks() { return chunks; }
    public boolean isStarterPackBought() { return starterPackBought; }
    public void setStarterPackBought(boolean b) { this.starterPackBought = b; }

    /** Czlonkowie (bez wlasciciela). */
    public Set<UUID> getMembers() { return members; }

    /** Czy gracz jest wlascicielem albo czlonkiem. */
    public boolean isMember(UUID player) {
        return owner.equals(player) || members.contains(player);
    }

    public boolean isOwner(UUID player) { return owner.equals(player); }

    /** Wlasciciel + czlonkowie. */
    public List<UUID> allPlayers() {
        List<UUID> l = new ArrayList<>();
        l.add(owner);
        l.addAll(members);
        return l;
    }

    /** Gracze panstwa ktorzy sa teraz online. */
    public List<Player> online() {
        List<Player> l = new ArrayList<>();
        for (UUID id : allPlayers()) {
            Player p = Bukkit.getPlayer(id);
            if (p != null) l.add(p);
        }
        return l;
    }

    public long getPaidUntil() { return paidUntil; }
    public void setPaidUntil(long t) { this.paidUntil = t; }

    public ChunkPos getCapital() {
        return new ChunkPos(fundWorld, fundX >> 4, fundZ >> 4);
    }

    /** Ustawiony dom (/p ustawdom) albo null. */
    private Location home;

    public Location getRawHome() { return home == null ? null : home.clone(); }
    public void setHome(Location loc) { this.home = loc == null ? null : loc.clone(); }

    /**
     * Miejsce do ktorego teleportuje /p dom: ustawiony dom, a jesli go nie ma
     * albo jego chunk nie nalezy juz do panstwa - na fundament.
     */
    public Location getHome() {
        if (home != null && home.getWorld() != null && chunks.contains(ChunkPos.of(home))) return home.clone();
        World w = Bukkit.getWorld(fundWorld);
        if (w == null) return null;
        return new Location(w, fundX + 0.5, fundY + 1, fundZ + 0.5);
    }

    public Block getFundamentBlock() {
        World w = Bukkit.getWorld(fundWorld);
        return w == null ? null : w.getBlockAt(fundX, fundY, fundZ);
    }

    public boolean isFundament(Location loc) {
        return loc.getWorld() != null && loc.getWorld().getName().equals(fundWorld)
                && loc.getBlockX() == fundX && loc.getBlockY() == fundY && loc.getBlockZ() == fundZ;
    }

    public int getUnits(UnitType t) { return army.getOrDefault(t, 0); }
    public void setUnits(UnitType t, int n) { army.put(t, Math.max(0, n)); }
    public void addUnits(UnitType t, int n) { setUnits(t, getUnits(t) + n); }

    /** Najblizszy wlasny chunk do celu i odleglosc do niego. */
    public ChunkPos nearestChunk(ChunkPos target) {
        ChunkPos best = null;
        int bestD = Integer.MAX_VALUE;
        for (ChunkPos c : chunks) {
            int d = c.distance(target);
            if (d < bestD) { bestD = d; best = c; }
        }
        return best;
    }

    public int distanceTo(ChunkPos target) {
        ChunkPos n = nearestChunk(target);
        return n == null ? Integer.MAX_VALUE : n.distance(target);
    }
}
