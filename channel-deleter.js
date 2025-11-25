var readline = require("readline");
var fetch = require("node-fetch");
var https = require("https");

// ULTRA FAST HTTPS agent - maximized for extreme performance
var agent = new https.Agent({
    keepAlive: true,
    maxSockets: 500,              // Maximum sockets for ultra speed
    maxFreeSockets: 500,
    keepAliveMsecs: 120000,       // 2 minute keep-alive
    timeout: 15000,               // Shorter timeout for faster failures
    scheduling: "lifo"            // Last-in-first-out for hot connections
});

// ULTRA FAST Batching configuration
var BATCH_SIZE = 100;             // Process 100 channels at a time
var BATCH_DELAY = 10;             // Minimal 10ms delay between batches

var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function ask(q) {
    return new Promise(function(resolve) {
        rl.question(q, resolve);
    });
}

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

async function getChannels(token, guild) {
    var authToken = normalizeToken(token);

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

async function deleteChannelFast(token, channelId, channelName, silent) {
    var authToken = normalizeToken(token);
    var maxRetries = 2; // Reduced retries for speed
    var retryCount = 0;

    while (retryCount < maxRetries) {
        try {
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
                var json = await res.json();
                var retry = Math.min(json.retry_after * 1000, 2000); // Cap at 2s for ultra speed
                if (!silent) console.log("⏳ Rate limited — waiting " + retry + "ms");
                await new Promise(function(r) { setTimeout(r, retry); });
                retryCount++;
                continue;
            }

            if (res.status === 204 || res.status === 200) {
                if (!silent) console.log("🗑️  Deleted:", channelName);
                return { success: true, name: channelName };
            }

            // Handle other errors
            if (!silent) {
                try {
                    var errorData = await res.json();
                    console.log("❌ Error:", errorData.message || "HTTP " + res.status);
                } catch (e) {
                    console.log("❌ Error: HTTP " + res.status);
                }
            }
            return { success: false, name: channelName, error: res.status };
        } catch (e) {
            if (!silent) console.log("❌ Network error:", e.message);
            retryCount++;
            if (retryCount < maxRetries) {
                await new Promise(function(r) { setTimeout(r, 500); }); // Quick retry
            }
        }
    }
    
    return { success: false, name: channelName, error: "Max retries exceeded" };
}

// Process channels in batches for extreme speed
async function processBatch(token, channels, batchNum, totalBatches, silent) {
    if (!silent) {
        console.log("🚀 Batch " + batchNum + "/" + totalBatches + " - Deleting " + channels.length + " channels...");
    }
    
    var promises = channels.map(function(channel) {
        return deleteChannelFast(token, channel.id, channel.name, silent);
    });
    
    return await Promise.all(promises);
}

async function main() {
    console.log("\n⚡⚡⚡ ULTRA FAST DISCORD CHANNEL DELETER ⚡⚡⚡\n");
    console.log("🚀 Lightning speed | 500 channels in eye blink!");
    console.log("💨 100 channels per batch | Maximum parallelism!\n");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log("⚠️  WARNING: This will delete channels permanently!");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

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
    
    // Only show first 10 if more than 10 channels
    if (channels.length <= 10) {
        console.log("\nChannels to delete:");
        channels.forEach(function(ch, idx) {
            console.log("  " + (idx + 1) + ". " + ch.name + " (ID: " + ch.id + ")");
        });
    } else {
        console.log("\nShowing first 10 channels:");
        for (var i = 0; i < Math.min(10, channels.length); i++) {
            console.log("  " + (i + 1) + ". " + channels[i].name + " (ID: " + channels[i].id + ")");
        }
        console.log("  ... and " + (channels.length - 10) + " more channels");
    }

    var confirm = await ask("\n⚠️  Delete ALL " + channels.length + " channels? (yes/no): ");

    if (confirm.toLowerCase() !== "yes" && confirm.toLowerCase() !== "y") {
        console.log("\n❌ Deletion cancelled.\n");
        rl.close();
        process.exit(0);
    }

    rl.close();

    // TIMER START
    var start = Date.now();

    console.log("\n⚡⚡⚡ ULTRA FAST MODE ACTIVATED! ⚡⚡⚡\n");
    console.log("💨 Deleting " + channels.length + " channels with MAXIMUM parallelism...\n");

    // Split into batches for optimal performance
    var allResults = [];
    var batches = [];
    
    for (var i = 0; i < channels.length; i += BATCH_SIZE) {
        var batchChannels = channels.slice(i, Math.min(i + BATCH_SIZE, channels.length));
        batches.push(batchChannels);
    }

    var totalBatches = batches.length;
    var silent = channels.length > 10; // Silent mode for operations > 10

    // Process batches with minimal delay between them
    for (var b = 0; b < batches.length; b++) {
        var batchResults = await processBatch(BOT_TOKEN, batches[b], b + 1, totalBatches, silent);
        allResults = allResults.concat(batchResults);
        
        // Minimal delay between batches (only if not last batch)
        if (b < batches.length - 1) {
            await new Promise(function(r) { setTimeout(r, BATCH_DELAY); });
        }
    }

    // TIMER END
    var end = Date.now();
    var seconds = ((end - start) / 1000).toFixed(3);
    var successful = allResults.filter(function(r) { return r.success; }).length;

    console.log("\n⚡⚡⚡ ULTRA FAST COMPLETED! ⚡⚡⚡");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log("⏱️  Time taken: " + seconds + " seconds");
    console.log("✅ Successfully deleted: " + successful + "/" + channels.length + " channels");
    console.log("🚀 Average: " + ((end - start) / channels.length).toFixed(0) + "ms per channel");
    console.log("💨 Speed: " + (channels.length / (end - start) * 1000).toFixed(1) + " channels/second");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    if (successful < channels.length) {
        console.log("⚠️  Some channels failed to delete. Check bot permissions.\n");
    }

    if (successful === channels.length) {
        console.log("🎉 All channels deleted successfully!\n");
    }

    process.exit(0);
}

main();
