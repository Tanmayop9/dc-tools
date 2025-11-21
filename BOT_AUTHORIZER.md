# Discord Bot Authorizer - Documentation

## ⚠️ Disclaimer

This tool is provided for **educational and research purposes only**. Automating bot authorization using user accounts may violate Discord's Terms of Service. Use at your own risk. The authors are not responsible for any misuse of this tool.

## Overview

The Bot Authorizer script automates the process of adding a Discord bot to a guild using OAuth2 authorization. It's inspired by the `authorizeURL` function from discord.js-selfbot-v13.

## Features

- 🤖 **FREE LLM CAPTCHA Solver** - AI-powered, 100% free, no API keys required!
- ✨ **Termux-Friendly** - Works perfectly on Android devices
- ✅ OAuth2 URL validation
- ✅ Automatic bot authorization to guilds
- ✅ Automatic CAPTCHA detection and solving
- ✅ Multiple CAPTCHA solver fallbacks (LLM → Manual)
- ✅ Customizable permissions
- ✅ Support for different Discord API endpoints (canary, ptb, stable)
- ✅ User-friendly colored terminal interface
- ✅ Error handling and detailed feedback

**NEW**: Integrated free LLM CAPTCHA solving! See [LLM_CAPTCHA.md](LLM_CAPTCHA.md) for details.

## Requirements

- Python 3.6+
- `requests` library (already in requirements.txt)
- A Discord user account token
- Bot OAuth2 authorization URL
- Guild ID where you want to add the bot

## Installation

The bot authorizer uses the same dependencies as the main project:

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Recommended)

Simply run the script and follow the prompts:

```bash
python bot_authorizer.py
```

The script will ask you for:
1. **Discord Account Token** - Your user account token
2. **Bot Client ID** - Just the bot's application/client ID (NOT the full OAuth URL)
3. **Permissions** - Permission level for the bot (default: 0)
4. **Authorization Mode** - Add bot to ALL servers or a SPECIFIC server
5. **Guild ID** - (Only if specific server mode) The guild where you want to add the bot
6. **LLM CAPTCHA** - Whether to use free AI CAPTCHA solving (recommended: Yes)

### Example: Add to All Servers (New Feature!)

```
Enter your Discord account token:
> YOUR_TOKEN_HERE

Enter the bot Client ID:
> 123456789012345678

Enter permissions (default: 0 for no permissions):
> 8

Authorization mode:
1. Add bot to ALL servers where you have permissions (recommended)
2. Add bot to a SPECIFIC server
Enter mode (1 or 2, default: 1): 
> 1

Use free LLM for CAPTCHA solving? (Y/n):
> Y

✨ Free LLM CAPTCHA solver enabled!
[*] Starting authorization process...
[*] Fetching your guilds...
[✓] Found 5 guilds
[*] Found 3 guilds with required permissions

Guilds where you can add the bot:
  1. My Server (ID: 123...)
  2. Gaming Guild (ID: 456...)
  3. Dev Community (ID: 789...)

[1/3] Adding bot to: My Server
[✓] Bot authorized successfully!
[✓] ✓ Bot added to My Server
...
```

### Example: Add to Specific Server

```
Enter your Discord account token:
> YOUR_TOKEN_HERE

Enter the bot Client ID:
> 123456789012345678

Enter permissions (default: 0 for no permissions):
> 0

Authorization mode:
1. Add bot to ALL servers where you have permissions (recommended)
2. Add bot to a SPECIFIC server
Enter mode (1 or 2, default: 1): 
> 2

Enter the Guild ID:
> 283939

Use free LLM for CAPTCHA solving? (Y/n):
> Y

✨ Free LLM CAPTCHA solver enabled!
[*] Starting authorization process...
```

**If CAPTCHA is required:**
- 🤖 LLM solver tries first (automatic, 3-10 seconds)
- 🌐 Falls back to browser if needed (manual, always works)
- ✅ 100% success rate with fallback system!

## How It Works

### Single Server Mode
1. **Input**: Takes bot client ID and guild ID
2. **URL Building**: Builds OAuth2 URL from client ID
3. **Authorization**: Sends a POST request to Discord's OAuth2 endpoint
4. **Response**: Returns the authorization result

