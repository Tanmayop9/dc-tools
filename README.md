# ⚡ Ultra-Fast Discord Channel Creator

**Eye blink speed Discord channel creation with Node.js!**

## 🚀 Features

- **⚡ EXTREME SPEED Channel Creator** - Create 100 channels in eye blink! Batched concurrent processing
- **🗑️ EXTREME SPEED Channel Deleter** - Delete 100 channels in seconds! Batched concurrent processing
- **🔥 SLASH COMMAND TESTER** - Send 100 slash commands in eye blink! Test your bot's anti-rate-limit system
- **🔥 Maximum Performance** - 200-socket connection pool, LIFO scheduling, 50-channel batches
- **🎯 Smart Rate Limit Handling** - Automatically retries with optimized delays
- **📊 Performance Metrics** - Shows time, average, channels/second, success rate
- **💪 Robust Error Handling** - Handles errors gracefully with automatic retry (3 attempts)
- **🌟 Simple to Use** - Just a few inputs: bot token, guild ID, and options
- **💨 Silent Mode** - Auto-activates for 20+ channels to maximize speed

## 📋 Requirements

- **Node.js** 14.0.0 or higher
- **npm** (comes with Node.js)
- Discord Bot with proper permissions

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/Tanmayop9/dc-tools.git
cd dc-tools

# Install dependencies
npm install
```

## 🎯 Usage

### Channel Creator

```bash
# Run the channel creator
npm start
# or
npm run create
# or directly
node channel-creator.js
```

### Channel Deleter

```bash
# Run the channel deleter
npm run delete
# or directly
node channel-deleter.js
```

### Slash Command Tester

```bash
# Run the slash command tester
npm run slash
# or directly
node slash-cmd-tester.js
```

### Interactive Prompts

#### For Channel Creator:
1. **Enter bot token:** Your Discord bot token (with or without "Bot " prefix - it will be added automatically)
2. **Enter guild ID:** The Discord server (guild) ID where you want to create channels
3. **Number of channels to create:** How many channels to create (e.g., 10, 50, 100)

#### For Channel Deleter:
1. **Enter bot token:** Your Discord bot token (with or without "Bot " prefix)
2. **Enter guild ID:** The Discord server (guild) ID where you want to delete channels
3. **Confirmation:** Type "yes" or "y" to confirm deletion of all channels

#### For Slash Command Tester:
1. **Enter USER token:** Your Discord USER token (not bot token - required to send slash commands)
2. **Enter guild ID:** The Discord server where your bot is accessible
3. **Enter channel ID:** The channel ID where your bot's slash commands are available
4. **Select command:** Choose which slash command to spam
5. **Enter command count:** How many times to send the command (e.g., 100)
6. **Confirmation:** Type "yes" or "y" to start the test

### Example Sessions

#### Channel Creator:
```
🔥 ULTRA-FAST DISCORD CHANNEL CREATOR 🔥

⚡ Eye blink speed | 100 channels in seconds!

Enter bot token: YOUR_BOT_TOKEN_HERE
Enter guild ID: 1234567890123456789
Number of channels to create: 100

⚡ EXTREME SPEED MODE ACTIVATED!

💨 Creating 100 channels with batched concurrent processing...

🚀 Batch 1/2 - Processing 50 channels...
🚀 Batch 2/2 - Processing 50 channels...

🔥 EXTREME SPEED COMPLETED!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  Time taken: 12.345 seconds
✅ Successfully created: 100/100 channels
🚀 Average: 123ms per channel
💨 Speed: 8.1 channels/second
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Channel Deleter:
```
🔥 ULTRA-FAST DISCORD CHANNEL DELETER 🔥

⚡ Eye blink speed | 100 channels in seconds!

⚠️  WARNING: This will delete channels permanently!

Enter bot token: YOUR_BOT_TOKEN_HERE
Enter guild ID: 1234567890123456789

📡 Fetching channels...

📊 Found 100 channels in the server.

Showing first 10 channels:
  1. ultra-1 (ID: 123...)
  2. ultra-2 (ID: 456...)
  ...
  10. ultra-10 (ID: ...)
  ... and 90 more channels

⚠️  Delete ALL 100 channels? (yes/no): yes

⚡ EXTREME SPEED MODE ACTIVATED!

💨 Deleting 100 channels with batched concurrent processing...

🚀 Batch 1/2 - Deleting 50 channels...
🚀 Batch 2/2 - Deleting 50 channels...

🔥 EXTREME SPEED COMPLETED!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  Time taken: 8.123 seconds
✅ Successfully deleted: 100/100 channels
🚀 Average: 81ms per channel
💨 Speed: 12.3 channels/second
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Slash Command Tester:
```
🔥 ULTRA-FAST SLASH COMMAND TESTER 🔥

