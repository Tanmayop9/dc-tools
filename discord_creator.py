#!/usr/bin/env python3
"""
Discord Account Creator - For Educational Purposes Only
Creates Discord accounts with email verification and saves tokens
Designed to work on Termux
"""

import requests
import json
import time
import random
import string
import re
from datetime import datetime

class DiscordAccountCreator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/register'
        })
        self.discord_api = "https://discord.com/api/v9"
        
    def generate_username(self):
        """Generate a random username"""
        adjectives = ['cool', 'super', 'mega', 'ultra', 'pro', 'epic', 'great', 'awesome']
        nouns = ['user', 'player', 'gamer', 'master', 'ninja', 'dragon', 'tiger', 'wolf']
        numbers = ''.join(random.choices(string.digits, k=4))
        return f"{random.choice(adjectives)}{random.choice(nouns)}{numbers}"
    
    def generate_password(self):
        """Generate a strong random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choices(chars, k=16))
        return password
    
    def get_temp_email(self):
        """Get a temporary email using 1secmail API (free service)"""
        try:
            # Get random email
            response = self.session.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1')
            if response.status_code == 200:
                email = response.json()[0]
                print(f"[+] Generated temp email: {email}")
                return email
            return None
        except Exception as e:
            print(f"[-] Error getting temp email: {e}")
            return None
    
    def check_email_messages(self, email):
        """Check for new messages in temp email"""
        try:
            login, domain = email.split('@')
            url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"[-] Error checking email: {e}")
            return []
    
    def get_email_content(self, email, message_id):
        """Get specific email message content"""
        try:
            login, domain = email.split('@')
            url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={message_id}'
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"[-] Error reading email: {e}")
            return None
    
    def extract_verification_link(self, email_content):
        """Extract verification link from Discord email"""
        try:
            if 'textBody' in email_content:
                text = email_content['textBody']
            elif 'htmlBody' in email_content:
                text = email_content['htmlBody']
            else:
                return None
            
            # Find Discord verification link
            pattern = r'https://click\.discord\.com/ls/click\?upn=[^\s<>"\']+'
            match = re.search(pattern, text)
            if match:
                return match.group(0)
            
            # Alternative pattern
            pattern = r'https://discord\.com/verify[^\s<>"\']+'
            match = re.search(pattern, text)
            if match:
                return match.group(0)
                
            return None
        except Exception as e:
            print(f"[-] Error extracting link: {e}")
            return None
    
    def get_fingerprint(self):
        """Get Discord fingerprint"""
        try:
            response = self.session.get(f'{self.discord_api}/experiments')
            if response.status_code == 200:
                data = response.json()
                return data.get('fingerprint')
            return None
        except Exception as e:
            print(f"[-] Error getting fingerprint: {e}")
            return None
    
    def register_account(self, email, username, password):
        """Register a Discord account"""
        try:
            fingerprint = self.get_fingerprint()
            if not fingerprint:
                print("[-] Failed to get fingerprint")
                return None
            
            print(f"[+] Got fingerprint: {fingerprint[:20]}...")
            
            # Prepare registration data
            data = {
                'fingerprint': fingerprint,
                'email': email,
                'username': username,
                'password': password,
                'invite': None,
                'consent': True,
                'date_of_birth': '1995-01-01',
                'gift_code_sku_id': None,
                'captcha_key': None
            }
            
            # Register
            response = self.session.post(
                f'{self.discord_api}/auth/register',
                json=data
            )
            
            if response.status_code == 201 or response.status_code == 200:
                result = response.json()
                token = result.get('token')
                if token:
                    print(f"[+] Account created successfully!")
                    return token
                else:
                    print(f"[-] No token in response: {result}")
                    return None
            else:
                print(f"[-] Registration failed: {response.status_code}")
                print(f"[-] Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"[-] Error during registration: {e}")
            return None
    
    def verify_email(self, email, token):
        """Wait for and verify email"""
        print("[*] Waiting for verification email...")
        
        max_attempts = 30
        for attempt in range(max_attempts):
            time.sleep(10)  # Wait 10 seconds between checks
            
            print(f"[*] Checking email... (Attempt {attempt + 1}/{max_attempts})")
            messages = self.check_email_messages(email)
            
            if messages:
                for msg in messages:
                    if 'discord' in msg.get('from', '').lower():
                        print(f"[+] Found Discord email!")
                        
                        # Get full email content
                        content = self.get_email_content(email, msg['id'])
                        if content:
                            link = self.extract_verification_link(content)
                            if link:
                                print(f"[+] Found verification link!")
                                
                                # Visit verification link
                                try:
                                    verify_response = self.session.get(link, allow_redirects=True)
                                    print(f"[+] Verification completed!")
                                    return True
                                except Exception as e:
                                    print(f"[-] Error visiting link: {e}")
                                    return False
        
        print("[-] Email verification timeout")
        return False
    
    def save_token(self, token, email, username, password):
        """Save token and account info to file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save to tokens.txt
            with open('tokens.txt', 'a') as f:
                f.write(f"{token}\n")
            
            # Save full account details to accounts.txt
            with open('accounts.txt', 'a') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"Created: {timestamp}\n")
                f.write(f"Email: {email}\n")
                f.write(f"Username: {username}\n")
                f.write(f"Password: {password}\n")
                f.write(f"Token: {token}\n")
                f.write(f"{'='*60}\n")
            
            print(f"[+] Token saved to tokens.txt")
            print(f"[+] Account details saved to accounts.txt")
            return True
        except Exception as e:
            print(f"[-] Error saving token: {e}")
            return False
    
    def create_account(self):
        """Main function to create a complete Discord account"""
        print("\n" + "="*60)
        print("Discord Account Creator - Educational Purposes Only")
        print("="*60 + "\n")
        
        # Step 1: Generate credentials
        username = self.generate_username()
        password = self.generate_password()
        print(f"[+] Generated username: {username}")
        print(f"[+] Generated password: {password}")
        
        # Step 2: Get temporary email
        email = self.get_temp_email()
        if not email:
            print("[-] Failed to get temporary email")
            return False
        
        # Step 3: Register account
        print("[*] Registering Discord account...")
        token = self.register_account(email, username, password)
        if not token:
            print("[-] Failed to register account")
            return False
        
        # Step 4: Verify email
        verified = self.verify_email(email, token)
        if not verified:
            print("[!] Warning: Email not verified automatically")
            print("[!] Account may have limited functionality")
        
        # Step 5: Save token
        self.save_token(token, email, username, password)
        
        print("\n[✓] Account creation completed!")
        print(f"[✓] Token: {token[:20]}...")
        print(f"[✓] Saved to tokens.txt and accounts.txt\n")
        
        return True

def main():
    """Main entry point"""
    try:
        print("Discord Account Creator")
        print("For Educational Purposes Only\n")
        
        # Ask how many accounts to create
        try:
            count = input("How many accounts to create? (default: 1): ").strip()
            count = int(count) if count else 1
        except ValueError:
            count = 1
        
        creator = DiscordAccountCreator()
        
        successful = 0
        for i in range(count):
            print(f"\n{'='*60}")
            print(f"Creating account {i + 1} of {count}")
            print(f"{'='*60}")
            
            if creator.create_account():
                successful += 1
            else:
                print("[-] Failed to create account")
            
            # Wait between accounts to avoid rate limiting
            if i < count - 1:
                print("\n[*] Waiting 30 seconds before next account...")
                time.sleep(30)
        
        print(f"\n{'='*60}")
        print(f"Summary: {successful}/{count} accounts created successfully")
        print(f"{'='*60}\n")
        
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
    except Exception as e:
        print(f"\n[-] Error: {e}")

if __name__ == "__main__":
    main()
