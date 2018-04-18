import asyncio
import mysql.connector
import time
import random
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())
#Connecting to DB
cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
cursor = cnx.cursor()

async def duel(message,challenger,target,channelid,bot):
	print(str(challenger) + str(target))
	print("FIGHT")
	sqlA = "SELECT * FROM stats "" WHERE name = '%s'" % (challenger)		
	cursor.execute(sqlA)		
	# Fetch all the rows in a list of lists.
	AttackerData = cursor.fetchall()	
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
	while AHp >= 0 & DHp >=0 :	
			
		if coinwinner == 0 :
			AHp = combat(AInfo , DInfo)
			coinwinner = 1
			AInfo = (AName, ALevel, AExp, AHp, AMaxHp, AConst, AStr, AIntel, ADex)
			n = n+1
		else:
			DHp = combat(DInfo , AInfo)
			coinwinner = 0
			DInfo = (DName, DLevel, DExp, DHp, DMaxHp, DConst, DStr, DIntel, DDex)
			n = n+1
		await asyncio.sleep(1)
		await bot.edit_message(msg,new_content="%s 🗡 Remaining HP : %s \n %s 🛡 Remaining HP : %s" % (AName,AHp , DName, DHp))
		print(n)
	if AHp <=0 :
		winner = DName
		exp(DInfo,AInfo)
	else:
		winner = AName
		exp(AInfo,DInfo)
	return winner ,AInfo ,DInfo

def combat(AInfo , DInfo):
	AStr = AInfo[6]
	DDex = DInfo[8]
	DHp = DInfo[3]
	Dice = random.randint(1, 6)
	DMG = (AStr + Dice) - DDex
	if DMG <=0:
		DMG = 0
	print("dmg"+str(DMG))
	DHp -= DMG
	return DHp

def exp(W,L):
	WExp = W[2]
	LExp = L[2]
	WName = W[0]
	LName = L[0]

	WExp = WExp+random.randint(9, 11)
	LExp = LExp+random.randint(4, 6)
	sqlW = "UPDATE stats SET Exp = %s WHERE Name = '%s'" % (WExp,WName)
	print(sqlW)
	cursor.execute(sqlW)
	sqlL = "UPDATE stats SET Exp = %s WHERE Name = '%s'" % (LExp,LName)
	print(sqlL)
	cursor.execute(sqlL)
	cnx.commit()

