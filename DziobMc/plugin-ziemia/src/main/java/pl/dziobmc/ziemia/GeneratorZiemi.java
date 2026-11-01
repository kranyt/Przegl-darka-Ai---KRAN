package pl.dziobmc.ziemia;

import org.bukkit.HeightMap;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.World;
import org.bukkit.block.Biome;
import org.bukkit.generator.BiomeProvider;
import org.bukkit.generator.ChunkGenerator;
import org.bukkit.generator.WorldInfo;

import java.util.List;
import java.util.Random;

/** Generator świata: Ziemia w odwzorowaniu walcowym równoodległościowym (x = długość, z = -szerokość). */
public final class GeneratorZiemi extends ChunkGenerator {
    static final int WODA = 62;               // najwyższy blok wody morskiej (poziom morza 63)
    static final int LAD = 0, OCEAN = 1, JEZIORO = 2, RZEKA = 3;

    final Dane d;
    final double bpd;                         // kratek na stopień
    final double spawnLat, spawnLon;
    private volatile Szum szum;
    private volatile long szumSeed;

    static final class Kol { int h, woda = Integer.MIN_VALUE, klasa, typ; double lat; }

    public GeneratorZiemi(Dane d, int skala, double spawnLat, double spawnLon) {
        this.d = d;
        this.bpd = 111320.0 / skala;
        this.spawnLat = spawnLat;
        this.spawnLon = spawnLon;
    }

    Szum szum(long seed) {
        Szum s = szum;
        if (s == null || szumSeed != seed) {
            synchronized (this) {
                if (szum == null || szumSeed != seed) { szum = new Szum(seed); szumSeed = seed; }
                s = szum;
            }
        }
        return s;
    }

