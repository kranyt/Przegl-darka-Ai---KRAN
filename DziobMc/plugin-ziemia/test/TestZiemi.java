package pl.dziobmc.ziemia;

import org.bukkit.Material;
import org.bukkit.generator.ChunkGenerator;
import org.bukkit.generator.WorldInfo;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;

/**
 * Test generatora poza serwerem (na zaślepkach API).
 *   mapa  <plik.png> <skala> <lonMin> <lonMax> <latMin> <latMax> <szer_px>
 *   scena <plik.json> <skala> <lat> <lon> <promien_kratek>
 */
public class TestZiemi {
    static final long SEED = 20261101L;

    public static void main(String[] a) throws Exception {
        long t = System.currentTimeMillis();
        Dane d = new Dane(n -> new FileInputStream("src/main/resources/" + n));
        System.out.println("dane: " + (System.currentTimeMillis() - t) + " ms");
        int skala = Integer.parseInt(a[2]);
        GeneratorZiemi g = new GeneratorZiemi(d, skala, 52.23, 21.01);
        if (a[0].equals("kol")) {
            double lat = Double.parseDouble(a[3]), lon = Double.parseDouble(a[4]);
            int cx0 = (int) Math.round(lon * g.bpd), cz0 = (int) Math.round(-lat * g.bpd);
            int dx = Integer.parseInt(a[5]), dz = Integer.parseInt(a[6]);
            for (int i = -2; i <= 3; i++) {
                int x = cx0 + dx + i, z = cz0 + dz;
                double la = -z / g.bpd, lo = x / g.bpd;
                GeneratorZiemi.Kol k = g.kolumna(SEED, x, z);
                System.out.printf("x=%d z=%d lat=%.4f lon=%.4f lad=%.3f jez=%.3f rz=%.3f e=%.0f typ=%d h=%d woda=%d kl=%d%n", x, z, la, lo,
                        d.maska(d.lad, lo, la), d.maska(d.jeziora, lo, la), d.maska(d.rzeki, lo, la), d.wysokosc(lo, la), k.typ, k.h, k.woda, k.klasa);
            }
            return;
        }
        if (a[0].equals("mapa")) mapa(g, a);
        else scena(g, a);
    }

    // ------------------------------------------------------------------ mapa z góry
    static int kolor(GeneratorZiemi.Kol k) {
        int kl = k.klasa;
        int[] c;
        if (k.typ == GeneratorZiemi.OCEAN) {
            double gl = Math.min(1, (62 - k.h) / 40.0);
            c = new int[]{(int) (60 - 40 * gl), (int) (130 - 80 * gl), (int) (225 - 90 * gl)};
        } else if (k.typ != GeneratorZiemi.LAD) c = new int[]{70, 130, 230};
        else {
            switch (kl) {
                case Biomy.DESERT: c = new int[]{219, 207, 163}; break;
                case Biomy.BEACH: case Biomy.SNOWY_BEACH: c = new int[]{230, 220, 170}; break;
                case Biomy.BADLANDS: case Biomy.ERODED_BADLANDS: case Biomy.WOODED_BADLANDS: c = new int[]{190, 100, 50}; break;
                case Biomy.SAVANNA: case Biomy.SAVANNA_PLATEAU: case Biomy.WINDSWEPT_SAVANNA: c = new int[]{170, 165, 80}; break;
                case Biomy.JUNGLE: case Biomy.BAMBOO_JUNGLE: case Biomy.SPARSE_JUNGLE: c = new int[]{40, 120, 20}; break;
                case Biomy.FOREST: case Biomy.FLOWER_FOREST: case Biomy.BIRCH_FOREST: c = new int[]{60, 125, 45}; break;
                case Biomy.DARK_FOREST: c = new int[]{35, 85, 30}; break;
                case Biomy.TAIGA: case Biomy.OLD_GROWTH_SPRUCE_TAIGA: c = new int[]{50, 95, 70}; break;
                case Biomy.CHERRY_GROVE: c = new int[]{235, 160, 200}; break;
                case Biomy.SNOWY_PLAINS: case Biomy.SNOWY_TAIGA: case Biomy.SNOWY_SLOPES: case Biomy.LADOLOD:
                case Biomy.FROZEN_PEAKS: case Biomy.JAGGED_PEAKS: case Biomy.GROVE: c = new int[]{235, 240, 245}; break;
                case Biomy.STONY_PEAKS: case Biomy.STONY_SHORE: case Biomy.WINDSWEPT_HILLS: c = new int[]{130, 130, 130}; break;
                case Biomy.MANGROVE_SWAMP: case Biomy.SWAMP: c = new int[]{70, 90, 45}; break;
                default: c = new int[]{110, 175, 70};
            }
            double sh = 0.85 + Math.min(0.4, (k.h - 64) / 300.0);
            c = new int[]{(int) Math.min(255, c[0] * sh), (int) Math.min(255, c[1] * sh), (int) Math.min(255, c[2] * sh)};
        }
        return (c[0] << 16) | (c[1] << 8) | c[2];
    }

