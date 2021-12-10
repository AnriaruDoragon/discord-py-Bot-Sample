import os, time, logging, discord
from discord.ext import commands

from config.secret import token
from config.logging import *
from config.client import *

logging.basicConfig(filename=log_file, filemode="w", encoding=log_encoding, format=log_format, datefmt=log_dateformat, level=logging.INFO)

client = commands.Bot(command_prefix=command_prefix)

@client.event
async def on_ready():
    logging.info("{0.user} is Ready!".format(client))

@client.group(name="modules")
async def modules_group(ctx:commands.Context):
    if ctx.invoked_subcommand == None:
        embed = discord.Embed(color=color, title="Modules")
        modules = [f[:-3] for f in os.listdir("Bot/Modules") if f.endswith(".py")]
        loaded = list(client.cogs)
        for lm in loaded:
            if lm in modules:
                modules.remove(lm)
        if len(loaded) > 0:
            embed.add_field(name="✅ Loaded", value=", ".join(loaded), inline=True)
        if len(modules) > 0:
            embed.add_field(name="❌ Unloaded", value=", ".join(modules), inline=True)
        if len(modules) == 0 and len(loaded) == 0:
            embed.description = "No modules found."
        await ctx.reply(embed=embed)

@modules_group.command(name="load", description="Load a module.")
async def load_module(ctx, module:str):
    embed = discord.Embed(title="Loading {0}".format(module))
    try:
        client.load_extension("Modules.{0}".format(module))
    except commands.ExtensionNotFound:
        embed.description = "Module {0} is not found.".format(module)
        embed.color = 0xFF0000
    except commands.ExtensionAlreadyLoaded:
        embed.description = "Module {0} is already loaded.".format(module)
        embed.color = 0xFF0000
    except commands.NoEntryPointError:
        embed.description = "Module {0} doesn't have a setup function.".format(module)
        embed.color = 0xFF0000
    except commands.ExtensionFailed:
        embed.description = "Module {0} is broken.".format(module)
        embed.color = 0xFF0000
    else:
        embed.description = "Module {0} is loaded.".format(module)
        embed.color = color
    finally:
        await ctx.reply(embed=embed)

@modules_group.command(name="unload", description="Unload a module.")
async def unload_module(ctx, module:str):
    embed = discord.Embed(title="Unloading {0}".format(module))
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
        embed.color = color
    finally:
        await ctx.reply(embed=embed)

@modules_group.command(name="reload", description="Reload a module.")
async def reload_module(ctx, module:str):
    embed = discord.Embed(title="Reloading {0}".format(module))
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
        embed.color = color
    finally:
        bot_msg = await ctx.reply(embed=embed)
        if to_load:
            await load_module(bot_msg, module)

while True:
    try:
        client.run(token)
    except BaseException as run_error:
        logging.critical(run_error)
        time.sleep(30)