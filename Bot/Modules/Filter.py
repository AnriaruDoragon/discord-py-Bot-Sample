import discord, logging, typing, misc
from discord.ext import commands
from Data.Filter import Filter as FilterDB

from config.client import *

class Filter(commands.Cog, name="Filter", description="Manage server messages filter."):

    def __init__(self, client):
        self.client = client
        self.filter = FilterDB(client.data)

    def CheckMessage(self, message:discord.Message, is_check=False):
        filter = self.filter.Get(message.guild.id)
        triggered = []

        if len(filter) > 0:
            content = misc.GetEntireContent(message)
            for word in filter:
                if word.lower() in content:
                    if is_check:
                        triggered.append(word.lower())
                    else:
                        return [word.lower()]

        return triggered

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author.permissions_in(message.channel).manage_messages:
            return

        if len(self.CheckMessage(message)) > 0:
            try:
                await message.delete()
            except Exception as error:
                logging.warning(error)
    
    @commands.group(name="filter", description="Manage messages filter on this server.")
    @commands.has_guild_permissions(manage_messages=True)
    async def filter_group(self, ctx):
        if ctx.invoked_subcommand == None:
            await self.filter_list(ctx)
    
    @filter_group.command(name="list", description="Get all banned words for this server.")
    @commands.has_guild_permissions(manage_messages=True)
    async def filter_list(self, ctx):
        filter = self.filter.Get(ctx.guild.id)

        if len(filter) > 0:
            messages = misc.SplitString("Banned words for `{0}`:\n{1}".format(ctx.guild.name, " ".join(["`{0}`".format(word) for word in filter])))
            await ctx.channel.trigger_typing()
            for message in messages:
                try:
                    await ctx.author.send(message)
                except discord.HTTPException as error:
                    logging.info(error)
                    await ctx.reply("Please, open tour DMs.")
                    return
                except BaseException as error:
                    logging.error(error)
                    await ctx.reply("Something went wrong.")
                    return
            await ctx.reply("Check your DMs.")
        else:
            await ctx.reply("There is no banned words on this server.\nUse `{0}{1} add <words>` to ban words.".format(ctx.prefix, ctx.command.root_parent.name))

    @filter_group.command(name="add", description="Add words to the filter.")
    @commands.has_guild_permissions(manage_messages=True)
    async def filter_add(self, ctx, *words):
        filter = self.filter.Get(ctx.guild.id)

        # Lower, Trim, Remove Duplicates
        words = [word.lower().replace(" ", "") for word in words]
        proceed = [word for word in list(dict.fromkeys(words)) if word not in filter]
        ignored = [word for word in words if word not in proceed]

        embed = discord.Embed(title="Add words to the filter", color=color)
        if len(proceed) > 0:
            self.filter.Add(ctx.guild.id, proceed)
            embed.add_field(name="✅ Success", value=" ".join(["`{0}`".format(word) for word in proceed]), inline=True)
        if len(ignored) > 0:
            embed.add_field(name="❌ Ignored", value=" ".join(["`{0}`".format(word) for word in ignored]), inline=True)
            embed.set_footer(text="Ignored are the words that are already in the filter.")

        await ctx.reply(embed=embed)

    @filter_group.command(name="remove", description="Remove words from the filter.")
    @commands.has_guild_permissions(manage_messages=True)
    async def filter_remove(self, ctx, *words):
        filter = self.filter.Get(ctx.guild.id)

        # Remove Duplicates
        proceed = [word for word in list(dict.fromkeys(words)) if word in filter]
        ignored = [word for word in words if word not in proceed]

        embed = discord.Embed(title="Remove words from the filter", color=color)
        if len(proceed) > 0:
            self.filter.Remove(ctx.guild.id, proceed)
            embed.add_field(name="✅ Success", value=" ".join(["`{0}`".format(word) for word in proceed]), inline=True)
        if len(ignored) > 0:
            embed.add_field(name="❌ Ignored", value=" ".join(["`{0}`".format(word) for word in ignored]), inline=True)
            embed.set_footer(text="Ignored are the words that were not in the filter.")

        await ctx.reply(embed=embed)
    
    @filter_group.command(name="check", description="Check if the following text or message violates the filter for this server.")
    @commands.has_guild_permissions(manage_messages=True)
    async def filter_check(self, ctx, message:typing.Optional[discord.Message]=None):
        if message == None:
            message = ctx.message

        triggered = self.CheckMessage(message, True)
        embed = discord.Embed(title="Filter check", color=color)

        if len(triggered) > 0:
            embed.description = "Triggered words:\n" + " ".join(["`{0}`".format(word) for word in triggered])
        else:
            embed.description = "It seems okay to me."

        await ctx.reply(embed=embed)

def setup(client):
    client.add_cog(Filter(client))
