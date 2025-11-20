# Quick Start Guide - 5 Minutes to Your First Account

The fastest way to create Discord accounts on Termux!

## 🚀 Super Quick Start (Termux)

```bash
# 1. Install dependencies
pkg install python git termux-api

# 2. Clone repo
git clone https://github.com/Tanmayop9/dc-tools.git
cd dc-tools

# 3. Install Python packages
pip install requests

# 4. Run it!
python discord_creator_free.py
```

That's it! 🎉

## 📱 What Happens

1. **Script starts** - Shows cool banner
2. **Enter number of accounts** - Type 1 and press Enter
3. **Script generates credentials** - Automatic
4. **Gets temp email** - Automatic
5. **Registers account** - Automatic
6. **CAPTCHA appears** - Browser opens automatically
7. **You solve CAPTCHA** - Takes 10-30 seconds
8. **Click Submit** - In browser
9. **Email verification** - Automatic
10. **Done!** - Token saved to `tokens.txt`

## 🎯 First Run Example

```bash
$ python discord_creator_free.py

╔══════════════════════════════════════════════════════════════════╗
║      Discord Account Creator - 100% FREE VERSION                ║
║      No Paid Services | Works on Termux | Manual CAPTCHA        ║
╚══════════════════════════════════════════════════════════════════╝

How many accounts to create? (default: 1): 1

[*] Will create 1 account(s)
[*] You may need to solve CAPTCHA for each account
[*] Browser will open automatically when CAPTCHA is required

Press ENTER to start...
```

Press ENTER and watch the magic happen!

## ✅ What You Get

After successful creation, you'll have:

1. **tokens.txt** - Contains your Discord token
   ```
   MTIzNDU2Nzg5MDEyMzQ1Njc4OTAuGHiJ8K.dQw4w9WgXcQ...
   ```

2. **accounts.txt** - Contains full account details
   ```
   ============================================================
   Created: 2025-11-20 13:20:00
   Email: user123@1secmail.com
   Username: cooluser1234
   Password: aB3$xY9#mN2@pQ5!
   Token: MTIzNDU2Nzg5MDEyMzQ1Njc4OTAuGHiJ8K.dQw4w9WgXcQ...
   Verified: Yes
   ============================================================
   ```

## 🔧 If Browser Doesn't Open

Don't worry! Script shows you the URL:

```
[*] If browser doesn't open automatically, open this URL manually:
    http://localhost:8888/
```

Just copy and paste that URL into any browser on your phone!

## 💡 Pro Tips

### Tip 1: Multiple Accounts
```bash
$ python discord_creator_free.py
How many accounts to create? (default: 1): 5
```

Creates 5 accounts with 30-second delays between them.

### Tip 2: Keep Screen On
While solving CAPTCHA, keep your phone screen on. You can:
- Use split-screen mode (Termux + Browser)
- Or switch between apps quickly

### Tip 3: Good Internet
Use WiFi for best results. Mobile data works too, just slower.

### Tip 4: Save Tokens Safely
```bash
# Backup your tokens
cp tokens.txt tokens_backup.txt

# Or move to phone storage
termux-setup-storage
cp tokens.txt ~/storage/shared/
```

## 🎓 CAPTCHA Solving Guide

When CAPTCHA appears:

1. **Browser opens** showing CAPTCHA box
2. **Click checkbox** "I am human"
3. **Solve puzzle** (if images appear)
4. **Click Submit** button
5. **Success page** appears
6. **Return to Termux** - script continues

Takes only 10-30 seconds!

## ❓ Troubleshooting

### Problem: "Module not found"
```bash
pip install requests
```

### Problem: "Browser not opening"
```bash
# Install Termux:API
pkg install termux-api

# Also install Termux:API app from F-Droid
```

### Problem: "Connection refused"
Open the URL manually in browser: `http://localhost:8888/`

### Problem: "Permission denied"
```bash
chmod +x discord_creator_free.py
```

## 📊 Success Checklist

- [x] Termux installed (from F-Droid)
- [x] Python installed (`pkg install python`)
- [x] Git installed (`pkg install git`)
- [x] Repository cloned
- [x] Dependencies installed (`pip install requests`)
- [x] Script runs without errors
- [x] Browser opens for CAPTCHA
- [x] CAPTCHA solved successfully
- [x] Token saved to `tokens.txt`

## 🎉 You're Done!

You now have:
- ✅ Working Discord account
- ✅ Token for API access
- ✅ Full credentials saved
- ✅ Email verified (usually)

Create more accounts anytime by running:
```bash
python discord_creator_free.py
```

## 📚 Learn More

- **Termux Guide**: [TERMUX_SETUP.md](TERMUX_SETUP.md)
- **Advanced Features**: [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)
- **Full README**: [README.md](README.md)

## 🆘 Need Help?

1. Read [TERMUX_SETUP.md](TERMUX_SETUP.md) for detailed troubleshooting
2. Check error messages carefully
3. Make sure all dependencies are installed
4. Try again - sometimes Discord servers are slow

## ⚡ Advanced Usage

Once comfortable, try:

```bash
# Use advanced version with all features
python discord_creator_advanced.py

# Manage your accounts
python account_manager.py
```

Happy account creating! 🚀
