package pl.dziobmc.ziemia;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.zip.GZIPInputStream;

/** Dane Ziemi: maska lądu, jezior i rzek (2 km), wysokości i biomy (~7,4 km). Tylko do odczytu. */
final class Dane {
    final int lw, lh;          // siatka 2 km
    final byte[] lad, jeziora, rzeki;
    final int ww, wh;          // siatka wysokości/biomów
    final short[] wys;
    final byte[] biom;

    interface Zrodlo { InputStream otworz(String nazwa) throws IOException; }

    Dane(Zrodlo z) throws IOException {
        int[] wym = new int[2];
        lad = bity(z.otworz("ziemia/lad.bin.gz"), wym);
        lw = wym[0]; lh = wym[1];
        jeziora = bity(z.otworz("ziemia/jeziora.bin.gz"), wym);
        rzeki = bity(z.otworz("ziemia/rzeki.bin.gz"), wym);
        try (DataInputStream in = new DataInputStream(new GZIPInputStream(z.otworz("ziemia/wys.bin.gz"), 1 << 16))) {
            ww = in.readInt(); wh = in.readInt();
            byte[] raw = new byte[ww * wh * 2];
            in.readFully(raw);
            wys = new short[ww * wh];
            for (int i = 0; i < wys.length; i++) wys[i] = (short) (((raw[2 * i] & 0xff) << 8) | (raw[2 * i + 1] & 0xff));
        }
        try (DataInputStream in = new DataInputStream(new GZIPInputStream(z.otworz("ziemia/biom.bin.gz"), 1 << 16))) {
            in.readInt(); in.readInt();
            biom = new byte[ww * wh];
            in.readFully(biom);
        }
    }

    private static byte[] bity(InputStream is, int[] wym) throws IOException {
        if (is == null) throw new IOException("Brak pliku danych Ziemi w pluginie");
        try (DataInputStream in = new DataInputStream(new GZIPInputStream(is, 1 << 16))) {
            wym[0] = in.readInt(); wym[1] = in.readInt();
            byte[] b = new byte[(wym[0] / 8) * wym[1]];
            in.readFully(b);
            return b;
        }
    }

    private int bit(byte[] b, int x, int y) {
        x = Math.floorMod(x, lw);
        if (y < 0) y = 0; else if (y >= lh) y = lh - 1;
        return (b[y * (lw >> 3) + (x >> 3)] >> (7 - (x & 7))) & 1;
    }

    /** Dwuliniowa interpolacja maski bitowej (siatka 2 km) – wynik 0..1. */
    double maska(byte[] b, double lon, double lat) {
        double px = (lon + 180.0) / 360.0 * lw - 0.5, py = (90.0 - lat) / 180.0 * lh - 0.5;
        int x0 = (int) Math.floor(px), y0 = (int) Math.floor(py);
        double fx = px - x0, fy = py - y0;
        double a = bit(b, x0, y0), c = bit(b, x0 + 1, y0), d = bit(b, x0, y0 + 1), e = bit(b, x0 + 1, y0 + 1);
        return (a * (1 - fx) + c * fx) * (1 - fy) + (d * (1 - fx) + e * fx) * fy;
    }

    private int w(int x, int y) {
        x = Math.floorMod(x, ww);
        if (y < 0) y = 0; else if (y >= wh) y = wh - 1;
        return wys[y * ww + x];
    }

    /** Wysokość/głębokość w metrach (dwuliniowo). */
    double wysokosc(double lon, double lat) {
        double px = (lon + 180.0) / 360.0 * ww - 0.5, py = (90.0 - lat) / 180.0 * wh - 0.5;
        int x0 = (int) Math.floor(px), y0 = (int) Math.floor(py);
        double fx = px - x0, fy = py - y0;
        return (w(x0, y0) * (1 - fx) + w(x0 + 1, y0) * fx) * (1 - fy) + (w(x0, y0 + 1) * (1 - fx) + w(x0 + 1, y0 + 1) * fx) * fy;
    }

    /** Klasa biomu (najbliższy piksel). */
    int biom(double lon, double lat) {
        int x = Math.floorMod((int) Math.floor((lon + 180.0) / 360.0 * ww), ww);
        int y = (int) Math.floor((90.0 - lat) / 180.0 * wh);
        if (y < 0) y = 0; else if (y >= wh) y = wh - 1;
        return biom[y * ww + x] & 0xff;
    }
}