    static void mapa(GeneratorZiemi g, String[] a) throws IOException {
        double lon0 = Double.parseDouble(a[3]), lon1 = Double.parseDouble(a[4]);
        double lat0 = Double.parseDouble(a[5]), lat1 = Double.parseDouble(a[6]);
        int W = Integer.parseInt(a[7]);
        int H = (int) Math.round(W * (lat1 - lat0) / (lon1 - lon0));
        BufferedImage img = new BufferedImage(W, H, BufferedImage.TYPE_INT_RGB);
        int[] prev = new int[W];
        for (int py = 0; py < H; py++) {
            for (int px = 0; px < W; px++) {
                double lon = lon0 + (lon1 - lon0) * (px + 0.5) / W, lat = lat1 - (lat1 - lat0) * (py + 0.5) / H;
                int x = (int) Math.round(lon * g.bpd), z = (int) Math.round(-lat * g.bpd);
                GeneratorZiemi.Kol k = g.kolumna(SEED, x, z);
                int c = kolor(k);
                if (k.typ == GeneratorZiemi.LAD && py > 0) {          // cieniowanie zboczy
                    int dh = k.h - prev[px];
                    double f = Math.max(0.6, Math.min(1.4, 1 + dh * 0.06));
                    c = (Math.min(255, (int) (((c >> 16) & 255) * f)) << 16) | (Math.min(255, (int) (((c >> 8) & 255) * f)) << 8) | Math.min(255, (int) ((c & 255) * f));
                }
                prev[px] = k.h;
                img.setRGB(px, py, c);
            }
        }
        ImageIO.write(img, "png", new java.io.File(a[1]));
        System.out.println("mapa " + W + "x" + H + " -> " + a[1]);
    }

    // ------------------------------------------------------------------ scena 3D (bloki przy powierzchni)
    static final class Info implements WorldInfo {
        public String getName() { return "ziemia"; }
        public long getSeed() { return SEED; }
        public int getMinHeight() { return -64; }
        public int getMaxHeight() { return 320; }
    }

    static final class Kawalek implements ChunkGenerator.ChunkData {
        final Material[] b = new Material[16 * 16 * 384];
        public int getMinHeight() { return -64; }
        public int getMaxHeight() { return 320; }
        int i(int x, int y, int z) { return ((y + 64) * 16 + z) * 16 + x; }
        public void setBlock(int x, int y, int z, Material m) { if (y >= -64 && y < 320) b[i(x, y, z)] = m; }
        public void setRegion(int x0, int y0, int z0, int x1, int y1, int z1, Material m) {
            for (int y = Math.max(-64, y0); y < Math.min(320, y1); y++) for (int z = z0; z < z1; z++) for (int x = x0; x < x1; x++) b[i(x, y, z)] = m;
        }
        public Material getType(int x, int y, int z) { Material m = b[i(x, y, z)]; return m == null ? Material.AIR : m; }
    }

