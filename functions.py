import asyncio
import mysql.connector
import time
import random
import database
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())

async def duel(message, challenger, target, channelid, bot):
	if str(target) == str(challenger):
		await bot.send_message(channelid, "FUCK YOU CHEATER GO SELFHARM SOMEWHERE ELSE")
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
			coinwinner = random.randint(0,1)
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
				await asyncio.sleep(1)
				await bot.edit_message(msg,new_content="%s 🗡 Remaining HP : %s \n %s 🛡 Remaining HP : %s" % (AName,AHp , DName, DHp))
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
	Dice = random.randint(1, 12)
	DMG = (AStr + Dice) - DDex
	if DMG <=0:
		DMG = 0
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
	msg = await bot.send_message(channelid, "------------------------------------------- \n Congratulations @%s you leveled up \n Please react with the corresponding emote to this message what you want to level up \n 💪 Strength \n ❤ Constitution \n 🤓 Intelligence \n 🖐 Dexterity" % (Playername))
	# 💪❤🤓🖐
	Reactioncheck = True
	while Reactioncheck == True :
		def check(reaction, user):
			e = str(reaction.emoji)
			return e.startswith(('💪','❤','🤓','🖐'))
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
				await database.IncrementFieldByValue(PlayerPlayername, "stats", "Str", 1)
				await bot.send_message(channelid, "You have chosen to upgrade your strength.")		
			elif emoji == "❤":
				await database.IncrementFieldByValue(Playername, "stats", "Const", 1)
				await bot.send_message(channelid, "You have chosen to upgrade your constitution.")		
			elif emoji == "🤓":
				await database.IncrementFieldByValue(Playername, "stats", "Intel", 1)
				await bot.send_message(channelid, "You have chosen to upgrade your intelligence.")		
			elif emoji == "🖐":
				await database.IncrementFieldByValue(Playername, "stats", "Dex", 1)
				await bot.send_message(channelid, "You have chosen to upgrade your dexterity.")		

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
	msg = "The sun rises and you feel refreshed after a nice night rest."
	return msg

async def Brothel(PlayerName):
	return msg

async def Gamble(PlayerName):
	return msg 

async def Shop(PlayerName):
	return msg 

async def Forrest(PlayerName):
	return msg

async def Sewer(PlayerName):
	return msg

async def Mountain(PlayerName):
	return msg