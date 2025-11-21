# dc-tools

Discord Account Creator - For Educational Purposes Only

## 📚 Documentation

- 🚀 **[Quick Start Guide](QUICKSTART.md)** - Get your first account in 5 minutes!
- 📱 **[Termux Setup Guide](TERMUX_SETUP.md)** - Complete Termux installation
- ⚡ **[Advanced Features](ADVANCED_FEATURES.md)** - Professional features guide
- 🤖 **[Bot Authorizer Guide](BOT_AUTHORIZER.md)** - Automatically add bots to guilds
- 📖 **[Full README](#)** - You are here!

## ⚠️ Disclaimer

This tool is provided for **educational purposes only**. Creating multiple Discord accounts or automating account creation may violate Discord's Terms of Service. Use at your own risk. The authors are not responsible for any misuse of this tool.

## 🎯 Recommended for Termux Users

**Use `discord_creator_free.py` for 100% FREE manual CAPTCHA solving!**
- No paid services needed
- Browser opens automatically for CAPTCHA
- Just solve CAPTCHA when prompted (takes 10-30 seconds)
- Everything else is fully automatic
- 📖 **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes!
- 📖 **[Complete Termux Setup](TERMUX_SETUP.md)** - Full installation guide

## 🎯 Three Versions Available

### 🆓 FREE Version (`discord_creator_free.py`) ⭐ RECOMMENDED FOR TERMUX
**100% FREE - No paid services!**
- Manual CAPTCHA solving via browser
- Browser opens automatically on Termux
- Just solve CAPTCHA when prompted
- Perfect for Termux users
- See [TERMUX_SETUP.md](TERMUX_SETUP.md)

### Basic Version (`discord_creator.py`)
Simple and straightforward account creation
- No CAPTCHA support
- May fail if CAPTCHA required

### Ultra Advanced Version (`discord_creator_advanced.py`)
Professional-grade automation with advanced features
- Supports paid CAPTCHA solvers OR free manual solving
- Proxy support, multi-threading, database, etc.

## Features

### 🆓 FREE Version Features (BEST FOR TERMUX)
- ✅ **100% FREE** - No paid services required
- ✅ **Manual CAPTCHA Solving** - Browser opens automatically
- ✅ **Termux Optimized** - Uses termux-open-url
- ✅ **Fully Automatic** - Except for solving CAPTCHA
- ✅ **Robust Email Retrieval** - Automatic retry with fallback (NEW!)
- ✅ Email verification using free temporary email
- ✅ Token extraction and storage
- ✅ Beautiful colored terminal output
- ✅ Multiple account creation support
- ✅ Easy to use - just solve CAPTCHA when browser opens

### Basic Version
- ✅ Fully automatic Discord account creation
- ✅ **Robust Email Retrieval** - Automatic retry with fallback (NEW!)
- ✅ Email verification using free temporary email service (1secmail)
- ✅ Token extraction and storage
- ✅ Works on Termux (Android)
- ✅ No GUI dependencies
- ✅ Multiple account creation support
- ✅ Saves account details and tokens
- ⚠️ No CAPTCHA support (may fail)

### Ultra Advanced Version Features 🚀
- ✅ **Multi-Provider Email Support** (1secmail, TempMail, GuerrillaMail)
- ✅ **Automatic Email Service Fallback** - Tries all services with retry (NEW!)
- ✅ **CAPTCHA Solving** (2captcha, Anti-Captcha integration)
- ✅ **Proxy Support** (HTTP/HTTPS/SOCKS5 with rotation)
- ✅ **Advanced Fingerprinting** (Anti-detection measures)
- ✅ **User Agent Rotation** (Multiple realistic agents)
- ✅ **Smart Retry Mechanism** (Exponential backoff with 3 attempts per service)
- ✅ **Profile Customization** (Bio, avatar support)
- ✅ **Token Validation** (Real-time verification)
- ✅ **Database Integration** (SQLite for account management)
- ✅ **Multi-Threading** (Parallel account creation)
- ✅ **Auto Server Joining** (Join Discord servers automatically)
- ✅ **Rich Terminal Output** (Colored, professional display)
- ✅ **Configuration File** (JSON-based settings)
- ✅ **Account Manager** (Dedicated management tool)

## Requirements

- Python 3.6+
- Internet connection

## Installation

### On Termux (Android)

```bash
# Update packages
pkg update && pkg upgrade

# Install Python
pkg install python

# Install git (if not already installed)
pkg install git

# Clone the repository
git clone https://github.com/Tanmayop9/dc-tools.git
cd dc-tools

# Install dependencies
pip install -r requirements.txt
```

### On Linux/macOS

```bash
# Clone the repository
git clone https://github.com/Tanmayop9/dc-tools.git
cd dc-tools

# Install dependencies
pip3 install -r requirements.txt
```

## Usage

### 🆓 FREE Version (RECOMMENDED FOR TERMUX) ⭐

```bash
# Run the FREE version with manual CAPTCHA solving
python discord_creator_free.py
```

**What happens:**
1. Script generates random credentials
2. Gets temporary email automatically
3. Registers Discord account
4. **If CAPTCHA required**: Browser opens automatically
5. You solve CAPTCHA in browser (10-30 seconds)
6. Click submit button
7. Script continues automatically
8. Email verification happens
9. Token saved to `tokens.txt`

**Perfect for Termux!** See complete guide: [TERMUX_SETUP.md](TERMUX_SETUP.md)

### Basic Version

```bash
# Run the basic account creator (no CAPTCHA support)
python discord_creator.py
```

The script will:
1. Ask how many accounts you want to create
2. Generate random credentials for each account
3. Create a temporary email address
4. Register the Discord account
5. Attempt to verify the email automatically
6. Save the token to `tokens.txt`
7. Save full account details to `accounts.txt`

⚠️ May fail if CAPTCHA is required

### Ultra Advanced Version 🚀

```bash
# First, configure settings (optional)
nano config.json

# Run the advanced creator
python discord_creator_advanced.py
```

**Advanced Features Setup:**

1. **Configure Proxies** (Optional but recommended)
```bash
# Create proxy list
cp proxies.txt.example proxies.txt
nano proxies.txt  # Add your proxies

# Enable in config.json
# Set "proxy": {"enabled": true}
```

2. **Setup CAPTCHA Solver** (Optional)
```bash
# Get API key from 2captcha.com or anti-captcha.com
# Add to config.json:
# "captcha": {"enabled": true, "api_key": "YOUR_KEY"}
```

3. **Enable Advanced Features**
```bash
# Edit config.json to enable:
# - Multi-threading
# - Database storage
# - Profile customization
# - Auto server joining
```

### Account Manager Tool

```bash
# Manage your created accounts
python account_manager.py
```

Features:
- List all accounts
- Validate tokens
- Export to various formats
- View statistics
- Delete invalid accounts

### Bot Authorizer Tool 🤖

```bash
# Add bots to guilds automatically
python bot_authorizer.py
```

Features:
- OAuth2 bot authorization
- Automatic bot-to-guild addition
- Customizable permissions
- Support for multiple Discord endpoints
- Educational/research purposes only
- See [BOT_AUTHORIZER.md](BOT_AUTHORIZER.md) for details

## Output Files

- **tokens.txt** - Contains only the tokens (one per line)
- **accounts.txt** - Contains full account details (email, username, password, token)

## 📖 Documentation

- **[ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)** - Complete guide to advanced features
- **[config.json](config.json)** - Configuration file with all options
- **[example_output.txt](example_output.txt)** - Example of what to expect

## Notes

### Basic Version
- Uses free temporary email service (1secmail.com)
- Email verification may take up to 5 minutes
- Some accounts may require manual verification
- Rate limiting: 30 seconds between accounts
- Works completely in terminal (no GUI required)

### Advanced Version
- Supports multiple email providers with automatic fallback
- CAPTCHA solving increases success rate (requires paid API)
- Proxy support prevents IP bans (highly recommended for bulk creation)
- Multi-threading speeds up bulk creation
- Database enables better account management
- Configurable delays and retry mechanisms
- See [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) for full documentation

## Troubleshooting

### "Failed to get email"
- **NEW**: Improved error handling with automatic retry and fallback
- The script now automatically retries 3 times with exponential backoff
- If all attempts fail, it falls back to offline email generation
- Check your internet connection if you see this error repeatedly
- The temporary email service (1secmail.com) might be temporarily unavailable
- Advanced version automatically tries alternative services (tempmail, guerrillamail)

### "Failed to get fingerprint"
- Check your internet connection
- Discord API might be temporarily unavailable

### "Registration failed"
- Discord might have implemented new anti-bot measures
- Try again later or check if there are updates to the script

### "Email verification timeout"
- The temporary email service might be slow
- The account is still created but may have limited functionality
- Check `accounts.txt` for credentials

### Network Connection Issues
- The script includes robust error handling for network failures
- Retry logic with exponential backoff (2s, 4s delays)
- Automatic fallback to alternative email services (advanced version)
- Offline email generation as last resort

## Legal Notice

This tool is for educational and research purposes only. Automated account creation may violate Discord's Terms of Service. Users are responsible for ensuring their use complies with all applicable laws and terms of service.

## License

MIT License - Use at your own risk