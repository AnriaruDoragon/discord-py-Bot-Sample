import discord, logging
from discord.ext import commands

from config.client import *

class BetterHelpCommand(commands.HelpCommand):

    def get_command_signature(self, command, only_name=False, is_short=False):
        if only_name:
            signature = "{1.name}".format(self, command)
        else:
            signature = "{0.clean_prefix}{1.qualified_name}".format(self, command)

        if is_short:
            return "`{0}`".format(signature)
        else:
            return "```{0} {1.signature}```".format(signature, command)
    
    async def send_bot_help(self, mapping):
        embed = discord.Embed(color=color, title="{0.context.bot.user.name} Help".format(self))
        embed.set_footer(text="Type `{0.clean_prefix}help <command/group/module>` for more info on a command/group/module.".format(self))

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c, is_short=True) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Main")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        try:
            await self.context.send(embed=embed)
        except BaseException as error:
            logging.error(error)

    async def send_command_help(self, command):
        embed = discord.Embed(color=color, title="{0.context.bot.user.name} Help {1.qualified_name}".format(self, command), description=command.description)
        embed.add_field(name="Usage", value=self.get_command_signature(command), inline=False)
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)

        try:
            await self.context.send(embed=embed)
        except BaseException as error:
            logging.error(error)

    async def send_group_help(self, group):
        embed = discord.Embed(color=color, title="{0.context.bot.user.name} Help {1.qualified_name}".format(self, group))
        embed.set_footer(text="Type `{0.clean_prefix}help <command/group>` for more info on a command/group.".format(self))
        filtered = await self.filter_commands(group.commands, sort=True)
        if filtered:
            embed.description = "\n".join(["`{0}` - {1}".format(self.get_command_signature(c, only_name=True, is_short=True)[:25], c.description[:50]) for c in filtered])
        else:
            embed.description = "It's silent here..."

        try:
            await self.context.send(embed=embed)
        except BaseException as error:
            logging.error(error)

    async def send_cog_help(self, cog):
        embed = discord.Embed(color=color, title="{0.context.bot.user.name} Help {1.qualified_name}".format(self, cog), description=cog.description)

        try:
            await self.context.send(embed=embed)
        except BaseException as error:
            logging.error(error)

class BetterHelp(commands.Cog, name="BetterHelp", description="Provides a better command help system with embeds."):

    def __init__(self, client):
        self.client = client
        self._original_help = client.help_command
        client.help_command = BetterHelpCommand()
        client.help_command.cog = self
    
    def cog_unload(self):
        self.client.help_command = self._original_help

def setup(client):
    client.add_cog(BetterHelp(client))
