import discord
from discord.ext.commands import bot
from discord.ext import commands
import asyncio
import mysql.connector
import time
import random
import functions
import sys
import debug
import configparser
import database
import rndchatcommands
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())
Client = discord.Client()
bot = commands.Bot(command_prefix = "$")
bot.get_all_emojis()
user = discord.User()

ScriptName = "Text-Based RPG game for Discord"
Website = "https://discord.gg/rm5Mbyu"
Description = "......"
Creator = "@DoneFear & @BoySanic"
Version = "2.0.0.0"

#on startup of bot in console
@bot.event
async def on_ready():
	print('Connected!')
	print('Username: ' + bot.user.name)
	print('ID: ' + bot.user.id)
	print('----------------------------------------')


#on recieve msg in discord
@bot.event
async def on_message(message):

	if message.content == "$create":
		await bot.send_message(message.channel, "Character being created...")
		Name = str(message.author)
		msg = database.CreateRecord(Name)
		await bot.send_message(message.channel, msg)
	elif message.content == "$info":
		name = str(message.author)		
		Data = await database.DownloadFullRecord(name, "stats")	
		count = len(Data)
		print(count)
		if count == 0:
			await bot.send_message(message.channel,"No character created ! use `$create`")	
		else:
			for row in Data:
				ID = row[0]
				Name = row[1]
				Level = row[2]
				Exp = row[3]
				Hp = row[4]
				MaxHp = row[5]
				Const = row[6]
				Str = row[7]
				Intel = row[8]
				Dex = row[9]
				# Now print fetched result'💪','❤','🤓','🖐'
				await bot.send_message(message.channel, "Name = %s \nLevel: %s Exp: %s \nHp: %s      | MaxHp: %s \n❤Const: %s | 💪Str: %s \n🤓Intel: %s | 🖐Dex: %s" % (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex))	
		cnx.close()

	elif message.content == ("$exp"):
		await debug.expdebug(bot, message.channel, message.author)

	elif message.content.startswith("$duel"):
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
			print(target)
			if target != "432953678840725515":
				text = ("@%s Challenged %s please react to this message with :+1: or :-1: respectively for accepting or denying the duel" % (challenger,args[1]))
				msg = await bot.send_message(message.channel, text)

				for n in range(100):
					def check(reaction, user):
						e = str(reaction.emoji)
						return e.startswith(('👍', '👎'))

					res = await bot.wait_for_reaction(message=msg, check=check)
					emoji = "{0.reaction.emoji}".format(res)
					emojiuser = "{0.user}".format(res)

					if str(emojiuser) == str(targetid):
						if emoji == "👍":
							newmsg = "challenge accepted"
							# await bot.send_message(message.channel,":+1: Accepted")
							await bot.edit_message(msg,new_content=newmsg)
							await functions.duel(message,challenger,targetid,message.channel,bot)
							
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
			else:
				await bot.send_message(message.channel, "I'm almighty you can't duel me")
				active = 0



		# else:
		# 	await bot.send_message(message.channel,"DEBUG:clear reactions: message = %s , emoji = %s , member = %s" % (msg,emoji,emojiuser))
		# 	bot.clear_reactions(message=msg)
	
	else :
		await rndchatcommands.chat(message,message.channel,bot)


# file = open('token.txt', 'r')
# bot.run(file.read())

config = configparser.ConfigParser()
config.read(['config.ini', 'persontoken.ini'])
DBToken = config['Bot-Token']
token = DBToken['token']
bot.run(token)
cnx.close()