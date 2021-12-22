import discord
from discord.ext import commands

from config.client import *

class BetterHelp(commands.Cog, name="BetterHelp", description="Provides a better command help system with embeds."):

    def __init__(self, client):
        self.client = client



def setup(client):
    client.add_cog(BetterHelp(client))
