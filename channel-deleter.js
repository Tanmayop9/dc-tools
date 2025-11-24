var readline = require("readline");
var fetch = require("node-fetch");
var https = require("https");

// Ultra-fast HTTPS agent with aggressive keep-alive settings
var agent = new https.Agent({
    keepAlive: true,
    maxSockets: 100,
    maxFreeSockets: 100,
    keepAliveMsecs: 30000,
    timeout: 60000
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

async function getChannels(token, guild) {
    // Normalize token - add "Bot " prefix if not present
    var authToken = token.trim();
    if (!authToken.startsWith("Bot ")) {
        authToken = "Bot " + authToken;
    }

    var res = await fetch(
        "https://discord.com/api/v10/guilds/" + guild + "/channels",
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
        console.log("❌ Error fetching channels:", errorData.message || "Unknown error");
    } catch (e) {
        console.log("❌ Error fetching channels: HTTP " + res.status);
    }
    return null;
}

async function deleteChannelFast(token, channelId, channelName) {
    while (true) {
        // Normalize token - add "Bot " prefix if not present
        var authToken = token.trim();
        if (!authToken.startsWith("Bot ")) {
            authToken = "Bot " + authToken;
        }

        var res = await fetch(
            "https://discord.com/api/v10/channels/" + channelId,
            {
                method: "DELETE",
                agent: agent,
                headers: {
                    "Authorization": authToken
                }
            }
        );

        if (res.status === 429) {
            try {
                var json = await res.json();
                var retry = json.retry_after * 1000;
                console.log("⏳ Rate limited — retrying in " + retry + "ms");
                await new Promise(function(r) { setTimeout(r, retry); });
                continue;
            } catch (e) {
                console.log("⏳ Rate limited — retrying in 5s");
                await new Promise(function(r) { setTimeout(r, 5000); });
                continue;
            }
        }

        if (res.status === 204 || res.status === 200) {
            console.log("🗑️  Deleted:", channelName);
            return true;
        }

        // Handle other errors - safely parse JSON
        try {
            var errorData = await res.json();
            console.log("❌ Error deleting " + channelName + ":", errorData.message || "Unknown error");
        } catch (e) {
            console.log("❌ Error deleting " + channelName + ": HTTP " + res.status);
        }
        return false;
    }
}

async function main() {
    console.log("\n🔥 ULTRA-FAST DISCORD CHANNEL DELETER 🔥\n");
    console.log("⚡ Eye blink speed | Maximum performance\n");
    console.log("⚠️  WARNING: This will delete channels permanently!\n");

    var BOT_TOKEN = await ask("Enter bot token: ");
    var GUILD_ID = await ask("Enter guild ID: ");

    console.log("\n📡 Fetching channels...\n");

    var channels = await getChannels(BOT_TOKEN, GUILD_ID);

    if (!channels || channels.length === 0) {
        console.log("❌ No channels found or error occurred.\n");
        rl.close();
        process.exit(1);
    }

    console.log("📊 Found " + channels.length + " channels in the server.");
    console.log("\nChannels to delete:");
    channels.forEach(function(ch, idx) {
        console.log("  " + (idx + 1) + ". " + ch.name + " (ID: " + ch.id + ")");
    });

    var confirm = await ask("\n⚠️  Delete ALL " + channels.length + " channels? (yes/no): ");

    if (confirm.toLowerCase() !== "yes" && confirm.toLowerCase() !== "y") {
        console.log("\n❌ Deletion cancelled.\n");
        rl.close();
        process.exit(0);
    }

    rl.close();

    // TIMER START
    var start = Date.now();

    console.log("\n⚡ Deleting channels at MAX ultra speed...\n");
    console.log("⚠️  Note: All channels are deleted concurrently for maximum speed.");
    console.log("    Discord may rate limit if deleting many channels.\n");

    var tasks = [];
    channels.forEach(function(channel) {
        tasks.push(deleteChannelFast(BOT_TOKEN, channel.id, channel.name));
    });

    // Delete all channels concurrently for maximum speed
    // Rate limits are handled automatically with retry logic
    var results = await Promise.all(tasks);

    // TIMER END
    var end = Date.now();
    var seconds = ((end - start) / 1000).toFixed(3);
    var successful = results.filter(function(r) { return r; }).length;

    console.log("\n🔥 Finished! Ultra-fast deletion completed!");
    console.log("⏱️  Time taken: " + seconds + " seconds");
    console.log("✅ Successfully deleted: " + successful + "/" + channels.length + " channels");
    console.log("🚀 Average: " + ((end - start) / channels.length).toFixed(0) + "ms per channel\n");

    process.exit(0);
}

main();