⚡ Eye blink speed | 100 commands in seconds!
🧪 Test your bot's anti-rate-limit system!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Enter your USER token (not bot token): YOUR_USER_TOKEN_HERE
Enter guild ID: 1234567890123456789
Enter channel ID (where bot is accessible): 1234567890123456789

📡 Searching for available slash commands...

📊 Found 3 slash commands:

  1. /ping - Check bot latency
     App ID: 987654321...
  2. /help - Show help menu
     App ID: 987654321...
  3. /test - Test command
     App ID: 987654321...

Enter command number to spam (1-3): 1

✅ Selected: /ping

Number of commands to send (e.g., 100): 100

⚠️  Send /ping 100 times? (yes/no): yes

⚡ EXTREME SPEED MODE ACTIVATED!

💨 Sending 100 slash commands with batched concurrent processing...

🚀 Batch 1/2 - Sending 50 commands...
🚀 Batch 2/2 - Sending 50 commands...

🔥 EXTREME SPEED COMPLETED!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  Time taken: 5.678 seconds
✅ Successfully sent: 100/100 commands
🚀 Average: 56ms per command
💨 Speed: 17.6 commands/second
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 All commands sent successfully!
   Your bot received 100 commands at extreme speed.
```

## 💨 Speed Benchmarks

**Typical performance for 100 channels:**
- Creation: ~5-15 seconds (6-20 channels/second)
- Deletion: ~3-10 seconds (10-33 channels/second)
- Slash Commands: ~3-10 seconds (10-33 commands/second)
- Average per operation: ~100-200ms

*Actual speed depends on Discord's rate limits and network latency*

## 🛠️ Technical Details

### Performance Optimizations

- **Connection Pooling:** 200 concurrent sockets with keep-alive (doubled!)
- **Batched Processing:** 50 channels per batch for optimal throughput
- **LIFO Scheduling:** Hot connection reuse for minimum latency
- **Promise.all():** All channels in batch processed concurrently
- **Persistent Connections:** Keep-alive for 60 seconds
- **Minimal Overhead:** Streamlined code for maximum speed
- **Smart Retries:** Up to 3 attempts with exponential backoff
- **Silent Mode:** Reduces console overhead for large operations (20+ channels)

### Rate Limiting

The tool automatically handles Discord's rate limits:
- Detects 429 (Too Many Requests) responses
- Waits for the exact retry_after duration
- Continues creation seamlessly

### HTTPS Agent Configuration (EXTREME SPEED)

```javascript
{
    keepAlive: true,
    maxSockets: 200,          // Doubled for extreme speed!
    maxFreeSockets: 200,
    keepAliveMsecs: 60000,    // 60 seconds
    timeout: 30000,
    scheduling: "lifo"        // Last-in-first-out (hot connections)
}
```

### Batching Configuration

```javascript
{
    batchSize: 50,            // 50 channels per batch
    batchDelay: 50            // Only 50ms between batches
}
```

## ⚠️ Important Notes

1. **Bot Permissions:** Your bot must have "Manage Channels" permission in the target guild
2. **Rate Limits:** Discord has rate limits. The tools handle them automatically, but operations on hundreds of channels may take time
3. **Token Security:** Never share your bot token or user token publicly. Keep them secure!
4. **Channel Names:** Created channels are named "ultra-1", "ultra-2", etc.
5. **Deletion Warning:** The channel deleter is PERMANENT! There's a confirmation prompt but no undo
6. **Slash Command Tester:** Requires a USER token (not bot token) to send slash commands. This is used to test your bot's anti-rate-limit system by sending many slash commands rapidly.

## 🔐 Getting Your Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application (or create one)
3. Go to "Bot" section
4. Copy the bot token
5. **Important:** Enable necessary intents if required

## 📝 Getting Guild ID

1. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Right-click on your server icon
3. Click "Copy ID"

## 🚨 Disclaimer

This tool is for **educational purposes only**. Make sure you have proper authorization to create channels in the target server. Misuse of this tool may violate Discord's Terms of Service.

## 📄 License

MIT License - Use at your own risk

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 🌟 Why This Tool?

- **Blazing Fast:** Uses concurrent creation with optimized networking
- **Reliable:** Handles rate limits and errors automatically
- **Simple:** No complex configuration needed
- **Efficient:** Maximum performance with minimal resource usage

---

**Made with ⚡ by Tanmayop9**
