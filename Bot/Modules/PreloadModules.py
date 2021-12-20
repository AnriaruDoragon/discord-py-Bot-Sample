import discord, logging
from discord.ext import commands
from Data.PreloadModules import PreloadModules as PreloadDB

class PreloadModules(commands.Cog, name="PreloadModules", description="Manage preload modules for the client that will launch on start."):
    
    def __init__(self, client):
        self.client = client
        self.preload = PreloadDB(client.data)

    @commands.group(name="preload", description="Manage preload modules.")
    @commands.has_guild_permissions(administrator=True)
    async def preload_group(self, ctx):
        if ctx.invoked_subcommand == None:
            pass
    
    

def setup(client):
    client.add_cog(PreloadModules(client))
