var readline = require("readline");
var fetch = require("node-fetch");
var https = require("https");

// EXTREME SPEED HTTPS agent - maximized for eye blink performance
var agent = new https.Agent({
    keepAlive: true,
    maxSockets: 200,              // Double the sockets
    maxFreeSockets: 200,
    keepAliveMsecs: 60000,        // Longer keep-alive
    timeout: 30000,
    scheduling: "lifo"            // Last-in-first-out for hot connections
});

// Batching configuration for extreme speed
var BATCH_SIZE = 50;              // Process 50 channels at a time
var BATCH_DELAY = 50;             // Tiny 50ms delay between batches

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

async function createChannelFast(token, guild, name, silent) {
    var authToken = normalizeToken(token);
    var maxRetries = 3;
    var retryCount = 0;

    while (retryCount < maxRetries) {
        try {
            var res = await fetch(
                "https://discord.com/api/v10/guilds/" + guild + "/channels",
                {
                    method: "POST",
                    agent: agent,
                    headers: {
                        "Authorization": authToken,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        name: name,
                        type: 0
                    })
                }
            );

            if (res.status === 429) {
                var json = await res.json();
                var retry = Math.min(json.retry_after * 1000, 5000); // Cap at 5s
                if (!silent) console.log("⏳ Rate limited — waiting " + retry + "ms");
                await new Promise(function(r) { setTimeout(r, retry); });
                retryCount++;
                continue;
            }

            if (res.status === 201 || res.status === 200) {
                var data = await res.json();
                if (!silent) console.log("⚡ Created:", data.name);
                return { success: true, data: data };
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
            return { success: false, error: res.status };
        } catch (e) {
            if (!silent) console.log("❌ Network error:", e.message);
            retryCount++;
            if (retryCount < maxRetries) {
                await new Promise(function(r) { setTimeout(r, 1000); });
            }
        }
    }
    
    return { success: false, error: "Max retries exceeded" };
}

// Process channels in batches for extreme speed
async function processBatch(token, guild, names, batchNum, totalBatches, silent) {
    if (!silent) {
        console.log("🚀 Batch " + batchNum + "/" + totalBatches + " - Processing " + names.length + " channels...");
    }
    
    var promises = names.map(function(name) {
        return createChannelFast(token, guild, name, silent);
    });
    
    return await Promise.all(promises);
}

async function main() {
    console.log("\n🔥 ULTRA-FAST DISCORD CHANNEL CREATOR 🔥\n");
    console.log("⚡ Eye blink speed | 100 channels in seconds!\n");

    var BOT_TOKEN = await ask("Enter bot token: ");
    var GUILD_ID = await ask("Enter guild ID: ");
    var COUNT = parseInt(await ask("Number of channels to create: "));

    rl.close();

    // TIMER START
    var start = Date.now();

    console.log("\n⚡ EXTREME SPEED MODE ACTIVATED!\n");
    console.log("💨 Creating " + COUNT + " channels with batched concurrent processing...\n");

    // Split into batches for optimal performance
    var allResults = [];
    var batches = [];
    
    for (var i = 0; i < COUNT; i += BATCH_SIZE) {
        var batchNames = [];
        for (var j = i; j < Math.min(i + BATCH_SIZE, COUNT); j++) {
            batchNames.push("ultra-" + (j + 1));
        }
        batches.push(batchNames);
    }

    var totalBatches = batches.length;
    var silent = COUNT > 20; // Silent mode for large operations

    // Process batches with minimal delay between them
    for (var b = 0; b < batches.length; b++) {
        var batchResults = await processBatch(BOT_TOKEN, GUILD_ID, batches[b], b + 1, totalBatches, silent);
        allResults = allResults.concat(batchResults);
        
        // Tiny delay between batches (only if not last batch)
        if (b < batches.length - 1) {
            await new Promise(function(r) { setTimeout(r, BATCH_DELAY); });
        }
    }

    // TIMER END
    var end = Date.now();
    var seconds = ((end - start) / 1000).toFixed(3);
    var successful = allResults.filter(function(r) { return r.success; }).length;

    console.log("\n🔥 EXTREME SPEED COMPLETED!");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log("⏱️  Time taken: " + seconds + " seconds");
    console.log("✅ Successfully created: " + successful + "/" + COUNT + " channels");
    console.log("🚀 Average: " + ((end - start) / COUNT).toFixed(0) + "ms per channel");
    console.log("💨 Speed: " + (COUNT / (end - start) * 1000).toFixed(1) + " channels/second");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    if (successful < COUNT) {
        console.log("⚠️  Some channels failed to create. Check bot permissions.\n");
    }

    process.exit(0);
}

main();
