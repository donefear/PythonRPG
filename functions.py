import asyncio
import mysql.connector
import time
import random
import database
import configparser

from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())
config = configparser.ConfigParser()
config.read(['config.ini', 'persontoken.ini', 'monsters.ini','prices.ini'])

async def battle(Name,location,channelid,bot):
	#get info of the player
	mob = 'potato'
	UserData = await database.DownloadFullRecord(Name, 'stats')
	for row in UserData:
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
			coins = row[11]
	#get info of the monster
	print('location = %s' % (location))
	area = config['%s' % (location)]
	moblist = area['monster']
	print(moblist)
	roll = (random.randint(0,(len(moblist)-1)))
	print(roll)
	mob = config['%s%s' % (location , roll)]
	print(mob)
	MonsterName = mob['Name']
	MonsterHp = int(mob['Hp'])
	MonsterAttack = int(mob['Attack'])
	MonsterDefence = int(mob['Defence'])
	MonsterCoins = int(mob['Coins'])
		
	
	####actual combat
	await bot.send_message(channelid, "You run into a %s\nand it looks vicious and you're ready for combat" % (MonsterName))
	PlayerData = (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex)
	MonsterData = (MonsterName, 0, 0, MonsterHp, MonsterHp, 0, MonsterAttack, 0, MonsterDefence)
	# DefenderData = (DName, DLevel, DExp, DHp, DMaxHp, DConst, DStr, DIntel, DDex)
	# AttackerData = (AName, ALevel, AExp, AHp, AMaxHp, AConst, AStr, AIntel, ADex)
	await asyncio.sleep(2)
	coinwinner = 0
	msg  = await bot.send_message(channelid, "%s 🗡 Remaining HP : %s \n %s 🛡 Remaining HP : %s" % (Name, Hp , MonsterName, MonsterHp))
	print("HP : %s  HP : %s" % (Hp, MonsterHp))
	while Hp > 1 and MonsterHp > 1 :	
		print(coinwinner)
		if coinwinner == 0 :
			MonsterHp = combat(PlayerData , MonsterData)
			coinwinner = 1
			MonsterData = (MonsterName, 0, 0, MonsterHp, MonsterHp, 0, MonsterAttack, 0, MonsterDefence)
		else:
			Hp = combat(MonsterData , PlayerData)
			coinwinner = 0
			PlayerData = (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex)			
		await asyncio.sleep(1)
		await bot.edit_message(msg,new_content="%s 🗡 Remaining HP : %s \n %s 🛡 Remaining HP : %s" % (Name, round(Hp+0.5) , MonsterName, round(MonsterHp+0.5)))
	if Hp <=0 :
		#PLAYER DEAD
		winner = MonsterName
		loser = Name
		await bot.send_message(channelid,"The winner was @%s" % winner)
		
	else:
		#PLAYER WIN
		winner = Name
		loser = MonsterName
		await bot.send_message(channelid,"The winner was @%s" % winner)
		await exp(winner, random.randint(9, 11), Exp, bot, channelid)
		await database.UpdateField(Name, 'stats', 'Hp', round(Hp+0.5))
		winnings = coins + MonsterCoins
		await database.UpdateField(Name, 'stats', 'coins', winnings)


	


