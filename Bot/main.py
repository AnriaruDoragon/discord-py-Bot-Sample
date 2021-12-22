import discord, os, logging, time
from discord.ext import commands
from Data.Data import Database
from Data.PreloadModules import PreloadModules as PreloadDB

from config.secret import token
from config.logging import *
from config.client import *

logging.basicConfig(filename=log_file, filemode="w", encoding=log_encoding, format=log_format, datefmt=log_dateformat, level=logging.INFO)
client = commands.Bot(command_prefix=command_prefix, owner_id=owner_id)
client.data = Database()

async def PreloadModules():
    try:
        client.load_extension("Modules.PreloadModules")
    except commands.ExtensionAlreadyLoaded:
        return
    except BaseException as error:
        logging.critical(error)

@client.event
async def on_ready():
    logging.info("{0.user} is Ready!".format(client))
    await PreloadModules()

@client.group(name="modules")
@commands.has_guild_permissions(administrator=True)
async def modules_group(ctx):
    if ctx.invoked_subcommand == None:
        await modules_list(ctx)

@modules_group.command(name="list", description="Get list of the all available modules.")
@commands.has_guild_permissions(administrator=True)
async def modules_list(ctx):
    embed = discord.Embed(color=color, title="Modules")
    loaded = list(client.cogs)
    # If it's a .py file and not registered as a module by the client, it makes a list out of their names.
    modules = [module[:-3] for module in os.listdir("Bot/Modules") if module.endswith(".py") and module[:-3] not in loaded]

    if len(loaded) > 0:
        embed.add_field(name="✅ Loaded", value="\n".join(["`{0}`".format(module) for module in loaded]), inline=True)
    if len(modules) > 0:
        embed.add_field(name="❌ Unloaded", value="\n".join(["`{0}`".format(module) for module in modules]), inline=True)
    if len(embed.fields) == 0:
        embed.description = "No modules found."

    await ctx.reply(embed=embed)

@modules_group.command(name="load", description="Load a module.")
@commands.has_guild_permissions(administrator=True)
async def load_module(ctx, module:str):
    embed = discord.Embed(color=color, title="Loading {0}".format(module))
    try:
        client.load_extension("Modules.{0}".format(module))
    except commands.ExtensionNotFound:
        embed.description = "The module `{0}` is not found.".format(module)
        embed.color = 0xFF0000
    except commands.ExtensionAlreadyLoaded:
        embed.description = "The module `{0}` is already loaded.".format(module)
        embed.color = 0xFF0000
    except commands.NoEntryPointError:
        embed.description = "The module `{0}` doesn't have a setup function.".format(module)
        embed.color = 0xFF0000
    except commands.ExtensionFailed:
        embed.description = "The module `{0}` is broken.".format(module)
        embed.color = 0xFF0000
    else:
        embed.description = "The module `{0}` is loaded.".format(module)
        logging.info("{0} - The module '{1}' is loaded.".format(ctx.author.id, module))
    finally:
        await ctx.reply(embed=embed)

@modules_group.command(name="unload", description="Unload a module.")
@commands.has_guild_permissions(administrator=True)
async def unload_module(ctx, module:str):
    embed = discord.Embed(color=color, title="Unloading {0}".format(module))
    try:
        client.unload_extension("Modules.{0}".format(module))
    except commands.ExtensionNotFound:
        embed.description = "Module {0} is not found.".format(module)
        embed.color = 0xFF0000
    except commands.ExtensionNotLoaded:
        embed.description = "Module {0} is not loaded.".format(module)
        embed.color = 0xFF0000
    else:
        embed.description = "Module {0} is unloaded.".format(module)
        logging.info("{0} - The module '{1}' is unloaded.".format(ctx.author.id, module))
    finally:
        await ctx.reply(embed=embed)

@modules_group.command(name="reload", description="Reload a module.")
@commands.has_guild_permissions(administrator=True)
async def reload_module(ctx, module:str):
    embed = discord.Embed(color=color, title="Reloading {0}".format(module))
    to_load = False
    try:
        client.reload_extension("Modules.{0}".format(module))
    except commands.ExtensionNotLoaded:
        embed.description = "Module {0} is not loaded.\nForwarding...".format(module)
        embed.color = 0xFF0000
        to_load = True
    except commands.ExtensionNotFound:
        embed.description = "Module {0} is not found.".format(module)
        embed.color = 0xFF0000
    except commands.NoEntryPointError:
        embed.description = "Module {0} doesn't have a setup function.".format(module)
        embed.color = 0xFF0000
    except commands.ExtensionFailed:
        embed.description = "Module {0} is broken.".format(module)
        embed.color = 0xFF0000
    else:
        embed.description = "Module {0} is reloaded.".format(module)
        logging.info("{0} - The module '{1}' is reloaded.".format(ctx.author.id, module))
    finally:
        bot_msg = await ctx.reply(embed=embed)
        if to_load:
            await load_module(bot_msg, module)

@client.command(name="log", description="Get logs for the current session.")
@commands.has_guild_permissions(administrator=True)
async def get_logs(ctx):
    await ctx.reply(file=discord.File(log_file, "client.log"))
    logging.info("{0} - Log request.".format(ctx.author.id))

while True:
    try:
        client.run(token)
    except BaseException as run_error:
        print(run_error)
        logging.critical(run_error)
        time.sleep(30)
