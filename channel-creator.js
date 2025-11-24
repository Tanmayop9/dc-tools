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

async function createChannelFast(token, guild, name) {
    while (true) {
        var res = await fetch(
            "https://discord.com/api/v10/guilds/" + guild + "/channels",
            {
                method: "POST",
                agent: agent,
                headers: {
                    "Authorization": "Bot " + token,
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
            var retry = json.retry_after * 1000;
            console.log("⏳ Rate limited — retrying in " + retry + "ms");
            await new Promise(function(r) { setTimeout(r, retry); });
            continue;
        }

        if (res.status === 201 || res.status === 200) {
            var data = await res.json();
            console.log("⚡ Created:", data.name);
            return data;
        }

        // Handle other errors
        var errorData = await res.json();
        console.log("❌ Error:", errorData.message || "Unknown error");
        return null;
    }
}

async function main() {
    console.log("\n🔥 ULTRA-FAST DISCORD CHANNEL CREATOR 🔥\n");
    console.log("⚡ Eye blink speed | Maximum performance\n");

    var BOT_TOKEN = await ask("Enter bot token: ");
    var GUILD_ID = await ask("Enter guild ID: ");
    var COUNT = parseInt(await ask("Number of channels to create: "));

    rl.close();

    // TIMER START
    var start = Date.now();

    console.log("\n⚡ Creating channels at MAX ultra speed...\n");

    var tasks = [];
    for (var i = 1; i <= COUNT; i++) {
        tasks.push(createChannelFast(BOT_TOKEN, GUILD_ID, "ultra-" + i));
    }

    await Promise.all(tasks);

    // TIMER END
    var end = Date.now();
    var seconds = ((end - start) / 1000).toFixed(3);

    console.log("\n🔥 Finished! Ultra-fast burst completed!");
    console.log("⏱️  Time taken: " + seconds + " seconds");
    console.log("🚀 Average: " + ((end - start) / COUNT).toFixed(0) + "ms per channel\n");

    process.exit(0);
}

main();
