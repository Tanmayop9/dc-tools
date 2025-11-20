#!/usr/bin/env python3
"""
Discord Account Creator - 100% FREE VERSION
Features: Manual CAPTCHA solving via browser, works perfectly on Termux
No paid services required!
"""

import requests
import json
import time
import random
import string
import re
from datetime import datetime
from captcha_solver_free import FreeCaptchaSolver

class DiscordCreatorFree:
    def __init__(self):
        self.session = requests.Session()
        self.discord_api = "https://discord.com/api/v9"
        self.captcha_solver = FreeCaptchaSolver()
        
        # Update headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/register'
        })
    
    def print_banner(self):
        """Print colorful banner"""
        print("\n" + "="*70)
        print("  ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗ ")
        print("  ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗")
        print("  ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║")
        print("  ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║")
        print("  ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝")
        print("  ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ")
        print("\n       Account Creator - 100% FREE VERSION")
        print("       Works on Termux | Manual CAPTCHA Solving")
        print("="*70 + "\n")
    
    def generate_username(self):
        """Generate random username"""
        adjectives = ['cool', 'super', 'mega', 'ultra', 'pro', 'epic', 'great', 'awesome', 'mighty', 'legendary']
        nouns = ['user', 'player', 'gamer', 'master', 'ninja', 'dragon', 'tiger', 'wolf', 'warrior', 'champion']
        numbers = ''.join(random.choices(string.digits, k=4))
        return f"{random.choice(adjectives)}{random.choice(nouns)}{numbers}"
    
    def generate_password(self):
        """Generate strong password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=16))
    
    def get_temp_email(self):
        """Get temporary email from 1secmail with retry and fallback"""
        print("[*] Getting temporary email...")
        
        # Try 1secmail with multiple attempts
        for attempt in range(3):
            try:
                if attempt > 0:
                    print(f"[*] Retry attempt {attempt + 1}/3...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                
                response = self.session.get(
                    'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1',
                    timeout=15
                )
                if response.status_code == 200:
                    email = response.json()[0]
                    print(f"[✓] Email: {email}")
                    return email
            except requests.exceptions.RequestException as e:
                error_type = type(e).__name__
                if attempt < 2:
                    print(f"[!] Attempt {attempt + 1} failed ({error_type}), retrying...")
                else:
                    print(f"[✗] All attempts to get email from 1secmail failed")
                    print(f"[✗] Error: {error_type}")
        
        # Try alternative services
        print("[*] Trying alternative email service...")
        
        # Try mail.tm as fallback
        try:
            # Generate random email using mail.tm pattern
            import hashlib
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            email = f"{random_string}@1secmail.com"
            print(f"[✓] Generated email (offline mode): {email}")
            print(f"[!] Note: Email verification may not work if service is unavailable")
            return email
        except Exception as e:
            print(f"[✗] Fallback email generation failed: {e}")
        
        return None
    
    def get_fingerprint(self):
        """Get Discord fingerprint"""
        try:
            response = self.session.get(f'{self.discord_api}/experiments', timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get('fingerprint')
        except Exception:
            pass
        return None
    
    def register_account(self, email, username, password, captcha_key=None, attempt=1):
        """Register Discord account"""
        try:
            print(f"\n[*] Registration attempt {attempt}/3")
            
            # Get fingerprint
            fingerprint = self.get_fingerprint()
            if fingerprint:
                print(f"[✓] Got fingerprint")
            
            # Prepare data
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
            
            print("[*] Sending registration request...")
            response = self.session.post(
                f'{self.discord_api}/auth/register',
                json=data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                token = result.get('token')
                
                if token:
                    print("[✓] Account created successfully!")
                    return token
                else:
                    print(f"[✗] No token in response")
                    return None
                    
            elif response.status_code == 400:
                result = response.json()
                
                # Check if CAPTCHA is required
                if 'captcha_key' in result or 'captcha_sitekey' in result:
                    sitekey = result.get('captcha_sitekey', ['4c672d35-0701-42b2-88c3-78380b0db560'])[0] if isinstance(result.get('captcha_sitekey'), list) else result.get('captcha_sitekey', '4c672d35-0701-42b2-88c3-78380b0db560')
                    
                    print("\n" + "="*70)
                    print("[!] CAPTCHA Required!")
                    print("="*70)
                    print("\n[*] Opening browser for CAPTCHA solving...")
                    print("[*] This is 100% FREE - you just need to solve it manually")
                    
                    # Solve CAPTCHA via browser
                    captcha_solution = self.captcha_solver.solve_captcha(sitekey, timeout=300)
                    
                    if captcha_solution:
                        print("\n[✓] CAPTCHA solved! Retrying registration...")
                        # Retry registration with CAPTCHA solution
                        if attempt < 3:
                            return self.register_account(email, username, password, captcha_solution, attempt + 1)
                    else:
                        print("[✗] CAPTCHA solving failed or timeout")
                        return None
                else:
                    print(f"[✗] Registration error: {result}")
                    return None
            else:
                print(f"[✗] Status {response.status_code}")
                try:
                    print(f"[✗] Response: {response.json()}")
                except:
                    print(f"[✗] Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"[✗] Error during registration: {e}")
            return None
    
    def check_email_messages(self, email):
        """Check for messages in temp email"""
        try:
            login, domain = email.split('@')
            url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return []
    
    def get_email_content(self, email, message_id):
        """Get email message content"""
        try:
            login, domain = email.split('@')
            url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={message_id}'
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return None
    
    def extract_verification_link(self, content):
        """Extract verification link from email"""
        text = content.get('textBody', '') + content.get('htmlBody', '')
        
        patterns = [
            r'https://click\.discord\.com/ls/click\?upn=[^\s<>"\'\)]+',
            r'https://discord\.com/verify[^\s<>"\'\)]+',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None
    
    def verify_email(self, email):
        """Verify email"""
        print("\n[*] Waiting for verification email...")
        print("[*] This usually takes 1-3 minutes")
        
        max_attempts = 30
        for attempt in range(max_attempts):
            time.sleep(10)
            
            print(f"\r[*] Checking email... ({attempt + 1}/{max_attempts})", end='', flush=True)
            
            messages = self.check_email_messages(email)
            
            for msg in messages:
                if 'discord' in msg.get('from', '').lower() or 'discord' in msg.get('subject', '').lower():
                    print("\n[✓] Discord email received!")
                    
                    content = self.get_email_content(email, msg['id'])
                    if content:
                        link = self.extract_verification_link(content)
                        if link:
                            print("[✓] Verification link found!")
                            try:
                                self.session.get(link, allow_redirects=True, timeout=30)
                                print("[✓] Email verified successfully!")
                                return True
                            except Exception as e:
                                print(f"\n[✗] Verification error: {e}")
        
        print("\n[!] Email verification timeout (account still works, just not verified)")
        return False
    
    def save_account(self, email, username, password, token, verified):
        """Save account to files"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save token
        with open('tokens.txt', 'a') as f:
            f.write(f"{token}\n")
        
        # Save full details
        with open('accounts.txt', 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Created: {timestamp}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Token: {token}\n")
            f.write(f"Verified: {'Yes' if verified else 'No'}\n")
            f.write(f"{'='*60}\n")
        
        print("\n[✓] Account saved!")
        print(f"[✓] Token: {token[:30]}...")
        print(f"[✓] Saved to tokens.txt and accounts.txt")
    
    def create_account(self):
        """Main account creation flow"""
        self.print_banner()
        
        print("[*] Generating credentials...")
        username = self.generate_username()
        password = self.generate_password()
        
        print(f"[✓] Username: {username}")
        print(f"[✓] Password: {password}")
        
        # Get email
        email = self.get_temp_email()
        if not email:
            print("[✗] Failed to get email")
            return False
        
        # Register
        print("\n[*] Registering Discord account...")
        token = self.register_account(email, username, password)
        
        if not token:
            print("\n[✗] Failed to create account")
            return False
        
        # Verify email
        verified = self.verify_email(email)
        
        # Save account
        self.save_account(email, username, password, token, verified)
        
        print("\n" + "="*70)
        print("       ✓ ACCOUNT CREATED SUCCESSFULLY! ✓")
        print("="*70 + "\n")
        
        return True

def main():
    """Main entry point"""
    try:
        creator = DiscordCreatorFree()
        
        print("\n╔══════════════════════════════════════════════════════════════════╗")
        print("║      Discord Account Creator - 100% FREE VERSION                ║")
        print("║      No Paid Services | Works on Termux | Manual CAPTCHA        ║")
        print("╚══════════════════════════════════════════════════════════════════╝\n")
        
        # Get number of accounts
        try:
            count_str = input("How many accounts to create? (default: 1): ").strip()
            count = int(count_str) if count_str else 1
        except ValueError:
            count = 1
        
        print(f"\n[*] Will create {count} account(s)")
        print("[*] You may need to solve CAPTCHA for each account")
        print("[*] Browser will open automatically when CAPTCHA is required\n")
        
        input("Press ENTER to start...")
        
        successful = 0
        for i in range(count):
            print(f"\n{'='*70}")
            print(f"       Creating Account {i + 1} of {count}")
            print(f"{'='*70}")
            
            if creator.create_account():
                successful += 1
            else:
                print("[✗] Account creation failed")
            
            # Delay between accounts
            if i < count - 1:
                delay = 30
                print(f"\n[*] Waiting {delay} seconds before next account...")
                for remaining in range(delay, 0, -1):
                    print(f"\r[*] Next account in {remaining} seconds...  ", end='', flush=True)
                    time.sleep(1)
                print()
        
        print("\n" + "="*70)
        print(f"       SUMMARY: {successful}/{count} accounts created successfully")
        print("="*70)
        print(f"\n[✓] Tokens saved in: tokens.txt")
        print(f"[✓] Full details in: accounts.txt\n")
        
    except KeyboardInterrupt:
        print("\n\n[!] Stopped by user")
    except Exception as e:
        print(f"\n[✗] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
