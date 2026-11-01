package org.bukkit.configuration.file;
public abstract class FileConfiguration {
  public int getInt(String path, int def) { return def; }
  public double getDouble(String path, double def) { return def; }
  public String getString(String path, String def) { return def; }
  public boolean getBoolean(String path, boolean def) { return def; }
}