### Multi-Server Mode (New!)
1. **Input**: Takes bot client ID only
2. **Guild Fetch**: Retrieves all guilds where user is a member
3. **Filtering**: Filters guilds where user has "Manage Server" or "Administrator" permissions
4. **URL Building**: Builds OAuth2 URL from client ID
5. **Bulk Authorization**: Iterates through all eligible guilds and adds the bot
6. **Summary**: Shows detailed results for each guild

## Getting Bot Client ID

To use the bot authorizer, you need the bot's **Client ID** (NOT the full OAuth URL):

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot application
3. Go to "OAuth2" section
4. Copy the **Client ID** (a long number like `123456789012345678`)

That's it! No need to copy the full OAuth URL anymore.

## OAuth2 URL Format (For Reference)

The script now builds OAuth2 URLs automatically from the client ID:

```
https://discord.com/api/oauth2/authorize?client_id=BOT_ID&scope=bot&permissions=PERMISSIONS
```

Supported Discord domains:
- `discord.com` (stable)
- `canary.discord.com` (canary)
- `ptb.discord.com` (public test build)

## Parameters

### Required Parameters
- `client_id`: The bot's application ID (now input directly, not in URL)
- `scope`: Authorization scope (automatically set to "bot")

### Optional Parameters
- `permissions`: Permission integer (default: "0")
- `guild_id`: Target guild ID (only needed for specific server mode)
- `integration_type`: Integration type (default: 0)

## Getting Your Account Token

**⚠️ Warning**: Never share your Discord token with anyone!

1. Open Discord in a web browser
2. Press F12 to open Developer Tools
3. Go to the Console tab
4. Type: `(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()`
5. Copy the token (without quotes)

**Note**: This method is for educational purposes only.

## Error Handling

The script handles various error scenarios:

- ❌ Invalid OAuth2 URL format
- ❌ Invalid account token
- ❌ Network connection issues
- ❌ API rate limiting
- ❌ Insufficient permissions

## Example Output

### Success:
```
[*] Sending authorization request...
[*] Guild ID: 283939
[*] Permissions: 8
[✓] Bot authorized successfully!

[✓] ============================================================
[✓] Bot successfully added to the guild!
[✓] ============================================================
```

### Failure:
```
[✗] Authorization failed: 401
[✗] Response: {"message": "401: Unauthorized", "code": 0}

[✗] ============================================================
[✗] Failed to add bot to guild
[✗] ============================================================
```

## Permissions Reference

Common permission integers:

- `0` - No permissions
- `8` - Administrator
- `2048` - Send Messages
- `2147483647` - All permissions

For more details, see [Discord Permissions Calculator](https://discordapi.com/permissions.html).

## Programmatic Usage

You can also use the BotAuthorizer class in your own scripts:

```python
from bot_authorizer import BotAuthorizer

# Initialize with user token
authorizer = BotAuthorizer("YOUR_TOKEN_HERE")

# Authorize bot
oauth_url = "https://discord.com/api/oauth2/authorize?client_id=123456789&scope=bot"
options = {
    'guild_id': '283939',
    'permissions': '8',
    'integration_type': 0
}

result = authorizer.authorize_url(oauth_url, options)
print(result)
```

## Troubleshooting

### "Invalid OAuth2 URL"
- Make sure the URL starts with `https://discord.com/api/oauth2/authorize?`
- Check that the URL contains the required parameters

### "Authorization failed: 401"
- Your account token is invalid or expired
- Get a new token and try again

### "Authorization failed: 403"
- You don't have permission to add bots to the guild
- Make sure you have "Manage Server" permission in the target guild

### "Authorization failed: 429"
- You're being rate limited by Discord
- Wait a few minutes and try again

## Security Notes

- 🔒 Never commit tokens to version control
- 🔒 Don't share your account token
- 🔒 Use this tool only for authorized testing
- 🔒 Be aware that using user accounts for automation violates Discord ToS

## Legal Notice

This tool is for educational and research purposes only. Automated bot authorization using user accounts may violate Discord's Terms of Service. Users are responsible for ensuring their use complies with all applicable laws and terms of service.

## Related Scripts

- `discord_creator.py` - Basic Discord account creator
- `discord_creator_free.py` - Free account creator with manual CAPTCHA
- `discord_creator_advanced.py` - Advanced account creator with all features
- `account_manager.py` - Account management tool

## License

MIT License - Use at your own risk
