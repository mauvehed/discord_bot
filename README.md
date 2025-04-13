# Discord Bot Framework

A Discord bot framework built with Python 3 and discord.py, designed to support slash commands and modular cogs.

## Features

- Slash command support
- Modular cog system
- Environment-based configuration
- Automatic command syncing
- Error handling for common Discord issues
- Comprehensive test coverage
- Modern datetime handling

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Discord bot token (get one from the [Discord Developer Portal](https://discord.com/developers/applications))

## Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd discord_bot
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"  # Installs both main and development dependencies
```

4. Configure your bot:
   - Copy `.env.example` to `.env`
   - Replace `your_bot_token_here` with your actual Discord bot token

5. Run the bot:
```bash
python bot.py
```

## Bot Structure

```
discord_bot/
├── bot.py              # Main bot file
├── requirements.txt    # Python dependencies
├── setup.py           # Project installation configuration
├── .env.example       # Environment variables template
├── tests/             # Test directory
│   └── test_whois_cog.py  # Tests for whois command
└── cogs/              # Cog directory
    ├── __init__.py
    ├── whois_cog.py   # User information command
    └── template_cog.py # Example cog template
```

## Available Commands

### /whois
Displays detailed information about a Discord user, including:
- Basic information (username, ID, nickname)
- Account information (creation date, join date)
- Status and activity
- Roles
- Bot status
- Server owner status

Usage:
- `/whois` - Shows information about yourself
- `/whois @username` - Shows information about another user

## Creating New Cogs

To create a new cog, follow the template in `cogs/template_cog.py`. Here's a basic example:

```python
import discord
from discord import app_commands
from discord.ext import commands

class YourCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="command", description="Your command description")
    async def your_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Your response")

async def setup(bot):
    await bot.add_cog(YourCog(bot))
```

Place your new cog file in the `cogs` directory. The bot will automatically load it on startup.

## Testing

The project includes comprehensive tests for the whois command. To run the tests:

```bash
pytest tests/
```

For coverage report:
```bash
pytest --cov=cogs tests/
```

Current test coverage:
- whois_cog.py: 88%
- __init__.py: 100%
- template_cog.py: 0% (template file)

## Important Notes

- Make sure your bot has the necessary permissions in your Discord server
- Slash commands may take up to an hour to appear in Discord after the first sync
- The bot requires the following Discord intents:
  - message_content
  - members

## Troubleshooting

1. **Commands not appearing in Discord**
   - Wait up to an hour for the first sync
   - Make sure your bot has the correct permissions
   - Check that the command is properly registered in your cog

2. **Bot not connecting**
   - Verify your token in the `.env` file
   - Check your internet connection
   - Ensure the bot has been invited to your server with proper permissions

3. **Tests failing**
   - Make sure all dependencies are installed: `pip install -e ".[dev]"`
   - Check that you're in the correct directory
   - Verify your Python version is 3.8 or higher

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Write tests for your new functionality
4. Commit your changes
5. Push to your branch
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 