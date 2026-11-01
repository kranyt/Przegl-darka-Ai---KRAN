package org.bukkit;
public class WorldCreator {
  public WorldCreator(String name) {}
  public WorldCreator generator(org.bukkit.generator.ChunkGenerator generator) { return this; }
  public WorldCreator environment(World.Environment env) { return this; }
  public World createWorld() { return null; }
}
