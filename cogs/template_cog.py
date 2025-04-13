import discord
from discord import app_commands
from discord.ext import commands

class TemplateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready!')

    # Example slash command
    @app_commands.command(name="ping", description="A simple ping command")
    async def ping(self, interaction: discord.Interaction):
        """A simple ping command"""
        await interaction.response.send_message('Pong!')

async def setup(bot):
    await bot.add_cog(TemplateCog(bot)) 