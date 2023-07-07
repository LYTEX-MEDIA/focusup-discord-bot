import discord
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv
import datetime
import os

import utils.database as db
from utils.config import Config


load_dotenv()
config = Config('config.json')

COMMANDS_DIR = Path.cwd() / 'cogs' / 'commands'
TICKET_DIR = Path.cwd() / 'cogs' / 'ticket-support'

current_year = datetime.datetime.now().year

client = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix=commands.when_mentioned_or(),
    status=discord.Status.online,
    activity=discord.Activity(type=discord.ActivityType.watching, name=config.getdata('status-text')),
    sync_commands=True,
    delete_not_existing_commands=True,
    )


@client.event
async def on_ready():
    print(f"""
          Version: {config.getdata("version")}
          Authors: {', '.join(config.getdata('authors'))}
          {current_year} © LYTEX MEDIA
          """)
    
    db.TicketDatabase().create_table()


def load_cogs():
    print('Loading cogs...\n')

    command_cogs = [file.stem for file in COMMANDS_DIR.glob('**/*.py') if not file.name.startswith('__')]
    ticket_cogs = [file.stem for file in TICKET_DIR.glob('**/*.py') if not file.name.startswith('__')]

    for cog in command_cogs:
        client.load_extension(f'cogs.commands.{cog}')

    for cog in ticket_cogs:
        client.load_extension(f'cogs.ticket-support.{cog}')
        

def start_bot():
    try:
        load_cogs()
        client.run(os.getenv('DISCORD_SECRET_TOKEN'))
    except Exception as e:
        print(f"Error: couldn't start the client...\n{e}")


if __name__ == '__main__':
    start_bot()