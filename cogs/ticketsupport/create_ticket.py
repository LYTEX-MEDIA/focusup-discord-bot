import discord
from discord.ext import commands
from discord import Button, ButtonStyle

import main
import utils.ticket_database as db


class CreateTicket(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.slash_command(name='ticket', description='Create a support ticket in DM')
    async def create_ticket(self, ctx, reason: str='No reason provided'):
        await ctx.defer()
        
        if self.hasAlreadyTicket(ctx.author.id):
            await ctx.respond(f'You already have a ticket open!\n➜ {self.client.user.mention}', hidden=True)
            return
        
        if db.BannedDatabase().is_banned(ctx.author.id):
            await ctx.respond(f'You are banned from creating tickets!\nBy typing /ticket-ban-appeal <content> you can create a unban request.', hidden=True)
            return
        
        if ctx.guild is not None:
            await ctx.respond(f'Please use this command DM!\n➜ {self.client.user.mention}', hidden=True)
            return
            
        author_close_button=Button(label='Close Ticket',
                                    custom_id='close-ticket-btn',
                                    style=ButtonStyle.red,
                                    emoji='🔒')
        author_panel_embed=discord.Embed(title='FocusUp | Ticket Support',
                            description="""Your Ticket has been created! Please wait for a staff member to respond.
                                            \nAll communication will take place via our Private Chat.
                                            Your messages will be sent to our staff members and we
                                            respond you in the private chat until you close the ticket by clicking
                                            on the "close" button on this message (pinned).""",
                            timestamp=ctx.created_at,
                            color=0x7500e3)
            
        author_panel_embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
        author_panel_embed.add_field(name='Reason', value=reason, inline=len(reason) < 75)
        author_panel_embed.add_field(name='Other contact', value='contact@lytexmedia.com', inline=len(reason) < 75)
        author_panel_embed_msg = await ctx.respond(embed=author_panel_embed, components=[author_close_button])
        await author_panel_embed_msg.pin()
        
        # Todo: Add getFocusUpID function
        focusup_id = None
        
        
        guild = self.client.get_guild(main.config.getdata('lytex-media-guild-id'))
        open_tickets_category = guild.get_channel(main.config.getdata('open-tickets-category-id'))
        
        ticket_channel = await open_tickets_category.create_text_channel(name=f'┝┇{ctx.author.name}',
                                                                        topic=f"""FocusUp Support Ticket | {ctx.author.name} | {ctx.author.id}
                                                                                Reason: {reason}
                                                                                FocusUp ID: {focusup_id}""",
                                                                        permission_synced=True)
            
        ticketdb = db.TicketDatabase()
        ticketdb.add_ticket(ctx.author.id, author_panel_embed_msg.id, ticket_channel.id)
        ticketdb.close()
        
        
        # Send message to ticket channel
        mod_close_button=Button(label='Close Ticket',
                                    custom_id='mod-close-ticket-btn',
                                    style=ButtonStyle.red,
                                    emoji='🔒')
        mod_panel_embed=discord.Embed(title='FocusUp | Ticket Support',
                            description=f'{ctx.author.mention} has created a ticket!',
                            timestamp=ctx.created_at,
                            color=0x7500e3)
        
        mod_panel_embed.set_author(name=f'{ctx.author} | {ctx.author.id}', icon_url=ctx.author.avatar_url)
        mod_panel_embed.add_field(name='Reason', value=reason, inline=len(reason) < 75)
        mod_panel_embed.add_field(name='FocusUp ID', value=focusup_id, inline=len(reason) < 75)
        mod_panel_embed = await ticket_channel.send(embed=mod_panel_embed,
                                                    components=[mod_close_button])
        
        await mod_panel_embed.pin()
    
    
    def hasAlreadyTicket(self, user_id):
        """Checks if the user already has a ticket.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user has a ticket, False otherwise.
        """
        try:
            ticketdb = db.TicketDatabase()
            ticket = ticketdb.get_ticket(user_id)
            return ticket is not None
        except Exception as e:
            print(f"Error while checking if user has a ticket: {str(e)}")
            return False
        finally:
            ticketdb.close()


def setup(client):
    client.add_cog(CreateTicket(client))