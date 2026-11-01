package org.bukkit;
public interface World extends org.bukkit.generator.WorldInfo {
  boolean setSpawnLocation(int x, int y, int z);
  enum Environment { NORMAL, NETHER, THE_END, CUSTOM }
}
