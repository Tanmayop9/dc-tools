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
import time
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict

# Import free CAPTCHA solvers
try:
    from captcha_solver_llm import LLMCaptchaSolver
    LLM_CAPTCHA_AVAILABLE = True
except ImportError:
    LLM_CAPTCHA_AVAILABLE = False

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
    """Handles Discord bot OAuth2 authorization with free LLM CAPTCHA solving"""
    
    def __init__(self, user_token: str, use_llm_captcha: bool = True):
        """
        Initialize the bot authorizer
        
        Args:
            user_token: Discord user account token
            use_llm_captcha: Use free LLM for CAPTCHA solving (default: True)
        """
        self.user_token = user_token
        self.api_base = "https://discord.com/api/v9"
        self.use_llm_captcha = use_llm_captcha
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': user_token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Initialize CAPTCHA solvers
        self.llm_solver = None
        self.manual_solver = None
        
        if use_llm_captcha and LLM_CAPTCHA_AVAILABLE:
            ColoredOutput.print_success("✨ Free LLM CAPTCHA solver enabled!")
            self.llm_solver = LLMCaptchaSolver()
        elif FREE_CAPTCHA_AVAILABLE:
            ColoredOutput.print_info("Using manual CAPTCHA solver (browser-based)")
            self.manual_solver = FreeCaptchaSolver()
        else:
            ColoredOutput.print_warning("No CAPTCHA solver available")
    
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
            
            # Check if CAPTCHA is required
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    if 'captcha_key' in error_data or 'captcha_sitekey' in error_data:
                        ColoredOutput.print_warning("CAPTCHA required! Attempting to solve...")
                        
                        captcha_sitekey = error_data.get('captcha_sitekey', [''])[0] if isinstance(error_data.get('captcha_sitekey'), list) else error_data.get('captcha_sitekey', '')
                        captcha_service = error_data.get('captcha_service', 'hcaptcha')
                        
                        ColoredOutput.print_info(f"CAPTCHA service: {captcha_service}")
                        ColoredOutput.print_info(f"Site key: {captcha_sitekey}")
                        
                        # Try to solve CAPTCHA
                        captcha_solution = self._solve_captcha(captcha_sitekey, oauth_url, captcha_service)
                        
                        if captcha_solution:
                            ColoredOutput.print_success("CAPTCHA solved! Retrying authorization...")
                            
                            # Add CAPTCHA solution to options
                            final_options['captcha_key'] = captcha_solution
                            
                            # Retry with CAPTCHA solution
                            response = self.session.post(
                                api_url,
                                params=query_only,
                                json=final_options
                            )
                            
                            if response.status_code == 200:
                                ColoredOutput.print_success("Bot authorized successfully (with CAPTCHA)!")
                                return response.json()
                            else:
                                ColoredOutput.print_error(f"Authorization failed even with CAPTCHA: {response.status_code}")
                                return {'error': response.text, 'status_code': response.status_code}
                        else:
                            ColoredOutput.print_error("Failed to solve CAPTCHA")
                            return {'error': 'CAPTCHA solving failed', 'status_code': 400}
                except:
                    pass
            
            ColoredOutput.print_error(f"Authorization failed: {response.status_code}")
            ColoredOutput.print_error(f"Response: {response.text}")
            return {'error': response.text, 'status_code': response.status_code}
                
        except Exception as e:
            ColoredOutput.print_error(f"Request failed: {str(e)}")
            return {'error': str(e)}
    
    def _solve_captcha(self, sitekey: str, url: str, service: str = 'hcaptcha') -> Optional[str]:
        """
        Solve CAPTCHA using available methods
        
        Args:
            sitekey: CAPTCHA site key
            url: Page URL
            service: CAPTCHA service type (hcaptcha, recaptcha)
            
        Returns:
            CAPTCHA solution token or None
        """
        ColoredOutput.print_info(f"Attempting to solve {service} CAPTCHA...")
        
        # Try LLM solver first (free, automatic)
        if self.llm_solver and self.use_llm_captcha:
            ColoredOutput.print_info("🤖 Using free LLM CAPTCHA solver...")
            try:
                solution = self.llm_solver.solve_hcaptcha(sitekey, url)
                if solution:
                    return solution
                else:
                    ColoredOutput.print_warning("LLM solver couldn't solve, trying fallback...")
            except Exception as e:
                ColoredOutput.print_warning(f"LLM solver error: {str(e)}")
        
        # Fallback to manual solver (browser-based, free)
        if self.manual_solver:
            ColoredOutput.print_info("🌐 Opening browser for manual CAPTCHA solving...")
            ColoredOutput.print_warning("Please solve the CAPTCHA in your browser")
            try:
                solution = self.manual_solver.solve_captcha(sitekey, url)
                return solution
            except Exception as e:
                ColoredOutput.print_error(f"Manual solver error: {str(e)}")
        
        # No solver available
        ColoredOutput.print_error("No CAPTCHA solver available!")
        return None


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
    
    # Ask about LLM CAPTCHA
    print(f"\n{ColoredOutput.CYAN}Use free LLM for CAPTCHA solving? (Y/n):{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.WARNING}LLM solver is 100% free and automatic (Termux-friendly){ColoredOutput.ENDC}")
    use_llm = input("> ").strip().lower()
    use_llm_captcha = use_llm != 'n'
    
    # Create authorizer
    authorizer = BotAuthorizer(user_token, use_llm_captcha=use_llm_captcha)
    
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
