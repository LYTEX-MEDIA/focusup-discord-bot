import discord
from discord.ext import commands
import main


class ShowWebsite(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.slash_command(name='website', description='Shows the FocusUp Website')
    async def show_website(self, ctx):
        embed=discord.Embed(title='', description='\n', color=0x5b26a6)
        embed.add_field(name='FocusUp', value=f'[focusup.app]({main.config.getdata("focusup-web-link")})', inline=True)
        embed.add_field(name='LYTEX MEDIA', value=f'[Founder of Focusup]({main.config.getdata("lytex-media-web-link")})', inline=True)
        embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
        
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(ShowWebsite(client))
