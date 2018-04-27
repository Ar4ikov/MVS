package ru.ar4ikov;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.MySQLConnection;
import net.md_5.bungee.api.ChatColor;
import net.minecraft.server.v1_12_R1.PlayerConnection;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerPreLoginEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.server.ServerListPingEvent;
import org.bukkit.material.Button;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.java.JavaPlugin;

import javax.activation.DataSource;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import java.io.IOException;
import java.sql.*;
import java.util.HashMap;
import java.util.Objects;
import java.util.Random;
import java.util.function.Supplier;

public class MVSAuth extends JavaPlugin implements Listener {

    /**
     *
     * Initial Connection by using params under
     *
     */
    private Random rnd = new Random();

    //Host
    private static final String HOST = "127.0.0.1";

    // Database name
    private static final String DATABASE = "Auth";

    // Database user login
    private static final String USERNAME = "root";

    // Database password
    private static final String PASSWORD = "password";


    private static String getPluginPrefix() {
        return ConsoleColors.CONSOLE_CYAN + " [MVS-Auth] " + ConsoleColors.CONSOLE_WHITE;
    }
    private static Plugin instance;
    private static Plugin getPluginInstance() {
        return instance;
    }

    // Technical variables
    private Connection connection = null;
    private Statement query = null;

    public void onEnable() {
        instance = this;
        Bukkit.getServer().getPluginManager().registerEvents((Listener) getPluginInstance(),this);

        // Simple connecting to MySql database
        String url = "jdbc:mysql://" + HOST + ":3306/" + DATABASE + "?autoReconnect=true&useSSL=false";

        Bukkit.getLogger().info(getPluginPrefix() + "Connection to Database...");

        // I hate try/catch
        try {
            connection = (Connection) DriverManager.getConnection(url, USERNAME, PASSWORD);
            Bukkit.getLogger().info(getPluginPrefix() + "Connected to " + url);

            query = connection.createStatement();

            ResultSet result = query.executeQuery("SELECT * FROM `auth`");
            if (!result.next()) {
                query.execute("CREATE TABLE IF NOT EXISTS `auth` (" +
                        "  `id` INT AUTO_INCREMENT," +
                        "  `uuid` TEXT NOT NULL," +
                        "  `access_token` TEXT NOT NULL," +
                        "  `ip` TEXT NOT NULL," +
                        "  `nickname` TEXT NOT NULL," +
                        "  `created_date` INT NOT NULL," +
                        "  PRIMARY KEY (`id`));");
            }
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }

    }

    public void onDisable() {
        try {
            connection.close();
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    // Simple token generation by using matrix of 62 symbols
    public String generateAccessToken() {
        String access_token = "";
        String[] matrix = {
                "A", "B", "C", "D", "E",
                "F", "G", "H", "I", "J",
                "K", "L", "M", "N", "O",
                "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y",
                "Z", "a", "b", "c", "d",
                "e", "f", "g", "h", "i",
                "j", "k", "l", "m", "n",
                "o", "p", "q", "r", "s",
                "t", "u", "v", "w", "x",
                "y", "z", "0", "1", "2",
                "3", "4", "5", "6", "7",
                "8", "9"
        };

        for (int i = 0; i < 32; i++) {
            access_token = access_token + matrix[rnd.nextInt(matrix.length)];
        }

        return access_token;
    }

    @EventHandler
    public void onJoin(AsyncPlayerPreLoginEvent event) throws SQLException {
        String sql = "SELECT `access_token` FROM `auth` WHERE `uuid` = '" + event.getUniqueId().toString().replace("-", "") + "'";
        Bukkit.getLogger().info(sql);
        ResultSet result = query.executeQuery(sql);

        String ip = event.getAddress().getHostAddress();
        String uuid = event.getUniqueId().toString().replace("-", "");
        long unixTime = System.currentTimeMillis() / 1000L;
        String nickname = event.getName();
        String token = generateAccessToken();

        if (!result.next()) {
            query.executeUpdate("INSERT INTO `auth` (uuid, access_token, ip, nickname, created_date) VALUES ('" + uuid + "', '" + token + "', '" +  ip + "', '" + nickname + "', '" + unixTime + "')");
            event.disallow(AsyncPlayerPreLoginEvent.Result.KICK_OTHER,"§3Minecraft Verification System\n\n§fYour token is - §e" + token);
        } else {
            query.executeUpdate("UPDATE `auth` SET `access_token` = '" + token + "', `nickname` = '" + nickname + "' WHERE `uuid` = '" + uuid + "'");
            result = query.executeQuery("SELECT `access_token` FROM `auth` WHERE `uuid` = '" + event.getUniqueId().toString().replace("-", "") + "'");
            result.next();
            event.disallow(AsyncPlayerPreLoginEvent.Result.KICK_OTHER, "§3Minecraft Verification System\n\n§fYour token is - §e" + result.getString("access_token"));
        }
    }
    @EventHandler
    public void onConnect(ServerListPingEvent event) {
        event.setMaxPlayers(-1);
        event.setMotd("                   §9§lM§3§lV§b§lS §fAuth Server §61.12\n" +
                      "        §fCheck https://github.com/Ar4ikov/MVS");
    }
}