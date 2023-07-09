import discord
from discord.ext import commands
import asyncio

import main


class PurgeBotDmHistory(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.slash_command(name='purge-dm-history', description='Purge the bot DM history')
    async def purge_dm_history(self, ctx):
        if ctx.author.bot:
            return
        
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.defer()
            
            deleted_count = 0
            messages = []
            
            async for message in ctx.channel.history(limit=None):
                if message.author == self.client.user:
                    messages.append(message)
            
            delay = 1
            
            for message in messages:
                await message.delete()
                deleted_count += 1
                await asyncio.sleep(delay)
        else:
            await ctx.respond("This command can only be used in a DM.", hidden=True)


def setup(client):
    client.add_cog(PurgeBotDmHistory(client))
