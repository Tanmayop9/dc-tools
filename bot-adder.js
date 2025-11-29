var readline = require("readline");
var fetch = require("node-fetch");
var https = require("https");

// HTTPS agent for API calls - consistent with existing tools
var agent = new https.Agent({
    keepAlive: true,
    maxSockets: 500,              // Maximum sockets for ultra speed (consistent with other tools)
    maxFreeSockets: 500,
    keepAliveMsecs: 120000,       // 2 minute keep-alive
    timeout: 15000,               // Shorter timeout for faster failures
    scheduling: "lifo"            // Last-in-first-out for hot connections
});

var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function ask(q) {
    return new Promise(function(resolve) {
        rl.question(q, resolve);
    });
}

// Permission flags for Discord bots
var PERMISSIONS = {
    ADMINISTRATOR: 8,
    MANAGE_CHANNELS: 16,
    MANAGE_GUILD: 32,
    MANAGE_MESSAGES: 8192,
    SEND_MESSAGES: 2048,
    READ_MESSAGES: 1024,
    MANAGE_ROLES: 268435456,
    KICK_MEMBERS: 2,
    BAN_MEMBERS: 4,
    VIEW_AUDIT_LOG: 128
};

// Permission presets for common use cases
var PERMISSION_PRESETS = {
    ADMINISTRATOR: PERMISSIONS.ADMINISTRATOR,  // Full access (8)
    MODERATOR: 268454912,                       // Manage messages + roles
    BASIC: 3072                                 // Read + send messages
};

// Pre-normalize token once for all requests
var normalizedToken = null;

function normalizeToken(token) {
    if (!normalizedToken) {
        var authToken = token.trim();
        if (!authToken.startsWith("Bot ")) {
            authToken = "Bot " + authToken;
        }
        normalizedToken = authToken;
    }
    return normalizedToken;
}

// Get bot information
async function getBotInfo(token) {
    var authToken = normalizeToken(token);

    try {
        var res = await fetch(
            "https://discord.com/api/v10/users/@me",
            {
                method: "GET",
                agent: agent,
                headers: {
                    "Authorization": authToken,
                    "Content-Type": "application/json"
                }
            }
        );

        if (res.status === 200) {
            return await res.json();
        }

        try {
            var errorData = await res.json();
            console.log("❌ Error fetching bot info:", errorData.message || "Unknown error");
        } catch (e) {
            console.log("❌ Error fetching bot info: HTTP " + res.status);
        }
        return null;
    } catch (e) {
        console.log("❌ Network error:", e.message);
        return null;
    }
}

// Get application info
async function getApplicationInfo(token) {
    var authToken = normalizeToken(token);

    try {
        var res = await fetch(
            "https://discord.com/api/v10/oauth2/applications/@me",
            {
                method: "GET",
                agent: agent,
                headers: {
                    "Authorization": authToken,
                    "Content-Type": "application/json"
                }
            }
        );

        if (res.status === 200) {
            return await res.json();
        }

        try {
            var errorData = await res.json();
            console.log("❌ Error fetching application info:", errorData.message || "Unknown error");
        } catch (e) {
            console.log("❌ Error fetching application info: HTTP " + res.status);
        }
        return null;
    } catch (e) {
        console.log("❌ Network error:", e.message);
        return null;
    }
}

// Add bot to guild using OAuth2 authorization
// Note: This requires the guild owner or admin to have authorized the bot
async function addBotToGuild(token, guildId, permissions) {
    try {
        // First get the application info to get the client ID
        var appInfo = await getApplicationInfo(token);
        if (!appInfo) {
            console.log("❌ Could not get application info");
            return null;
        }

        var clientId = appInfo.id;
        console.log("\n📋 Application ID: " + clientId);
        console.log("📋 Application Name: " + appInfo.name);

        // Generate the OAuth2 authorization URL
        var permInt = parseInt(permissions) || PERMISSIONS.ADMINISTRATOR;
        var oauthUrl = "https://discord.com/api/oauth2/authorize?" +
            "client_id=" + clientId +
            "&scope=bot%20applications.commands" +
            "&permissions=" + permInt +
            "&guild_id=" + guildId;

        console.log("\n🔗 OAuth2 Authorization URL:");
        console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        console.log(oauthUrl);
        console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

        return {
            success: true,
            clientId: clientId,
            appName: appInfo.name,
            oauthUrl: oauthUrl,
            guildId: guildId,
            permissions: permInt
        };
    } catch (e) {
        console.log("❌ Error:", e.message);
        return null;
    }
}

