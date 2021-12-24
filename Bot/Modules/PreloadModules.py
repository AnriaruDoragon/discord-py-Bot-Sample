import discord, os, logging
from discord.ext import commands
from Data.PreloadModules import PreloadModules as PreloadDB

from config.client import *

class PreloadModules(commands.Cog, name="PreloadModules", description="Manage preload modules for the client that will load on start."):
    
    def __init__(self, client):
        self.client = client
        self.preload = PreloadDB(client.data)

        modules = self.preload.Get()
        if modules:
            for module in modules:
                try:
                    self.client.load_extension("Modules.{0}".format(module))
                except BaseException as error:
                    logging.error(error)
                else:
                    logging.info("Preload - The module '{0}' is loaded.".format(module))

    @commands.group(name="preload", description="Manage preload modules.")
    @commands.has_guild_permissions(administrator=True)
    async def preload_group(self, ctx):
        if ctx.invoked_subcommand == None:
            pass
    
    @preload_group.command(name="list", description="Get the list of all preloaded modules.")
    @commands.has_guild_permissions(administrator=True)
    async def preload_list(self, ctx):
        embed = discord.Embed(color=color, title="Preload Modules")
        preloads = self.preload.Get()

        if preloads:
            embed.description = "\n".join(["`{0}`".format(module) for module in preloads])
        else:
            embed.description = "Not found."
        
        await ctx.reply(embed=embed)

    @preload_group.command(name="add", description="Add modules to the preload list.")
    @commands.has_guild_permissions(administrator=True)
    async def preload_add(self, ctx, module, push:str=None):
        embed = discord.Embed(color=color, title="Adding {0} to the preload list".format(module))
        preloads = self.preload.Get()

        if module in preloads:
            embed.description = "The module `{0}` is already in the preload list.".format(module)
            embed.color = 0xFF0000
        elif module not in [m[:-3] for m in os.listdir("Bot/Modules") if m.endswith(".py")]:
            if push != None and push.lower() == "push":
                self.preload.Add(module)
                embed.description = "The module `{0}` has been pushed to the preload list.".format(module)
            else:
                embed.description = "The module `{0}` is not found.".format(module)
                embed.set_footer(text="If you want to add this module to the list anyway, add `push` to the end of the command.")
                embed.color = 0xFF0000
        else:
            self.preload.Add(module)
            embed.description = "The module `{0}` has been added to the preload list.".format(module)

        await ctx.reply(embed=embed)
    
    @preload_group.command(name="remove", description="Remove modules from the preload list.")
    @commands.has_guild_permissions(administrator=True)
    async def preload_remove(self, ctx, module):
        embed = discord.Embed(color=color, title="Removing {0} from the preload list".format(module))
        preloads = self.preload.Get()

        if module in preloads:
            self.preload.Remove(module)
            embed.description = "The module `{0}` has been removed from the preload list.".format(module)
        else:
            embed.description = "The module `{0}` is not in the preload list.".format(module)
            embed.color = 0xFF0000
        
        await ctx.reply(embed=embed)

def setup(client):
    client.add_cog(PreloadModules(client))
