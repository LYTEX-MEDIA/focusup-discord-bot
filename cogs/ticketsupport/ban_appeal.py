import discord
from discord.ext import commands
from discord import Button, ButtonStyle

import main
import utils.ticket_database as db


class TicketBanAppeal(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.slash_command(name='ticket-ban-appeal', description='Create a ticket ban appeal')
    async def ticket_ban_appeal(self, ctx, content):
        await ctx.defer()
        
        if ctx.author.bot:
            return
        
        if not db.BannedDatabase().is_banned(ctx.author.id):
            await ctx.respond(f'You are not banned!\nYou can create tickets by typing `/ticket`', hidden=True)
            return
        
        if ctx.channel.type != discord.ChannelType.private:
            await ctx.respond(f'Please use this command in a private message with me!', hidden=True)
            return
        
        if db.BannedDatabase().get_ban_appeal(ctx.author.id):
            await ctx.respond(f'You have already sent a ban appeal!\nIf it is important, contact and happy to email `support@lytexmedia.com`', hidden=True)
            return
        
        # update the ban appeal status in the database
        db.BannedDatabase().update_ban_appeal(ctx.author.id)
        
        
        # Send the ban appeal to the user
        embed = discord.Embed(title='FocusUp | Ticket Support',
                                description=f'Your ticket ban appeal has been sent to the staff team!\n\n**Your appeal:**\n`{content}`',
                                color=0xd4d63a
                                )
        embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
        
        await ctx.respond(embed=embed)
        
        
        # Send the ban appeal to the staff team
        unban_reqeusts_channel = self.client.get_channel(id=main.config.getdata('unban-reqeusts-channel-id'))
        
        embed = discord.Embed(title='FocusUp | Ticket Support',
                                description=f'{ctx.author.mention}: `{content}`',
                                color=0xd4d63a
                                )
        embed.add_field(name='User ID', value=f'`{ctx.author.id}`', inline=False)
        embed.add_field(name='Ban-Reason', value=f'||`{db.BannedDatabase().get_ban_reason(ctx.author.id)}`||', inline=False)
        embed.set_author(name=f'Requested by {ctx.author.mention}', icon_url=ctx.author.avatar_url)
        embed.set_footer(text='Type /unban <user-id> to unban the user or ignore this message to keep the user banned.')
        
        await unban_reqeusts_channel.send(embed=embed)
        
        db.BannedDatabase().close()


def setup(client):
    client.add_cog(TicketBanAppeal(client))