// Check if bot is in a guild
async function checkBotInGuild(token, guildId) {
    var authToken = normalizeToken(token);

    try {
        var res = await fetch(
            "https://discord.com/api/v10/guilds/" + guildId,
            {
                method: "GET",
                agent: agent,
                headers: {
                    "Authorization": authToken,
                    "Content-Type": "application/json"
                }
            }
        );

        if (res.status === 200) {
            return await res.json();
        }

        if (res.status === 403) {
            return { error: "Bot is not in this guild or lacks permissions" };
        }

        return null;
    } catch (e) {
        return null;
    }
}

// Get all guilds the bot is in
async function getBotGuilds(token) {
    var authToken = normalizeToken(token);

    try {
        var res = await fetch(
            "https://discord.com/api/v10/users/@me/guilds",
            {
                method: "GET",
                agent: agent,
                headers: {
                    "Authorization": authToken,
                    "Content-Type": "application/json"
                }
            }
        );

        if (res.status === 200) {
            return await res.json();
        }

        try {
            var errorData = await res.json();
            console.log("❌ Error fetching guilds:", errorData.message || "Unknown error");
        } catch (e) {
            console.log("❌ Error fetching guilds: HTTP " + res.status);
        }
        return null;
    } catch (e) {
        console.log("❌ Network error:", e.message);
        return null;
    }
}

