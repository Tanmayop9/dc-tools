# ⚡ Quick Start Guide

Get started with the Ultra-Fast Discord Channel Tools in 3 simple steps!

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

⚡ Eye blink speed | Maximum performance

Enter bot token: YOUR_BOT_TOKEN_HERE
Enter guild ID: 1234567890123456789
Number of channels to create: 5

⚡ Creating channels at MAX ultra speed...

⚠️  Note: All channels are created concurrently for maximum speed.
    Discord may rate limit if creating many channels.

⚡ Created: ultra-1
⚡ Created: ultra-2
⚡ Created: ultra-3
⚡ Created: ultra-4
⚡ Created: ultra-5

🔥 Finished! Ultra-fast burst completed!
⏱️  Time taken: 1.234 seconds
🚀 Average: 246ms per channel
```

### Deleting Channels

```
$ npm run delete

🔥 ULTRA-FAST DISCORD CHANNEL DELETER 🔥

⚡ Eye blink speed | Maximum performance

⚠️  WARNING: This will delete channels permanently!

Enter bot token: YOUR_BOT_TOKEN_HERE
Enter guild ID: 1234567890123456789

📡 Fetching channels...

📊 Found 5 channels in the server.

Channels to delete:
  1. ultra-1 (ID: 123...)
  2. ultra-2 (ID: 456...)
  3. ultra-3 (ID: 789...)
  4. ultra-4 (ID: 012...)
  5. ultra-5 (ID: 345...)

⚠️  Delete ALL 5 channels? (yes/no): yes

⚡ Deleting channels at MAX ultra speed...

🗑️  Deleted: ultra-1
🗑️  Deleted: ultra-2
🗑️  Deleted: ultra-3
🗑️  Deleted: ultra-4
🗑️  Deleted: ultra-5

🔥 Finished! Ultra-fast deletion completed!
⏱️  Time taken: 1.123 seconds
✅ Successfully deleted: 5/5 channels
🚀 Average: 224ms per channel
```

## 💡 Tips

- **Small batches:** Start with 5-10 channels to avoid rate limits
- **Rate limits:** The tools automatically handle rate limits and retries
- **Speed:** Concurrent operations mean everything happens at once!
- **Channel names:** Created channels are named "ultra-1", "ultra-2", etc.
- **Be careful with delete:** The deleter is permanent - make sure you want to delete ALL channels!

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
