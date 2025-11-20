# Discord Voice Channel 24/7 Script with Web Dashboard

⚠️ **WARNING: FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY**

This tool is designed for educational purposes to understand Discord's API and selfbot mechanisms. Using selfbots violates Discord's Terms of Service and can result in account termination.

## Features

- ✅ Stays connected to Discord voice channel 24/7
- ✅ User account (selfbot) support
- ✅ Beautiful web dashboard for monitoring
- ✅ Auto-reconnection with exponential backoff
- ✅ Natural behavior patterns to minimize detection risk
- ✅ Real-time stats and connection monitoring
- ✅ Single file implementation

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/Tanmayop9/dc-tools.git
cd dc-tools
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
- `DISCORD_TOKEN`: Your Discord user account token
- `GUILD_ID`: Server ID where you want to join
- `CHANNEL_ID`: Voice channel ID to stay in
- `WEB_PORT`: Port for web dashboard (default: 3000)

### How to Get Your Discord Token

⚠️ **Keep your token private! Never share it with anyone.**

1. Open Discord in your web browser (not the app)
2. Press `F12` to open Developer Tools
3. Go to the `Application` or `Storage` tab
4. Navigate to `Local Storage` → `https://discord.com`
5. Find the key named `token` and copy its value (without quotes)

### How to Get Guild ID and Channel ID

1. Enable Developer Mode in Discord:
   - User Settings → Advanced → Enable Developer Mode
2. Right-click on the server name and click "Copy ID" (Guild ID)
3. Right-click on the voice channel and click "Copy ID" (Channel ID)

## Usage

1. **Start the script**
```bash
npm start
```

2. **Access the web dashboard**
Open your browser and go to: `http://localhost:3000`

The dashboard will show:
- Connection status
- Uptime
- Reconnection count
- Current channel and user info
- Manual reconnect button

## How It Works

The script uses:
- `discord.js-selfbot-v13` for user account support
- `@discordjs/voice` for voice connection management
- `express` for the web dashboard
- Auto-reconnection with exponential backoff to handle disconnections
- Natural behavior patterns to minimize ban risk

## Safety Features

- ✅ Self-mute enabled (no audio transmission)
- ✅ Exponential backoff for reconnections
- ✅ No spam or excessive API calls
- ✅ Natural connection patterns
- ✅ Proper error handling

## Important Notes

1. **Account Safety**: Use a dummy/alt account for testing
2. **Ban Risk**: While the script implements safety measures, there is NO guarantee of zero ban risk
3. **Terms of Service**: This violates Discord's ToS - use at your own risk
4. **Educational Only**: This is for learning about Discord's API and bot mechanisms

## Troubleshooting

**Connection Issues:**
- Verify your token is correct
- Make sure the account has access to the server and channel
- Check that the channel ID is a voice channel

**Bot Disconnects:**
- Check console logs for errors
- Use the dashboard to monitor reconnection attempts
- Ensure stable internet connection

**Dashboard Not Loading:**
- Check if the port is already in use
- Try changing WEB_PORT in .env file

## License

MIT License - For educational purposes only

## Disclaimer

This tool is provided for educational and research purposes only. The authors and contributors are not responsible for any misuse or damage caused by this tool. Using selfbots violates Discord's Terms of Service and may result in account termination. Use at your own risk.