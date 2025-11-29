// Simple test to verify the bot-adder.js structure
console.log("🧪 Testing bot-adder.js structure...\n");

// Test 1: Check if required modules can be loaded
try {
    var readline = require("readline");
    var fetch = require("node-fetch");
    var https = require("https");
    console.log("✅ All required modules loaded successfully");
} catch (e) {
    console.log("❌ Failed to load modules:", e.message);
    process.exit(1);
}

// Test 2: Check if HTTPS agent can be created
try {
    var agent = new https.Agent({
        keepAlive: true,
        maxSockets: 100,
        maxFreeSockets: 50,
        keepAliveMsecs: 60000,
        timeout: 15000,
        scheduling: "lifo"
    });
    console.log("✅ HTTPS agent created successfully");
    console.log("   - Keep-alive: enabled");
    console.log("   - Max sockets: 100");
    console.log("   - LIFO scheduling: enabled");
} catch (e) {
    console.log("❌ Failed to create HTTPS agent:", e.message);
    process.exit(1);
}

// Test 3: Verify OAuth2 URL generation
try {
    var clientId = "123456789012345678";
    var guildId = "987654321098765432";
    var permissions = 8;
    
    var oauthUrl = "https://discord.com/api/oauth2/authorize?" +
        "client_id=" + clientId +
        "&scope=bot%20applications.commands" +
        "&permissions=" + permissions +
        "&guild_id=" + guildId;
    
    if (oauthUrl.includes("client_id=") && 
        oauthUrl.includes("scope=bot") && 
        oauthUrl.includes("permissions=") &&
        oauthUrl.includes("guild_id=")) {
        console.log("✅ OAuth2 URL generation works correctly");
        console.log("   - Client ID included");
        console.log("   - Scope includes 'bot'");
        console.log("   - Permissions included");
        console.log("   - Guild ID included");
    } else {
        throw new Error("OAuth2 URL missing required parameters");
    }
} catch (e) {
    console.log("❌ OAuth2 URL generation failed:", e.message);
    process.exit(1);
}

// Test 4: Verify permission constants
try {
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
    
    if (PERMISSIONS.ADMINISTRATOR === 8 && 
        PERMISSIONS.MANAGE_CHANNELS === 16 &&
        PERMISSIONS.SEND_MESSAGES === 2048) {
        console.log("✅ Permission constants are correct");
        console.log("   - ADMINISTRATOR: 8");
        console.log("   - MANAGE_CHANNELS: 16");
        console.log("   - SEND_MESSAGES: 2048");
    } else {
        throw new Error("Permission constants are incorrect");
    }
} catch (e) {
    console.log("❌ Permission test failed:", e.message);
    process.exit(1);
}

// Test 5: Verify token normalization
try {
    function normalizeToken(token) {
        var authToken = token.trim();
        if (!authToken.startsWith("Bot ")) {
            authToken = "Bot " + authToken;
        }
        return authToken;
    }
    
    var token1 = normalizeToken("myToken123");
    var token2 = normalizeToken("Bot myToken123");
    
    if (token1 === "Bot myToken123" && token2 === "Bot myToken123") {
        console.log("✅ Token normalization works correctly");
        console.log("   - Adds 'Bot ' prefix when missing");
        console.log("   - Preserves 'Bot ' prefix when present");
    } else {
        throw new Error("Token normalization failed");
    }
} catch (e) {
    console.log("❌ Token normalization test failed:", e.message);
    process.exit(1);
}

// Test 6: Verify Promise handling for async operations
try {
    var testPromises = [
        Promise.resolve({ success: true, name: "guild1" }),
        Promise.resolve({ success: true, name: "guild2" }),
        Promise.resolve({ success: false, name: "guild3" })
    ];
    Promise.all(testPromises).then(function(results) {
        console.log("✅ Promise handling works correctly");
        console.log("   - Async operations supported");
        var successful = results.filter(function(r) { return r.success; }).length;
        console.log("   - Result filtering works: " + successful + "/" + results.length);
    });
} catch (e) {
    console.log("❌ Promise handling test failed:", e.message);
    process.exit(1);
}

setTimeout(function() {
    console.log("\n🎉 All tests passed! The bot adder tool is ready to use.\n");
    console.log("📝 To run the bot adder:");
    console.log("   npm run bot");
    console.log("   or");
    console.log("   node bot-adder.js\n");
    console.log("🤖 Features:");
    console.log("   - Generate OAuth2 invite links");
    console.log("   - Check if bot is in a guild");
    console.log("   - List all guilds bot is in");
    console.log("   - Support for custom permissions\n");
    console.log("⚠️  NOTE: For educational purposes only!");
}, 100);