    static void scena(GeneratorZiemi g, String[] a) throws IOException {
        double lat = Double.parseDouble(a[3]), lon = Double.parseDouble(a[4]);
        int R = Integer.parseInt(a[5]);
        int cx0 = (int) Math.round(lon * g.bpd), cz0 = (int) Math.round(-lat * g.bpd);
        Map<Long, Material> sw = new HashMap<>();
        Map<Long, Integer> topy = new HashMap<>();
        Info info = new Info();
        Random rnd = new Random(1);
        for (int cx = (cx0 - R) >> 4; cx <= (cx0 + R) >> 4; cx++) {
            for (int cz = (cz0 - R) >> 4; cz <= (cz0 + R) >> 4; cz++) {
                Kawalek k = new Kawalek();
                g.generateNoise(info, rnd, cx, cz, k);
                for (int lx = 0; lx < 16; lx++) for (int lz = 0; lz < 16; lz++) {
                    int x = (cx << 4) + lx, z = (cz << 4) + lz;
                    if (Math.abs(x - cx0) > R || Math.abs(z - cz0) > R) continue;
                    GeneratorZiemi.Kol kol = g.kolumna(SEED, x, z);
                    topy.put(klucz(x, 0, z), kol.h);
                    int mn = kol.h;
                    for (int[] o : new int[][]{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}) mn = Math.min(mn, g.kolumna(SEED, x + o[0], z + o[1]).h);
                    for (int y = Math.max(-64, mn - 2); y <= Math.max(kol.h, kol.woda); y++) {
                        Material m = k.getType(lx, y, lz);
                        if (m == Material.WATER && y != kol.woda) continue;
                        if (m != Material.AIR) sw.put(klucz(x, y, z), m);
                    }
                }
            }
        }
        // przybliżone drzewa wg biomu (w grze stawia je vanilla)
        Random r = new Random(7);
        for (int x = cx0 - R + 3; x <= cx0 + R - 3; x++) for (int z = cz0 - R + 3; z <= cz0 + R - 3; z++) {
            GeneratorZiemi.Kol kol = g.kolumna(SEED, x, z);
            if (kol.typ != GeneratorZiemi.LAD) continue;
            Material top = sw.get(klucz(x, kol.h, z));
            if (top != Material.GRASS_BLOCK && top != Material.PODZOL) continue;
            double gest = gestosc(kol.klasa);
            if (r.nextDouble() > gest) continue;
            drzewo(sw, x, kol.h + 1, z, kol.klasa, r);
        }
        try (PrintWriter w = new PrintWriter(new FileWriter(a[1]))) {
            List<String> typy = new ArrayList<>();
            Map<String, Integer> idx = new HashMap<>();
            StringBuilder bl = new StringBuilder();
            boolean first = true;
            for (Map.Entry<Long, Material> e : sw.entrySet()) {
                String n = e.getValue().name().toLowerCase(Locale.ROOT);
                Integer id = idx.get(n);
                if (id == null) { id = typy.size(); typy.add(n); idx.put(n, id); }
                long kk = e.getKey();
                int x = (int) (kk >> 40) - (1 << 20), y = (int) ((kk >> 20) & 0xfffff) - 1000, z = (int) (kk & 0xfffff) - (1 << 19);
                if (!first) bl.append(',');
                first = false;
                bl.append('[').append(x - cx0).append(',').append(y).append(',').append(z - cz0).append(',').append(id).append(']');
            }
            w.print("{\"typy\":[");
            for (int i = 0; i < typy.size(); i++) w.print((i > 0 ? "," : "") + "\"" + typy.get(i) + "\"");
            int hs = g.kolumna(SEED, cx0, cz0).h;
            w.print("],\"bloki\":[" + bl + "],\"encje\":[],\"srodek\":[0," + hs + ",0]}");
        }
        System.out.println("scena: " + sw.size() + " bloków, wysokość w środku " + g.kolumna(SEED, cx0, cz0).h + " -> " + a[1]);
    }

    static long klucz(int x, int y, int z) {
        return ((long) (x + (1 << 20)) << 40) | ((long) (y + 1000) << 20) | (long) (z + (1 << 19));
    }

