import discord
from discord.ext.commands import bot
from discord.ext import commands
import asyncio
import mysql.connector
import time
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())
Client = discord.Client()
bot = commands.Bot(command_prefix = "$")
bot.get_all_emojis()
user = discord.User()

#Connecting to DB
cnx = mysql.connector.connect(user='bot', password='potato',host='127.0.0.1',database='test')
cursor = cnx.cursor()


#on duel
async def duel(message,challenger,target):
	print("FIGHT")
	winner = await bot.send_message(message.channel,"⚔EVERYONE LOSES⚔")


#on startup of bot in console
@bot.event
async def on_ready():
	print('Connected!')
	print('Username: ' + bot.user.name)
	print('ID: ' + bot.user.id)


#on recieve msg in discord
@bot.event
async def on_message(message):
	if message.content == "suicide":
		await bot.send_message(message.channel, "THE WORLD IS GOING TO DIE DIE DIE")

	if message.content == "$create":
		await bot.send_message(message.channel, "Character being created...")

	if message.content.upper() == "POOP":
		await bot.send_message(message.channel, ":poop:")

	if message.content.upper() == "PANDA":
		await bot.send_message(message.channel, ":DonefearHugg:")

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
		await bot.send_message(message.channel, "%s" % (cdate))

	if message.content.upper() == "CUMMIES":
		await bot.send_message(message.channel, "<@%s> is a bloody wanker" % (293846787784179714))

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


	if message.content.startswith("$duel"):
		active = 1
		if active == 1:
			#$duel @name
			args = message.content.split(" ")
			#[0] $duel ; [1] @name
			target = args[1]
			challenger = message.author	
			#get the array of mentions
			mentions = message.mentions
			#filter out the first mention
			targetid = mentions[0]
			mentionsraw = message.raw_mentions
			target = mentionsraw[0]
			text = ("@%s Challenged %s please react to this message with :+1: or :-1: respectively for accepting or denying the duel" % (challenger,args[1]))
			msg = await bot.send_message(message.channel, text)

			for n in range(100):
				def check(reaction, user):
					e = str(reaction.emoji)
					return e.startswith(('👍', '👎'))

				res = await bot.wait_for_reaction(message=msg, check=check)
				#await bot.send_message(message.channel, '{0.user} reacted with {0.reaction.emoji}!'.format(res))
				emoji = "{0.reaction.emoji}".format(res)
				emojiuser = "{0.user}".format(res)
				#await bot.send_message(message.channel,"DEBUG:emojiuser vs targetid: emojiuser : %s | target : %s " %  (emojiuser,targetid))
				print(emojiuser)
				print(targetid)


				if str(emojiuser) == str(targetid):
					if emoji == "👍":
						newmsg = "challenge accepted"
						# await bot.send_message(message.channel,":+1: Accepted")
						await bot.edit_message(msg,new_content=newmsg)
						await duel(message,challenger,target)
					elif emoji == "👎":
						newmsg = "challenge DENIED"
						# await bot.send_message(message.channel,":-1: DENIED")
						await bot.edit_message(msg,new_content=newmsg)
					break
				else:
					async def clear(msg2):
						print("waiting 2 sec")
						await asyncio.sleep(2)
						print("deleting msg")
						await bot.delete_message(msg2)
					msg2 = await bot.send_message(message.channel, "@%s you were not challenged why you response to this ......:unamused: " % (emojiuser))
					await bot.clear_reactions(message=msg)
					await clear(msg2)



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






		# else:
		# 	await bot.send_message(message.channel,"DEBUG:clear reactions: message = %s , emoji = %s , member = %s" % (msg,emoji,emojiuser))
		# 	bot.clear_reactions(message=msg)


cnx.close()
bot.run("NDMyOTUzNjc4ODQwNzI1NTE1.Da1ANQ.TRV7uagT0Q0NhPCvKafsQ4VJ7xA")
