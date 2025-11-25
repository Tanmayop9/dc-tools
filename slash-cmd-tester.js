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
var BATCH_SIZE = 100;             // Process 100 commands at a time
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
        normalizedToken = token.trim();
    }
    return normalizedToken;
}

// Generate a random nonce for Discord interactions (snowflake format)
function generateNonce() {
    // Discord snowflake-like nonce for maximum compatibility
    var timestamp = Date.now() - 1420070400000; // Discord epoch
    var random = Math.floor(Math.random() * 4194304);
    return String((BigInt(timestamp) << BigInt(22)) | BigInt(random));
}

// Generate session ID
function generateSessionId() {
    var chars = "abcdef0123456789";
    var result = "";
    for (var i = 0; i < 32; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

// Cached session ID for all requests
var cachedSessionId = generateSessionId();

// ULTRA FAST: Get application commands using multiple methods
async function getApplicationCommands(token, channelId, guildId) {
    var authToken = normalizeToken(token);
    var allCommands = [];
    var seenIds = new Set();
    
    // Method 1: Multiple search endpoints in parallel (gets popular/recent commands)
    var methods = [
        { url: "https://discord.com/api/v9/channels/" + channelId + "/application-commands/search?type=1&limit=25&include_applications=true", name: "search-v9" },
        { url: "https://discord.com/api/v10/channels/" + channelId + "/application-commands/search?type=1&limit=25&include_applications=true", name: "search-v10" },
        { url: "https://discord.com/api/v9/guilds/" + guildId + "/application-command-index", name: "guild-index-v9" },
        { url: "https://discord.com/api/v10/guilds/" + guildId + "/application-command-index", name: "guild-index-v10" },
    ];
    
    // Run all search methods in parallel for speed
    var searchPromises = methods.map(async function(method) {
        try {
            var res = await fetch(method.url, {
                method: "GET",
                agent: agent,
                headers: {
                    "Authorization": authToken,
                    "Content-Type": "application/json"
                }
            });

            if (res.status === 200) {
                var data = await res.json();
                // Handle different response structures
                if (data.application_commands) {
                    return data.application_commands;
                } else if (Array.isArray(data)) {
                    return data;
                } else if (data.applications) {
                    // Guild index returns applications with commands
                    var cmds = [];
                    data.applications.forEach(function(app) {
                        if (app.commands && Array.isArray(app.commands)) {
                            app.commands.forEach(function(cmd) {
                                cmd.application_id = app.id;
                                cmds.push(cmd);
                            });
                        }
                    });
                    return cmds;
                }
                return [];
            }
            return [];
        } catch (e) {
            return [];
        }
    });
    
    var results = await Promise.all(searchPromises);
    
    // Merge all results
    results.forEach(function(cmds) {
        if (Array.isArray(cmds)) {
            cmds.forEach(function(cmd) {
                if (cmd && cmd.id && !seenIds.has(cmd.id)) {
                    seenIds.add(cmd.id);
                    allCommands.push(cmd);
                }
            });
        }
    });
    
    // Method 2: If no commands found, try with common query prefixes (alphabetic search)
    if (allCommands.length === 0) {
        var queries = ["", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
        var queryPromises = queries.map(async function(q) {
            try {
                var url = "https://discord.com/api/v9/channels/" + channelId + "/application-commands/search?type=1&limit=25&include_applications=true";
                if (q) url += "&query=" + encodeURIComponent(q);
                
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
        });
        
        var queryResults = await Promise.all(queryPromises);
        queryResults.forEach(function(cmds) {
            if (Array.isArray(cmds)) {
                cmds.forEach(function(cmd) {
                    if (cmd && cmd.id && !seenIds.has(cmd.id)) {
                        seenIds.add(cmd.id);
                        allCommands.push(cmd);
                    }
                });
            }
        });
    }
    
    return allCommands;
}

// ULTRA FAST: Send a slash command interaction with minimal overhead
// Note: Reduced retries (2 vs 3) for speed - acceptable since slash commands
// are idempotent and can be retried by the user if needed
async function sendSlashCommand(token, applicationId, guildId, channelId, commandData, cmdIndex, silent) {
    var authToken = normalizeToken(token);
    var maxRetries = 2; // Reduced retries for speed (trade-off: less reliable in poor networks)
    var retryCount = 0;

    while (retryCount < maxRetries) {
        try {
            // Build the interaction payload
            var payload = {
                type: 2,  // APPLICATION_COMMAND
                application_id: applicationId,
                guild_id: guildId,
                channel_id: channelId,
                session_id: cachedSessionId,
                data: commandData,
                nonce: generateNonce(),
                analytics_location: "slash_ui"
            };

            var res = await fetch(
                "https://discord.com/api/v9/interactions",
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
                var retry = Math.min(json.retry_after * 1000, 2000); // Cap at 2s for speed
                if (!silent) console.log("⏳ Rate limited — waiting " + retry + "ms (cmd #" + cmdIndex + ")");
                await new Promise(function(r) { setTimeout(r, retry); });
                retryCount++;
                continue;
            }

            if (res.status === 204 || res.status === 200) {
                if (!silent) console.log("⚡ Sent command #" + cmdIndex);
                return { success: true, index: cmdIndex };
            }

            // Log error status for debugging (only in non-silent mode)
            if (!silent) {
                console.log("❌ Command #" + cmdIndex + " failed: HTTP " + res.status);
            }
            return { success: false, index: cmdIndex, error: res.status };
        } catch (e) {
            retryCount++;
            if (retryCount < maxRetries) {
                await new Promise(function(r) { setTimeout(r, 500); }); // Quick retry
            }
        }
    }
    
    return { success: false, index: cmdIndex, error: "Max retries exceeded" };
}

// ULTRA FAST: Process commands in massive batches
async function processBatch(token, applicationId, guildId, channelId, commandData, startIndex, count, batchNum, totalBatches, silent) {
    if (!silent) {
        console.log("🚀 Batch " + batchNum + "/" + totalBatches + " - Sending " + count + " commands...");
    }
    
    var promises = [];
    for (var i = 0; i < count; i++) {
        promises.push(sendSlashCommand(token, applicationId, guildId, channelId, commandData, startIndex + i + 1, true)); // Always silent for max speed
    }
    
    return await Promise.all(promises);
}

// Search for slash commands by name - ULTRA FAST with parallel queries
async function searchCommands(token, channelId, guildId, query) {
    var authToken = normalizeToken(token);
    var allCommands = [];
    var seenIds = new Set();
    
    // Multiple API versions and endpoints in parallel
    var urls = [
        "https://discord.com/api/v9/channels/" + channelId + "/application-commands/search?type=1&limit=25&include_applications=true" + (query ? "&query=" + encodeURIComponent(query) : ""),
        "https://discord.com/api/v10/channels/" + channelId + "/application-commands/search?type=1&limit=25" + (query ? "&query=" + encodeURIComponent(query) : "")
    ];
    
    var searchPromises = urls.map(async function(url) {
        try {
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
    });
    
    var results = await Promise.all(searchPromises);
    results.forEach(function(cmds) {
        cmds.forEach(function(cmd) {
            if (!seenIds.has(cmd.id)) {
                seenIds.add(cmd.id);
                allCommands.push(cmd);
            }
        });
    });
    
    return allCommands;
}

async function main() {
    console.log("\n⚡⚡⚡ ULTRA FAST SLASH COMMAND TESTER ⚡⚡⚡\n");
    console.log("🚀 Lightning speed | 100 commands in eye blink!");
    console.log("🧪 Test your bot's anti-rate-limit system!\n");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    var USER_TOKEN = await ask("Enter your USER token (not bot token): ");
    var GUILD_ID = await ask("Enter guild ID: ");
    var CHANNEL_ID = await ask("Enter channel ID (where bot is accessible): ");

    console.log("\n📡 Searching for available slash commands (ultra fast parallel search)...\n");

    // ULTRA FAST: Use parallel command discovery
    var commands = await getApplicationCommands(USER_TOKEN, CHANNEL_ID, GUILD_ID);

    if (!commands || commands.length === 0) {
        console.log("⚠️  No slash commands found automatically.");
        console.log("   Trying manual search...\n");
        
        // Try searching with common command prefixes
        var searchQuery = await ask("Enter command name to search (or press Enter to skip): ");
        if (searchQuery.trim()) {
            commands = await searchCommands(USER_TOKEN, CHANNEL_ID, GUILD_ID, searchQuery.trim());
        }
        
        if (!commands || commands.length === 0) {
            console.log("\n❌ No slash commands found in this channel.");
            console.log("   Tips:");
            console.log("   1. Make sure you're in a channel where the bot has access");
            console.log("   2. The bot must have slash commands registered");
            console.log("   3. Try typing / in Discord to see available commands\n");
            rl.close();
            process.exit(1);
        }
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

    // Build command data with full application_command structure
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
            contexts: selectedCmd.contexts,
            integration_types: selectedCmd.integration_types,
            options: selectedCmd.options || []
        },
        attachments: []
    };

    // Handle command options
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

    console.log("\n⚡⚡⚡ ULTRA FAST MODE ACTIVATED! ⚡⚡⚡\n");
    console.log("💨 Sending " + COUNT + " slash commands with MAXIMUM parallelism...\n");

    // ULTRA FAST: Split into massive batches
    var allResults = [];
    var batches = [];
    
    for (var i = 0; i < COUNT; i += BATCH_SIZE) {
        var batchCount = Math.min(BATCH_SIZE, COUNT - i);
        batches.push({ startIndex: i, count: batchCount });
    }

    var totalBatches = batches.length;

    // Process batches with minimal delay
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
            false
        );
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
        console.log("   Your bot received " + COUNT + " commands at ULTRA speed.\n");
    }

    process.exit(0);
}

main();
