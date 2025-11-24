# ⚡ Ultra-Fast Discord Channel Creator

**Eye blink speed Discord channel creation with Node.js!**

## 🚀 Features

- **⚡ Ultra-Fast Channel Creator** - Creates multiple channels simultaneously at maximum speed
- **🗑️ Ultra-Fast Channel Deleter** - Deletes all channels in a server with confirmation
- **🔥 Optimized Performance** - Aggressive HTTPS keep-alive, connection pooling (100 sockets)
- **🎯 Smart Rate Limit Handling** - Automatically retries with proper delays when rate limited
- **📊 Performance Metrics** - Shows total time and average time per channel
- **💪 Robust Error Handling** - Handles errors gracefully and continues operation
- **🌟 Simple to Use** - Just a few inputs: bot token, guild ID, and options

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

### Interactive Prompts

#### For Channel Creator:
1. **Enter bot token:** Your Discord bot token (with or without "Bot " prefix - it will be added automatically)
2. **Enter guild ID:** The Discord server (guild) ID where you want to create channels
3. **Number of channels to create:** How many channels to create (e.g., 10, 50, 100)

#### For Channel Deleter:
1. **Enter bot token:** Your Discord bot token (with or without "Bot " prefix)
2. **Enter guild ID:** The Discord server (guild) ID where you want to delete channels
3. **Confirmation:** Type "yes" or "y" to confirm deletion of all channels

### Example Sessions

#### Channel Creator:
```
🔥 ULTRA-FAST DISCORD CHANNEL CREATOR 🔥

⚡ Eye blink speed | Maximum performance

Enter bot token: YOUR_BOT_TOKEN_HERE
Enter guild ID: 1234567890123456789
Number of channels to create: 10

⚡ Creating channels at MAX ultra speed...

⚡ Created: ultra-1
⚡ Created: ultra-2
⚡ Created: ultra-3
...
⚡ Created: ultra-10

🔥 Finished! Ultra-fast burst completed!
⏱️  Time taken: 3.456 seconds
🚀 Average: 345ms per channel
```

#### Channel Deleter:
```
🔥 ULTRA-FAST DISCORD CHANNEL DELETER 🔥

⚡ Eye blink speed | Maximum performance

⚠️  WARNING: This will delete channels permanently!

Enter bot token: YOUR_BOT_TOKEN_HERE
Enter guild ID: 1234567890123456789

📡 Fetching channels...

📊 Found 10 channels in the server.

Channels to delete:
  1. ultra-1 (ID: 123...)
  2. ultra-2 (ID: 456...)
  ...

⚠️  Delete ALL 10 channels? (yes/no): yes

⚡ Deleting channels at MAX ultra speed...

🗑️  Deleted: ultra-1
🗑️  Deleted: ultra-2
...

🔥 Finished! Ultra-fast deletion completed!
⏱️  Time taken: 2.145 seconds
✅ Successfully deleted: 10/10 channels
🚀 Average: 214ms per channel
```

## 🛠️ Technical Details

### Performance Optimizations

- **Connection Pooling:** 100 concurrent sockets with keep-alive
- **Promise.all():** All channels are created concurrently
- **Persistent Connections:** Keep-alive for 30 seconds
- **Minimal Overhead:** Streamlined code for maximum speed

### Rate Limiting

The tool automatically handles Discord's rate limits:
- Detects 429 (Too Many Requests) responses
- Waits for the exact retry_after duration
- Continues creation seamlessly

### HTTPS Agent Configuration

```javascript
{
    keepAlive: true,
    maxSockets: 100,
    maxFreeSockets: 100,
    keepAliveMsecs: 30000,
    timeout: 60000
}
```

## ⚠️ Important Notes

1. **Bot Permissions:** Your bot must have "Manage Channels" permission in the target guild
2. **Rate Limits:** Discord has rate limits. The tools handle them automatically, but operations on hundreds of channels may take time
3. **Token Security:** Never share your bot token publicly. Keep it secure!
4. **Channel Names:** Created channels are named "ultra-1", "ultra-2", etc.
5. **Deletion Warning:** The channel deleter is PERMANENT! There's a confirmation prompt but no undo

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