async def duel(message, challenger, target, channelid, bot):
	if str(target) == str(challenger):
		await bot.send_message(channelid, "No you can't duel yourself, try duelling another player instead")
	else:
		print(str(challenger) + str(target))
		print("FIGHT")
		AttackerData = await database.DownloadFullRecord(challenger, 'stats')	
		print(AttackerData)
		countA = len(AttackerData)
		for row in AttackerData:
			AID = row[0]
			AName = row[1]
			ALevel = row[2]
			AExp = row[3]
			AHp = row[4]
			AMaxHp = row[5]
			AConst = row[6]
			AStr = row[7]
			AIntel = row[8]
			ADex = row[9]
		DefenderData = await database.DownloadFullRecord(target, 'stats')
		countD = len(DefenderData)
		for row in DefenderData:
			DID = row[0]
			DName = row[1]
			DLevel = row[2]
			DExp = row[3]
			DHp = row[4]
			DMaxHp = row[5]
			DConst = row[6]
			DStr = row[7]
			DIntel = row[8]
			DDex = row[9]	
		print(countD)
		DefenderData = (DName, DLevel, DExp, DHp, DMaxHp, DConst, DStr, DIntel, DDex)
		AttackerData = (AName, ALevel, AExp, AHp, AMaxHp, AConst, AStr, AIntel, ADex)	
		if countA == 0 :
			await bot.send_message(channelid," @%s ERROR : No character found please make a character with the '$create' command" % (challenger))
		elif countD == 0 :
			await bot.send_message(channelid," @%s ERROR : No character found please make a character with the '$create' command" % (target))
		else:
			DefenderData = (DName, DLevel, DExp, DHp, DMaxHp, DConst, DStr, DIntel, DDex)
			AttackerData = (AName, ALevel, AExp, AHp, AMaxHp, AConst, AStr, AIntel, ADex)
			await asyncio.sleep(2)
			if (AIntel+random.randint(1,6)) > (DIntel+random.randint(1,6)):
				coinwinner = 0 
			else:
				coinwinner = 1
			if coinwinner == 0:
				await bot.send_message(channelid, "Winner of the CoinFlip is %s they get the first strike" % (AName))
			else:
				await bot.send_message(channelid, "Winner of the CoinFlip is %s they get the first strike" % (DName))
			msg  = await bot.send_message(channelid, "%s 🗡 Remaining HP : %s \n %s 🛡 Remaining HP : %s" % (AName, AHp , DName, DHp))
			print("AHP : %s  DHP : %s" % (AHp, DHp))
			while AHp > 0 and DHp > 0 :	
				if coinwinner == 0 :
					DHp = combat(AttackerData , DefenderData)
					coinwinner = 1
					DefenderData = (DName, DLevel, DExp, DHp, DMaxHp, DConst, DStr, DIntel, DDex)
				else:
					AHp = combat(DefenderData , AttackerData)
					coinwinner = 0
					AttackerData = (AName, ALevel, AExp, AHp, AMaxHp, AConst, AStr, AIntel, ADex)				
				await bot.edit_message(msg,new_content="%s 🗡 Remaining HP : %s \n %s 🛡 Remaining HP : %s" % (AName,AHp , DName, DHp))
				await asyncio.sleep(1.5)
			if AHp <=0 :
				winner = DName
				loser = AName
				await bot.send_message(channelid,"The winner was @%s" % winner)
				await exp(winner, random.randint(9, 11), DExp, bot, channelid)
				await exp(loser, random.randint(4, 6), AExp, bot, channelid)
			else:
				winner = AName
				loser = DName
				await bot.send_message(channelid,"The winner was @%s" % winner)
				await exp(winner, random.randint(9, 11), AExp, bot, channelid)
				await exp(loser, random.randint(4, 6), DExp, bot, channelid)
		return

def combat(AInfo, DInfo):
	#DInfo = DefenderData = (DName, DLevel, DExp, DHp, DMaxHp, DConst, DStr, DIntel, DDex)
	#AInfo = AttackerData = (AName, ALevel, AExp, AHp, AMaxHp, AConst, AStr, AIntel, ADex)
	AName = AInfo[0]
	AStr = AInfo[6]
	DDex = DInfo[8]
	DHp = DInfo[3]
	DName = DInfo[0]
	critchance = random.randint(0,100)
	if (Aintel + random.randint(1,6)) <= critchance :
		crit = Astr*0.25
	else:
		crit = 0
	Dice = random.randint(1, 12)
	DMG = (AStr + Dice + crit) - DDex
	if DMG <=0:
		DMG = 0
	print('crit : %s' % crit)
	print("%s did %s dmg" % (AName,DMG))
	DHp -= DMG
	print("%s HP = %s" % (DName,DHp))
	return DHp

