# ⚡ Quick Start Guide

Get started with EXTREME SPEED Discord Channel Tools in 3 simple steps!

**100 channels in eye blink! 💨**

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/Tanmayop9/dc-tools.git
cd dc-tools

# 2. Install dependencies
npm install

# 3. Run the tools
npm start        # Create channels
npm run delete   # Delete channels
```

## 📝 What You'll Need

Before running the tool, make sure you have:

1. **Bot Token** - From [Discord Developer Portal](https://discord.com/developers/applications)
   - Go to your application → Bot section → Copy token
   - Can be entered with or without "Bot " prefix

2. **Guild ID** - The Discord server where you want to create channels
   - Enable Developer Mode: User Settings → Advanced → Developer Mode
   - Right-click your server → Copy ID

3. **Permissions** - Your bot needs "Manage Channels" permission in the server

## ⚡ Usage Examples

### Creating Channels

```
$ npm start

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
⏱️  Time taken: 10.567 seconds
✅ Successfully created: 100/100 channels
🚀 Average: 105ms per channel
💨 Speed: 9.5 channels/second
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Deleting Channels

```
$ npm run delete

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
⏱️  Time taken: 7.891 seconds
✅ Successfully deleted: 100/100 channels
🚀 Average: 78ms per channel
💨 Speed: 12.7 channels/second
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 💡 Tips

- **EXTREME SPEED:** Tools optimized for 100+ channels with batched processing
- **Rate limits:** Automatically handled with smart retry logic
- **Batching:** Processes 50 channels per batch for optimal throughput
- **Silent mode:** Auto-activates for 20+ channels to maximize speed
- **Channel names:** Created channels are named "ultra-1", "ultra-2", etc.
- **Be careful with delete:** The deleter is permanent - make sure you want to delete ALL channels!
- **Performance:** Expect 6-20 channels/second for creation, 10-33 for deletion

## 🔧 Troubleshooting

**"Unauthorized" or "Invalid token"**
- Check your bot token is correct
- Make sure the token is not expired

**"Missing Permissions"**
- Ensure your bot has "Manage Channels" permission
- Re-invite the bot with proper permissions if needed

**"Rate limited"**
- Normal! The tool will automatically retry
- Consider creating fewer channels at once

## 📚 More Information

See [README.md](README.md) for detailed documentation and advanced features.

---

**Ready to manage channels at eye blink speed?** 🚀
- Create: `npm start` or `npm run create`
- Delete: `npm run delete`
