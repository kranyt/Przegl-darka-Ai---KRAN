package pl.kran.panstwa.util;

import org.bukkit.Bukkit;
import org.bukkit.Chunk;
import org.bukkit.Location;
import org.bukkit.World;

/** Pozycja chunka niezalezna od tego czy chunk jest zaladowany. */
public record ChunkPos(String world, int x, int z) {

    public static ChunkPos of(Location loc) {
        return new ChunkPos(loc.getWorld().getName(), loc.getBlockX() >> 4, loc.getBlockZ() >> 4);
    }

    public static ChunkPos of(Chunk chunk) {
        return new ChunkPos(chunk.getWorld().getName(), chunk.getX(), chunk.getZ());
    }

    public static ChunkPos parse(String s) {
        String[] p = s.split(";");
        return new ChunkPos(p[0], Integer.parseInt(p[1]), Integer.parseInt(p[2]));
    }

    public String serialize() {
        return world + ";" + x + ";" + z;
    }

    public World bukkitWorld() {
        return Bukkit.getWorld(world);
    }

    /** Odleglosc w chunkach (Chebyshev), Integer.MAX_VALUE jesli inny swiat. */
    public int distance(ChunkPos other) {
        if (!world.equals(other.world)) return Integer.MAX_VALUE;
        return Math.max(Math.abs(x - other.x), Math.abs(z - other.z));
    }

    /** Srodek chunka na powierzchni. */
    public Location surfaceCenter(double extraY) {
        World w = bukkitWorld();
        if (w == null) return null;
        int bx = (x << 4) + 8;
        int bz = (z << 4) + 8;
        int y = w.getHighestBlockYAt(bx, bz);
        return new Location(w, bx + 0.5, y + 1 + extraY, bz + 0.5);
    }

    public boolean contains(Location loc) {
        return loc.getWorld() != null && loc.getWorld().getName().equals(world)
                && (loc.getBlockX() >> 4) == x && (loc.getBlockZ() >> 4) == z;
    }

    @Override
    public String toString() {
        return "[" + x + ", " + z + "]";
    }
}
