import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
import datetime
import os

from utils.config import Config
import utils.ticket_database as db


load_dotenv()
config = Config('config.json')

COMMANDS_DIR = Path.cwd() / 'cogs' / 'commands'
TICKET_DIR = Path.cwd() / 'cogs' / 'ticketsupport'

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
    print(f'Version: {config.getdata("version")}')
    print(f'Authors: {config.getdata("authors")}')
    print(f'License: {config.getdata("license")}')
    print(f'Copyright: {current_year} © LYTEX MEDIA')
    
    create_database()


def load_cogs():
    print('Loading cogs...\n')

    command_cogs = [file.stem for file in COMMANDS_DIR.glob('**/*.py') if not file.name.startswith('__')]
    ticket_cogs = [file.stem for file in TICKET_DIR.glob('**/*.py') if not file.name.startswith('__')]

    for cog in command_cogs:
        client.load_extension(f'cogs.commands.{cog}')

    for cog in ticket_cogs:
        client.load_extension(f'cogs.ticketsupport.{cog}')
        

def start_bot():
    try:
        load_cogs()
        client.run(os.getenv('DISCORD_SECRET_TOKEN'))
    except Exception as e:
        print(f"Error: couldn't start the client...\n{e}")


def create_database():
    ticket_db = db.TicketDatabase()
    ticket_db.create_table()
    ticket_db.close()

    banned_db = db.BannedDatabase()
    banned_db.create_table()
    banned_db.close()


if __name__ == '__main__':
    start_bot()