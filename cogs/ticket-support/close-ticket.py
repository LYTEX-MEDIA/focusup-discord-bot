import discord
from discord.ext import commands
from discord import Button, ButtonStyle

import main


class CloseTicket(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.on_click(custom_id='close-ticket-btn')
    async def close_ticket_button(self, ctx, _):
        await ctx.message.edit(components=[Button(label='Close Ticket',
                                         custom_id='close-ticket-btn',
                                         style=ButtonStyle.red,
                                         emoji='🔒',
                                         disabled=True)])
        await ctx.message.unpin()
        
        ticketdb = main.db.TicketDatabase()
        ticketdb.remove_ticket(ctx.author.id)
        ticketdb.close()
        
        embed=discord.Embed(title='FocusUp | Support Ticket',
                                           description='Your Ticket has been closed!',
                                           color=0x8f39c4)
        embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
        await ctx.respond(embed=embed)
        
        
        # Send message to ticket channel
        try:
            ticket_channel = self.client.get_channel(ticketdb.get_channel_id(ctx.author.id))
            
            embed = discord.Embed(title='FocusUp | Support Ticket',
                                            description=f'{ctx.author.mention} has closed the ticket!',
                                            timestamp=ctx.created_at,
                                            color=0x8f39c4)
            embed.set_author(name=f'{ctx.author} | {ctx.author.id}', icon_url=ctx.author.avatar_url)
            await ticket_channel.send(embed=embed)
        except:
            print('Wtf???\nTicket channel not found!')


def setup(client):
	client.add_cog(CloseTicket(client))