var readline = require("readline");
var fetch = require("node-fetch");
var https = require("https");

// EXTREME SPEED HTTPS agent - maximized for eye blink performance
var agent = new https.Agent({
    keepAlive: true,
    maxSockets: 200,              // Maximum sockets for extreme speed
    maxFreeSockets: 200,
    keepAliveMsecs: 60000,        // Longer keep-alive
    timeout: 30000,
    scheduling: "lifo"            // Last-in-first-out for hot connections
});

// Batching configuration for extreme speed
var BATCH_SIZE = 50;              // Process 50 commands at a time
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
        normalizedToken = token.trim();
    }
    return normalizedToken;
}

// Generate a random nonce for Discord interactions
function generateNonce() {
    // Use timestamp + random suffix for unique nonces (safe integer range)
    var timestamp = Date.now();
    var random = Math.floor(Math.random() * 1000000);
    return String(timestamp) + String(random).padStart(6, "0");
}

// Get application commands from a channel
async function getApplicationCommands(token, channelId) {
    var authToken = normalizeToken(token);
    
    try {
        var res = await fetch(
            "https://discord.com/api/v10/channels/" + channelId + "/application-commands/search?type=1&limit=25",
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
            var data = await res.json();
            return data.application_commands || [];
        }

        console.log("❌ Error fetching commands: HTTP " + res.status);
        try {
            var errorData = await res.json();
            console.log("   ", errorData.message || "Unknown error");
        } catch (e) {
            // ignore parse errors
        }
        return null;
    } catch (e) {
        console.log("❌ Network error:", e.message);
        return null;
    }
}

