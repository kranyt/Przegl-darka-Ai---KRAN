package pl.kran.panstwa.command;

import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabExecutor;
import org.bukkit.entity.Player;
import pl.kran.panstwa.PanstwaPlugin;
import pl.kran.panstwa.market.Share;
import pl.kran.panstwa.model.Nation;
import pl.kran.panstwa.util.Msg;

import java.util.ArrayList;
import java.util.List;

/** /akcje, /sprzedajakcje, /mojeakcje */
public class StockCommands implements TabExecutor {
    private final PanstwaPlugin plugin;

    public StockCommands(PanstwaPlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        if (!(sender instanceof Player p)) {
            sender.sendMessage("Tylko dla graczy.");
            return true;
        }
        switch (cmd.getName().toLowerCase()) {
            case "akcje" -> plugin.menus().openMarket(p, 0);
            case "sprzedajakcje" -> {
                if (args.length == 0) {
                    plugin.menus().openSell(p, 0);
                    return true;
                }
                Share s;
                try {
                    s = plugin.market().get(Integer.parseInt(args[0].replace("#", "")));
                } catch (NumberFormatException e) {
                    s = null;
                }
                if (s == null) {
                    Msg.send(p, "&cNie ma takiej akcji. Uzycie: /sprzedajakcje [id]");
                    return true;
                }
                int price = s.getPrice();
                String err = plugin.market().sellToServer(p, s);
                if (err != null) Msg.send(p, "&c" + err);
                else Msg.send(p, "&aSprzedales akcje &f#" + s.getId() + "&a serwerowi za &b" + price + " diamentow&a.");
            }
            case "mojeakcje" -> {
                List<String> notes = plugin.market().takeNotices(p.getUniqueId());
                if (!notes.isEmpty()) {
                    Msg.send(p, "&c&lWygaslo ci " + notes.size() + " akcji:");
                    for (String n : notes) Msg.raw(p, " &8- " + n);
                }
                List<Share> list = plugin.market().ownedBy(p.getUniqueId());
                if (list.isEmpty()) {
                    Msg.send(p, "&7Nie masz zadnych akcji. Kup je: &f/akcje");
                    return true;
                }
                Msg.send(p, "&6Twoje akcje (" + list.size() + "):");
                int total = 0;
                for (Share s : list) {
                    Nation n = plugin.nations().get(s.getIssuer());
                    total += s.getPrice();
                    Msg.raw(p, " &8- &eAkcja #" + s.getId() + " &7cena: &b" + s.getPrice() + " diamentow &7| "
                            + (n == null ? "" : "&6" + n.getName() + " &7| ") + "&f" + s.getX() + ", " + s.getZ()
                            + (s.isForSale() ? " &a(wystawiona na sprzedaz)" : ""));
                    Msg.raw(p, "    &7Trend: " + s.trendText());
                }
                Msg.raw(p, " &7Lacznie warte: &b" + total + " diamentow");
            }
            default -> { }
        }
        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command cmd, String label, String[] args) {
        List<String> out = new ArrayList<>();
        if (cmd.getName().equalsIgnoreCase("sprzedajakcje") && args.length == 1 && sender instanceof Player p) {
            for (Share s : plugin.market().ownedBy(p.getUniqueId())) if (!s.isForSale()) out.add(String.valueOf(s.getId()));
        }
        return out;
    }
}
