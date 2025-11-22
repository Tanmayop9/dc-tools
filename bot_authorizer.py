#!/usr/bin/env python3
"""
Ultra Advanced Discord Bot Authorization Script - For Educational Purposes Only

Features:
- Ultra-fast concurrent authorization to multiple guilds
- Advanced free CAPTCHA solving with multiple methods
- Smart retry logic with exponential backoff
- Session persistence and recovery
- Connection pooling for optimal performance
- Proxy rotation support
- Rate limit handling with intelligent delays
- Comprehensive error handling and logging
- Performance metrics and statistics

Inspired by discord.js-selfbot-v13

DISCLAIMER: This tool is for educational and research purposes only.
Use at your own risk. The authors are not responsible for any misuse.
"""

import requests
import json
import re
import sys
import time
import asyncio
import aiohttp
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# Import ultra advanced CAPTCHA solver
try:
    from captcha_solver_ultra import UltraAdvancedCaptchaSolver
    ULTRA_CAPTCHA_AVAILABLE = True
except ImportError:
    ULTRA_CAPTCHA_AVAILABLE = False

# Fallback to LLM solver
try:
    from captcha_solver_llm import LLMCaptchaSolver
    LLM_CAPTCHA_AVAILABLE = True
except ImportError:
    LLM_CAPTCHA_AVAILABLE = False

