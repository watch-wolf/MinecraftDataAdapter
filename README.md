# MinecraftDataAdapter
Adapting [minecraft-data](https://github.com/PrismarineJS/minecraft-data) (the library used by Mineflayer) into WatchWolf.

### The items

WatchWolf uses the Spigot Material enum found in the latest version, while Mineflayer uses some unconsistant (changes over versions) item names. *items-adapter* will specify the bidirectional conversion between WatchWolf and Mineflayer, for each Minecraft version.