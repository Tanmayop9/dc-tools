# dc-tools

Discord Account Creator - For Educational Purposes Only

## ⚠️ Disclaimer

This tool is provided for **educational purposes only**. Creating multiple Discord accounts or automating account creation may violate Discord's Terms of Service. Use at your own risk. The authors are not responsible for any misuse of this tool.

## Features

- ✅ Fully automatic Discord account creation
- ✅ Email verification using free temporary email service (1secmail)
- ✅ Token extraction and storage
- ✅ Works on Termux (Android)
- ✅ No GUI dependencies
- ✅ Multiple account creation support
- ✅ Saves account details and tokens

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

```bash
# Run the account creator
python discord_creator.py
```

Or make it executable:

```bash
chmod +x discord_creator.py
./discord_creator.py
```

The script will:
1. Ask how many accounts you want to create
2. Generate random credentials for each account
3. Create a temporary email address
4. Register the Discord account
5. Attempt to verify the email automatically
6. Save the token to `tokens.txt`
7. Save full account details to `accounts.txt`

## Output Files

- **tokens.txt** - Contains only the tokens (one per line)
- **accounts.txt** - Contains full account details (email, username, password, token)

## Notes

- The script uses a free temporary email service (1secmail.com)
- Email verification may take up to 5 minutes
- Some accounts may require manual verification if automatic verification fails
- Rate limiting: The script waits 30 seconds between creating multiple accounts
- Works completely in terminal (no GUI required)

## Troubleshooting

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

## Legal Notice

This tool is for educational and research purposes only. Automated account creation may violate Discord's Terms of Service. Users are responsible for ensuring their use complies with all applicable laws and terms of service.

## License

MIT License - Use at your own risk