#!/usr/bin/env python3
"""
Discord Bot Authorization Script - For Educational Purposes Only
Automatically authorizes a bot to join a guild using OAuth2
Inspired by discord.js-selfbot-v13

DISCLAIMER: This tool is for educational and research purposes only.
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
        print(f"{ColoredOutput.GREEN}[+] {msg}{ColoredOutput.ENDC}")
    
    @staticmethod
    def print_error(msg):
        print(f"{ColoredOutput.FAIL}[-] {msg}{ColoredOutput.ENDC}")
    
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
            use_llm_captcha: Use free LLM for CAPTCHA solving (default: True).
                           If False, uses manual browser-based solving only.
                           LLM is faster and automatic, manual is 100% reliable.
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
            ColoredOutput.print_success("Free LLM CAPTCHA solver enabled!")
            self.llm_solver = LLMCaptchaSolver()
            # Always initialize manual solver as fallback
            if FREE_CAPTCHA_AVAILABLE:
                self.manual_solver = FreeCaptchaSolver()
        elif FREE_CAPTCHA_AVAILABLE:
            ColoredOutput.print_info("Using manual CAPTCHA solver (browser-based)")
            self.manual_solver = FreeCaptchaSolver()
        else:
            ColoredOutput.print_warning("No CAPTCHA solver available")
    
    def get_user_guilds(self) -> list:
        """
        Get all guilds where the user has permissions
        
        Returns:
            List of guilds with their details
        """
        try:
            response = self.session.get(f"{self.api_base}/users/@me/guilds")
            
            if response.status_code == 200:
                guilds = response.json()
                ColoredOutput.print_success(f"Found {len(guilds)} guilds")
                return guilds
            else:
                ColoredOutput.print_error(f"Failed to fetch guilds: {response.status_code}")
                return []
        except Exception as e:
            ColoredOutput.print_error(f"Error fetching guilds: {str(e)}")
            return []
    
    def filter_guilds_with_permissions(self, guilds: list, required_permission: int = 0x20) -> list:
        """
        Filter guilds where user has specific permissions
        
        Args:
            guilds: List of guilds
            required_permission: Permission bit (0x20 = MANAGE_GUILD, 0x8 = ADMINISTRATOR)
            
        Returns:
            List of guilds where user has required permissions
        """
        filtered_guilds = []
        for guild in guilds:
            permissions = int(guild.get('permissions', 0))
            # Check if user has required permission or is administrator
            if (permissions & required_permission) or (permissions & 0x8):
                filtered_guilds.append(guild)
        
        ColoredOutput.print_info(f"Found {len(filtered_guilds)} guilds with required permissions")
        return filtered_guilds
    
    def build_oauth_url(self, client_id: str, permissions: str = "0", scope: str = "bot") -> str:
        """
        Build OAuth2 URL from client ID
        
        Args:
            client_id: Bot's application/client ID
            permissions: Permission integer (default: "0")
            scope: OAuth scope (default: "bot")
            
        Returns:
            Full OAuth2 authorization URL
        """
        return f"https://discord.com/api/oauth2/authorize?client_id={client_id}&scope={scope}&permissions={permissions}"
    
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
                        captcha_rqtoken = error_data.get('captcha_rqtoken', '')
                        
                        ColoredOutput.print_info(f"CAPTCHA service: {captcha_service}")
                        ColoredOutput.print_info(f"Site key: {captcha_sitekey}")
                        if captcha_rqtoken:
                            ColoredOutput.print_info(f"RQToken: {captcha_rqtoken[:20]}...")
                        
                        # Try to solve CAPTCHA
                        captcha_solution = self._solve_captcha(captcha_sitekey, oauth_url, captcha_service)
                        
                        if captcha_solution:
                            ColoredOutput.print_success("CAPTCHA solved! Retrying authorization...")
                            
                            # Add CAPTCHA solution to options - must be list format for Discord API
                            final_options['captcha_key'] = captcha_solution
                            if captcha_rqtoken:
                                final_options['captcha_rqtoken'] = captcha_rqtoken
                            
                            # Log the retry attempt for debugging
                            ColoredOutput.print_info("Retrying authorization with CAPTCHA solution...")
                            ColoredOutput.print_info(f"Request params: {query_only}")
                            ColoredOutput.print_info(f"Guild ID: {final_options.get('guild_id', 'N/A')}")
                            
                            # Retry with CAPTCHA solution
                            retry_response = self.session.post(
                                api_url,
                                params=query_only,
                                json=final_options
                            )
                            
                            if retry_response.status_code == 200:
                                ColoredOutput.print_success("Bot authorized successfully (with CAPTCHA)!")
                                return retry_response.json()
                            else:
                                ColoredOutput.print_error(f"Authorization failed even with CAPTCHA: {retry_response.status_code}")
                                ColoredOutput.print_error(f"Response body: {retry_response.text}")
                                # Try to parse error details
                                try:
                                    error_details = retry_response.json()
                                    ColoredOutput.print_error(f"Error details: {json.dumps(error_details, indent=2)}")
                                except:
                                    pass
                                return {'error': retry_response.text, 'status_code': retry_response.status_code, 'details': 'CAPTCHA solution may be invalid or expired'}
                        else:
                            ColoredOutput.print_error("Failed to solve CAPTCHA")
                            return {'error': 'CAPTCHA solving failed', 'status_code': 400}
                except Exception as e:
                    ColoredOutput.print_error(f"Error handling CAPTCHA: {str(e)}")
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
            ColoredOutput.print_info("Using free LLM CAPTCHA solver...")
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
            ColoredOutput.print_info("Opening browser for manual CAPTCHA solving...")
            ColoredOutput.print_warning("Please solve the CAPTCHA in your browser")
            try:
                solution = self.manual_solver.solve_captcha(sitekey, url)
                return solution
            except Exception as e:
                ColoredOutput.print_error(f"Manual solver error: {str(e)}")
        
        # No solver available
        ColoredOutput.print_error("No CAPTCHA solver available!")
        return None
    
    def authorize_bot_to_all_guilds(self, client_id: str, permissions: str = "0") -> Dict:
        """
        Authorize bot to all guilds where user has permissions
        
        Args:
            client_id: Bot's application/client ID
            permissions: Permission integer (default: "0")
            
        Returns:
            Dictionary with results for each guild
        """
        # Get all user guilds
        ColoredOutput.print_info("Fetching your guilds...")
        guilds = self.get_user_guilds()
        
        if not guilds:
            ColoredOutput.print_error("No guilds found or unable to fetch guilds")
            return {'error': 'No guilds found', 'results': []}
        
        # Filter guilds where user has manage server permission
        manageable_guilds = self.filter_guilds_with_permissions(guilds)
        
        if not manageable_guilds:
            ColoredOutput.print_warning("No guilds found where you have manage server permissions")
            return {'error': 'No manageable guilds', 'results': []}
        
        # Display guilds
        print(f"\n{ColoredOutput.CYAN}╔{'═' * 58}╗{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.CYAN}║{ColoredOutput.ENDC} {ColoredOutput.BOLD}Guilds where you can add the bot:{ColoredOutput.ENDC}                    {ColoredOutput.CYAN}║{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.CYAN}╠{'═' * 58}╣{ColoredOutput.ENDC}")
        for i, guild in enumerate(manageable_guilds, 1):
            guild_name = guild.get('name', 'Unknown')
            # Safely truncate guild name to fit in 40 characters, handling Unicode
            if len(guild_name) > 40:
                guild_name = guild_name[:37] + '...'
            guild_id = guild.get('id', 'Unknown')
            # Use ljust for better Unicode handling
            print(f"{ColoredOutput.CYAN}║{ColoredOutput.ENDC} {ColoredOutput.WARNING}[{i}]{ColoredOutput.ENDC} {guild_name.ljust(40)} {ColoredOutput.CYAN}║{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.CYAN}╚{'═' * 58}╝{ColoredOutput.ENDC}")
        
        print()
        results = []
        successful = 0
        failed = 0
        
        # Build OAuth URL
        oauth_url = self.build_oauth_url(client_id, permissions)
        
        # Authorize bot to each guild
        for i, guild in enumerate(manageable_guilds, 1):
            guild_id = guild.get('id')
            guild_name = guild.get('name', 'Unknown')
            
            print(f"\n{ColoredOutput.BLUE}[{i}/{len(manageable_guilds)}]{ColoredOutput.ENDC} Adding bot to: {ColoredOutput.BOLD}{guild_name}{ColoredOutput.ENDC}")
            
            options = {
                'guild_id': guild_id,
                'permissions': permissions,
                'integration_type': 0
            }
            
            result = self.authorize_url(oauth_url, options)
            
            if 'error' not in result:
                ColoredOutput.print_success(f"Bot added to {guild_name}")
                successful += 1
                results.append({
                    'guild_id': guild_id,
                    'guild_name': guild_name,
                    'status': 'success',
                    'result': result
                })
            else:
                ColoredOutput.print_error(f"Failed to add bot to {guild_name}")
                failed += 1
                results.append({
                    'guild_id': guild_id,
                    'guild_name': guild_name,
                    'status': 'failed',
                    'error': result.get('error', 'Unknown error')
                })
            
            # Rate limiting - wait between requests to avoid Discord API rate limits
            # Discord typically allows around 5 requests per second, so 2 seconds is conservative
            if i < len(manageable_guilds):
                time.sleep(2)
        
        # Summary
        print()
        print(f"{ColoredOutput.CYAN}{'─' * 60}{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.BOLD}{ColoredOutput.CYAN}           AUTHORIZATION SUMMARY{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.CYAN}{'─' * 60}{ColoredOutput.ENDC}")
        ColoredOutput.print_success(f"Successful: {successful}/{len(manageable_guilds)}")
        if failed > 0:
            ColoredOutput.print_error(f"Failed: {failed}/{len(manageable_guilds)}")
        
        return {
            'total': len(manageable_guilds),
            'successful': successful,
            'failed': failed,
            'results': results
        }


def main():
    """Main function"""
    print(f"{ColoredOutput.BOLD}{ColoredOutput.HEADER}")
    print(r"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    ____        __     ___       __    __                 ║
║   / __ )____  / /_   /   | ____/ /___/ /__  _____        ║
║  / __  / __ \/ __/  / /| |/ __  / __  / _ \/ ___/        ║
║ / /_/ / /_/ / /_   / ___ / /_/ / /_/ /  __/ /            ║
║/_____/\____/\__/  /_/  |_\__,_/\__,_/\___/_/             ║
║                                                           ║
║                  By Kaala Tanmay                          ║
║                                                           ║
║         Discord Bot Authorizer - Educational Use          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    print(f"{ColoredOutput.ENDC}")
    
    print(f"{ColoredOutput.WARNING}╔{'═' * 58}╗{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.WARNING}║ WARNING: This tool is for educational purposes only!     ║{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.WARNING}║ WARNING: Use at your own risk!                           ║{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.WARNING}╚{'═' * 58}╝{ColoredOutput.ENDC}")
    print()
    
    # Get user token
    print(f"\n{ColoredOutput.CYAN}┌{'─' * 58}┐{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.BOLD}Enter your Discord account token:{ColoredOutput.ENDC}                  {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}└{'─' * 58}┘{ColoredOutput.ENDC}")
    user_token = input(f"{ColoredOutput.GREEN}>> {ColoredOutput.ENDC}").strip()
    
    if not user_token:
        ColoredOutput.print_error("Token is required!")
        sys.exit(1)
    
    # Get bot client ID
    print(f"\n{ColoredOutput.CYAN}┌{'─' * 58}┐{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.BOLD}Enter the bot Client ID:{ColoredOutput.ENDC}                           {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.WARNING}Example: 123456789012345678{ColoredOutput.ENDC}                        {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}└{'─' * 58}┘{ColoredOutput.ENDC}")
    client_id = input(f"{ColoredOutput.GREEN}>> {ColoredOutput.ENDC}").strip()
    
    if not client_id:
        ColoredOutput.print_error("Client ID is required!")
        sys.exit(1)
    
    # Get permissions (optional)
    print(f"\n{ColoredOutput.CYAN}┌{'─' * 58}┐{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.BOLD}Enter permissions (default: 0):{ColoredOutput.ENDC}                    {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.WARNING}0=None | 8=Admin | 2048=Messages | 2147483647=All{ColoredOutput.ENDC}  {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}└{'─' * 58}┘{ColoredOutput.ENDC}")
    permissions = input(f"{ColoredOutput.GREEN}>> {ColoredOutput.ENDC}").strip() or "0"
    
    # Ask about authorization mode
    print(f"\n{ColoredOutput.CYAN}┌{'─' * 58}┐{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.BOLD}Authorization Mode:{ColoredOutput.ENDC}                                 {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.WARNING}[1]{ColoredOutput.ENDC} Add bot to ALL servers (recommended)           {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.WARNING}[2]{ColoredOutput.ENDC} Add bot to a SPECIFIC server                   {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}└{'─' * 58}┘{ColoredOutput.ENDC}")
    mode = input(f"{ColoredOutput.GREEN}>> {ColoredOutput.ENDC}").strip() or "1"
    
    # Get guild ID only if specific mode
    guild_id = None
    if mode == "2":
        print(f"\n{ColoredOutput.CYAN}┌{'─' * 58}┐{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.BOLD}Enter the Guild ID:{ColoredOutput.ENDC}                                 {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.CYAN}└{'─' * 58}┘{ColoredOutput.ENDC}")
        guild_id = input(f"{ColoredOutput.GREEN}>> {ColoredOutput.ENDC}").strip()
        if not guild_id:
            ColoredOutput.print_error("Guild ID is required for specific server mode!")
            sys.exit(1)
    
    # Ask about LLM CAPTCHA
    print(f"\n{ColoredOutput.CYAN}┌{'─' * 58}┐{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.BOLD}Use free LLM for CAPTCHA solving? (Y/n):{ColoredOutput.ENDC}           {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.WARNING}LLM solver is 100% free and automatic{ColoredOutput.ENDC}              {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}└{'─' * 58}┘{ColoredOutput.ENDC}")
    use_llm = input(f"{ColoredOutput.GREEN}>> {ColoredOutput.ENDC}").strip().lower()
    use_llm_captcha = use_llm != 'n'
    
    # Create authorizer
    authorizer = BotAuthorizer(user_token, use_llm_captcha=use_llm_captcha)
    
    print()
    print(f"{ColoredOutput.BLUE}{'═' * 60}{ColoredOutput.ENDC}")
    ColoredOutput.print_info("Starting authorization process...")
    print(f"{ColoredOutput.BLUE}{'═' * 60}{ColoredOutput.ENDC}")
    
    # Authorize based on mode
    if mode == "1":
        # Add to all guilds
        result = authorizer.authorize_bot_to_all_guilds(client_id, permissions)
        
        # Display results
        print()
        if result.get('successful', 0) > 0:
            print(f"{ColoredOutput.GREEN}╔{'═' * 58}╗{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.GREEN}║{ColoredOutput.ENDC} {ColoredOutput.BOLD}Bot authorization completed!{ColoredOutput.ENDC}                          {ColoredOutput.GREEN}║{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.GREEN}╚{'═' * 58}╝{ColoredOutput.ENDC}")
            print()
            ColoredOutput.print_info("Summary:")
            print(json.dumps({
                'total_guilds': result.get('total', 0),
                'successful': result.get('successful', 0),
                'failed': result.get('failed', 0)
            }, indent=2))
            
            if result.get('failed', 0) > 0:
                ColoredOutput.print_warning("\nSome guilds failed. Check details above.")
        else:
            print(f"{ColoredOutput.FAIL}╔{'═' * 58}╗{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.FAIL}║{ColoredOutput.ENDC} {ColoredOutput.BOLD}Failed to add bot to any guild{ColoredOutput.ENDC}                       {ColoredOutput.FAIL}║{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.FAIL}╚{'═' * 58}╝{ColoredOutput.ENDC}")
            sys.exit(1)
    else:
        # Add to specific guild
        oauth_url = authorizer.build_oauth_url(client_id, permissions)
        options = {
            'guild_id': guild_id,
            'permissions': permissions,
            'integration_type': 0
        }
        
        result = authorizer.authorize_url(oauth_url, options)
        
        # Display results
        print()
        if 'error' not in result:
            print(f"{ColoredOutput.GREEN}╔{'═' * 58}╗{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.GREEN}║{ColoredOutput.ENDC} {ColoredOutput.BOLD}Bot successfully added to the guild!{ColoredOutput.ENDC}                  {ColoredOutput.GREEN}║{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.GREEN}╚{'═' * 58}╝{ColoredOutput.ENDC}")
            print()
            ColoredOutput.print_info("Response details:")
            print(json.dumps(result, indent=2))
        else:
            print(f"{ColoredOutput.FAIL}╔{'═' * 58}╗{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.FAIL}║{ColoredOutput.ENDC} {ColoredOutput.BOLD}Failed to add bot to guild{ColoredOutput.ENDC}                           {ColoredOutput.FAIL}║{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.FAIL}╚{'═' * 58}╝{ColoredOutput.ENDC}")
            print()
            ColoredOutput.print_info("Error details:")
            print(json.dumps(result, indent=2))
            sys.exit(1)


if __name__ == "__main__":
    main()
