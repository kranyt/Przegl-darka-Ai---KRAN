package pl.dziobmc.ziemia;

import java.util.Random;

/** Klasyczny szum Perlina 2D (improved noise) + fbm i szum grzbietowy. Bezstanowy po utworzeniu – bezpieczny wątkowo. */
final class Szum {
    private final int[] p = new int[512];

    Szum(long seed) {
        int[] perm = new int[256];
        for (int i = 0; i < 256; i++) perm[i] = i;
        Random r = new Random(seed);
        for (int i = 255; i > 0; i--) {
            int j = r.nextInt(i + 1);
            int t = perm[i]; perm[i] = perm[j]; perm[j] = t;
        }
        for (int i = 0; i < 512; i++) p[i] = perm[i & 255];
    }

    private static double fade(double t) { return t * t * t * (t * (t * 6 - 15) + 10); }
    private static double lerp(double t, double a, double b) { return a + t * (b - a); }
    private static double grad(int h, double x, double y) {
        switch (h & 7) {
            case 0: return x + y;   case 1: return -x + y;
            case 2: return x - y;   case 3: return -x - y;
            case 4: return x;       case 5: return -x;
            case 6: return y;       default: return -y;
        }
    }

    /** Wartość w przybliżeniu [-1, 1]. */
    double get(double x, double y) {
        int xi = (int) Math.floor(x), yi = (int) Math.floor(y);
        double xf = x - xi, yf = y - yi;
        int X = xi & 255, Y = yi & 255;
        double u = fade(xf), v = fade(yf);
        int aa = p[p[X] + Y], ab = p[p[X] + Y + 1], ba = p[p[X + 1] + Y], bb = p[p[X + 1] + Y + 1];
        double w = lerp(v, lerp(u, grad(aa, xf, yf), grad(ba, xf - 1, yf)),
                           lerp(u, grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1)));
        return w * 0.9;
    }

    double fbm(double x, double y, int oktawy) {
        double s = 0, a = 1, n = 0;
        for (int i = 0; i < oktawy; i++) {
            s += get(x, y) * a; n += a;
            x *= 2.03; y *= 2.03; a *= 0.5;
        }
        return s / n;
    }

    /** Szum grzbietowy (pasma górskie), wartości [0, 1]. */
    double grzbiety(double x, double y, int oktawy) {
        double s = 0, a = 1, n = 0;
        for (int i = 0; i < oktawy; i++) {
            double v = 1 - Math.abs(get(x, y));
            s += v * v * a; n += a;
            x *= 2.1; y *= 2.1; a *= 0.5;
        }
        return s / n;
    }
}
