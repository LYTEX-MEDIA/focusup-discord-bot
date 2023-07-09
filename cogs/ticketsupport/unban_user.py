import discord
from discord.ext import commands
from discord import Button, ButtonStyle
from discord.utils import get
from discord.ext.commands import has_role

import main
import utils.ticket_database as db


class TicketUnBan(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.slash_command(name='ticket-unban', description='Unban a user so he can create tickets again', guild_ids=[main.config.getdata('lytex-media-guild-id')])
    @has_role(main.config.getdata('moderator-team-role-id'))
    async def ticket_unban(self, ctx, user_id):
        await ctx.defer()
        
        if ctx.author.bot:
            return
        
        if not db.BannedDatabase().is_banned(user_id):
            await ctx.respond(f'User is not banned!', hidden=True)
            return
        
        try:
            user = await self.client.fetch_user(user_id)  
        except Exception as e:
            await ctx.respond(f'User not found!\n{e}', hidden=True)
            return
        
        db.BannedDatabase().remove_banned_user(user_id)
        
        embed = discord.Embed(title='FocusUp | Ticket Support',
                                description=f'{ctx.author.mention} has unbanned {user.mention} from creating tickets!',
                                color=0x21fc50
                                )
        embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
        
        await ctx.respond(embed=embed)
        
        db.BannedDatabase.close()
        
        # Try to send a DM to the user
        try:
            embed = discord.Embed(title='FocusUp | Ticket Support',
                                    description=f'You have been unbanned from creating tickets!',
                                    color=0x21fc50
                                    )
            embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
            
            await user.send(embed=embed)
        except:
            pass
        

def setup(client):
    client.add_cog(TicketUnBan(client))