    private static double gladko(double t) { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); }

    // --- pamięć podręczna kolumn (na wątek), bo BiomeProvider pyta wiele razy o te same miejsca
    private static final int CACHE = 4096;
    private final ThreadLocal<long[]> cacheKlucze = ThreadLocal.withInitial(() -> { long[] a = new long[CACHE]; java.util.Arrays.fill(a, Long.MIN_VALUE); return a; });
    private final ThreadLocal<Kol[]> cacheWart = ThreadLocal.withInitial(() -> new Kol[CACHE]);

    Kol kolumna(long seed, int x, int z) {
        long klucz = ((long) x << 32) ^ (z & 0xffffffffL) ^ (seed * 31);
        int idx = (int) ((x * 73856093L ^ z * 19349663L) & (CACHE - 1));
        long[] kk = cacheKlucze.get();
        Kol[] kv = cacheWart.get();
        if (kk[idx] == klucz) return kv[idx];
        Kol k = policz(szum(seed), x, z);
        kk[idx] = klucz; kv[idx] = k;
        return k;
    }

    private Kol policz(Szum s, int x, int z) {
        Kol k = new Kol();
        double lat = -z / bpd, lon = x / bpd;
        k.lat = lat;
        if (lat > 89.95 || lat < -89.95) {          // poza mapą: zamarznięty ocean
            k.typ = OCEAN; k.h = 30; k.woda = WODA; k.klasa = Biomy.DEEP_FROZEN_OCEAN;
            return k;
        }
        lon = ((lon + 180.0) % 360.0 + 360.0) % 360.0 - 180.0;
        double alat = Math.abs(lat);
        double nk = s.fbm(x / 40.0, z / 40.0, 3);
        double f = d.maska(d.lad, lon, lat) + nk * 0.22;
        double e = d.wysokosc(lon, lat);
        double jit = 5.0 / bpd;
        int kl = d.biom(lon + s.get(x / 23.0, z / 23.0) * jit, lat + s.get(z / 23.0 + 50, x / 23.0) * jit);

        if (f >= 0.5) {
            k.typ = LAD;
            e = Math.max(e, 2);
            double baza = 64 + e / 36.0;
            double amp = 2.0 + e / 300.0;
            double det = s.fbm(x / 110.0, z / 110.0, 4) * amp + s.fbm(x / 28.0 + 300, z / 28.0, 3) * amp * 0.3;
            if (e > 1200) det += (s.grzbiety(x / 160.0, z / 160.0, 4) - 0.45) * (e - 1200) / 140.0;
            double h = baza + det;
            h = 63 + (h - 63) * gladko((f - 0.5) / 0.35);
            k.h = (int) Math.max(63, Math.min(315, Math.round(h)));
            if (Biomy.ocean(kl)) kl = alat > 62 ? Biomy.SNOWY_PLAINS : alat < 25 ? Biomy.SAVANNA : Biomy.PLAINS;

            // jeziora – własny poziom lustra wody
            double jz = d.maska(d.jeziora, lon, lat) + nk * 0.2;
            int lustro = Math.max(WODA, (int) Math.round(64 + e / 36.0) - 1);
            if (jz > 0.5) {
                int glebokosc = 2 + (int) (Math.min(1.0, (jz - 0.5) * 3) * 8);
                k.typ = JEZIORO; k.woda = lustro; k.h = lustro - glebokosc;
                kl = (alat > 55 || Biomy.zimny(kl)) ? Biomy.FROZEN_RIVER : Biomy.RIVER;
            } else if (jz > 0.3) {
                k.h = Math.min(k.h, lustro + 1 + (int) ((0.5 - jz) * 10));
            }
            // rzeki
            if (k.typ == LAD) {
                double rz = d.maska(d.rzeki, lon, lat) + s.get(x / 9.0, z / 9.0) * 0.12;
                if (rz > 0.42) {
                    int brzeg = k.h;
                    k.typ = RZEKA; k.woda = Math.max(WODA, brzeg - 1); k.h = k.woda - 2 - (rz > 0.7 ? 1 : 0);
                    kl = (alat > 58 || Biomy.zimny(kl)) ? Biomy.FROZEN_RIVER : Biomy.RIVER;
                } else if (rz > 0.25) {
                    k.h = Math.max(63, k.h - 1);
                }
            }
            if (k.typ == LAD) {
                if (k.h <= 65 && f < 0.9 && kl != Biomy.LADOLOD && !Biomy.badlands(kl) && kl != Biomy.MANGROVE_SWAMP) {
                    kl = e > 250 ? Biomy.STONY_SHORE : (alat > 58 || Biomy.zimny(kl)) ? Biomy.SNOWY_BEACH : Biomy.BEACH;
                } else if (k.h > 205 && !Biomy.gory(kl) && kl != Biomy.LADOLOD) {
                    kl = alat > 33 ? Biomy.SNOWY_SLOPES : Biomy.STONY_PEAKS;
                }
            }
        } else {
            k.typ = OCEAN;
            double gl = Math.max(-e, 5);
            double dno = WODA - (1.5 + Math.sqrt(gl) * 0.42);
            double t = Math.min(1.0, (0.5 - f) / 0.35);
            dno = WODA - (WODA - dno) * (0.15 + 0.85 * t);
            dno += s.fbm(x / 50.0, z / 50.0, 2) * 2;
            k.h = (int) Math.max(8, Math.min(WODA - 1, Math.round(dno)));
            k.woda = WODA;
            if (!Biomy.ocean(kl)) {
                kl = alat > 63 ? Biomy.FROZEN_OCEAN : alat > 45 ? Biomy.COLD_OCEAN : alat > 30 ? Biomy.OCEAN
                        : alat > 18 ? Biomy.LUKEWARM_OCEAN : Biomy.WARM_OCEAN;
            }
        }
        k.klasa = kl;
        return k;
    }

    // ------------------------------------------------------------------ bloki

    private static final Material[] PASY = {Material.TERRACOTTA, Material.ORANGE_TERRACOTTA, Material.YELLOW_TERRACOTTA,
            Material.BROWN_TERRACOTTA, Material.WHITE_TERRACOTTA, Material.RED_TERRACOTTA, Material.LIGHT_GRAY_TERRACOTTA,
            Material.ORANGE_TERRACOTTA, Material.TERRACOTTA, Material.RED_TERRACOTTA};

    @Override
    public void generateNoise(WorldInfo w, Random random, int cx, int cz, ChunkData cd) {
        long seed = w.getSeed();
        Szum s = szum(seed);
        int minY = cd.getMinHeight();
        for (int lx = 0; lx < 16; lx++) {
            for (int lz = 0; lz < 16; lz++) {
                int x = (cx << 4) + lx, z = (cz << 4) + lz;
                Kol k = kolumna(seed, x, z);
                kolumnaBloki(cd, s, lx, lz, x, z, k, minY);
            }
        }
    }

    void kolumnaBloki(ChunkData cd, Szum s, int lx, int lz, int x, int z, Kol k, int minY) {
        int top = k.h;
        cd.setBlock(lx, minY, lz, Material.BEDROCK);
        if (minY + 1 < Math.min(0, top + 1)) cd.setRegion(lx, minY + 1, lz, lx + 1, Math.min(0, top + 1), lz + 1, Material.DEEPSLATE);
        if (top >= 0) cd.setRegion(lx, 0, lz, lx + 1, top + 1, lz + 1, Material.STONE);

        int kl = k.klasa;
        double n = s.get(x / 13.0, z / 13.0);
        Material wierzch = Material.GRASS_BLOCK, pod = Material.DIRT;
        int gl = 4;
        boolean pasy = false;
        if (k.typ == OCEAN) {
            boolean cieply = kl == Biomy.WARM_OCEAN || kl == Biomy.LUKEWARM_OCEAN || kl == Biomy.DEEP_LUKEWARM_OCEAN;
            wierzch = cieply ? Material.SAND : (n > 0.35 ? Material.CLAY : n > -0.1 ? Material.GRAVEL : Material.SAND);
            if (top < 40 && !cieply) wierzch = Material.GRAVEL;
            pod = wierzch == Material.CLAY ? Material.CLAY : Material.SAND; gl = 3;
        } else if (k.typ == JEZIORO || k.typ == RZEKA) {
            wierzch = n > 0.3 ? Material.CLAY : n > -0.2 ? Material.SAND : Material.GRAVEL; pod = Material.SAND; gl = 3;
        } else if (kl == Biomy.BEACH || kl == Biomy.SNOWY_BEACH) {
            wierzch = Material.SAND; pod = Material.SAND; gl = 4;
            cd.setRegion(lx, Math.max(minY + 1, top - 7), lz, lx + 1, Math.max(minY + 1, top - 3), lz + 1, Material.SANDSTONE);
        } else if (kl == Biomy.STONY_SHORE || kl == Biomy.STONY_PEAKS) {
            wierzch = n > 0.4 ? Material.CALCITE : Material.STONE; pod = Material.STONE; gl = 1;
        } else if (kl == Biomy.DESERT) {
            wierzch = Material.SAND; pod = Material.SAND; gl = 4;
            cd.setRegion(lx, Math.max(minY + 1, top - 8), lz, lx + 1, Math.max(minY + 1, top - 3), lz + 1, Material.SANDSTONE);
        } else if (Biomy.badlands(kl)) {
            wierzch = kl == Biomy.WOODED_BADLANDS && top > 90 ? Material.COARSE_DIRT : Material.RED_SAND;
            pod = Material.TERRACOTTA; gl = 1; pasy = true;
        } else if (kl == Biomy.SNOWY_SLOPES || kl == Biomy.JAGGED_PEAKS) {
            wierzch = Material.SNOW_BLOCK; pod = Material.SNOW_BLOCK; gl = 3;
        } else if (kl == Biomy.FROZEN_PEAKS) {
            wierzch = n > 0.2 ? Material.PACKED_ICE : Material.SNOW_BLOCK; pod = Material.PACKED_ICE; gl = 3;
        } else if (kl == Biomy.LADOLOD) {
            wierzch = Material.SNOW_BLOCK; pod = Material.PACKED_ICE; gl = 9;
            cd.setRegion(lx, Math.max(minY + 1, top - 12), lz, lx + 1, Math.max(minY + 1, top - 8), lz + 1, Material.BLUE_ICE);
        } else if (kl == Biomy.MANGROVE_SWAMP) {
            wierzch = Material.MUD; pod = Material.MUD; gl = 3;
        } else if (kl == Biomy.OLD_GROWTH_SPRUCE_TAIGA) {
            wierzch = n > 0.25 ? Material.PODZOL : n < -0.35 ? Material.COARSE_DIRT : Material.GRASS_BLOCK;
        } else if (kl == Biomy.WINDSWEPT_HILLS || kl == Biomy.GROVE) {
            if (top > 150 && n > 0.15) { wierzch = Material.STONE; pod = Material.STONE; }
            if (kl == Biomy.GROVE && top > 170) { wierzch = Material.SNOW_BLOCK; }
        } else if (kl == Biomy.SAVANNA_PLATEAU || kl == Biomy.WINDSWEPT_SAVANNA) {
            if (n > 0.45) wierzch = Material.COARSE_DIRT;
        }
        if (k.typ == LAD && !Biomy.badlands(kl) && kl != Biomy.DESERT) {
            double ng = s.get(x / 7.0 + 99, z / 7.0) * 6;
            if (top > 235 + ng) { wierzch = Material.SNOW_BLOCK; }
            else if (top > 212 + ng && wierzch == Material.GRASS_BLOCK) { wierzch = Material.STONE; pod = Material.STONE; }
        }
        for (int i = 0; i < gl; i++) {
            int y = top - i;
            if (y <= minY) break;
            cd.setBlock(lx, y, lz, i == 0 ? wierzch : pod);
        }
        if (pasy) {
            double off = s.get(x / 60.0, z / 60.0) * 3;
            for (int y = top - 1; y > top - 16 && y > minY; y--) {
                cd.setBlock(lx, y, lz, PASY[Math.floorMod((int) Math.floor((y + off) / 2.0), PASY.length)]);
            }
        }
        if (k.woda > top) cd.setRegion(lx, top + 1, lz, lx + 1, k.woda + 1, lz + 1, Material.WATER);
    }

    // ------------------------------------------------------------------ Bukkit

    @Override public BiomeProvider getDefaultBiomeProvider(WorldInfo worldInfo) { return new DostawcaBiomow(this); }

    @Override
    public int getBaseHeight(WorldInfo w, Random random, int x, int z, HeightMap heightMap) {
        Kol k = kolumna(w.getSeed(), x, z);
        if (heightMap == HeightMap.OCEAN_FLOOR || heightMap == HeightMap.OCEAN_FLOOR_WG) return k.h + 1;
        return Math.max(k.h, k.woda) + 1;
    }

    @Override
    public Location getFixedSpawnLocation(World world, Random random) {
        int x = (int) Math.round(spawnLon * bpd), z = (int) Math.round(-spawnLat * bpd);
        Kol k = kolumna(world.getSeed(), x, z);
        return new Location(world, x + 0.5, Math.max(k.h, k.woda) + 1, z + 0.5);
    }

    int[] spawnXYZ(long seed) {
        int x = (int) Math.round(spawnLon * bpd), z = (int) Math.round(-spawnLat * bpd);
        Kol k = kolumna(seed, x, z);
        return new int[]{x, Math.max(k.h, k.woda) + 1, z};
    }

    @Override public boolean shouldGenerateNoise() { return false; }
    @Override public boolean shouldGenerateSurface() { return false; }
    @Override public boolean shouldGenerateCaves() { return true; }
    @Override public boolean shouldGenerateDecorations() { return true; }
    @Override public boolean shouldGenerateMobs() { return true; }
    @Override public boolean shouldGenerateStructures() { return true; }

    /** Biomy: powierzchnia wg danych, pod ziemią czasem jaskinie bujne / naciekowe / głęboka ciemność. */
    static final class DostawcaBiomow extends BiomeProvider {
        private final GeneratorZiemi g;
        private final List<Biome> lista = Biomy.wszystkie();
        DostawcaBiomow(GeneratorZiemi g) { this.g = g; }

        @Override
        public Biome getBiome(WorldInfo w, int x, int y, int z) {
            Kol k = g.kolumna(w.getSeed(), x, z);
            if (y < k.h - 16 && y < 48) {
                double c = g.szum(w.getSeed()).get(x / 70.0 + y / 45.0, z / 70.0 - y / 45.0);
                if (y < -10 && c > 0.5) return Biome.DEEP_DARK;
                if (c < -0.5) return Biome.DRIPSTONE_CAVES;
                if (c > 0.4 && k.klasa != Biomy.DESERT && !Biomy.zimny(k.klasa)) return Biome.LUSH_CAVES;
            }
            return Biomy.MAPA[k.klasa & 63];
        }

        @Override public List<Biome> getBiomes(WorldInfo w) { return lista; }
    }
}
