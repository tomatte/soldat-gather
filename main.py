import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from soldat_connect import init_soldat_connection

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!status'):
        print('send refresh')

client.run(os.getenv('TOKEN'))