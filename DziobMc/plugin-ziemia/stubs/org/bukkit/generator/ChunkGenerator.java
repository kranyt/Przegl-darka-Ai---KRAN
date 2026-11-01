package org.bukkit.generator;
import java.util.Random;
public abstract class ChunkGenerator {
  public void generateNoise(WorldInfo worldInfo, Random random, int chunkX, int chunkZ, ChunkData chunkData) {}
  public void generateSurface(WorldInfo worldInfo, Random random, int chunkX, int chunkZ, ChunkData chunkData) {}
  public void generateBedrock(WorldInfo worldInfo, Random random, int chunkX, int chunkZ, ChunkData chunkData) {}
  public void generateCaves(WorldInfo worldInfo, Random random, int chunkX, int chunkZ, ChunkData chunkData) {}
  public BiomeProvider getDefaultBiomeProvider(WorldInfo worldInfo) { return null; }
  public int getBaseHeight(WorldInfo worldInfo, Random random, int x, int z, org.bukkit.HeightMap heightMap) { return 0; }
  public org.bukkit.Location getFixedSpawnLocation(org.bukkit.World world, Random random) { return null; }
  public boolean shouldGenerateNoise() { return false; }
  public boolean shouldGenerateSurface() { return false; }
  public boolean shouldGenerateCaves() { return false; }
  public boolean shouldGenerateDecorations() { return false; }
  public boolean shouldGenerateMobs() { return false; }
  public boolean shouldGenerateStructures() { return false; }
  public interface ChunkData {
    int getMinHeight(); int getMaxHeight();
    void setBlock(int x, int y, int z, org.bukkit.Material material);
    void setRegion(int xMin, int yMin, int zMin, int xMax, int yMax, int zMax, org.bukkit.Material material);
    org.bukkit.Material getType(int x, int y, int z);
  }
}
