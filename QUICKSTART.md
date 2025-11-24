# ⚡ Quick Start Guide

Get started with the Ultra-Fast Discord Channel Creator in 3 simple steps!

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/Tanmayop9/dc-tools.git
cd dc-tools

# 2. Install dependencies
npm install

# 3. Run the tool
npm start
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

## ⚡ Usage Example

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

## 💡 Tips

- **Small batches:** Start with 5-10 channels to avoid rate limits
- **Rate limits:** The tool automatically handles rate limits and retries
- **Speed:** Concurrent creation means all channels are created at once!
- **Channel names:** Channels are named "ultra-1", "ultra-2", etc.

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

**Ready to create channels at eye blink speed? Run `npm start` now!** 🚀