    static double gestosc(int kl) {
        switch (kl) {
            case Biomy.JUNGLE: case Biomy.BAMBOO_JUNGLE: case Biomy.DARK_FOREST: return 0.09;
            case Biomy.FOREST: case Biomy.BIRCH_FOREST: case Biomy.FLOWER_FOREST: case Biomy.TAIGA:
            case Biomy.OLD_GROWTH_SPRUCE_TAIGA: case Biomy.SNOWY_TAIGA: case Biomy.GROVE: case Biomy.CHERRY_GROVE: return 0.05;
            case Biomy.SPARSE_JUNGLE: case Biomy.SWAMP: case Biomy.MANGROVE_SWAMP: return 0.025;
            case Biomy.PLAINS: case Biomy.SUNFLOWER_PLAINS: case Biomy.MEADOW: case Biomy.WINDSWEPT_HILLS: return 0.004;
            case Biomy.SAVANNA: case Biomy.SAVANNA_PLATEAU: case Biomy.WINDSWEPT_SAVANNA: case Biomy.WOODED_BADLANDS: return 0.006;
            default: return 0;
        }
    }

    static void drzewo(Map<Long, Material> sw, int x, int y, int z, int kl, Random r) {
        String pien = "OAK_LOG", lisc = "OAK_LEAVES";
        boolean swierk = kl == Biomy.TAIGA || kl == Biomy.OLD_GROWTH_SPRUCE_TAIGA || kl == Biomy.SNOWY_TAIGA || kl == Biomy.GROVE;
        if (swierk) { pien = "SPRUCE_LOG"; lisc = "SPRUCE_LEAVES"; }
        else if (kl == Biomy.BIRCH_FOREST) { pien = "BIRCH_LOG"; lisc = "BIRCH_LEAVES"; }
        else if (kl == Biomy.JUNGLE || kl == Biomy.BAMBOO_JUNGLE || kl == Biomy.SPARSE_JUNGLE) { pien = "JUNGLE_LOG"; lisc = "JUNGLE_LEAVES"; }
        else if (kl == Biomy.SAVANNA || kl == Biomy.SAVANNA_PLATEAU || kl == Biomy.WINDSWEPT_SAVANNA) { pien = "ACACIA_LOG"; lisc = "ACACIA_LEAVES"; }
        else if (kl == Biomy.CHERRY_GROVE) { pien = "CHERRY_LOG"; lisc = "CHERRY_LEAVES"; }
        else if (kl == Biomy.DARK_FOREST) { pien = "DARK_OAK_LOG"; lisc = "DARK_OAK_LEAVES"; }
        else if (kl == Biomy.MANGROVE_SWAMP) { pien = "MANGROVE_LOG"; lisc = "MANGROVE_LEAVES"; }
        int h = swierk ? 7 + r.nextInt(4) : (kl == Biomy.JUNGLE ? 9 + r.nextInt(6) : 5 + r.nextInt(2));
        Material mp = Material.valueOf(pienM(pien)), ml = Material.valueOf(pienM(lisc));
        for (int i = 0; i < h; i++) sw.put(klucz(x, y + i, z), mp);
        if (swierk) {
            for (int i = 2; i <= h; i++) {
                int rr = Math.max(0, (h - i) / 3 + ((i % 2 == 0) ? 1 : 0));
                for (int dx = -rr; dx <= rr; dx++) for (int dz = -rr; dz <= rr; dz++)
                    if (Math.abs(dx) + Math.abs(dz) <= rr + 1) sw.putIfAbsent(klucz(x + dx, y + i, z + dz), ml);
            }
            sw.put(klucz(x, y + h, z), ml);
        } else {
            int rr = kl == Biomy.JUNGLE ? 3 : 2;
            for (int dy = -2; dy <= 1; dy++) for (int dx = -rr; dx <= rr; dx++) for (int dz = -rr; dz <= rr; dz++) {
                if (dx * dx + dz * dz + dy * dy * 2 <= rr * rr + 2 && r.nextDouble() > 0.08)
                    sw.putIfAbsent(klucz(x + dx, y + h + dy, z + dz), ml);
            }
        }
    }

    // Materiały drzew nie istnieją w zaślepce – mapujemy na nazwy, które tam są (tylko w teście)
    static String pienM(String n) { return n; }
}
