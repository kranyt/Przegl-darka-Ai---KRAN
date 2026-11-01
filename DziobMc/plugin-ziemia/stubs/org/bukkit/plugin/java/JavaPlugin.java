package org.bukkit.plugin.java;
public abstract class JavaPlugin {
  public void onEnable() {}
  public void onDisable() {}
  public java.util.logging.Logger getLogger() { return null; }
  public org.bukkit.configuration.file.FileConfiguration getConfig() { return null; }
  public void saveDefaultConfig() {}
  public java.io.InputStream getResource(String filename) { return null; }
  public org.bukkit.generator.ChunkGenerator getDefaultWorldGenerator(String worldName, String id) { return null; }
}
