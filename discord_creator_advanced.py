#!/usr/bin/env python3
"""
Ultra Advanced Discord Account Creator - For Educational Purposes Only
Features: CAPTCHA solving, Proxy support, Multi-threading, Profile customization, Token validation
Designed for Termux and Linux environments
"""

import requests
import json
import time
import random
import string
import re
import threading
import sqlite3
import base64
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# Import free CAPTCHA solver
try:
    from captcha_solver_free import FreeCaptchaSolver
    FREE_CAPTCHA_AVAILABLE = True
except ImportError:
    FREE_CAPTCHA_AVAILABLE = False

class ColoredOutput:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print_success(msg):
        print(f"{ColoredOutput.GREEN}[✓] {msg}{ColoredOutput.ENDC}")
    
    @staticmethod
    def print_error(msg):
        print(f"{ColoredOutput.FAIL}[✗] {msg}{ColoredOutput.ENDC}")
    
    @staticmethod
    def print_info(msg):
        print(f"{ColoredOutput.CYAN}[*] {msg}{ColoredOutput.ENDC}")
    
    @staticmethod
    def print_warning(msg):
        print(f"{ColoredOutput.WARNING}[!] {msg}{ColoredOutput.ENDC}")

class ProxyManager:
    """Advanced proxy management"""
    def __init__(self, config):
        self.config = config
        self.proxies = []
        self.current_index = 0
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from file"""
        if not self.config.get('proxy', {}).get('enabled', False):
            return
        
        proxy_file = self.config.get('proxy', {}).get('proxy_list_file', 'proxies.txt')
        if Path(proxy_file).exists():
            with open(proxy_file, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            ColoredOutput.print_success(f"Loaded {len(self.proxies)} proxies")
    
    def get_proxy(self) -> Optional[Dict]:
        """Get next proxy in rotation"""
        if not self.proxies or not self.config.get('proxy', {}).get('enabled', False):
            return None
        
        proxy = self.proxies[self.current_index]
        if self.config.get('proxy', {}).get('rotate_proxies', True):
            self.current_index = (self.current_index + 1) % len(self.proxies)
        
        proxy_type = self.config.get('proxy', {}).get('proxy_type', 'http')
        return {
            'http': f'{proxy_type}://{proxy}',
            'https': f'{proxy_type}://{proxy}'
        }

class UserAgentManager:
    """Advanced user agent rotation"""
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        ]
    
    def get_random(self) -> str:
        """Get random user agent"""
        return random.choice(self.user_agents)

class CaptchaSolver:
    """Advanced CAPTCHA solving with multiple providers including FREE manual solving"""
    def __init__(self, config):
        self.config = config
        self.enabled = config.get('captcha', {}).get('enabled', False)
        self.solver = config.get('captcha', {}).get('solver', 'manual')
        self.api_key = config.get('captcha', {}).get('api_key', '')
        
        # Initialize free manual solver
        self.free_solver = None
        if FREE_CAPTCHA_AVAILABLE and self.solver == 'manual':
            self.free_solver = FreeCaptchaSolver()
    
    def solve_hcaptcha(self, sitekey: str, url: str) -> Optional[str]:
        """Solve hCaptcha using configured solver"""
        if not self.enabled:
            return None
        
        # Try manual (free) solver first if configured
        if self.solver == 'manual' and self.free_solver:
            ColoredOutput.print_info("Using FREE manual CAPTCHA solver (browser-based)")
            return self._solve_manual(sitekey, url)
        
        # Try paid solvers if API key is provided
        if self.api_key:
            ColoredOutput.print_info(f"Solving CAPTCHA with {self.solver}...")
            
            if self.solver == '2captcha':
                return self._solve_2captcha(sitekey, url)
            elif self.solver == 'anticaptcha':
                return self._solve_anticaptcha(sitekey, url)
        
        # Fallback to manual if no API key
        if self.free_solver:
            ColoredOutput.print_warning("No API key, falling back to manual solver")
            return self._solve_manual(sitekey, url)
        
        return None
    
    def _solve_manual(self, sitekey: str, url: str) -> Optional[str]:
        """Solve CAPTCHA manually via browser (FREE)"""
        try:
            solution = self.free_solver.solve_captcha(sitekey, timeout=300)
            return solution
        except Exception as e:
            ColoredOutput.print_error(f"Manual CAPTCHA solving failed: {e}")
            return None
    
    def _solve_2captcha(self, sitekey: str, url: str) -> Optional[str]:
        """Solve with 2captcha.com"""
        try:
            # Submit CAPTCHA
            submit_url = f"http://2captcha.com/in.php?key={self.api_key}&method=hcaptcha&sitekey={sitekey}&pageurl={url}&json=1"
            response = requests.get(submit_url, timeout=30)
            result = response.json()
            
            if result['status'] != 1:
                return None
            
            captcha_id = result['request']
            
            # Wait for solution
            for _ in range(24):
                time.sleep(5)
                check_url = f"http://2captcha.com/res.php?key={self.api_key}&action=get&id={captcha_id}&json=1"
                response = requests.get(check_url, timeout=30)
                result = response.json()
                
                if result['status'] == 1:
                    ColoredOutput.print_success("CAPTCHA solved!")
                    return result['request']
            
            return None
        except Exception as e:
            ColoredOutput.print_error(f"CAPTCHA solving failed: {e}")
            return None
    
    def _solve_anticaptcha(self, sitekey: str, url: str) -> Optional[str]:
        """Solve with anti-captcha.com"""
        # Implementation for anti-captcha
        ColoredOutput.print_warning("Anti-captcha solver not yet implemented")
        return None

class AccountDatabase:
    """SQLite database for account management"""
    def __init__(self, db_file: str = 'accounts.db'):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                token TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                verified BOOLEAN DEFAULT 0,
                status TEXT DEFAULT 'active'
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_account(self, email: str, username: str, password: str, token: str, verified: bool = False):
        """Save account to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (email, username, password, token, verified)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, username, password, token, verified))
        conn.commit()
        conn.close()
    
    def get_all_accounts(self) -> List[Tuple]:
        """Get all accounts"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts')
        accounts = cursor.fetchall()
        conn.close()
        return accounts

class EmailService:
    """Advanced email service with multiple providers"""
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.primary_service = config.get('email', {}).get('primary_service', '1secmail')
    
    def get_email(self) -> Optional[str]:
        """Get temporary email from primary or fallback service"""
        if self.primary_service == '1secmail':
            return self._get_1secmail()
        elif self.primary_service == 'tempmail':
            return self._get_tempmail()
        elif self.primary_service == 'guerrillamail':
            return self._get_guerrillamail()
        
        return self._get_1secmail()
    
    def _get_1secmail(self) -> Optional[str]:
        """Get email from 1secmail"""
        try:
            response = self.session.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1', timeout=10)
            if response.status_code == 200:
                return response.json()[0]
        except Exception as e:
            ColoredOutput.print_error(f"1secmail error: {e}")
        return None
    
    def _get_tempmail(self) -> Optional[str]:
        """Get email from temp-mail.org"""
        try:
            # temp-mail.org API implementation
            md5_hash = hashlib.md5(str(time.time()).encode()).hexdigest()
            email = f"{md5_hash[:10]}@tempmail.plus"
            return email
        except Exception as e:
            ColoredOutput.print_error(f"tempmail error: {e}")
        return None
    
    def _get_guerrillamail(self) -> Optional[str]:
        """Get email from guerrillamail"""
        try:
            response = self.session.get('https://api.guerrillamail.com/ajax.php?f=get_email_address', timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('email_addr')
        except Exception as e:
            ColoredOutput.print_error(f"guerrillamail error: {e}")
        return None
    
    def check_messages(self, email: str) -> List[Dict]:
        """Check messages based on email provider"""
        if '@1secmail.com' in email:
            return self._check_1secmail(email)
        elif '@tempmail.plus' in email:
            return self._check_tempmail(email)
        elif '@sharklasers.com' in email or '@guerrillamail' in email:
            return self._check_guerrillamail(email)
        return []
    
    def _check_1secmail(self, email: str) -> List[Dict]:
        """Check 1secmail messages"""
        try:
            login, domain = email.split('@')
            url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return []
    
    def _check_tempmail(self, email: str) -> List[Dict]:
        """Check tempmail messages"""
        # Implementation for tempmail
        return []
    
    def _check_guerrillamail(self, email: str) -> List[Dict]:
        """Check guerrillamail messages"""
        # Implementation for guerrillamail
        return []
    
    def get_message_content(self, email: str, message_id: str) -> Optional[Dict]:
        """Get message content"""
        if '@1secmail.com' in email:
            try:
                login, domain = email.split('@')
                url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={message_id}'
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    return response.json()
            except Exception:
                pass
        return None

class AdvancedDiscordCreator:
    """Ultra advanced Discord account creator"""
    def __init__(self, config_file: str = 'config.json'):
        self.config = self.load_config(config_file)
        self.session = requests.Session()
        self.discord_api = "https://discord.com/api/v9"
        
        # Initialize managers
        self.proxy_manager = ProxyManager(self.config)
        self.ua_manager = UserAgentManager()
        self.captcha_solver = CaptchaSolver(self.config)
        self.email_service = EmailService(self.config)
        
        # Initialize database if enabled
        self.db = None
        if self.config.get('advanced', {}).get('use_database', False):
            self.db = AccountDatabase(self.config.get('advanced', {}).get('database_file', 'accounts.db'))
        
        self.update_headers()
    
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        if Path(config_file).exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def update_headers(self):
        """Update session headers"""
        user_agent = self.ua_manager.get_random() if self.config.get('advanced', {}).get('user_agent_rotation', True) else 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/register',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })
        
        # Set proxy if enabled
        proxy = self.proxy_manager.get_proxy()
        if proxy:
            self.session.proxies.update(proxy)
    
    def generate_username(self) -> str:
        """Generate random username"""
        adjectives = ['cool', 'super', 'mega', 'ultra', 'pro', 'epic', 'great', 'awesome', 'mighty', 'legendary']
        nouns = ['user', 'player', 'gamer', 'master', 'ninja', 'dragon', 'tiger', 'wolf', 'warrior', 'champion']
        numbers = ''.join(random.choices(string.digits, k=4))
        return f"{random.choice(adjectives)}{random.choice(nouns)}{numbers}"
    
    def generate_password(self) -> str:
        """Generate strong password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choices(chars, k=16))
        return password
    
    def generate_fingerprint(self) -> str:
        """Generate random fingerprint for spoofing"""
        if self.config.get('advanced', {}).get('fingerprint_spoofing', True):
            # Generate realistic fingerprint
            random_bytes = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            return base64.b64encode(random_bytes.encode()).decode()[:32]
        return None
    
    def get_discord_fingerprint(self) -> Optional[str]:
        """Get Discord fingerprint"""
        try:
            response = self.session.get(f'{self.discord_api}/experiments', timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get('fingerprint')
        except Exception as e:
            ColoredOutput.print_error(f"Error getting fingerprint: {e}")
        
        # Fallback to generated fingerprint
        return self.generate_fingerprint()
    
    def register_account(self, email: str, username: str, password: str, captcha_key: Optional[str] = None) -> Optional[str]:
        """Register Discord account with retry mechanism"""
        max_retries = self.config.get('general', {}).get('max_retries', 3)
        retry_delay = self.config.get('general', {}).get('retry_delay', 5)
        
        for attempt in range(max_retries):
            try:
                fingerprint = self.get_discord_fingerprint()
                if not fingerprint:
                    ColoredOutput.print_warning("No fingerprint, using generated one")
                    fingerprint = self.generate_fingerprint()
                
                ColoredOutput.print_info(f"Attempt {attempt + 1}/{max_retries}")
                
                data = {
                    'fingerprint': fingerprint,
                    'email': email,
                    'username': username,
                    'password': password,
                    'invite': None,
                    'consent': True,
                    'date_of_birth': f"{random.randint(1990, 2003)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                    'gift_code_sku_id': None,
                    'captcha_key': captcha_key
                }
                
                response = self.session.post(
                    f'{self.discord_api}/auth/register',
                    json=data,
                    timeout=30
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    token = result.get('token')
                    if token:
                        ColoredOutput.print_success("Account registered successfully!")
                        return token
                    else:
                        ColoredOutput.print_error(f"No token in response: {result}")
                elif response.status_code == 400:
                    result = response.json()
                    if 'captcha_key' in result:
                        ColoredOutput.print_warning("CAPTCHA required")
                        sitekey = result.get('captcha_sitekey')
                        if self.captcha_solver.enabled:
                            captcha_key = self.captcha_solver.solve_hcaptcha(sitekey, 'https://discord.com/register')
                            if captcha_key:
                                return self.register_account(email, username, password, captcha_key)
                    ColoredOutput.print_error(f"Registration failed: {result}")
                else:
                    ColoredOutput.print_error(f"Status {response.status_code}: {response.text}")
                
                if attempt < max_retries - 1:
                    ColoredOutput.print_info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    
            except Exception as e:
                ColoredOutput.print_error(f"Registration error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        
        return None
    
    def verify_email(self, email: str) -> bool:
        """Verify email with advanced checking"""
        timeout = self.config.get('email', {}).get('verification_timeout', 300)
        check_interval = self.config.get('email', {}).get('check_interval', 10)
        max_attempts = timeout // check_interval
        
        ColoredOutput.print_info("Waiting for verification email...")
        
        for attempt in range(max_attempts):
            time.sleep(check_interval)
            ColoredOutput.print_info(f"Checking... ({attempt + 1}/{max_attempts})")
            
            messages = self.email_service.check_messages(email)
            
            for msg in messages:
                if 'discord' in msg.get('from', '').lower() or 'discord' in msg.get('subject', '').lower():
                    ColoredOutput.print_success("Discord email found!")
                    
                    content = self.email_service.get_message_content(email, msg.get('id'))
                    if content:
                        link = self.extract_verification_link(content)
                        if link:
                            ColoredOutput.print_success("Verification link found!")
                            try:
                                self.session.get(link, allow_redirects=True, timeout=30)
                                ColoredOutput.print_success("Email verified!")
                                return True
                            except Exception as e:
                                ColoredOutput.print_error(f"Verification error: {e}")
        
        ColoredOutput.print_warning("Email verification timeout")
        return False
    
    def extract_verification_link(self, content: Dict) -> Optional[str]:
        """Extract verification link"""
        text = content.get('textBody', '') + content.get('htmlBody', '')
        
        patterns = [
            r'https://click\.discord\.com/ls/click\?upn=[^\s<>"\'\)]+',
            r'https://discord\.com/verify[^\s<>"\'\)]+',
            r'https?://[^\s<>"\'\)]*discord[^\s<>"\'\)]*verify[^\s<>"\'\)]+'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None
    
    def validate_token(self, token: str) -> bool:
        """Validate Discord token"""
        if not self.config.get('general', {}).get('verify_tokens', True):
            return True
        
        try:
            headers = {'Authorization': token}
            response = self.session.get(f'{self.discord_api}/users/@me', headers=headers, timeout=10)
            return response.status_code == 200
        except Exception:
            return False
    
    def customize_profile(self, token: str, username: str):
        """Customize profile (avatar, bio, etc.)"""
        if not self.config.get('profile', {}).get('customize_profile', False):
            return
        
        ColoredOutput.print_info("Customizing profile...")
        
        # Set bio
        if self.config.get('profile', {}).get('set_bio', False):
            bio_templates = self.config.get('profile', {}).get('bio_templates', [])
            if bio_templates:
                bio = random.choice(bio_templates)
                self.set_bio(token, bio)
    
    def set_bio(self, token: str, bio: str):
        """Set account bio"""
        try:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            data = {'bio': bio}
            self.session.patch(f'{self.discord_api}/users/@me', headers=headers, json=data, timeout=10)
            ColoredOutput.print_success("Bio set!")
        except Exception as e:
            ColoredOutput.print_error(f"Failed to set bio: {e}")
    
    def join_servers(self, token: str):
        """Auto-join Discord servers"""
        if not self.config.get('auto_join', {}).get('enabled', False):
            return
        
        invites = self.config.get('auto_join', {}).get('server_invites', [])
        for invite in invites:
            try:
                headers = {'Authorization': token}
                self.session.post(f'{self.discord_api}/invites/{invite}', headers=headers, timeout=10)
                ColoredOutput.print_success(f"Joined server: {invite}")
                time.sleep(2)
            except Exception as e:
                ColoredOutput.print_error(f"Failed to join {invite}: {e}")
    
    def save_account(self, email: str, username: str, password: str, token: str, verified: bool):
        """Save account to file and/or database"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save to tokens.txt
        with open('tokens.txt', 'a') as f:
            f.write(f"{token}\n")
        
        # Save to accounts.txt
        with open('accounts.txt', 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Created: {timestamp}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Token: {token}\n")
            f.write(f"Verified: {verified}\n")
            f.write(f"{'='*60}\n")
        
        # Save to database
        if self.db:
            self.db.save_account(email, username, password, token, verified)
        
        ColoredOutput.print_success("Account saved!")
    
    def create_account(self) -> bool:
        """Create a complete Discord account"""
        print("\n" + "="*60)
        print(f"{ColoredOutput.BOLD}Ultra Advanced Discord Account Creator{ColoredOutput.ENDC}")
        print("="*60 + "\n")
        
        # Generate credentials
        username = self.generate_username()
        password = self.generate_password()
        ColoredOutput.print_success(f"Username: {username}")
        ColoredOutput.print_success(f"Password: {password}")
        
        # Get email
        email = self.email_service.get_email()
        if not email:
            ColoredOutput.print_error("Failed to get email")
            return False
        ColoredOutput.print_success(f"Email: {email}")
        
        # Register account
        ColoredOutput.print_info("Registering account...")
        token = self.register_account(email, username, password)
        if not token:
            ColoredOutput.print_error("Registration failed")
            return False
        
        # Verify token
        if self.config.get('general', {}).get('verify_tokens', True):
            ColoredOutput.print_info("Validating token...")
            if self.validate_token(token):
                ColoredOutput.print_success("Token is valid!")
            else:
                ColoredOutput.print_warning("Token validation failed")
        
        # Verify email
        verified = self.verify_email(email)
        
        # Customize profile
        self.customize_profile(token, username)
        
        # Join servers
        self.join_servers(token)
        
        # Save account
        self.save_account(email, username, password, token, verified)
        
        print(f"\n{ColoredOutput.GREEN}{'='*60}")
        print(f"[✓] Account Created Successfully!")
        print(f"[✓] Token: {token[:30]}...")
        print(f"{'='*60}{ColoredOutput.ENDC}\n")
        
        return True

def create_single_account(creator: AdvancedDiscordCreator, account_num: int, total: int):
    """Worker function for threading"""
    print(f"\n{'='*60}")
    print(f"Thread: Creating account {account_num}/{total}")
    print(f"{'='*60}")
    return creator.create_account()

def main():
    """Main entry point"""
    try:
        print(f"{ColoredOutput.BOLD}{ColoredOutput.CYAN}")
        print("╔═══════════════════════════════════════════════════════╗")
        print("║   Ultra Advanced Discord Account Creator             ║")
        print("║   For Educational Purposes Only                       ║")
        print("╚═══════════════════════════════════════════════════════╝")
        print(ColoredOutput.ENDC)
        
        # Load config
        creator = AdvancedDiscordCreator()
        
        # Display config status
        print(f"\n{ColoredOutput.BOLD}Configuration:{ColoredOutput.ENDC}")
        print(f"  Proxy: {ColoredOutput.GREEN if creator.config.get('proxy', {}).get('enabled') else ColoredOutput.FAIL}{'Enabled' if creator.config.get('proxy', {}).get('enabled') else 'Disabled'}{ColoredOutput.ENDC}")
        print(f"  CAPTCHA Solver: {ColoredOutput.GREEN if creator.config.get('captcha', {}).get('enabled') else ColoredOutput.FAIL}{'Enabled' if creator.config.get('captcha', {}).get('enabled') else 'Disabled'}{ColoredOutput.ENDC}")
        print(f"  Database: {ColoredOutput.GREEN if creator.config.get('advanced', {}).get('use_database') else ColoredOutput.FAIL}{'Enabled' if creator.config.get('advanced', {}).get('use_database') else 'Disabled'}{ColoredOutput.ENDC}")
        print(f"  Multi-threading: {ColoredOutput.GREEN if creator.config.get('advanced', {}).get('multi_threading') else ColoredOutput.FAIL}{'Enabled' if creator.config.get('advanced', {}).get('multi_threading') else 'Disabled'}{ColoredOutput.ENDC}")
        
        # Get account count
        try:
            count_input = input(f"\n{ColoredOutput.BOLD}How many accounts to create? (default: 1): {ColoredOutput.ENDC}").strip()
            count = int(count_input) if count_input else 1
        except ValueError:
            count = 1
        
        # Multi-threading or sequential
        if creator.config.get('advanced', {}).get('multi_threading', False) and count > 1:
            max_threads = creator.config.get('advanced', {}).get('max_threads', 3)
            ColoredOutput.print_info(f"Using {max_threads} threads")
            
            threads = []
            successful = 0
            
            for i in range(count):
                thread = threading.Thread(target=create_single_account, args=(creator, i + 1, count))
                threads.append(thread)
                thread.start()
                
                # Limit concurrent threads
                if len(threads) >= max_threads:
                    for t in threads:
                        t.join()
                    threads = []
            
            # Wait for remaining threads
            for t in threads:
                t.join()
        else:
            # Sequential creation
            successful = 0
            for i in range(count):
                print(f"\n{'='*60}")
                print(f"{ColoredOutput.BOLD}Creating account {i + 1} of {count}{ColoredOutput.ENDC}")
                print(f"{'='*60}")
                
                if creator.create_account():
                    successful += 1
                
                # Rate limiting
                if i < count - 1:
                    delay = creator.config.get('general', {}).get('rate_limit_delay', 30)
                    ColoredOutput.print_info(f"Waiting {delay} seconds...")
                    time.sleep(delay)
            
            print(f"\n{ColoredOutput.BOLD}{'='*60}")
            print(f"Summary: {ColoredOutput.GREEN}{successful}{ColoredOutput.ENDC}/{count} accounts created")
            print(f"{'='*60}{ColoredOutput.ENDC}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{ColoredOutput.WARNING}[!] Interrupted by user{ColoredOutput.ENDC}")
    except Exception as e:
        ColoredOutput.print_error(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
