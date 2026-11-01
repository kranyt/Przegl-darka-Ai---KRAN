package pl.dziobmc.ziemia;

import org.bukkit.block.Biome;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/** Klasy biomów zapisane w danych (muszą się zgadzać z narzedzia/ziemia/dane.py). Bez switch/ordinal – działa też z Biome jako interfejsem (1.21.3+). */
final class Biomy {
    static final int OCEAN = 1, DEEP_OCEAN = 2, WARM_OCEAN = 3, LUKEWARM_OCEAN = 4, DEEP_LUKEWARM_OCEAN = 5, COLD_OCEAN = 6,
            DEEP_COLD_OCEAN = 7, FROZEN_OCEAN = 8, DEEP_FROZEN_OCEAN = 9, PLAINS = 10, SUNFLOWER_PLAINS = 11, FOREST = 12,
            BIRCH_FOREST = 13, DARK_FOREST = 14, TAIGA = 15, SNOWY_TAIGA = 16, SNOWY_PLAINS = 17, ICE_SPIKES = 18, DESERT = 19,
            BADLANDS = 20, SAVANNA = 21, SAVANNA_PLATEAU = 22, JUNGLE = 23, SPARSE_JUNGLE = 24, BAMBOO_JUNGLE = 25, SWAMP = 26,
            MANGROVE_SWAMP = 27, MEADOW = 28, WINDSWEPT_HILLS = 29, GROVE = 30, SNOWY_SLOPES = 31, JAGGED_PEAKS = 32,
            FROZEN_PEAKS = 33, STONY_PEAKS = 34, CHERRY_GROVE = 35, OLD_GROWTH_SPRUCE_TAIGA = 36, FLOWER_FOREST = 37,
            RIVER = 38, FROZEN_RIVER = 39, BEACH = 40, SNOWY_BEACH = 41, WINDSWEPT_SAVANNA = 42, ERODED_BADLANDS = 43,
            WOODED_BADLANDS = 44, STONY_SHORE = 45, LADOLOD = 50;

    static final Biome[] MAPA = new Biome[64];

    static {
        Arrays.fill(MAPA, Biome.PLAINS);
        MAPA[OCEAN] = Biome.OCEAN; MAPA[DEEP_OCEAN] = Biome.DEEP_OCEAN; MAPA[WARM_OCEAN] = Biome.WARM_OCEAN;
        MAPA[LUKEWARM_OCEAN] = Biome.LUKEWARM_OCEAN; MAPA[DEEP_LUKEWARM_OCEAN] = Biome.DEEP_LUKEWARM_OCEAN;
        MAPA[COLD_OCEAN] = Biome.COLD_OCEAN; MAPA[DEEP_COLD_OCEAN] = Biome.DEEP_COLD_OCEAN; MAPA[FROZEN_OCEAN] = Biome.FROZEN_OCEAN;
        MAPA[DEEP_FROZEN_OCEAN] = Biome.DEEP_FROZEN_OCEAN; MAPA[PLAINS] = Biome.PLAINS; MAPA[SUNFLOWER_PLAINS] = Biome.SUNFLOWER_PLAINS;
        MAPA[FOREST] = Biome.FOREST; MAPA[BIRCH_FOREST] = Biome.BIRCH_FOREST; MAPA[DARK_FOREST] = Biome.DARK_FOREST;
        MAPA[TAIGA] = Biome.TAIGA; MAPA[SNOWY_TAIGA] = Biome.SNOWY_TAIGA; MAPA[SNOWY_PLAINS] = Biome.SNOWY_PLAINS;
        MAPA[ICE_SPIKES] = Biome.ICE_SPIKES; MAPA[DESERT] = Biome.DESERT; MAPA[BADLANDS] = Biome.BADLANDS; MAPA[SAVANNA] = Biome.SAVANNA;
        MAPA[SAVANNA_PLATEAU] = Biome.SAVANNA_PLATEAU; MAPA[JUNGLE] = Biome.JUNGLE; MAPA[SPARSE_JUNGLE] = Biome.SPARSE_JUNGLE;
        MAPA[BAMBOO_JUNGLE] = Biome.BAMBOO_JUNGLE; MAPA[SWAMP] = Biome.SWAMP; MAPA[MANGROVE_SWAMP] = Biome.MANGROVE_SWAMP;
        MAPA[MEADOW] = Biome.MEADOW; MAPA[WINDSWEPT_HILLS] = Biome.WINDSWEPT_HILLS; MAPA[GROVE] = Biome.GROVE;
        MAPA[SNOWY_SLOPES] = Biome.SNOWY_SLOPES; MAPA[JAGGED_PEAKS] = Biome.JAGGED_PEAKS; MAPA[FROZEN_PEAKS] = Biome.FROZEN_PEAKS;
        MAPA[STONY_PEAKS] = Biome.STONY_PEAKS; MAPA[CHERRY_GROVE] = Biome.CHERRY_GROVE;
        MAPA[OLD_GROWTH_SPRUCE_TAIGA] = Biome.OLD_GROWTH_SPRUCE_TAIGA; MAPA[FLOWER_FOREST] = Biome.FLOWER_FOREST;
        MAPA[RIVER] = Biome.RIVER; MAPA[FROZEN_RIVER] = Biome.FROZEN_RIVER; MAPA[BEACH] = Biome.BEACH;
        MAPA[SNOWY_BEACH] = Biome.SNOWY_BEACH; MAPA[WINDSWEPT_SAVANNA] = Biome.WINDSWEPT_SAVANNA;
        MAPA[ERODED_BADLANDS] = Biome.ERODED_BADLANDS; MAPA[WOODED_BADLANDS] = Biome.WOODED_BADLANDS;
        MAPA[STONY_SHORE] = Biome.STONY_SHORE; MAPA[LADOLOD] = Biome.SNOWY_PLAINS;
    }

    static List<Biome> wszystkie() {
        List<Biome> l = new ArrayList<>();
        for (Biome b : MAPA) if (!l.contains(b)) l.add(b);
        for (Biome b : new Biome[]{Biome.LUSH_CAVES, Biome.DRIPSTONE_CAVES, Biome.DEEP_DARK}) if (!l.contains(b)) l.add(b);
        return l;
    }

    static boolean ocean(int k) { return k >= 1 && k <= 9; }
    static boolean zimny(int k) {
        return k == SNOWY_TAIGA || k == SNOWY_PLAINS || k == ICE_SPIKES || k == SNOWY_SLOPES || k == FROZEN_PEAKS
                || k == JAGGED_PEAKS || k == GROVE || k == LADOLOD || k == FROZEN_OCEAN || k == DEEP_FROZEN_OCEAN || k == SNOWY_BEACH;
    }
    static boolean gory(int k) {
        return k == SNOWY_SLOPES || k == FROZEN_PEAKS || k == JAGGED_PEAKS || k == STONY_PEAKS || k == WINDSWEPT_HILLS || k == GROVE;
    }
    static boolean badlands(int k) { return k == BADLANDS || k == ERODED_BADLANDS || k == WOODED_BADLANDS; }
}
