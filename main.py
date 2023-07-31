import discord
from msg_commands import parse_message

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(msg):
    await parse_message(msg,client)

client.run('NzM5MjM5MzA5MzA3MjgxNDI5.GOmpqe.hwLsg4blu5YTavyS7t6w2wZeK5GNHjxHxbFH70')
