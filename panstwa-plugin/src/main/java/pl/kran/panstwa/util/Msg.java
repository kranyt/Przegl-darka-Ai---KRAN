package pl.kran.panstwa.util;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.TextDecoration;
import net.kyori.adventure.text.serializer.legacy.LegacyComponentSerializer;
import org.bukkit.command.CommandSender;

/** Wiadomosci z kolorami w formacie '&'. */
public final class Msg {
    public static final String PREFIX = "&8[&6Państwa&8] &7";
    private static final LegacyComponentSerializer SER = LegacyComponentSerializer.legacyAmpersand();

    private Msg() {}

    public static Component c(String text) {
        return SER.deserialize(text);
    }

    /** Komponent bez kursywy (do nazw i lore przedmiotow). */
    public static Component item(String text) {
        return SER.deserialize(text).decoration(TextDecoration.ITALIC, false);
    }

    public static void send(CommandSender to, String text) {
        to.sendMessage(c(PREFIX + text));
    }

    public static void raw(CommandSender to, String text) {
        to.sendMessage(c(text));
    }
}