async def exp(PlayerName, ExpAmount, PlayerExp, bot, channelid):
	#Generalized the exp giving code
	PlayerExp += ExpAmount
	print(PlayerName)
	print(str(PlayerExp) + "EXP CURRENTLY")
	LevelsToGive = 0
	if(PlayerExp >= 100):
		print("Level Up!")
		while(PlayerExp >= 100):
			PlayerExp -= 100
			LevelsToGive += 1
		#async def UpdateField(Name, Table, Field, Value):
		await database.IncrementFieldByValue(PlayerName, "stats", "Level", LevelsToGive)
		await levelup(PlayerName, bot, channelid)
	await database.UpdateField(PlayerName, "stats", "Exp", PlayerExp)

async def levelup(Playername,bot, channelid):
	msg = await bot.send_message(channelid, "------------------------------------------- \n Congratulations @%s you leveled up \n Please react with the corresponding emote to this message what you want to level up \n 💪 Attack \n ❤ Constitution \n 🍀 Luck \n 🖐 Defence" % (Playername))
	# 💪❤🤓🖐
	Reactioncheck = True
	while Reactioncheck == True :
		def check(reaction, user):
			e = str(reaction.emoji)
			return e.startswith(('💪','❤','🍀','🖐'))
		res = await bot.wait_for_reaction(message=msg, check=check)
		#await bot.send_message(message.channel, '{0.user} reacted with {0.reaction.emoji}!'.format(res))
		emoji = "{0.reaction.emoji}".format(res)
		emojiuser = "{0.user}".format(res)
		#await bot.send_message(message.channel,"DEBUG:emojiuser vs targetid: emojiuser : %s | target : %s " %  (emojiuser,targetid))
		print(emojiuser)
		AttackerData = await database.DownloadFullRecord(str(Playername), 'stats')
		for rows in AttackerData:
				ID = rows[0]
				Name = rows[1]
				Level = rows[2]
				Exp = rows[3]
				Hp = rows[4]
				MaxHp = rows[5]
				Const = rows[6]
				Str = rows[7]
				Intel = rows[8]
				Dex = rows[9]
		if str(emojiuser) == str(Playername):
			if emoji == "💪":
				# IncrementFieldByValue(Playername, Table, Field, Value):
				await database.IncrementFieldByValue(Playername, "stats", "Str", 1)
				await bot.send_message(channelid, "You have chosen to upgrade your Attack.")		
			elif emoji == "❤":
				await database.IncrementFieldByValue(Playername, "stats", "Const", 1)
				await bot.send_message(channelid, "You have chosen to upgrade your constitution.")		
			elif emoji == "🍀":
				await database.IncrementFieldByValue(Playername, "stats", "Intel", 1)
				await bot.send_message(channelid, "You have chosen to upgrade your Luck.")		
			elif emoji == "🖐":
				await database.IncrementFieldByValue(Playername, "stats", "Dex", 1)
				await bot.send_message(channelid, "You have chosen to upgrade your Defence.")		

			await database.IncrementFieldByValue(Playername, "stats", "MaxHP", Const)
			await database.IncrementFieldByValue(Playername, "stats", "HP", Const)
			Reactioncheck = False 
		else:
			await bot.send_message(channelid,"Sorry you didn't level up so you can't choose a stat")
			await bot.clear_reactions(message=msg)

async def Rest(PlayerName):
	Data = await database.DownloadFullRecord(PlayerName, 'stats')
	count = len(Data)
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
	print(count)
	Data = (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex)
	if count == 0 :
		await bot.send_message(channelid, "@%s ERROR : No character found please make a character with the '$create' command" % (PlayerName))
	else:
		await  database.UpdateField(PlayerName, "stats", "Hp", MaxHp)
	msg = "The sun rises and you feel refreshed after a nice night's rest."
	return msg

async def RestStable(PlayerName):
	Data = await database.DownloadFullRecord(PlayerName, 'stats')
	count = len(Data)
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
	print(count)
	Data = (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex)
	if count == 0 :
		await bot.send_message(channelid, "@%s ERROR : No character found please make a character with the '$create' command" % (PlayerName))
	else:
		await  database.UpdateField(PlayerName, "stats", "Hp", float(MaxHp/2))
	msg = "You get kicked by a horse while sleeping and feel croggy and tired."
	return msg

