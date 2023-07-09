import discord
from discord.ext import commands

import main
import utils.ticket_database as db


class TicketCommunication(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.author == self.client.user:
            return
        
        # Communication in ticket channels
        if message.channel.type == discord.ChannelType.text:
            ticketdb = db.TicketDatabase()
            
            if ticketdb.has_ticket(message.channel.id):
                if message.channel.id == ticketdb.get_channel_id(message.author.id):
                    await message.delete()
                    
                    ticket_user = self.client.get_user(ticketdb.get_user_id(message.channel.id))
                    
                    embed = discord.Embed(
                        title='FocusUp | Ticket Support',
                        description=message.content,
                        timestamp=message.created_at,
                        color=0xaf30e6
                    )
                    if self.checkIfAttachment(message) == 'image':
                        embed.set_image(url=message.attachments[0].url)
                    elif self.checkIfAttachment(message) == 'file':
                        embed.add_field(name='File', value=message.attachments[0].url)
                        
                    embed.set_author(name=f'{message.author} | {message.author.id}', icon_url=message.author.avatar_url)
                    
                    await ticket_user.send(embed=embed)
                    await message.channel.send(embed=embed)
                    
                    ticketdb.close()
        
        # Communication in DMs
        elif message.channel.type == discord.ChannelType.private or message.channel.type is None:
            ticketdb = db.TicketDatabase()
            
            ticket_channel_id = ticketdb.get_channel_id(message.author.id)
            
            if ticket_channel_id is None:
                ticketdb.close()
                return

            ticket_channel = self.client.get_channel(ticket_channel_id)
            
            embed = discord.Embed(
                title='FocusUp | Ticket Support',
                description=message.content,
                timestamp=message.created_at,
                color=0x4287f5
            )
            if self.checkIfAttachment(message) == 'image':
                embed.set_image(url=message.attachments[0].url)
            elif self.checkIfAttachment(message) == 'file':
                embed.add_field(name='File', value=message.attachments[0].url)
                
            embed.set_author(name=f'{message.author} | {message.author.id}', icon_url=message.author.avatar_url)
            
            await ticket_channel.send(embed=embed)
            
            ticketdb.close()
    
    
    def checkIfAttachment(self, message: discord.Message):
        """Checks if a message has an attachment and determines its type.

        Args:
            message (discord.Message): The message to check.

        Returns:
            str or None: The type of attachment ('image' or 'file') if it exists, None otherwise.
        """
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image'):
                    return 'image'
                else:
                    return 'file'
        else:
            return None


def setup(client):
    client.add_cog(TicketCommunication(client))
