#!/usr/bin/env python3
"""
Discord VC Bot - Joins and stays in a voice channel
For Educational Purposes Only
"""

import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID', 0))
CHANNEL_ID = int(os.getenv('CHANNEL_ID', 0))

# Validate environment variables
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")
if not GUILD_ID:
    raise ValueError("GUILD_ID environment variable is not set")
if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID environment variable is not set")

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Try to join the voice channel
    await join_voice_channel()

async def join_voice_channel():
    """Join the specified voice channel"""
    try:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            print(f"Error: Could not find guild with ID {GUILD_ID}")
            return
        
        channel = guild.get_channel(CHANNEL_ID)
        if not channel:
            print(f"Error: Could not find channel with ID {CHANNEL_ID}")
            return
        
        # Check if channel is a voice channel (type 2 only)
        if channel.type.value != 2:
            print(f"Error: Channel {channel.name} is not a voice channel (type {channel.type.value})")
            return
        
        # Join the voice channel
        voice_client = await channel.connect()
        print(f"Successfully joined voice channel: {channel.name}")
        
    except Exception as e:
        print(f"Error joining voice channel: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state updates"""
    if member == bot.user:
        if after.channel is None:
            print("Bot was disconnected from voice channel")
            # Try to rejoin after a delay
            await asyncio.sleep(5)
            await join_voice_channel()

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
