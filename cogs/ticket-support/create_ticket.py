import discord
from discord.ext import commands
from discord import Button, ButtonStyle

import main


class CreateTicket(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.slash_command(name='ticket', description='Create a support ticket in DM')
    async def create_ticket(self, ctx, reason: str='No reason provided'):
        if ctx.guild is not None:
            await ctx.respond(f'Please use this command DM!\n➜ {self.client.user.mention}', hidden=True)
        else:
            author_close_button=Button(label='Close Ticket',
                                         custom_id='close-ticket-btn',
                                         style=ButtonStyle.red,
                                         emoji='🔒')

            author_panel_embed=discord.Embed(title='FocusUp | Support Ticket',
                                  description="""Your Ticket has been created! Please wait for a staff member to respond.
                                                \nAll communication will take place via our Private Chat.
                                                Your messages will be sent to our staff members and we
                                                respond you in the private chat until you close the ticket by clicking
                                                on the "close" button on this message (pinned).""",
                                  timestamp=ctx.created_at,
                                  color=0x7500e3)
            
            author_panel_embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))

            author_panel_embed.add_field(name='Reason', value=reason, inline=len(reason) < 100)
            author_panel_embed.add_field(name='Other contact', value='contact@lytexmedia.com', inline=len(reason) < 100)

            author_panel_embed_msg = await ctx.respond(embed=author_panel_embed, components=[author_close_button])
            await author_panel_embed_msg.pin()


def setup(client):
    client.add_cog(CreateTicket(client))