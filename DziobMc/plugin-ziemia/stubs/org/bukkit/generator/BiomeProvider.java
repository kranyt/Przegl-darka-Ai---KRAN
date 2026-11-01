package org.bukkit.generator;
public abstract class BiomeProvider {
  public abstract org.bukkit.block.Biome getBiome(WorldInfo worldInfo, int x, int y, int z);
  public abstract java.util.List<org.bukkit.block.Biome> getBiomes(WorldInfo worldInfo);
}
