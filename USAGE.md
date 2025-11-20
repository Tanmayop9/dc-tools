# Quick Start Guide

## Step-by-Step Setup

### 1. Install Node.js
Make sure you have Node.js installed (v16 or higher):
```bash
node --version
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Get Your Discord Token

**Method 1: Browser (Recommended)**
1. Open Discord in Chrome/Firefox (not the app)
2. Press `F12` to open Developer Tools
3. Click on the `Application` tab (Chrome) or `Storage` tab (Firefox)
4. Expand `Local Storage` on the left sidebar
5. Click on `https://discord.com`
6. Find the row with key `token`
7. Double-click the value and copy it (without the quotes)

**Method 2: Using Browser Console**
1. Open Discord in your browser
2. Press `Ctrl+Shift+J` (Windows) or `Cmd+Option+J` (Mac)
3. Paste this code and press Enter:
```javascript
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
```
4. Copy the token that appears

### 4. Get Server and Channel IDs

1. Open Discord Settings
2. Go to `Advanced` and enable `Developer Mode`
3. Close Settings
4. Right-click on your server name → `Copy ID` (this is your GUILD_ID)
5. Right-click on the voice channel → `Copy ID` (this is your CHANNEL_ID)

### 5. Create .env File
```bash
cp .env.example .env
```

Edit `.env` file:
```env
DISCORD_TOKEN=YOUR_TOKEN_HERE
GUILD_ID=YOUR_SERVER_ID_HERE
CHANNEL_ID=YOUR_VOICE_CHANNEL_ID_HERE
WEB_PORT=3000
```

### 6. Run the Script
```bash
npm start
```

You should see:
```
🚀 Starting Discord VC 24/7 User Account Script...
⚠️  WARNING: Selfbots violate Discord ToS. For educational use only!
🌐 Web dashboard running at http://localhost:3000
✅ Logged in as YourUsername#1234
📍 Target Guild: 123456789
📍 Target Channel: 987654321
🔊 Connecting to voice channel: General
✅ Voice connection is ready
💓 Heartbeat: Connection alive (ready)
```

### 7. Open Dashboard
Open your browser and go to:
```
http://localhost:3000
```

## Features in the Dashboard

- **Real-time Status**: See connection status with color-coded indicator
- **Uptime Counter**: Track how long you've been connected
- **Reconnection Stats**: Monitor reconnection attempts
- **Connection Info**: View current channel, user, and server
- **Manual Reconnect**: Force reconnect if needed

## Tips for Staying Undetected

1. **Use a dummy/alt account** - Never use your main account
2. **Don't spam** - The script already has rate limiting built-in
3. **Natural patterns** - Script is muted and uses exponential backoff
4. **Monitor logs** - Watch for any errors or issues
5. **Be reasonable** - Don't stay connected 24/7 for months

## Troubleshooting

### Error: "Invalid token"
- Double-check your token in the .env file
- Make sure there are no extra spaces or quotes
- Token might have expired, get a new one

### Error: "Guild not found"
- Make sure you're a member of that server
- Verify the GUILD_ID is correct

### Error: "Channel not found"
- Verify the CHANNEL_ID is correct
- Make sure it's a voice channel (not text)
- Check if you have permission to join that channel

### Bot disconnects frequently
- Check your internet connection
- Look at console logs for specific errors
- Discord might be rate limiting you

### Dashboard won't load
- Check if port 3000 is already in use
- Try changing WEB_PORT in .env to a different port (e.g., 8080)
- Make sure the script is still running

## Safety Reminders

⚠️ **IMPORTANT**:
- This violates Discord's Terms of Service
- Your account CAN be banned
- Use ONLY with dummy/test accounts
- For educational purposes ONLY
- No guarantee of "zero ban risk"

## Support

If you encounter issues:
1. Check the console logs for error messages
2. Verify all IDs and tokens are correct
3. Make sure you have the latest version of Node.js
4. Try with a fresh .env file

## License

MIT - For educational purposes only
