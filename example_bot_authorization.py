#!/usr/bin/env python3
"""
Example: Using Bot Authorizer Programmatically
This demonstrates how to use the BotAuthorizer class in your own scripts.

⚠️ For educational purposes only!
"""

import time
from bot_authorizer import BotAuthorizer, ColoredOutput

def example_basic_authorization():
    """Basic example of bot authorization"""
    ColoredOutput.print_info("Example 1: Basic Bot Authorization")
    ColoredOutput.print_info("=" * 50)
    
    # Your account token (⚠️ NEVER share this!)
    user_token = "<YOUR_DISCORD_TOKEN>"
    
    # Bot OAuth2 URL (from Discord Developer Portal)
    oauth_url = "https://discord.com/api/oauth2/authorize?client_id=<YOUR_BOT_ID>&scope=bot"
    
    # Target guild ID (default: 283939)
    guild_id = "283939"
    
    # Initialize the authorizer
    authorizer = BotAuthorizer(user_token)
    
    # Prepare authorization options
    options = {
        'guild_id': guild_id,
        'permissions': '0',  # No permissions
        'integration_type': 0
    }
    
    # Authorize the bot (commented out to prevent accidental execution)
    # result = authorizer.authorize_url(oauth_url, options)
    # print(result)
    
    ColoredOutput.print_warning("⚠️  Uncomment the authorization lines to actually run")
    print()


def example_with_permissions():
    """Example with specific permissions"""
    ColoredOutput.print_info("Example 2: Bot Authorization with Permissions")
    ColoredOutput.print_info("=" * 50)
    
    user_token = "<YOUR_DISCORD_TOKEN>"
    oauth_url = "https://discord.com/api/oauth2/authorize?client_id=<YOUR_BOT_ID>&scope=bot"
    
    # Common permission values:
    # 8 = Administrator
    # 2048 = Send Messages
    # 3072 = Send Messages + Embed Links
    # 2147483647 = All permissions
    
    options = {
        'guild_id': '283939',
        'permissions': '8',  # Administrator permissions
        'integration_type': 0
    }
    
    authorizer = BotAuthorizer(user_token)
    
    # Authorize the bot (commented out)
    # result = authorizer.authorize_url(oauth_url, options)
    # if 'error' not in result:
    #     ColoredOutput.print_success("Bot added with administrator permissions!")
    # else:
    #     ColoredOutput.print_error(f"Failed: {result['error']}")
    
    ColoredOutput.print_warning("⚠️  Uncomment the authorization lines to actually run")
    print()


def example_multiple_bots():
    """Example: Adding multiple bots"""
    ColoredOutput.print_info("Example 3: Adding Multiple Bots")
    ColoredOutput.print_info("=" * 50)
    
    user_token = "<YOUR_DISCORD_TOKEN>"
    guild_id = "283939"
    
    # List of bot OAuth2 URLs
    bot_urls = [
        "https://discord.com/api/oauth2/authorize?client_id=BOT1_ID&scope=bot",
        "https://discord.com/api/oauth2/authorize?client_id=BOT2_ID&scope=bot",
        "https://discord.com/api/oauth2/authorize?client_id=BOT3_ID&scope=bot",
    ]
    
    authorizer = BotAuthorizer(user_token)
    
    # Add each bot (commented out)
    # for i, oauth_url in enumerate(bot_urls, 1):
    #     ColoredOutput.print_info(f"Adding bot {i}/{len(bot_urls)}...")
    #     
    #     options = {
    #         'guild_id': guild_id,
    #         'permissions': '0',
    #         'integration_type': 0
    #     }
    #     
    #     result = authorizer.authorize_url(oauth_url, options)
    #     
    #     if 'error' not in result:
    #         ColoredOutput.print_success(f"Bot {i} added successfully!")
    #     else:
    #         ColoredOutput.print_error(f"Bot {i} failed: {result['error']}")
    #     
    #     # Rate limiting - wait between requests
    #     if i < len(bot_urls):
    #         time.sleep(2)
    
    ColoredOutput.print_warning("⚠️  Uncomment the authorization lines to actually run")
    print()


def example_error_handling():
    """Example with proper error handling"""
    ColoredOutput.print_info("Example 4: Bot Authorization with Error Handling")
    ColoredOutput.print_info("=" * 50)
    
    user_token = "<YOUR_DISCORD_TOKEN>"
    oauth_url = "https://discord.com/api/oauth2/authorize?client_id=<YOUR_BOT_ID>&scope=bot"
    
    try:
        authorizer = BotAuthorizer(user_token)
        
        # Validate URL first
        if not authorizer.validate_oauth_url(oauth_url):
            ColoredOutput.print_error("Invalid OAuth2 URL!")
            return
        
        options = {
            'guild_id': '283939',
            'permissions': '0',
            'integration_type': 0
        }
        
        # Authorize (commented out)
        # result = authorizer.authorize_url(oauth_url, options)
        # 
        # if 'error' in result:
        #     if result.get('status_code') == 401:
        #         ColoredOutput.print_error("Invalid token!")
        #     elif result.get('status_code') == 403:
        #         ColoredOutput.print_error("No permission to add bot!")
        #     elif result.get('status_code') == 429:
        #         ColoredOutput.print_error("Rate limited! Wait and try again.")
        #     else:
        #         ColoredOutput.print_error(f"Error: {result['error']}")
        # else:
        #     ColoredOutput.print_success("Bot added successfully!")
        #     print(f"Guild: {result.get('guild', {}).get('id', 'N/A')}")
        
        ColoredOutput.print_warning("⚠️  Uncomment the authorization lines to actually run")
        
    except ValueError as e:
        ColoredOutput.print_error(f"Validation error: {e}")
    except Exception as e:
        ColoredOutput.print_error(f"Unexpected error: {e}")
    
    print()


def main():
    """Run all examples"""
    print()
    print("=" * 60)
    print("Bot Authorizer - Usage Examples")
    print("=" * 60)
    print()
    
    ColoredOutput.print_warning("⚠️  These examples are for demonstration only!")
    ColoredOutput.print_warning("⚠️  Replace placeholder values with real data to use them.")
    ColoredOutput.print_warning("⚠️  Uncomment the code to execute actual API calls.")
    print()
    
    # Run examples
    example_basic_authorization()
    example_with_permissions()
    example_multiple_bots()
    example_error_handling()
    
    print("=" * 60)
    ColoredOutput.print_info("See BOT_AUTHORIZER.md for more details!")
    print("=" * 60)


if __name__ == "__main__":
    main()