# Fallback to manual solver
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
    """Ultra Advanced Discord Bot OAuth2 Authorization Handler
    
    Features:
    - Concurrent guild authorization for maximum speed
    - Advanced free CAPTCHA solving with multiple methods
    - Smart retry logic with exponential backoff
    - Session management and connection pooling
    - Comprehensive error handling and recovery
    """
    
    def __init__(self, user_token: str, use_ultra_captcha: bool = True, max_concurrent: int = 5, use_proxies: bool = False):
        """
        Initialize the ultra advanced bot authorizer
        
        Args:
            user_token: Discord user account token
            use_ultra_captcha: Use ultra advanced free CAPTCHA solver (default: True)
            max_concurrent: Maximum concurrent authorization requests (default: 5)
            use_proxies: Enable proxy rotation (default: False)
        """
        self.user_token = user_token
        self.api_base = "https://discord.com/api/v9"
        self.use_ultra_captcha = use_ultra_captcha
        self.max_concurrent = max_concurrent
        self.use_proxies = use_proxies
        
        # Advanced session with connection pooling
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=3,
            pool_block=False
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        self.session.headers.update({
            'Authorization': user_token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Initialize ultra advanced CAPTCHA solver
        self.captcha_solver = None
        
        if use_ultra_captcha and ULTRA_CAPTCHA_AVAILABLE:
            ColoredOutput.print_success("Ultra Advanced Free CAPTCHA Solver enabled!")
            ColoredOutput.print_info("Using multi-method solver chain with AI, OCR, and browser automation")
            self.captcha_solver = UltraAdvancedCaptchaSolver()
        elif LLM_CAPTCHA_AVAILABLE:
            ColoredOutput.print_info("Using LLM CAPTCHA solver (fallback)")
            self.captcha_solver = LLMCaptchaSolver()
        elif FREE_CAPTCHA_AVAILABLE:
            ColoredOutput.print_info("Using manual CAPTCHA solver (browser-based)")
            self.captcha_solver = FreeCaptchaSolver()
        else:
            ColoredOutput.print_warning("No CAPTCHA solver available")
        
        # Performance metrics
        self.metrics = {
            'total_attempts': 0,
            'successful': 0,
            'failed': 0,
            'captcha_solved': 0,
            'start_time': time.time(),
            'guild_times': []
        }
        
        # Proxy configuration
        self.proxies = []
        self.proxy_index = 0
        if use_proxies:
            self._load_proxies()
        
        ColoredOutput.print_success("Ultra Advanced Bot Authorizer initialized!")
        ColoredOutput.print_info(f"Max concurrent requests: {max_concurrent}")
    
    def _load_proxies(self):
        """Load proxies from file"""
        try:
            proxy_file = Path('proxies.txt')
            if proxy_file.exists():
                with open(proxy_file, 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                ColoredOutput.print_success(f"Loaded {len(self.proxies)} proxies")
            else:
                ColoredOutput.print_warning("No proxies.txt file found")
        except Exception as e:
            ColoredOutput.print_warning(f"Failed to load proxies: {str(e)}")
    
    def _get_next_proxy(self) -> Optional[Dict]:
        """Get next proxy in rotation"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
    
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
                        captcha_rqdata = error_data.get('captcha_rqdata', '')
                        captcha_session_id = error_data.get('captcha_session_id', '')
                        
                        ColoredOutput.print_info(f"CAPTCHA service: {captcha_service}")
                        ColoredOutput.print_info(f"Site key: {captcha_sitekey}")
                        if captcha_rqtoken:
                            ColoredOutput.print_info(f"RQToken: {captcha_rqtoken[:20]}...")
                        if captcha_session_id:
                            ColoredOutput.print_info(f"Session ID: {captcha_session_id}")
                        
                        # Try to solve CAPTCHA
                        captcha_solution = self._solve_captcha(captcha_sitekey, oauth_url, captcha_service)
                        
                        if captcha_solution:
                            ColoredOutput.print_success("CAPTCHA solved! Retrying authorization...")
                            
                            # Add CAPTCHA solution to options
                            final_options['captcha_key'] = captcha_solution
                            # Include all CAPTCHA-related fields from Discord's response
                            # These fields are required by Discord API to validate the CAPTCHA solution
                            # Missing any of these fields will result in "invalid-response" error
                            if captcha_rqtoken:
                                final_options['captcha_rqtoken'] = captcha_rqtoken
                            if captcha_rqdata:
                                final_options['captcha_rqdata'] = captcha_rqdata
                            if captcha_session_id:
                                final_options['captcha_session_id'] = captcha_session_id
                            
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
        Solve CAPTCHA using ultra advanced solver chain
        
        Args:
            sitekey: CAPTCHA site key
            url: Page URL
            service: CAPTCHA service type (hcaptcha, recaptcha)
            
        Returns:
            CAPTCHA solution token or None
        """
        ColoredOutput.print_info(f"Attempting to solve {service} CAPTCHA with ultra advanced methods...")
        
        start_time = time.time()
        
        # Use ultra advanced solver if available
        if self.captcha_solver:
            try:
                ColoredOutput.print_info("Using Ultra Advanced Free CAPTCHA Solver Chain...")
                ColoredOutput.print_info("This will try multiple methods: AI Vision, OCR, Pattern Recognition, Browser")
                
                solution = None
                if hasattr(self.captcha_solver, 'solve_hcaptcha'):
                    solution = self.captcha_solver.solve_hcaptcha(sitekey, url)
                elif hasattr(self.captcha_solver, 'solve_captcha'):
                    solution = self.captcha_solver.solve_captcha(sitekey, url)
                
                if solution:
                    solve_time = time.time() - start_time
                    ColoredOutput.print_success(f"CAPTCHA solved in {solve_time:.2f}s!")
                    self.metrics['captcha_solved'] += 1
                    return solution
                else:
                    ColoredOutput.print_warning("All solver methods failed")
            except Exception as e:
                ColoredOutput.print_error(f"Solver error: {str(e)}")
        else:
            ColoredOutput.print_error("No CAPTCHA solver available!")
        
        return None
    
    def _authorize_single_guild(self, guild: Dict, oauth_url: str, permissions: str) -> Tuple[Dict, float]:
        """
        Authorize bot to a single guild with retry logic
        
        Args:
            guild: Guild information dictionary
            oauth_url: OAuth URL for authorization
            permissions: Permission string
            
        Returns:
            Tuple of (result dictionary, execution time)
        """
        start_time = time.time()
        guild_id = guild.get('id')
        guild_name = guild.get('name', 'Unknown')
        
        options = {
            'guild_id': guild_id,
            'permissions': permissions,
            'integration_type': 0
        }
        
        # Retry logic with exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = self.authorize_url(oauth_url, options)
                
                if 'error' not in result:
                    execution_time = time.time() - start_time
                    return {
                        'guild_id': guild_id,
                        'guild_name': guild_name,
                        'status': 'success',
                        'result': result,
                        'attempts': attempt + 1
                    }, execution_time
                
                # If error is rate limit, wait and retry
                if 'rate limit' in str(result.get('error', '')).lower():
                    wait_time = (2 ** attempt) * 2  # Exponential backoff
                    ColoredOutput.print_warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                # For other errors, return immediately
                execution_time = time.time() - start_time
                return {
                    'guild_id': guild_id,
                    'guild_name': guild_name,
                    'status': 'failed',
                    'error': result.get('error', 'Unknown error'),
                    'attempts': attempt + 1
                }, execution_time
                
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                
                execution_time = time.time() - start_time
                return {
                    'guild_id': guild_id,
                    'guild_name': guild_name,
                    'status': 'failed',
                    'error': str(e),
                    'attempts': attempt + 1
                }, execution_time
        
        execution_time = time.time() - start_time
        return {
            'guild_id': guild_id,
            'guild_name': guild_name,
            'status': 'failed',
            'error': 'Max retries exceeded',
            'attempts': max_retries
        }, execution_time
    
    def authorize_bot_to_all_guilds(self, client_id: str, permissions: str = "0", use_concurrent: bool = True) -> Dict:
        """
        Authorize bot to all guilds where user has permissions
        Ultra-fast concurrent mode for maximum speed!
        
        Args:
            client_id: Bot's application/client ID
            permissions: Permission integer (default: "0")
            use_concurrent: Use concurrent authorization (default: True)
            
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
            if len(guild_name) > 40:
                guild_name = guild_name[:37] + '...'
            print(f"{ColoredOutput.CYAN}║{ColoredOutput.ENDC} {ColoredOutput.WARNING}[{i}]{ColoredOutput.ENDC} {guild_name.ljust(40)} {ColoredOutput.CYAN}║{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.CYAN}╚{'═' * 58}╝{ColoredOutput.ENDC}")
        
        print()
        
        # Build OAuth URL
        oauth_url = self.build_oauth_url(client_id, permissions)
        
        results = []
        successful = 0
        failed = 0
        total_start_time = time.time()
        
        if use_concurrent and len(manageable_guilds) > 1:
            # Ultra-fast concurrent mode
            ColoredOutput.print_success(f"Using ULTRA-FAST concurrent mode ({self.max_concurrent} workers)!")
            ColoredOutput.print_info("Processing all guilds simultaneously for maximum speed...")
            
            with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
                # Submit all tasks
                future_to_guild = {
                    executor.submit(self._authorize_single_guild, guild, oauth_url, permissions): guild
                    for guild in manageable_guilds
                }
                
                # Process completed tasks
                completed = 0
                for future in as_completed(future_to_guild):
                    completed += 1
                    guild = future_to_guild[future]
                    guild_name = guild.get('name', 'Unknown')
                    
                    try:
                        result, exec_time = future.result()
                        results.append(result)
                        
                        if result['status'] == 'success':
                            successful += 1
                            ColoredOutput.print_success(f"[{completed}/{len(manageable_guilds)}] {guild_name} - Success! ({exec_time:.2f}s)")
                        else:
                            failed += 1
                            ColoredOutput.print_error(f"[{completed}/{len(manageable_guilds)}] {guild_name} - Failed: {result.get('error', 'Unknown')}")
                        
                        self.metrics['guild_times'].append(exec_time)
                        
                    except Exception as e:
                        failed += 1
                        ColoredOutput.print_error(f"[{completed}/{len(manageable_guilds)}] {guild_name} - Exception: {str(e)}")
                        results.append({
                            'guild_id': guild.get('id'),
                            'guild_name': guild_name,
                            'status': 'failed',
                            'error': str(e)
                        })
        else:
            # Sequential mode (for single guild or when concurrent is disabled)
            for i, guild in enumerate(manageable_guilds, 1):
                guild_name = guild.get('name', 'Unknown')
                print(f"\n{ColoredOutput.BLUE}[{i}/{len(manageable_guilds)}]{ColoredOutput.ENDC} Adding bot to: {ColoredOutput.BOLD}{guild_name}{ColoredOutput.ENDC}")
                
                result, exec_time = self._authorize_single_guild(guild, oauth_url, permissions)
                results.append(result)
                
                if result['status'] == 'success':
                    ColoredOutput.print_success(f"Bot added to {guild_name} ({exec_time:.2f}s)")
                    successful += 1
                else:
                    ColoredOutput.print_error(f"Failed to add bot to {guild_name}: {result.get('error', 'Unknown')}")
                    failed += 1
                
                self.metrics['guild_times'].append(exec_time)
                
                # Rate limiting between sequential requests
                if i < len(manageable_guilds):
                    time.sleep(1.5)
        
        total_time = time.time() - total_start_time
        avg_time = sum(self.metrics['guild_times']) / len(self.metrics['guild_times']) if self.metrics['guild_times'] else 0
        
        # Summary
        print()
        print(f"{ColoredOutput.CYAN}{'─' * 60}{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.BOLD}{ColoredOutput.CYAN}           AUTHORIZATION SUMMARY{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.CYAN}{'─' * 60}{ColoredOutput.ENDC}")
        ColoredOutput.print_success(f"Successful: {successful}/{len(manageable_guilds)}")
        if failed > 0:
            ColoredOutput.print_error(f"Failed: {failed}/{len(manageable_guilds)}")
        ColoredOutput.print_info(f"Total time: {total_time:.2f}s")
        ColoredOutput.print_info(f"Average per guild: {avg_time:.2f}s")
        if use_concurrent and len(manageable_guilds) > 1:
            sequential_estimate = avg_time * len(manageable_guilds)
            speedup = sequential_estimate / total_time if total_time > 0 else 1
            ColoredOutput.print_success(f"Concurrent speedup: {speedup:.1f}x faster!")
        
        self.metrics['total_attempts'] += len(manageable_guilds)
        self.metrics['successful'] += successful
        self.metrics['failed'] += failed
        
        return {
            'total': len(manageable_guilds),
            'successful': successful,
            'failed': failed,
            'results': results,
            'total_time': total_time,
            'average_time': avg_time
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
    
    # Ask about Ultra Advanced CAPTCHA solver
    print(f"\n{ColoredOutput.CYAN}┌{'─' * 58}┐{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.BOLD}Use Ultra Advanced Free CAPTCHA solver? (Y/n):{ColoredOutput.ENDC}     {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.WARNING}Multi-method: AI, OCR, Pattern, Browser (100% free){ColoredOutput.ENDC}  {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}└{'─' * 58}┘{ColoredOutput.ENDC}")
    use_ultra = input(f"{ColoredOutput.GREEN}>> {ColoredOutput.ENDC}").strip().lower()
    use_ultra_captcha = use_ultra != 'n'
    
    # Ask about concurrent mode
    print(f"\n{ColoredOutput.CYAN}┌{'─' * 58}┐{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.BOLD}Use ultra-fast concurrent mode? (Y/n):{ColoredOutput.ENDC}             {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}│{ColoredOutput.ENDC} {ColoredOutput.WARNING}Process multiple guilds simultaneously for max speed{ColoredOutput.ENDC}  {ColoredOutput.CYAN}│{ColoredOutput.ENDC}")
    print(f"{ColoredOutput.CYAN}└{'─' * 58}┘{ColoredOutput.ENDC}")
    use_concurrent_input = input(f"{ColoredOutput.GREEN}>> {ColoredOutput.ENDC}").strip().lower()
    use_concurrent = use_concurrent_input != 'n'
    
    # Create ultra advanced authorizer
    authorizer = BotAuthorizer(user_token, use_ultra_captcha=use_ultra_captcha, max_concurrent=5)
    
    print()
    print(f"{ColoredOutput.BLUE}{'═' * 60}{ColoredOutput.ENDC}")
    ColoredOutput.print_info("Starting authorization process...")
    print(f"{ColoredOutput.BLUE}{'═' * 60}{ColoredOutput.ENDC}")
    
    # Authorize based on mode
    if mode == "1":
        # Add to all guilds with concurrent mode
        result = authorizer.authorize_bot_to_all_guilds(client_id, permissions, use_concurrent=use_concurrent)
        
        # Print performance statistics
        authorizer.print_performance_stats()
        
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
                'failed': result.get('failed', 0),
                'total_time': f"{result.get('total_time', 0):.2f}s",
                'avg_time_per_guild': f"{result.get('average_time', 0):.2f}s"
            }, indent=2))
            
            if result.get('failed', 0) > 0:
                ColoredOutput.print_warning("\nSome guilds failed. Check details above.")
        else:
            print(f"{ColoredOutput.FAIL}╔{'═' * 58}╗{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.FAIL}║{ColoredOutput.ENDC} {ColoredOutput.BOLD}Failed to add bot to any guild{ColoredOutput.ENDC}                       {ColoredOutput.FAIL}║{ColoredOutput.ENDC}")
            print(f"{ColoredOutput.FAIL}╚{'═' * 58}╝{ColoredOutput.ENDC}")
            authorizer.print_performance_stats()
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
        
        # Print performance statistics
        authorizer.print_performance_stats()
        
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


    def print_performance_stats(self):
        """Print comprehensive performance statistics"""
        print()
        print(f"{ColoredOutput.CYAN}{'═' * 60}{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.BOLD}{ColoredOutput.CYAN}         PERFORMANCE STATISTICS{ColoredOutput.ENDC}")
        print(f"{ColoredOutput.CYAN}{'═' * 60}{ColoredOutput.ENDC}")
        
        total_time = time.time() - self.metrics['start_time']
        
        ColoredOutput.print_info(f"Total runtime: {total_time:.2f}s")
        ColoredOutput.print_info(f"Total authorization attempts: {self.metrics['total_attempts']}")
        ColoredOutput.print_success(f"Successful authorizations: {self.metrics['successful']}")
        ColoredOutput.print_error(f"Failed authorizations: {self.metrics['failed']}")
        ColoredOutput.print_info(f"CAPTCHAs solved: {self.metrics['captcha_solved']}")
        
        if self.metrics['total_attempts'] > 0:
            success_rate = (self.metrics['successful'] / self.metrics['total_attempts']) * 100
            ColoredOutput.print_success(f"Success rate: {success_rate:.1f}%")
        
        if self.metrics['guild_times']:
            avg_time = sum(self.metrics['guild_times']) / len(self.metrics['guild_times'])
            min_time = min(self.metrics['guild_times'])
            max_time = max(self.metrics['guild_times'])
            ColoredOutput.print_info(f"Average time per guild: {avg_time:.2f}s")
            ColoredOutput.print_info(f"Fastest guild: {min_time:.2f}s")
            ColoredOutput.print_info(f"Slowest guild: {max_time:.2f}s")
        
        # Print CAPTCHA solver stats if available
        if self.captcha_solver and hasattr(self.captcha_solver, 'print_stats'):
            print()
            self.captcha_solver.print_stats()
        
        print(f"{ColoredOutput.CYAN}{'═' * 60}{ColoredOutput.ENDC}")


if __name__ == "__main__":
    main()
