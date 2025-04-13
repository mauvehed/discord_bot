import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Load all cogs from the cogs directory
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename[:-3]}')
        
        # Sync commands with Discord
        await self.tree.sync()

bot = Bot()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is connected to {len(bot.guilds)} guilds')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, app_commands.CommandNotFound):
        await ctx.send("Command not found. Use /help to see available commands.")
    elif isinstance(error, app_commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main() 