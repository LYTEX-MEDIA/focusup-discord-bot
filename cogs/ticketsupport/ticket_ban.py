import discord
from discord.ext import commands
from discord import Button, ButtonStyle
from discord.utils import get
from discord.ext.commands import has_role

import main
import utils.ticket_database as db


class TicketBan(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.slash_command(name='ticket-ban', description='Prevent a user from creating further tickets', guild_ids=[main.config.getdata('lytex-media-guild-id')])
    @has_role(main.config.getdata('moderator-team-role-id'))
    async def ticket_ban(self, ctx, user_id, reason='No reason provided'):
        await ctx.defer()
        
        if ctx.author.bot:
            return
        
        if db.BannedDatabase().is_banned(user_id):
            await ctx.respond(f'User is already banned!', hidden=True)
            return
        
        try:
            user = await self.client.fetch_user(user_id)  
        except Exception as e:
            await ctx.respond(f'User not found!\n{e}', hidden=True)
            return
        
        # Todo: Add getFocusUpID function
        focusup_id = None
        
        db.BannedDatabase().add_banned_user(user_id, ctx.author.id, focusup_id, reason)
        
        embed = discord.Embed(title='FocusUp | Ticket Support',
                                description=f'{ctx.author.mention} has banned {user.mention} / {user.id} from creating tickets',
                                color=discord.Color.red()
                                )
        embed.add_field(name='Reason', value=f'{reason}', inline=False)
        embed.add_field(name='FocusUp ID', value=f'{focusup_id}', inline=False)
        embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
        
        await ctx.respond(embed=embed)
        
        db.BannedDatabase.close()
        

def setup(client):
    client.add_cog(TicketBan(client))