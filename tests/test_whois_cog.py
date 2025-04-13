import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
import discord
from discord.ext import commands
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cogs.whois_cog import WhoisCog

@pytest.fixture
def mock_bot():
    bot = MagicMock(spec=commands.Bot)
    return bot

@pytest.fixture
def mock_interaction():
    # Create the interaction mock
    interaction = AsyncMock(spec=discord.Interaction)
    
    # Create a mock response object
    response = AsyncMock()
    interaction.response = response
    
    # Create a mock user
    user = MagicMock(spec=discord.Member)
    user.name = "TestUser"
    user.discriminator = "0"
    user.id = 123456789
    user.display_avatar.url = "https://example.com/avatar.png"
    user.color = discord.Color.blue()
    user.created_at = datetime(2020, 1, 1)
    user.joined_at = datetime(2020, 2, 1)
    user.status = discord.Status.online
    user.activity = None
    user.roles = [MagicMock(spec=discord.Role, mention="@everyone")]
    user.bot = False
    user.guild = MagicMock()
    user.guild.owner_id = 987654321
    
    # Set the user on the interaction
    interaction.user = user
    
    return interaction

@pytest.fixture
def mock_member():
    member = MagicMock(spec=discord.Member)
    member.name = "TargetUser"
    member.discriminator = "0"
    member.id = 987654321
    member.display_avatar.url = "https://example.com/target_avatar.png"
    member.color = discord.Color.red()
    member.created_at = datetime(2019, 1, 1)
    member.joined_at = datetime(2019, 2, 1)
    member.status = discord.Status.offline
    member.activity = MagicMock()
    member.activity.type = discord.ActivityType.playing
    member.activity.name = "Test Game"
    member.roles = [
        MagicMock(spec=discord.Role, mention="@everyone"),
        MagicMock(spec=discord.Role, mention="@role1"),
        MagicMock(spec=discord.Role, mention="@role2")
    ]
    member.bot = False
    member.guild = MagicMock()
    member.guild.owner_id = 987654321
    return member

@pytest.mark.asyncio
async def test_whois_self(mock_bot, mock_interaction):
    cog = WhoisCog(mock_bot)
    # Get the command from the cog
    command = cog.whois
    # Call the command's callback directly
    await command.callback(cog, mock_interaction)
    
    # Verify that the interaction was responded to
    mock_interaction.response.send_message.assert_called_once()
    
    # Get the embed that was sent
    embed = mock_interaction.response.send_message.call_args[1]['embed']
    
    # Verify embed properties
    assert embed.title == "User Information"
    assert embed.color == discord.Color.blue()
    assert embed.thumbnail.url == "https://example.com/avatar.png"
    
    # Verify fields
    fields = {field.name: field.value for field in embed.fields}
    assert fields["Username"] == "TestUser#0"
    assert fields["ID"] == "123456789"
    assert fields["Status"] == "Online"
    assert fields["Activity"] == "None"
    assert fields["Is Bot"] == "No"
    assert fields["Is Server Owner"] == "No"

@pytest.mark.asyncio
async def test_whois_other_user(mock_bot, mock_interaction, mock_member):
    cog = WhoisCog(mock_bot)
    # Get the command from the cog
    command = cog.whois
    # Call the command's callback directly
    await command.callback(cog, mock_interaction, mock_member)
    
    # Verify that the interaction was responded to
    mock_interaction.response.send_message.assert_called_once()
    
    # Get the embed that was sent
    embed = mock_interaction.response.send_message.call_args[1]['embed']
    
    # Verify embed properties
    assert embed.title == "User Information"
    assert embed.color == discord.Color.red()
    assert embed.thumbnail.url == "https://example.com/target_avatar.png"
    
    # Verify fields
    fields = {field.name: field.value for field in embed.fields}
    assert fields["Username"] == "TargetUser#0"
    assert fields["ID"] == "987654321"
    assert fields["Status"] == "Offline"
    assert "Test Game" in fields["Activity"]
    assert fields["Is Bot"] == "No"
    assert fields["Is Server Owner"] == "Yes"

@pytest.mark.asyncio
async def test_whois_with_many_roles(mock_bot, mock_interaction):
    # Create a member with many roles
    member = MagicMock(spec=discord.Member)
    member.name = "ManyRolesUser"
    member.discriminator = "0"
    member.roles = [MagicMock(spec=discord.Role, mention=f"@role{i}") for i in range(50)]
    member.color = discord.Color.green()
    member.display_avatar.url = "https://example.com/many_roles.png"
    member.created_at = datetime(2020, 1, 1)
    member.joined_at = datetime(2020, 2, 1)
    member.status = discord.Status.online
    member.activity = None
    member.bot = False
    member.guild = MagicMock()
    member.guild.owner_id = 123456789
    
    cog = WhoisCog(mock_bot)
    # Get the command from the cog
    command = cog.whois
    # Call the command's callback directly
    await command.callback(cog, mock_interaction, member)
    
    # Verify that the interaction was responded to
    mock_interaction.response.send_message.assert_called_once()
    
    # Get the embed that was sent
    embed = mock_interaction.response.send_message.call_args[1]['embed']
    
    # Verify that roles are properly handled
    role_fields = [field for field in embed.fields if field.name.startswith("Roles")]
    assert len(role_fields) > 0
    assert all(len(field.value) <= 1024 for field in role_fields)

@pytest.mark.asyncio
async def test_whois_bot_user(mock_bot, mock_interaction):
    # Create a bot user
    bot_user = MagicMock(spec=discord.Member)
    bot_user.name = "BotUser"
    bot_user.discriminator = "0"
    bot_user.bot = True
    bot_user.color = discord.Color.purple()
    bot_user.display_avatar.url = "https://example.com/bot.png"
    bot_user.created_at = datetime(2020, 1, 1)
    bot_user.joined_at = datetime(2020, 2, 1)
    bot_user.status = discord.Status.online
    bot_user.activity = None
    bot_user.roles = [MagicMock(spec=discord.Role, mention="@everyone")]
    bot_user.guild = MagicMock()
    bot_user.guild.owner_id = 123456789
    
    cog = WhoisCog(mock_bot)
    # Get the command from the cog
    command = cog.whois
    # Call the command's callback directly
    await command.callback(cog, mock_interaction, bot_user)
    
    # Verify that the interaction was responded to
    mock_interaction.response.send_message.assert_called_once()
    
    # Get the embed that was sent
    embed = mock_interaction.response.send_message.call_args[1]['embed']
    
    # Verify fields
    fields = {field.name: field.value for field in embed.fields}
    assert fields["Is Bot"] == "Yes" 