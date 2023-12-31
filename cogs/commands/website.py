import discord
from discord.ext import commands
import main


class ShowWebsite(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.slash_command(name='website', description='Shows the FocusUp website')
    async def show_website(self, ctx):
        embed=discord.Embed(title='', description='\n', color=0x5b26a6)
        embed.add_field(name='FocusUp', value=f'[focusup.app]({main.config.getdata("focusup-web-link")})', inline=False)
        embed.add_field(name='LYTEX MEDIA', value=f'[Team of Focusup]({main.config.getdata("lytex-media-web-link")})', inline=False)
        embed.add_field(name='Sourcecode',
                        value=f'The Bot is btw Opensource: [click]({main.config.getdata("focusup-dc-bot-github-link")})',
                        inline=False)
        embed.add_field(name='Support Email', value=f'`{main.config.getdata("support-email")}`', inline=False)
        embed.add_field(name='Contact Email', value=f'`{main.config.getdata("contact-email")}`', inline=False)
        embed.set_author(name=f'{main.current_year} © LYTEX MEDIA', icon_url=main.config.getdata('lytex-media-logo-url'))
        
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(ShowWebsite(client))