async function main() {
    console.log("\n🤖 DISCORD BOT ADDER - API Integration Tool 🤖\n");
    console.log("📡 Add bots to servers using Discord API!");
    console.log("🔐 For educational purposes only\n");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    var BOT_TOKEN = await ask("Enter bot token: ");

    console.log("\n📡 Fetching bot information...\n");

    var botInfo = await getBotInfo(BOT_TOKEN);

    if (!botInfo) {
        console.log("❌ Invalid bot token or could not fetch bot info.\n");
        rl.close();
        process.exit(1);
    }

    console.log("✅ Bot Info:");
    console.log("   Username: " + botInfo.username + "#" + (botInfo.discriminator || "0"));
    console.log("   ID: " + botInfo.id);
    console.log("   Bot: " + (botInfo.bot ? "Yes" : "No"));

    // Get current guilds
    console.log("\n📡 Fetching bot's current guilds...\n");
    var guilds = await getBotGuilds(BOT_TOKEN);

    if (guilds && guilds.length > 0) {
        console.log("📊 Bot is currently in " + guilds.length + " guild(s):");
        guilds.slice(0, 10).forEach(function(g, idx) {
            console.log("   " + (idx + 1) + ". " + g.name + " (ID: " + g.id + ")");
        });
        if (guilds.length > 10) {
            console.log("   ... and " + (guilds.length - 10) + " more guilds");
        }
    } else {
        console.log("📊 Bot is not in any guilds yet.");
    }

    console.log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log("📝 Available Actions:");
    console.log("   1. Generate OAuth2 invite link for a specific guild");
    console.log("   2. Check if bot is in a specific guild");
    console.log("   3. List all guilds bot is in");
    console.log("   4. Generate general OAuth2 invite link");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    var action = await ask("Choose action (1-4): ");

    switch (action.trim()) {
        case "1":
            var guildId = await ask("\nEnter target guild ID: ");
            
            console.log("\n📋 Permission Presets:");
            console.log("   1. Administrator (full access) - " + PERMISSION_PRESETS.ADMINISTRATOR);
            console.log("   2. Moderator (manage msgs/roles) - " + PERMISSION_PRESETS.MODERATOR);
            console.log("   3. Basic (read/send messages) - " + PERMISSION_PRESETS.BASIC);
            console.log("   4. Custom (enter permission integer)\n");
            
            var permChoice = await ask("Choose permissions (1-4): ");
            var permissions = PERMISSION_PRESETS.ADMINISTRATOR;
            
            switch (permChoice.trim()) {
                case "1":
                    permissions = PERMISSION_PRESETS.ADMINISTRATOR;
                    break;
                case "2":
                    permissions = PERMISSION_PRESETS.MODERATOR;
                    break;
                case "3":
                    permissions = PERMISSION_PRESETS.BASIC;
                    break;
                case "4":
                    var customPerm = await ask("Enter permission integer: ");
                    permissions = parseInt(customPerm) || PERMISSION_PRESETS.ADMINISTRATOR;
                    break;
            }
            
            await addBotToGuild(BOT_TOKEN, guildId, permissions);
            
            console.log("📝 Instructions:");
            console.log("   1. Open the OAuth2 URL above in your browser");
            console.log("   2. Login with an account that has 'Manage Server' permission");
            console.log("   3. Select the target server and authorize");
            console.log("   4. The bot will be added to the server!\n");
            break;

        case "2":
            var checkGuildId = await ask("\nEnter guild ID to check: ");
            console.log("\n📡 Checking guild...\n");
            
            var guildInfo = await checkBotInGuild(BOT_TOKEN, checkGuildId);
            
            if (guildInfo && !guildInfo.error) {
                console.log("✅ Bot IS in this guild!");
                console.log("   Guild Name: " + guildInfo.name);
                console.log("   Guild ID: " + guildInfo.id);
                console.log("   Member Count: " + (guildInfo.approximate_member_count || "N/A"));
            } else if (guildInfo && guildInfo.error) {
                console.log("❌ " + guildInfo.error);
            } else {
                console.log("❌ Could not check guild status.");
            }
            break;

        case "3":
            if (guilds && guilds.length > 0) {
                console.log("\n📊 Full list of guilds:");
                guilds.forEach(function(g, idx) {
                    var ownerBadge = g.owner ? " 👑" : "";
                    console.log("   " + (idx + 1) + ". " + g.name + " (ID: " + g.id + ")" + ownerBadge);
                });
                console.log("\n   Total: " + guilds.length + " guilds");
            } else {
                console.log("\n📊 Bot is not in any guilds.");
            }
            break;

        case "4":
            console.log("\n📋 Permission Presets:");
            console.log("   1. Administrator (full access) - " + PERMISSION_PRESETS.ADMINISTRATOR);
            console.log("   2. Moderator (manage msgs/roles) - " + PERMISSION_PRESETS.MODERATOR);
            console.log("   3. Basic (read/send messages) - " + PERMISSION_PRESETS.BASIC);
            console.log("   4. Custom (enter permission integer)\n");
            
            var generalPermChoice = await ask("Choose permissions (1-4): ");
            var generalPermissions = PERMISSION_PRESETS.ADMINISTRATOR;
            
            switch (generalPermChoice.trim()) {
                case "1":
                    generalPermissions = PERMISSION_PRESETS.ADMINISTRATOR;
                    break;
                case "2":
                    generalPermissions = PERMISSION_PRESETS.MODERATOR;
                    break;
                case "3":
                    generalPermissions = PERMISSION_PRESETS.BASIC;
                    break;
                case "4":
                    var customGeneralPerm = await ask("Enter permission integer: ");
                    generalPermissions = parseInt(customGeneralPerm) || PERMISSION_PRESETS.ADMINISTRATOR;
                    break;
            }
            
            var appInfo = await getApplicationInfo(BOT_TOKEN);
            if (appInfo) {
                var generalOauthUrl = "https://discord.com/api/oauth2/authorize?" +
                    "client_id=" + appInfo.id +
                    "&scope=bot%20applications.commands" +
                    "&permissions=" + generalPermissions;
                
                console.log("\n🔗 General OAuth2 Authorization URL:");
                console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
                console.log(generalOauthUrl);
                console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
                
                console.log("📝 Instructions:");
                console.log("   1. Share this URL with server admins");
                console.log("   2. They can add the bot to any server they manage");
                console.log("   3. The bot will be added with the selected permissions!\n");
            }
            break;

        default:
            console.log("\n❌ Invalid action.\n");
    }

    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log("🔐 For educational purposes only!");
    console.log("   Respect Discord ToS and server rules.");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    rl.close();
    process.exit(0);
}

main();
