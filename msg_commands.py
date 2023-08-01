from discord import File
from blackjack import bjGame
from bj_bet import get_bet, add_money


keywords = ["*help",
    "*current guilds",
    "*hi",
    "*blackjack",
    "*bj",
    "*kys",
    "*img test"
]

async def send_message(text,chnl):
    await chnl.send(text)

async def show_current_guilds(client,channel):
    for i in client.guilds:
         await send_message(f"guild name and id: {i}, {i.id}",channel)

async def parse_message(msg,client):
    author = msg.author
    content = msg.content
    channel = msg.channel

    if author == client.user:
         return

    if content == keywords[0]:
        for i in keywords:
            await send_message(i,channel)
    
    if content == keywords[1]:
            await show_current_guilds(client,channel)

    if content == keywords[2]:
         await send_message(f"hi {author}",channel)

    #blackjack
    if content == keywords[3] or content == keywords[4]:
          bet = await get_bet(author=author,channel=channel, client=client)
          newgame = bjGame(channel=channel,author=author,client=client,bet_amnt=bet)
          await add_money(await newgame.STARTGAME(),author,channel)
    
    if content == keywords[5]:
         await send_message(f"bot is now offline",channel)

    if content == keywords[6]:
          pass

