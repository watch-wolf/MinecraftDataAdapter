# MinecraftDataAdapter
Adapting minecraft-data (the library used by Mineflayer) into WatchWolf.

### The items

WatchWolf uses the Spigot Material enum found in the latest version, while Mineflayer uses some unconsistant (changes over versions) item names. *items-adapter* will specify the bidirectional conversion between WW and Mineflayer, for each MC version.