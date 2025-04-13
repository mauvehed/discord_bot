import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class WhoisCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="whois", description="Get information about a user")
    @app_commands.describe(user="The user to get information about")
    async def whois(self, interaction: discord.Interaction, user: discord.Member = None):
        """Get detailed information about a user"""
        # If no user is specified, use the command author
        if user is None:
            user = interaction.user

        # Create embed
        embed = discord.Embed(
            title="User Information",
            color=user.color if user.color != discord.Color.default() else discord.Color.blue()
        )
        
        # Set thumbnail to user's avatar
        embed.set_thumbnail(url=user.display_avatar.url)
        
        # Basic Information
        embed.add_field(name="Username", value=f"{user.name}#{user.discriminator}", inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Nickname", value=user.nick if user.nick else "None", inline=True)
        
        # Account Information
        embed.add_field(
            name="Account Created", 
            value=user.created_at.strftime("%B %d, %Y at %I:%M %p UTC"),
            inline=True
        )
        embed.add_field(
            name="Joined Server", 
            value=user.joined_at.strftime("%B %d, %Y at %I:%M %p UTC") if user.joined_at else "Unknown",
            inline=True
        )
        
        # Status Information
        status = str(user.status).title()
        if user.activity:
            activity = f"{user.activity.type.name.title()}: {user.activity.name}"
        else:
            activity = "None"
        embed.add_field(name="Status", value=status, inline=True)
        embed.add_field(name="Activity", value=activity, inline=True)
        
        # Role Information
        roles = [role.mention for role in user.roles[1:]]  # Skip @everyone role
        roles_text = ", ".join(roles) if roles else "No roles"
        
        # If roles text is too long, split it into multiple fields
        if len(roles_text) > 1024:
            # Split roles into chunks of 1000 characters
            chunks = [roles_text[i:i+1000] for i in range(0, len(roles_text), 1000)]
            for i, chunk in enumerate(chunks, 1):
                field_name = f"Roles Part {i}" if len(chunks) > 1 else "Roles"
                embed.add_field(name=field_name, value=chunk, inline=False)
        else:
            embed.add_field(name=f"Roles ({len(roles)})", value=roles_text, inline=False)
        
        # Additional Information
        embed.add_field(
            name="Is Bot", 
            value="Yes" if user.bot else "No", 
            inline=True
        )
        embed.add_field(
            name="Is Server Owner", 
            value="Yes" if user.guild.owner_id == user.id else "No", 
            inline=True
        )
        
        # Footer with current time
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        embed.timestamp = datetime.utcnow()
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(WhoisCog(bot)) 