import discord
from discord.ext.commands import bot
from discord.ext import commands
import asyncio
import mysql.connector
import time
from time import gmtime, strftime
cdate = strftime("%d %m ", gmtime())

Client = discord.Client()
client = commands.Bot(command_prefix = "#")

cnx = mysql.connector.connect(user='bot', password='potato',host='127.0.0.1',database='bday')
cursor = cnx.cursor()


client.get_all_emojis()

@client.event
async def on_ready():
    print("World is about to DIE")


@client.event
async def on_message(message):
	if message.content == "suicide":
		await client.send_message(message.channel, "THE WORLD IS GOING TO DIE DIE DIE")
	if message.content == "poop":
		await client.send_message(message.channel, ":poop:")
	if message.content == "panda":
		await client.send_message(message.channel, ":DonefearHugg:")
	if message.content == "time":
		await client.send_message(message.channel, "%s" % (cdate))
	if message.content == "cummies":
		await client.send_message(message.channel, "@TheFlyingCrocodile is a bloody wanker")
	if message.content.startswith('#addbday'):
		args = message.content.split("-")
		await client.send_message(message.channel, "adding bday with params %s" % (args[1:]))
		bdate = args[1]
		bname = args[2]
		bbdate = "date(%s)" % (bdate)
		bbname = "'%s'" % (bname)
		add_bdate = ("INSERT INTO bday""(bdate,bname)""VALUES(%s, %s)")
		data_bdate = (bbdate,bname)
		await client.send_message(message.channel, "DEBUGG:::: bdate || %s" % (args[1]))
		await client.send_message(message.channel, "DEBUGG:::: bname || %s" % (args[2]))
		await client.send_message(message.channel, "DEBUGG:::: bbdate bbname || %s  %s" % bbdate  bbname)
		cursor.execute(add_bdate, data_bdate)
		cnx.commit()

cnx.close()

client.run("NDMyOTUzNjc4ODQwNzI1NTE1.Da1ANQ.TRV7uagT0Q0NhPCvKafsQ4VJ7xA")



	if message.content == "testupload":
		await client.send_message(message.channel, "params : %s" % (args[1:]))
		args = message.content.split("-")
		Name = args[1]
		Level = args[2]
		Exp = args[3]
		Hp = args[4]
		MaxHp = args[5]
		add_data = ("INSERT INTO test""(Name,Level,Exp,Hp,MaxHp)""VALUES(%s, %s, %s, %s, %s)")
		Data = (Name,Level,Exp,Hp,MaxHp)
		cursor.execute(add_data,Data)
		await client.send_message(message.channel, "DEBUGG:::: Name :  %s ; Level : %s ; Exp : %s ; Hp : %s ; MaxHp : %s" % (Name,Level,Exp,Hp,MaxHp))
		cnx.commit()
	if message.content.startswith('$react'):
		msg = await client.send_message(message.channel, 'React with thumbs up or thumbs down.')
		res = await client.wait_for_reaction([':thumbsup:', ':thumbsdown: '], message=msg)
		await client.send_message(message.channel, '{0.user} reacted with {0.reaction.emoji}!'.format(res))