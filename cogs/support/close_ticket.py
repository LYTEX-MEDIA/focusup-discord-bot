import discord
from discord.ext import commands
from discord import Button, ButtonStyle

import main
import utils.ticket_database as db


class CloseTicket(commands.Cog):
    def __init__(self, client):
        self.client = client


    # Handle user closing ticket
    @commands.Cog.on_click(custom_id='close-ticket-btn')
    async def close_ticket_button(self, ctx, _):
        await ctx.message.edit(components=[Button(label='Close Ticket',
                                         custom_id='close-ticket-btn',
                                         style=ButtonStyle.red,
                                         emoji='🔒',
                                         disabled=True)])
        await ctx.message.unpin()
        
        embed=discord.Embed(title='FocusUp | Ticket Support',
                                           description='Your Ticket has been closed!',
                                           color=0x8f39c4)
        embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
        await ctx.respond(embed=embed)
        
        ticketdb = db.TicketDatabase()
        
        
        # Send message to ticket channel
        try:
            ticket_channel = self.client.get_channel(ticketdb.get_channel_id(ctx.author.id))
            
            embed = discord.Embed(title='FocusUp | Ticket Support',
                                            description=f'{ctx.author.mention} has closed the ticket!',
                                            timestamp=ctx.created_at,
                                            color=0x8f39c4)
            embed.set_author(name=f'{ctx.author} | {ctx.author.id}', icon_url=ctx.author.avatar_url)
            await ticket_channel.send(embed=embed)
            await ticket_channel.edit(name=f'┝┇closed-{ctx.author.name}')
        except Exception as e:
            discord.logging.error(f'Ticket channel not found!\n{e}')
        
        ticketdb.remove_ticket(ctx.author.id)
        ticketdb.close()
        
        
    # Handle moderator closing ticket
    @commands.Cog.on_click(custom_id='mod-close-ticket-btn')
    async def close_ticket_button(self, ctx, _):
        await ctx.message.edit(components=[
            Button(label='Close Ticket',
                   custom_id='close-ticket-btn',
                   style=ButtonStyle.red,
                   emoji='🔒',
                   disabled=True)
            ])
        await ctx.message.unpin()
        
        embed=discord.Embed(title='FocusUp | Ticket Support',
                                           description=f'The Ticket has been closed by {ctx.author.mention}!',
                                           color=0x8f39c4)
        embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
        
        ticketdb = db.TicketDatabase()
        
        try:
            ticket_user = self.client.get_user(ticketdb.get_user_id(ctx.channel.id))
            await ticket_user.send(embed=embed)
        except Exception as e:
            discord.logging.error(f'Error: couldn\'t send message to user!\n{e}')
            
        await ctx.respond(embed=embed)
        await ctx.channel.edit(name=f'┝┇closed-{ticket_user.name}')
        
        ticketdb.remove_ticket(ctx.author.id)
        ticketdb.close()


def setup(client):
	client.add_cog(CloseTicket(client))