import discord, logging
from discord.ext import commands
from Data.PreloadModules import PreloadModules as PreloadDB

class PreloadModules(commands.Cog, name="PreloadModules", description="Manage preload modules for the client that will load on start."):
    
    def __init__(self, client):
        self.client = client
        self.preload = client.preload

    @commands.group(name="preload", description="Manage preload modules.")
    @commands.has_guild_permissions(administrator=True)
    async def preload_group(self, ctx):
        if ctx.invoked_subcommand == None:
            pass
    
    @preload_group.command(name="list", description="Get the list of all preloaded modules.")
    @commands.has_guild_permissions(administrator=True)
    async def preload_list(self, ctx, module):
        pass

    @preload_group.command(name="add", description="Add modules to the preload list.")
    @commands.has_guild_permissions(administrator=True)
    async def preload_add(self, ctx, module):
        pass
    
    @preload_group.command(name="remove", description="Remove modules from the preload list.")
    @commands.has_guild_permissions(administrator=True)
    async def preload_add(self, ctx, module):
        pass

def setup(client):
    client.add_cog(PreloadModules(client))
