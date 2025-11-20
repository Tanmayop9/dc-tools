# Ultra Advanced Features Documentation

## Overview

The advanced version (`discord_creator_advanced.py`) includes cutting-edge features for automated Discord account creation.

## 🚀 Advanced Features

### 1. **Multi-Provider Email Support**
- Primary: 1secmail (free, no registration)
- Fallback: TempMail, GuerrillaMail
- Automatic failover between providers
- Configurable check intervals

### 2. **CAPTCHA Solving**
- Integrated CAPTCHA solvers (2captcha, Anti-Captcha)
- Automatic hCaptcha detection and solving
- Fallback to alternative solvers
- Cost-effective solution tracking

### 3. **Proxy Support**
- HTTP/HTTPS/SOCKS5 proxy support
- Automatic proxy rotation
- Failed proxy detection
- Load balancing across proxies

### 4. **Advanced Fingerprinting**
- Browser fingerprint spoofing
- Random but realistic fingerprints
- Fallback to Discord's native fingerprints
- Anti-detection measures

### 5. **User Agent Rotation**
- 6+ realistic mobile user agents
- Automatic rotation per request
- Android and iOS variants
- Latest Chrome/Safari versions

### 6. **Smart Retry Mechanism**
- Exponential backoff
- Configurable retry attempts
- Intelligent error handling
- Rate limit detection

### 7. **Profile Customization**
- Auto-set bio from templates
- Avatar upload support
- Random birthdate generation
- Profile warming capabilities

### 8. **Token Validation**
- Real-time token verification
- Health checking
- Invalid token detection
- Automatic re-creation on failure

### 9. **Database Integration**
- SQLite database for account storage
- Query all accounts
- Status tracking (active/banned/limited)
- Timestamp logging

### 10. **Multi-Threading**
- Parallel account creation
- Configurable thread count
- Thread-safe operations
- Resource management

### 11. **Auto Server Joining**
- Automatically join specified servers
- Multiple invite support
- Delay between joins
- Success/failure tracking

### 12. **Rich Terminal Output**
- Colored output (ANSI codes)
- Progress indicators
- Clear success/error messages
- Professional formatting

## 📋 Configuration Guide

### Basic Configuration (config.json)

```json
{
  "general": {
    "max_retries": 3,              // Retry failed operations
    "retry_delay": 5,               // Seconds between retries
    "rate_limit_delay": 30,         // Delay between accounts
    "verify_tokens": true,          // Validate tokens
    "warm_accounts": false          // Simulate human behavior
  }
}
```

### Proxy Configuration

```json
{
  "proxy": {
    "enabled": true,                // Enable proxy support
    "proxy_list_file": "proxies.txt",
    "proxy_type": "http",           // http, https, or socks5
    "rotate_proxies": true          // Rotate through proxy list
  }
}
```

**Proxy File Format (proxies.txt):**
```
123.123.123.123:8080
124.124.124.124:3128
socks5://125.125.125.125:1080
127.127.127.127:8080:username:password
```

### CAPTCHA Configuration

```json
{
  "captcha": {
    "enabled": true,
    "solver": "2captcha",           // 2captcha or anticaptcha
    "api_key": "YOUR_API_KEY_HERE",
    "fallback_solver": "anticaptcha"
  }
}
```

**Supported CAPTCHA Solvers:**
- **2captcha**: https://2captcha.com (Pay per CAPTCHA)
- **Anti-Captcha**: https://anti-captcha.com (Pay per CAPTCHA)

### Email Configuration

```json
{
  "email": {
    "primary_service": "1secmail",
    "fallback_services": ["tempmail", "guerrillamail"],
    "verification_timeout": 300,    // Max wait time (seconds)
    "check_interval": 10            // Check every N seconds
  }
}
```

### Profile Customization

```json
{
  "profile": {
    "customize_profile": true,
    "upload_avatar": false,
    "avatar_folder": "avatars/",
    "set_bio": true,
    "bio_templates": [
      "Just a gamer",
      "Here to chat",
      "Gaming enthusiast",
      "Discord user"
    ]
  }
}
```

