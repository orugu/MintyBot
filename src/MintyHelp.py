import discord
from discord.ext import commands


class HelpCommands(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        help_message = """```**MintyBot Commands:**
        this help message is still fixing... so wait please!
- `!help rank`: help about rank commands.
- `!help shop`: help about shop commands.
- `!help`: Display help for a specific command.

For more information, visit our [documentation](https://example.com/docs).
```"""
        destination = self.get_destination()
        await destination.send(help_message)

    async def send_command_help(self, command):
        if command.name == "rank":
            help_message = """```**MintyBot Rank Commands:**
- `!rank`: Check your rank and experience.
- `!rank leaderboard`: View the rank leaderboard.
- `!rank reset`: Reset your rank data.

For more information, visit our [documentation](https://example.com/docs/rank).
```"""
        elif command.name == "shop":
            help_message = """```**MintyBot Shop Commands:**
- `!register` : register for your account
- `!shop view`: View the shop items.
- `!shop`: View the shop items.
- `!help`: Display this help message.


[For admin]
- `!shop initialize`: Initialize the shop.
- `!shop add [name] [price] [description]`: Add an item to the shop.
- `!shop remove [name]`: Remove an item from the shop.
- `!shop set [name or price or description] [value]`: Set the name, price, or description of an item.

For more information, visit our [documentation](https://example.com/docs).
```"""
        elif command.name == "money":
            help_message = """```**MintyBot Balance Command:**
- `!money`: Check your currency balance.
- `!transfer`: Transfer currency to other users.

For more information, visit our [documentation](https://example.com/docs/balance).
```"""

        elif command.name == "etc":
            help_message = """```**MintyBot Etc Commands:**
- `!ping`: Check the bot's responsiveness.
- `!info`: Get information about the bot.
- `!help`: Display this help message.
- `!hello`: Greet the bot.

For more information, visit our [documentation](https://example.com/docs/etc).  ```
```"""
        else:
            help_message = "```Command not found. Use `!help` to see the list of available commands.```"

        destination = self.get_destination()
        await destination.send(help_message)