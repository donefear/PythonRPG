import discord
from discord.ext.commands import bot
from discord.ext import commands
import asyncio
import mysql.connector
import time
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())
Client = discord.Client()
client = commands.Bot(command_prefix = "$")
user = discord.User()

@client.event
async def on_message(message):
	if message.content.startswith('$react'):
		msg = await client.send_message(message.channel, 'React with thumbs up or thumbs down.')
		res = await client.wait_for_reaction(['+1', '-1'], message=msg)
		await client.send_message(message.channel, '{0.user} reacted with {0.reaction.emoji}!'.format(res))

client.run("NDMyOTUzNjc4ODQwNzI1NTE1.Da1ANQ.TRV7uagT0Q0NhPCvKafsQ4VJ7xA")