#!/usr/bin/env python3
"""
Discord Bot Authorization Script - For Educational Purposes Only
Automatically authorizes a bot to join a guild using OAuth2
Inspired by discord.js-selfbot-v13

⚠️ DISCLAIMER: This tool is for educational and research purposes only.
Use at your own risk. The authors are not responsible for any misuse.
"""

import requests
import json
import re
import sys
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict

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


class BotAuthorizer:
    """Handles Discord bot OAuth2 authorization"""
    
    def __init__(self, user_token: str):
        """
        Initialize the bot authorizer
        
        Args:
            user_token: Discord user account token
        """
        self.user_token = user_token
        self.api_base = "https://discord.com/api/v9"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': user_token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def validate_oauth_url(self, oauth_url: str) -> bool:
        """
        Validate if the provided URL is a valid Discord OAuth2 authorization URL
        
        Args:
            oauth_url: OAuth2 URL to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Pattern from discord.js-selfbot-v13
        pattern = r'^https://(?:canary\.|ptb\.)?discord\.com(?:/api(?:/v\d{1,2})?)?/oauth2/authorize\?'
        return bool(re.match(pattern, oauth_url))
    
    def authorize_url(self, oauth_url: str, options: Optional[Dict] = None) -> Dict:
        """
        Authorize a bot using OAuth2 URL
        
        Args:
            oauth_url: The OAuth2 authorization URL
            options: Additional options for authorization
            
        Returns:
            Response from Discord API
        """
        # Validate URL
        if not self.validate_oauth_url(oauth_url):
            raise ValueError(f"Invalid OAuth2 URL: {oauth_url}")
        
        # Parse URL and extract query parameters
        parsed_url = urlparse(oauth_url)
        query_params = parse_qs(parsed_url.query)
        
        # Convert query params to single values (parse_qs returns lists)
        search_params = {k: v[0] if isinstance(v, list) and len(v) == 1 else v 
                        for k, v in query_params.items()}
        
        # Default options
        default_options = {
            'authorize': True,
            'permissions': '0',
            'integration_type': 0,
        }
        
        # Merge options
        if options:
            default_options.update(options)
        
        # Merge with search params (search params have lower priority)
        final_options = {**default_options, **search_params}
        
        # Remove these from search_params as they go in the body
        body_only_params = ['permissions', 'integration_type', 'guild_id', 'authorize']
        query_only = {k: v for k, v in search_params.items() if k not in body_only_params}
        
        # Build the authorization request
        api_url = f"{self.api_base}/oauth2/authorize"
        
        ColoredOutput.print_info(f"Sending authorization request...")
        ColoredOutput.print_info(f"Guild ID: {final_options.get('guild_id', 'Not specified')}")
        ColoredOutput.print_info(f"Permissions: {final_options.get('permissions', '0')}")
        
        try:
            response = self.session.post(
                api_url,
                params=query_only,
                json=final_options
            )
            
            if response.status_code == 200:
                ColoredOutput.print_success("Bot authorized successfully!")
                return response.json()
            else:
                ColoredOutput.print_error(f"Authorization failed: {response.status_code}")
                ColoredOutput.print_error(f"Response: {response.text}")
                return {'error': response.text, 'status_code': response.status_code}
                
        except Exception as e:
            ColoredOutput.print_error(f"Request failed: {str(e)}")
            return {'error': str(e)}


def main():
    """Main function"""
    print(f"{ColoredOutput.BOLD}{ColoredOutput.HEADER}")
    print("=" * 60)
    print("Discord Bot Authorizer - Educational Use Only")
    print("=" * 60)
    print(f"{ColoredOutput.ENDC}")
    
    ColoredOutput.print_warning("⚠️  This tool is for educational purposes only!")
    ColoredOutput.print_warning("⚠️  Use at your own risk!")
    print()
    
    # Get user token
    print(f"{ColoredOutput.CYAN}Enter your Discord account token:{ColoredOutput.ENDC}")
    user_token = input("> ").strip()
    
    if not user_token:
        ColoredOutput.print_error("Token is required!")
        sys.exit(1)
    
    # Get OAuth2 URL
    print(f"\n{ColoredOutput.CYAN}Enter the bot OAuth2 authorization URL:{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.WARNING}Example: https://discord.com/api/oauth2/authorize?client_id=123456789&scope=bot&permissions=8{ColoredOutput.ENDC}")
    oauth_url = input("> ").strip()
    
    if not oauth_url:
        ColoredOutput.print_error("OAuth2 URL is required!")
        sys.exit(1)
    
    # Get guild ID
    print(f"\n{ColoredOutput.CYAN}Enter the Guild ID (default: 283939):{ColoredOutput.ENDC}")
    guild_id = input("> ").strip() or "283939"
    
    # Get permissions (optional)
    print(f"\n{ColoredOutput.CYAN}Enter permissions (default: 0 for no permissions):{ColoredOutput.ENDC}")
    permissions = input("> ").strip() or "0"
    
    # Create authorizer
    authorizer = BotAuthorizer(user_token)
    
    # Prepare options
    options = {
        'guild_id': guild_id,
        'permissions': permissions,
        'integration_type': 0
    }
    
    print()
    ColoredOutput.print_info("Starting authorization process...")
    
    # Authorize the bot
    result = authorizer.authorize_url(oauth_url, options)
    
    # Display results
    print()
    if 'error' not in result:
        ColoredOutput.print_success("=" * 60)
        ColoredOutput.print_success("Bot successfully added to the guild!")
        ColoredOutput.print_success("=" * 60)
        print()
        ColoredOutput.print_info("Response details:")
        print(json.dumps(result, indent=2))
    else:
        ColoredOutput.print_error("=" * 60)
        ColoredOutput.print_error("Failed to add bot to guild")
        ColoredOutput.print_error("=" * 60)
        print()
        ColoredOutput.print_info("Error details:")
        print(json.dumps(result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
