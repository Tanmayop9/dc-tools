# dc-tools

Ultra Advanced Discord Bot Authorizer - For Educational Purposes Only

## 📚 Documentation

- 🤖 **[Bot Authorizer Guide](BOT_AUTHORIZER.md)** - Ultra advanced bot authorization with free CAPTCHA solving
- 🧠 **[Free LLM CAPTCHA Solver](LLM_CAPTCHA.md)** - AI-powered CAPTCHA solving (100% free!)
- ⚡ **[Advanced Features](ADVANCED_FEATURES.md)** - Professional features guide
- 🎯 **[Interactive CAPTCHA](INTERACTIVE_CAPTCHA.md)** - Manual CAPTCHA solving guide
- 📖 **[Full README](#)** - You are here!

## ⚠️ Disclaimer

This tool is provided for **educational purposes only**. Automating bot authorization may violate Discord's Terms of Service. Use at your own risk. The authors are not responsible for any misuse of this tool.

## 🎯 Main Feature: Ultra Advanced Bot Authorizer

**The world's fastest and most advanced FREE Discord bot authorization tool!**

### ⚡ Key Features
- 🚀 **Ultra-Fast Concurrent Authorization** - Process multiple guilds simultaneously (up to 5x faster!)
- 🧠 **Multi-Method Free CAPTCHA Solving** - AI Vision, OCR, Pattern Recognition, Browser automation
- 🔄 **Smart Retry Logic** - Exponential backoff with automatic recovery
- ⚙️ **Connection Pooling** - Optimized session management for peak performance
- 📊 **Performance Metrics** - Real-time statistics and detailed analytics
- 🎯 **100% FREE** - No paid services required, ever!

### 🆓 Free CAPTCHA Solver Chain
Our ultra-advanced solver tries multiple methods in order:
1. **Cache Lookup** - Instant if previously solved (fastest!)
2. **HuggingFace BLIP-2** - Advanced AI vision model
3. **HuggingFace ViT-GPT2** - Image-to-text captioning
4. **EasyOCR** - Multi-language OCR with high accuracy
5. **Tesseract Advanced** - Multiple preprocessing techniques
6. **Pattern Recognition** - ML-based pattern matching
7. **Local Ollama** - Local LLM vision models
8. **Browser Automation** - Manual solving (100% reliable)

## 🎯 Perfect for All Users

**Works on Termux, Linux, macOS, and Windows!**
- Ultra-fast concurrent processing
- Multiple free CAPTCHA solving methods
- Smart rate limiting and retry logic
- Comprehensive performance tracking
- 100% free - no paid services required

## Features

### 🚀 Ultra Advanced Bot Authorizer Features
- ✅ **Ultra-Fast Concurrent Processing** - Authorize multiple guilds simultaneously (5 workers)
- ✅ **100% FREE CAPTCHA Solving** - Multi-method solver chain with 8 different techniques
- ✅ **AI Vision Models** - HuggingFace BLIP-2, ViT-GPT2 for automatic solving
- ✅ **Advanced OCR** - EasyOCR + Tesseract with preprocessing
- ✅ **Pattern Recognition** - ML-based CAPTCHA analysis
- ✅ **Local LLM Support** - Ollama vision models integration
- ✅ **Browser Automation** - Manual solving fallback (always works!)
- ✅ **Smart Caching** - Never solve the same CAPTCHA twice
- ✅ **Connection Pooling** - Optimized session management
- ✅ **Proxy Rotation** - Support for proxy lists
- ✅ **Smart Retry Logic** - Exponential backoff with automatic recovery
- ✅ **Rate Limit Handling** - Intelligent delay management
- ✅ **Performance Metrics** - Real-time statistics and analytics
- ✅ **Beautiful Terminal Output** - Colored, professional display
- ✅ **Concurrent Speedup** - Up to 5x faster than sequential processing
- ✅ **Session Persistence** - Resume failed authorizations
- ✅ **Comprehensive Error Handling** - Detailed logging and recovery

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

### 🤖 Ultra Advanced Bot Authorizer ⭐ **MAIN FEATURE**

```bash
# Run the ultra advanced bot authorizer
python bot_authorizer.py
```

**What happens:**
1. Enter your Discord user token
2. Enter the bot's Client ID
3. Enter permissions (or use default: 0)
4. Choose authorization mode:
   - **Option 1**: Add bot to ALL servers (ultra-fast concurrent mode!)
   - **Option 2**: Add bot to a specific server
5. Enable Ultra Advanced Free CAPTCHA solver (recommended: Yes)
6. Enable ultra-fast concurrent mode (recommended: Yes for multiple guilds)
7. If CAPTCHA appears, the solver automatically tries 8 different methods
8. Bot is authorized to your guilds!

**Features:**
- ⚡ **Ultra-Fast**: Process multiple guilds concurrently (up to 5x speedup!)
- 🧠 **Smart CAPTCHA**: 8 different free solving methods with automatic fallback
- 📊 **Performance Metrics**: See detailed statistics on completion
- 🔄 **Auto-Retry**: Intelligent retry with exponential backoff
- 💾 **Caching**: Never solve the same CAPTCHA twice

**Example Output:**
```
Using ULTRA-FAST concurrent mode (5 workers)!
[1/10] Server Name 1 - Success! (2.34s)
[2/10] Server Name 2 - Success! (1.89s)
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           AUTHORIZATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Successful: 10/10
* Total time: 12.45s
* Average per guild: 1.24s
✓ Concurrent speedup: 4.2x faster!
```

### 🛠️ Configuration (Optional)

Create a `proxies.txt` file to enable proxy rotation:
```bash
# Create proxy list
cp proxies.txt.example proxies.txt
nano proxies.txt  # Add your proxies (one per line)
# Format: ip:port or user:pass@ip:port
```

The bot authorizer will automatically use proxies if the file exists.

## 📖 Documentation

- **[BOT_AUTHORIZER.md](BOT_AUTHORIZER.md)** - Detailed bot authorization guide
- **[LLM_CAPTCHA.md](LLM_CAPTCHA.md)** - Free LLM CAPTCHA solver documentation
- **[INTERACTIVE_CAPTCHA.md](INTERACTIVE_CAPTCHA.md)** - Manual CAPTCHA solving guide
- **[config.json](config.json)** - Configuration file with all options

## 🔧 Advanced Configuration

The bot authorizer supports advanced configuration through environment variables and proxies:

### Proxy Support
Create a `proxies.txt` file with one proxy per line:
```
ip:port
user:pass@ip:port
```

### Concurrent Workers
Adjust the number of concurrent workers (default: 5):
- More workers = faster processing
- Fewer workers = less likely to hit rate limits
- Recommended: 3-5 workers for best balance

### CAPTCHA Solver Customization
The ultra-advanced solver tries 8 methods in order:
1. Cache (instant)
2. HuggingFace BLIP-2
3. HuggingFace ViT-GPT2
4. EasyOCR
5. Tesseract Advanced
6. Pattern Recognition
7. Local Ollama (if installed)
8. Browser Manual (always works)

## Troubleshooting

### "CAPTCHA solving failed"
Don't worry! The solver tries 8 different methods:
1. Make sure you have internet connection (for AI models)
2. If all automatic methods fail, browser will open for manual solving
3. Install optional packages for better success:
   ```bash
   pip install easyocr pytesseract opencv-python-headless
   # For Ollama support: install from ollama.ai
   ```

### "Rate limit error"
- The bot automatically handles rate limits with exponential backoff
- Reduce concurrent workers if you see many rate limit errors
- Add delays between requests in sequential mode

### "Authorization failed"
- Check that your Discord token is valid
- Make sure you have "Manage Server" permission on the guild
- Verify the bot's Client ID is correct
- Some guilds may have restrictions on bot addition

### "Connection error"
- Check your internet connection
- If using proxies, verify they are working
- Discord API might be temporarily unavailable (retry later)

### Performance Issues
- Install optional AI/OCR packages for faster CAPTCHA solving
- Use concurrent mode for multiple guilds (much faster!)
- Enable proxy rotation to avoid IP-based throttling
- Consider running on a server with better internet connection

## Legal Notice

This tool is for educational and research purposes only. Automated account creation may violate Discord's Terms of Service. Users are responsible for ensuring their use complies with all applicable laws and terms of service.

## License

MIT License - Use at your own risk