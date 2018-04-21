import asyncio
import mysql.connector
import time
import random
import database
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())

async def duel(message,challenger,target,channelid,bot):
	if str(target) == str(challenger):
		await bot.send_message(channelid, "FUCK YOU CHEATER GO SELF HARM SOMEWHERE ELSE")
	else:
		cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
		cursor = cnx.cursor()
		print(str(challenger) + str(target))
		print("FIGHT")
		sqlA = "SELECT * FROM stats "" WHERE name = '%s'" % (challenger)		
		cursor.execute(sqlA)		
		# Fetch all the rows in a list of lists.
		AttackerData = cursor.fetchall()	
		countA = cursor.rowcount	
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

		sqlD = "SELECT * FROM stats "" WHERE name = '%s'" % (target)
		cursor.execute(sqlD)	
		# Fetch all the rows in a list of lists.
		DefenderData = cursor.fetchall()
		countD = cursor.rowcount
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
		print(DefenderData)
		print(countD)
		if countA == 0 :
			await bot.send_message(channelid," @%s ERROR : No character found please make a character with the '$create' command" % (challenger))
		elif countD == 0 :
			await bot.send_message(channelid," @%s ERROR : No character found please make a character with the '$create' command" % (target))
		else:

			await asyncio.sleep(2)
			AInfo = (AName, ALevel, AExp, AHp, AMaxHp, AConst, AStr, AIntel, ADex)
			DInfo = (DName, DLevel, DExp, DHp, DMaxHp, DConst, DStr, DIntel, DDex)


			coinwinner = random.randint(0,1)
			if coinwinner == 0:
				await bot.send_message(channelid, "Winner of the CoinFlip is %s they get the first strike" % (AName))
			else:
				await bot.send_message(channelid, "Winner of the CoinFlip is %s they get the first strike" % (DName))
			msg  = await bot.send_message(channelid, "%s 🗡 Remaining HP : %s \n %s 🛡 Remaining HP : %s" % (AName,AHp , DName, DHp))
			n = 1
			print("AHP : %s  DHP : %s" % (AHp,DHp))
			while AHp > 0 and DHp > 0 :	
					
				if coinwinner == 0 :
					DHp = combat(AInfo , DInfo)
					coinwinner = 1
					DInfo = (DName, DLevel, DExp, DHp, DMaxHp, DConst, DStr, DIntel, DDex)
					n = n+1
				else:
					AHp = combat(DInfo , AInfo)
					coinwinner = 0
					AInfo = (AName, ALevel, AExp, AHp, AMaxHp, AConst, AStr, AIntel, ADex)				
					n = n+1
				await asyncio.sleep(1)
				await bot.edit_message(msg,new_content="%s 🗡 Remaining HP : %s \n %s 🛡 Remaining HP : %s" % (AName,AHp , DName, DHp))
				print(n)
			if AHp <=0 :
				winner = DName
				loser = AName
				await bot.send_message(channelid,"The winner was @%s" % winner)
				await exp(winner, random.randint(9, 11), DInfo[2], bot, channelid)
				await exp(loser, random.randint(4, 6), AInfo[2], bot, channelid)
			else:
				winner = AName
				loser = DName
				await bot.send_message(channelid,"The winner was @%s" % winner)
				await exp(winner, random.randint(9, 11), AInfo[2], bot, channelid)
				await exp(loser, random.randint(4, 6), DInfo[2], bot, channelid)
		return winner ,AInfo ,DInfo

def combat(AInfo , DInfo):
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

#New code
async def exp(PlayerName, ExpAmount, PlayerExp, bot, channelid):
	#Generalized the exp giving code
	cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
	cursor = cnx.cursor()
	PlayerExp += ExpAmount
	print(PlayerName)
	print(str(PlayerExp) + "EXP CURRENTLY")
	LevelsToGive = 0
	if(PlayerExp >= 100):
		print("Level Up!")
		while(PlayerExp >= 100):
			PlayerExp -= 100
			LevelsToGive += 1
		Expcommand = "UPDATE stats SET Exp = %s WHERE Name = '%s'" % (PlayerExp, PlayerName)
		Levelcommand = "UPDATE stats SET Level = Level + %s WHERE Name = '%s'" % (LevelsToGive, PlayerName)
		cursor.execute(Expcommand)
		cnx.commit()
		cursor.execute(Levelcommand)
		cnx.commit()
		await levelup(PlayerName, bot, channelid)
	else:
		sql = "UPDATE stats SET Exp = %s WHERE Name = '%s'" % (PlayerExp, PlayerName)
		cursor.execute(sql)
		cnx.commit()
	cnx.close()

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
		AttackerData = await database.DownloadFullRecord(str(Playername), "stats")
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