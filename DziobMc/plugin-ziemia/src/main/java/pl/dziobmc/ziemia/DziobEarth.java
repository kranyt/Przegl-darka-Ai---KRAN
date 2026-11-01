package pl.dziobmc.ziemia;

import org.bukkit.World;
import org.bukkit.WorldCreator;
import org.bukkit.generator.ChunkGenerator;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.IOException;
import java.util.logging.Level;

/** DziobEarth – mapa Ziemi dla serwera DziobMc (Earth SMP). */
public final class DziobEarth extends JavaPlugin {
    private GeneratorZiemi generator;

    private synchronized GeneratorZiemi generator() {
        if (generator == null) {
            long t = System.currentTimeMillis();
            Dane dane;
            try {
                dane = new Dane(this::getResource);
            } catch (IOException e) {
                throw new IllegalStateException("DziobEarth: nie udało się wczytać danych Ziemi", e);
            }
            int skala = Math.max(250, Math.min(20000, getConfig().getInt("skala", 2000)));
            generator = new GeneratorZiemi(dane, skala,
                    getConfig().getDouble("spawn_szerokosc", 52.23), getConfig().getDouble("spawn_dlugosc", 21.01));
            getLogger().info("Dane Ziemi wczytane w " + (System.currentTimeMillis() - t) + " ms. Skala 1:" + skala
                    + " -> swiat " + Math.round(360 * generator.bpd) + " x " + Math.round(180 * generator.bpd) + " kratek.");
        }
        return generator;
    }

    @Override
    public void onEnable() {
        saveDefaultConfig();
        try {
            GeneratorZiemi g = generator();
            if (getConfig().getBoolean("utworz_swiat", true)) {
                String nazwa = getConfig().getString("nazwa_swiata", "ziemia");
                getLogger().info("Tworze/wczytuje swiat '" + nazwa + "' (pierwsze uruchomienie moze potrwac minute)...");
                World w = new WorldCreator(nazwa).environment(World.Environment.NORMAL).generator(g).createWorld();
                if (w != null) {
                    int[] sp = g.spawnXYZ(w.getSeed());
                    w.setSpawnLocation(sp[0], sp[1], sp[2]);
                    getLogger().info("Swiat '" + nazwa + "' gotowy. Spawn: " + sp[0] + " " + sp[1] + " " + sp[2]);
                }
            }
        } catch (RuntimeException e) {
            getLogger().log(Level.SEVERE, "DziobEarth: blad podczas uruchamiania", e);
        }
    }

    @Override
    public ChunkGenerator getDefaultWorldGenerator(String worldName, String id) {
        return generator();
    }
}
