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
############LOADING CONFIG FILES ##################
config = configparser.ConfigParser()
config.read(['config.ini', 'persontoken.ini', 'prices.ini'])
DBToken = config['Bot-Token']
prices = config['Tavern']
token = DBToken['token']
###################################################
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
		msg = await database.CreateRecord(Name)
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
				Location = row[10]
				Coins = row[11]
				# Now print fetched result'💪','❤','🤓','🖐'
				await bot.send_message(message.channel, "Name = %s \nLevel: %s Exp: %s \nHp: %s      | MaxHp: %s \n❤Const: %s | 💪Attack: %s \n🍀Luck^: %s | 🖐Defence: %s\n🗺Location: %s  | 💰Coins: %s" % (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex, Location , Coins))	

	elif message.content == ("$exp"):
		await debug.expdebug(bot, message.channel, message.author)

	elif message.content == ("$town"):
		user = message.author
		await bot.send_message(message.channel, "You walk in town and see some trees in the distance to your left where there is a vast `$forest`. \nIn front of you there's an old but cozy `$tavern` with a `$blacksmith` annexing it. \nBehind the Tavern you notice a range of `$mountains` in the distance. \nTo your right you see an old run down `$shop` with an entrance to the `$sewer` next to it.")
		place = "town"
		await database.UpdateLocation(user,place)

	elif message.content == ("$tavern"):
		user = message.author
		await bot.send_message(message.channel, 'Welcome %s how can i help you ?' % (user))
		await bot.send_message(message.channel, "I could offer you a nice bedroom to `$sleep` , Or if you're not tired, \ndownstairs we have a room to `$gamble` , or maybe the `$brothel` is more your style? \nWe have a fine selection of beautiful women.")
		place = "tavern"
		await database.UpdateLocation(user, place)
	
	elif message.content == ("$sleep"): 
		user = message.author
		location = await database.GetLocation(user)
		print(location)
		if str(location) == "tavern":
			price = float(prices['sleep'])
			print(price)
			UserCoins = await database.GetCoins(user)
			if UserCoins >= price :
				msg = await functions.Rest(user)
				await bot.send_message(message.channel, msg)
				purse = UserCoins - price
				await database.UpdateField(Name, 'stats', 'coins', purse)
			else:
				await bot.send_message(message.channel, "Got no coin, a'right then... You can sleep there.... *Gestures to the door.*")
		else:
			await bot.send_message(message.channel, "Why do you try to sleep here ? You are nowhere near a tavern/bed!")

	elif message.content == ("$brothel"): 
		user = message.author
		location = await database.GetLocation(user)
		print(location)
		if str(location) == "tavern":
			price = float(prices['brothel'])
			print(price)
			UserCoins = await database.GetCoins(user)
			if UserCoins >= price :
				msg = await functions.Brothel(user)
				await bot.send_message(message.channel, msg)
				purse = UserCoins - price
				await database.UpdateField(user, 'stats', 'coins', purse)
			else:
				await bot.send_message(message.channel, "*She looks at you and laughs* Go somewhere else scumbag")
		else:
			await bot.send_message(message.channel, "*You look around confussed* there are no ladies of the night here.....\nperhaps at the tavern there might be some")

	elif message.content == ("$gamble"): 
		user = message.author

	elif message.content == ("$shop"): 
		user = message.author

	elif message.content == ("$blacksmith"): 
		user = message.author

	elif message.content == ("$sewer"): 
		user = message.author
		await bot.send_message(message.channel, "You open an old squeeky metal door into the sewers" )
		place = "sewer"
		await database.UpdateLocation(user, place)
		await functions.battle(user,place,message.channel,bot)


	elif message.content == ("$forest"): 
		user = message.author
		await bot.send_message(message.channel, "You start walking towards the forest in the distance\nonce you arrive in the forrest you are glad for the shade of the tall trees" )
		place = "forest"
		await database.UpdateLocation(user, place)
		await functions.battle(user,place,message.channel,bot)

	elif message.content == ("$mountains"): 
		user = message.author
		await bot.send_message(message.channel, "You grab your climbing gear and head of to the mountains" )
		place = "mountains"
		await database.UpdateLocation(user, place)
		await functions.battle(user,place,message.channel,bot)

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


bot.run(token)
cnx.close()