### Auto Server Joining

```json
{
  "auto_join": {
    "enabled": true,
    "server_invites": [
      "discord-invite-code-1",
      "discord-invite-code-2"
    ]
  }
}
```

### Advanced Settings

```json
{
  "advanced": {
    "fingerprint_spoofing": true,   // Spoof fingerprints
    "user_agent_rotation": true,    // Rotate user agents
    "multi_threading": true,        // Use threads
    "max_threads": 3,               // Max concurrent threads
    "use_database": true,           // Use SQLite database
    "database_file": "accounts.db"
  }
}
```

## 🎯 Usage Examples

### Basic Usage
```bash
python discord_creator_advanced.py
```

### With Custom Config
```bash
# Edit config.json first, then run:
python discord_creator_advanced.py
```

### Bulk Account Creation
```bash
# When prompted, enter number of accounts:
# How many accounts to create? 10
```

### With Proxies
1. Create `proxies.txt` with your proxies
2. Edit `config.json` to enable proxies
3. Run the script

### With CAPTCHA Solving
1. Get API key from 2captcha.com or anti-captcha.com
2. Add API key to `config.json`
3. Enable CAPTCHA solver in config
4. Run the script

## 📊 Database Features

When database is enabled, accounts are stored in SQLite:

```python
# Query accounts from Python
import sqlite3
conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM accounts WHERE verified = 1')
verified_accounts = cursor.fetchall()
```

**Database Schema:**
```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    email TEXT,
    username TEXT,
    password TEXT,
    token TEXT,
    created_at TIMESTAMP,
    verified BOOLEAN,
    status TEXT
)
```

## 🔒 Security Best Practices

1. **Never share tokens publicly**
2. **Use proxies to avoid IP bans**
3. **Enable rate limiting**
4. **Don't create too many accounts from one IP**
5. **Use CAPTCHA solver for large batches**
6. **Keep config.json secure (contains API keys)**

## 🚨 Troubleshooting

### "Failed to get fingerprint"
- Check internet connection
- Enable proxy if IP is blocked
- Try fingerprint spoofing

### "CAPTCHA required"
- Enable CAPTCHA solver in config
- Add valid API key
- Ensure sufficient balance

### "Email verification timeout"
- Increase `verification_timeout` in config
- Try different email service
- Check if emails are being received

### "Proxy connection failed"
- Verify proxy format in proxies.txt
- Test proxy connectivity
- Try different proxy type

### "Rate limited"
- Increase `rate_limit_delay`
- Use more proxies
- Reduce concurrent threads

## 📈 Performance Tips

1. **Use multi-threading for bulk creation** (3-5 threads optimal)
2. **Rotate proxies** to avoid rate limits
3. **Enable database** for better account management
4. **Use CAPTCHA solver** for success rate
5. **Set reasonable delays** (30s between accounts minimum)

## 🎓 Comparison: Basic vs Advanced

| Feature | Basic | Advanced |
|---------|-------|----------|
| Email Services | 1 | 3+ |
| CAPTCHA Solving | ❌ | ✅ |
| Proxy Support | ❌ | ✅ |
| Multi-threading | ❌ | ✅ |
| Database | ❌ | ✅ |
| Profile Custom | ❌ | ✅ |
| Token Validation | ❌ | ✅ |
| Retry Logic | Basic | Advanced |
| User Agent Rotation | ❌ | ✅ |
| Fingerprint Spoofing | ❌ | ✅ |

## 📝 Notes

- The advanced version requires more configuration but provides better results
- CAPTCHA solving costs money (but is optional)
- Proxies are highly recommended for bulk creation
- Always respect Discord's Terms of Service
- This tool is for educational purposes only

## 🔗 Useful Links

- 2captcha: https://2captcha.com
- Anti-Captcha: https://anti-captcha.com
- Free Proxy Lists: https://free-proxy-list.net
- Discord API Docs: https://discord.com/developers/docs