async def Brothel(PlayerName):
	Data = await database.DownloadFullRecord(PlayerName, 'stats')
	count = len(Data)
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
	print(count)
	Data = (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex)
	if count == 0 :
		await bot.send_message(channelid, "@%s ERROR : No character found please make a character with the '$create' command" % (PlayerName))
	else:
		await  database.UpdateField(PlayerName, "stats", "Hp", MaxHp+5)
	Luck = random.randint(1,6)
	print("luck = %s" % (Luck))
	if Luck == 6 or Luck == 1 :
		await Robbed(PlayerName)
		msg = "I had a good night, hope I didn't catch anything though...\nHmm my pockets feel lighter."
	else:
		msg = "I had a good night, hope I didn't catch anything though..."
	return msg

async def Robbed(PlayerName):
	UserCoins = await database.GetCoins(PlayerName)
	purse = UserCoins - random.randint(1,5)
	if purse < 0:
		purse = 0
	await database.UpdateField(PlayerName, 'stats', 'coins', purse)
	return 

async def Gamble(PlayerName):
	await bot.send_message(channelid,)
	UserCoins = await database.GetCoins(PlayerName)
	return msg 

async def Shop(PlayerName):
	return msg 

async def Roulette(Playername,Value,Bet):
	roll = random.randint(0,36)
	Bet = int(Bet)
	print(roll)
	Winnings = 0
	msg = ""
	#wich numbers are black
	color = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
	#cheeck if roll is even or odd
	if roll % 2 == 0:
		num = 'even'
		print(num)
	else:
		num = 'odd'
		print(num)
	#check if roll is a black or red number
	if color.count(roll) == 1:
		colour1 = 'black'
		print(colour1)
	else:
		colour1 = 'red'
		print(colour1)
	output = colour1+str(roll)+num
	#checking the bet player placed
	if Value == 37 or Value == 38:		
		if Value == 37:
			Pick = 'black'
			print(Pick)
		else:
			Pick = 'red'
			print(Pick)
		if colour1 == Pick:
			Winnings = Bet*2
			msg = "The wheel slows down and the ball lands on `%s` and double your winnings" % (output)
		else:
			msg = "The wheel slows down and the ball lands on `%s` YOU LOSE" % (output)
			Winnings -= Bet
	elif Value == 39 or Value == 40:
		if Value == 39:
			Pick = 'even'
			print(Pick)
		else:
			Pick = 'odd'
			print(Pick)
		if num == Pick:
			Winnings = Bet*2
			msg = "The wheel slows down and the ball lands on `%s` and double your winnings" % (output) 
		else:
			msg = "The wheel slows down and the ball lands on `%s` YOU LOSE" % (output)
			Winnings -= Bet		
	elif Value == roll == 0:
		print(Value)
		Winnings = Bet*6
		msg = "The wheel slows down and the ball lands on `%s` and sixtruple your winnings" % (output)		
	elif Value == roll:
		print(Value)
		Winnings = Bet*4
		msg = "The wheel slows down and the ball lands on `%s` and quatruple your winnings" % (output) 
	else:
		msg = "The wheel slows down and the ball lands on `%s` YOU LOSE" % (output)
		Winnings -= Bet
	return msg,Winnings

async def TenK(Dice):
	prize = config['TenK']
	#Dice = array of rolls 1,5,5,5,6,4
	Winnings = 0
	msg = ''
	for x in Dice:
		if Dice == 12345:
			Winnings = prize['Straight']
			msg = "You won %s!" % (Winnings)
		elif Dice.count(x) == 3:
			Winnings = prize['%sx%s' % (Dice.count(x),x)]
			msg = "You won %s!" % (Winnings)
		elif Dice.count(x) == 4:
			Winnings = prize['%sx%s' % (Dice.count(x),x)]
			msg = "You won %s!" % (Winnings)
		elif Dice.count(x) == 5:
			Winnings = prize['%sx%s' % (Dice.count(x),x)]
			msg = "You won %s!" % (Winnings)
		elif Dice.count(x) == 6:
			Winnings = prize['%sx%s' % (Dice.count(x),x)]
			msg = "You won %s!" % (Winnings)
		else:
			msg = "You lost !"
		print('%sx%s' % (Dice.count(x),x))
	return msg,Winnings