// Send a slash command interaction
async function sendSlashCommand(token, applicationId, guildId, channelId, commandData, cmdIndex, silent) {
    var authToken = normalizeToken(token);
    var maxRetries = 3;
    var retryCount = 0;

    while (retryCount < maxRetries) {
        try {
            // Build the interaction payload
            var payload = {
                type: 2,  // APPLICATION_COMMAND
                application_id: applicationId,
                guild_id: guildId,
                channel_id: channelId,
                session_id: generateNonce().substring(0, 32),
                data: commandData,
                nonce: generateNonce()
            };

            var res = await fetch(
                "https://discord.com/api/v10/interactions",
                {
                    method: "POST",
                    agent: agent,
                    headers: {
                        "Authorization": authToken,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                }
            );

            if (res.status === 429) {
                var json = await res.json();
                var retry = Math.min(json.retry_after * 1000, 5000); // Cap at 5s
                if (!silent) console.log("⏳ Rate limited — waiting " + retry + "ms (cmd #" + cmdIndex + ")");
                await new Promise(function(r) { setTimeout(r, retry); });
                retryCount++;
                continue;
            }

            if (res.status === 204 || res.status === 200) {
                if (!silent) console.log("⚡ Sent command #" + cmdIndex);
                return { success: true, index: cmdIndex };
            }

            // Handle other errors
            if (!silent) {
                try {
                    var errorData = await res.json();
                    console.log("❌ Error #" + cmdIndex + ":", errorData.message || "HTTP " + res.status);
                } catch (e) {
                    console.log("❌ Error #" + cmdIndex + ": HTTP " + res.status);
                }
            }
            return { success: false, index: cmdIndex, error: res.status };
        } catch (e) {
            if (!silent) console.log("❌ Network error #" + cmdIndex + ":", e.message);
            retryCount++;
            if (retryCount < maxRetries) {
                await new Promise(function(r) { setTimeout(r, 1000); });
            }
        }
    }
    
    return { success: false, index: cmdIndex, error: "Max retries exceeded" };
}

// Process commands in batches for extreme speed
async function processBatch(token, applicationId, guildId, channelId, commandData, startIndex, count, batchNum, totalBatches, silent) {
    if (!silent) {
        console.log("🚀 Batch " + batchNum + "/" + totalBatches + " - Sending " + count + " commands...");
    }
    
    var promises = [];
    for (var i = 0; i < count; i++) {
        promises.push(sendSlashCommand(token, applicationId, guildId, channelId, commandData, startIndex + i + 1, silent));
    }
    
    return await Promise.all(promises);
}

// Search for slash commands by name
async function searchCommands(token, channelId, query) {
    var authToken = normalizeToken(token);
    
    try {
        var url = "https://discord.com/api/v10/channels/" + channelId + "/application-commands/search?type=1&limit=10";
        if (query) {
            url += "&query=" + encodeURIComponent(query);
        }
        
        var res = await fetch(url, {
            method: "GET",
            agent: agent,
            headers: {
                "Authorization": authToken,
                "Content-Type": "application/json"
            }
        });

        if (res.status === 200) {
            var data = await res.json();
            return data.application_commands || [];
        }

        return [];
    } catch (e) {
        return [];
    }
}

async function main() {
    console.log("\n🔥 ULTRA-FAST SLASH COMMAND TESTER 🔥\n");
    console.log("⚡ Eye blink speed | 100 commands in seconds!");
    console.log("🧪 Test your bot's anti-rate-limit system!\n");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    var USER_TOKEN = await ask("Enter your USER token (not bot token): ");
    var GUILD_ID = await ask("Enter guild ID: ");
    var CHANNEL_ID = await ask("Enter channel ID (where bot is accessible): ");

    console.log("\n📡 Searching for available slash commands...\n");

    // Search for commands in the channel
    var commands = await searchCommands(USER_TOKEN, CHANNEL_ID, "");

    if (!commands || commands.length === 0) {
        console.log("❌ No slash commands found in this channel.");
        console.log("   Make sure your bot has slash commands registered.\n");
        rl.close();
        process.exit(1);
    }

    console.log("📊 Found " + commands.length + " slash commands:\n");
    
    commands.forEach(function(cmd, idx) {
        console.log("  " + (idx + 1) + ". /" + cmd.name + " - " + (cmd.description || "No description"));
        console.log("     App ID: " + cmd.application_id);
    });

    console.log("\n");
    var cmdChoice = await ask("Enter command number to spam (1-" + commands.length + "): ");
    var selectedCmd = commands[parseInt(cmdChoice) - 1];

    if (!selectedCmd) {
        console.log("\n❌ Invalid command selection.\n");
        rl.close();
        process.exit(1);
    }

    console.log("\n✅ Selected: /" + selectedCmd.name);

    // Check if command has options
    var commandData = {
        version: selectedCmd.version,
        id: selectedCmd.id,
        name: selectedCmd.name,
        type: 1,
        options: [],
        application_command: {
            id: selectedCmd.id,
            application_id: selectedCmd.application_id,
            version: selectedCmd.version,
            default_member_permissions: selectedCmd.default_member_permissions,
            type: 1,
            nsfw: selectedCmd.nsfw || false,
            name: selectedCmd.name,
            description: selectedCmd.description,
            dm_permission: selectedCmd.dm_permission,
            options: selectedCmd.options || []
        }
    };

    // If command has required options, ask for values
    if (selectedCmd.options && selectedCmd.options.length > 0) {
        console.log("\n📝 This command has options:");
        
        for (var i = 0; i < selectedCmd.options.length; i++) {
            var opt = selectedCmd.options[i];
            var required = opt.required ? " (required)" : " (optional)";
            console.log("   - " + opt.name + ": " + (opt.description || "No description") + required);
            
            if (opt.required) {
                var optValue = await ask("   Enter value for '" + opt.name + "': ");
                commandData.options.push({
                    type: opt.type,
                    name: opt.name,
                    value: optValue
                });
            }
        }
    }

    var COUNT = parseInt(await ask("\nNumber of commands to send (e.g., 100): "));

    if (isNaN(COUNT) || COUNT < 1) {
        console.log("\n❌ Invalid number.\n");
        rl.close();
        process.exit(1);
    }

    var confirm = await ask("\n⚠️  Send /" + selectedCmd.name + " " + COUNT + " times? (yes/no): ");

    if (confirm.toLowerCase() !== "yes" && confirm.toLowerCase() !== "y") {
        console.log("\n❌ Cancelled.\n");
        rl.close();
        process.exit(0);
    }

    rl.close();

    // TIMER START
    var start = Date.now();

    console.log("\n⚡ EXTREME SPEED MODE ACTIVATED!\n");
    console.log("💨 Sending " + COUNT + " slash commands with batched concurrent processing...\n");

    // Split into batches for optimal performance
    var allResults = [];
    var batches = [];
    
    for (var i = 0; i < COUNT; i += BATCH_SIZE) {
        var batchCount = Math.min(BATCH_SIZE, COUNT - i);
        batches.push({ startIndex: i, count: batchCount });
    }

    var totalBatches = batches.length;
    var silent = COUNT > 20; // Silent mode for large operations

    // Process batches with minimal delay between them
    for (var b = 0; b < batches.length; b++) {
        var batchResults = await processBatch(
            USER_TOKEN,
            selectedCmd.application_id,
            GUILD_ID,
            CHANNEL_ID,
            commandData,
            batches[b].startIndex,
            batches[b].count,
            b + 1,
            totalBatches,
            silent
        );
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
    console.log("✅ Successfully sent: " + successful + "/" + COUNT + " commands");
    console.log("🚀 Average: " + ((end - start) / COUNT).toFixed(0) + "ms per command");
    console.log("💨 Speed: " + (COUNT / (end - start) * 1000).toFixed(1) + " commands/second");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    if (successful < COUNT) {
        console.log("⚠️  Some commands failed. This could be due to:");
        console.log("   - Rate limits from Discord");
        console.log("   - Your bot's anti-rate-limit system working!");
        console.log("   - Permission issues\n");
    }

    if (successful === COUNT) {
        console.log("🎉 All commands sent successfully!");
        console.log("   Your bot received " + COUNT + " commands at extreme speed.\n");
    }

    process.exit(0);
}

main();
