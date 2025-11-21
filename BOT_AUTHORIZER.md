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
2. **OAuth2 URL** - The bot's authorization URL
3. **Guild ID** - The guild where you want to add the bot (default: 283939)
4. **Permissions** - Permission level for the bot (default: 0)
5. **LLM CAPTCHA** - Whether to use free AI CAPTCHA solving (recommended: Yes)

### Example

```
Enter your Discord account token:
> YOUR_TOKEN_HERE

Enter the bot OAuth2 authorization URL:
> https://discord.com/api/oauth2/authorize?client_id=123456789&scope=bot&permissions=8

Enter the Guild ID (default: 283939):
> 283939

Enter permissions (default: 0 for no permissions):
> 8

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

1. **Validation**: Validates the OAuth2 URL format
2. **Parsing**: Extracts query parameters from the URL
3. **Authorization**: Sends a POST request to Discord's OAuth2 endpoint
4. **Response**: Returns the authorization result

## OAuth2 URL Format

The script accepts OAuth2 URLs in the following format:

```
https://discord.com/api/oauth2/authorize?client_id=BOT_ID&scope=bot&permissions=PERMISSIONS
```

Supported Discord domains:
- `discord.com` (stable)
- `canary.discord.com` (canary)
- `ptb.discord.com` (public test build)

## Parameters

### Required Parameters (from OAuth2 URL)
- `client_id`: The bot's application ID
- `scope`: Authorization scope (usually "bot")

### Optional Parameters
- `permissions`: Permission integer (default: "0")
- `guild_id`: Target guild ID (default: "283939")
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
