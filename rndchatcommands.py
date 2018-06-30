import asyncio
import time
import random
import database
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())

async def chat(message,channelid,bot):

	if message.content == "suicide":
		await bot.send_message(channelid, "THE WORLD IS GOING TO DIE DIE DIE")
		
	if message.content.upper() == "POOP":
		await bot.send_message(channelid, ":poop:")

	if message.content.upper() == "PANDA":
		await bot.send_message(channelid, "<:DonefearHugg:294457783557029899>")

	if message.content == "$fucks":
		text = "00% ▒▒▒▒▒▒▒▒▒▒"
		await bot.send_message(message.channel, "Attempting to give a fuck")
		await bot.send_message(message.channel, "Loading ...")
		msg = await bot.send_message(message.channel, text)
		await asyncio.sleep(1)
		newmsg = "00% ▒▒▒▒▒▒▒▒▒▒"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		newmsg = "10% █▒▒▒▒▒▒▒▒▒"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		newmsg = "20% ██▒▒▒▒▒▒▒▒"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		newmsg = "30% ███▒▒▒▒▒▒▒"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		newmsg = "40% ████▒▒▒▒▒▒"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		newmsg = "50% █████▒▒▒▒▒"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		newmsg = "60% ██████▒▒▒▒"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		newmsg = "70% ███████▒▒▒"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		newmsg = "80% ████████▒▒"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		newmsg = "90% █████████🖕"
		await bot.edit_message(msg,new_content=newmsg)
		await asyncio.sleep(1)
		await bot.send_message(message.channel, "ERROR no fucks found")

	if message.content == "time":
		await bot.send_message(channelid, "%s" % (cdate))

	if message.content.upper() == "CUMMIES":
		await bot.send_message(channelid, "<@%s> is a bloody wanker" % (293846787784179714))

	if message.content.startswith('$greet'):
		await bot.send_message(message.channel, 'Say hello')
		msg = await bot.wait_for_message(author=message.author, content='hello')
		await bot.send_message(message.channel, 'Hello.')

	if message.content.startswith('$cool'):
		await bot.send_message(message.channel, 'Who is cool? Type $name namehere')

		def check(msg):
			return msg.content.startswith('$name')

		message = await bot.wait_for_message(author=message.author, check=check)
		name = message.content[len('$name'):].strip()
		await bot.send_message(message.channel, '{} is cool indeed'.format(name), tts = True)

	if message.content.startswith("$test"):
		test = message.content[len('$test'):].strip()
		#get the array of mentions
		mentions = message.raw_mentions
		#filter out the first mention
		author = mentions[0]
		await bot.send_message(message.channel,"%s ID's =  %s" % (test,author))

	if message.content.startswith("$dbtest"):
		name = message.content[len('$dbtest'):].strip()
		info = await database.testrecord(name)
		await bot.send_message(message.channel,"%s" % (info))


	if message.content.startswith("$purge"):
		author = message.author
		#await bot.send_message(message.channel,"DEBUG:author :  %s " %  (author))
		if str(author) == 'DoneFear#0897':
			await bot.send_message(message.channel, "PURGING CHANNEL")
			await bot.send_message(message.channel, "💣💣💣💣💣💣💣💣💣💣")
			await bot.send_message(message.channel, "💥💥💥💥💥💥💥💥💥💥")
			await bot.send_message(message.channel, "☠☠☠☠☠☠☠☠☠☠")
			await bot.send_message(message.channel, "PURGING CHANNEL")
			async def purge(channel):
				print("waiting 2.5 sec")
				await asyncio.sleep(2.5)
				print("deleting msg")
				await bot.purge_from(channel,limit=1000)
			await purge(message.channel)
		else:
			async def clear(msg2):
				print("waiting 10 sec")
				await asyncio.sleep(10)
				print("deleting msg")
				await bot.delete_message(msg2)
			msg2 = await bot.send_message(message.channel, ":x: :x: :x: ACCESS DENIED :x: :x: :x: ")
			await clear(msg2)

	


	if message.content == "$ping":
		Name = message.author
		await bot.start_private_message(Name)
		await bot.send_message(Name, "PONG")

	