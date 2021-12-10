from discord.ext import commands

class Filter(commands.Cog, name="Filter", description="Manage server messages filter."):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        pass

def setup(client):
    client.add_cog(Filter(client))