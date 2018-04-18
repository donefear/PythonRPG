import discord
from discord.ext.commands import bot
from discord.ext import commands
import asyncio
import mysql.connector
import time
import random
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())
Client = discord.Client()
bot = commands.Bot(command_prefix = "$")
bot.get_all_emojis()
user = discord.User()

#Connecting to DB
cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
cursor = cnx.cursor()

async def duel(message,challenger,target):
	AID = 0
	AName = ""
	ALevel = 0
	AExp = 0
	AHp = 0
	AMaxHp = 0
	AConst = 0
	AStr = 0
	AIntel = 0
	ADex = 0
	DID = 0
	DName = ""
	DLevel = 0
	DExp = 0
	DHp = 0
	DMaxHp = 0
	DConst = 0
	DStr = 0
	DIntel = 0
	DDex = 0

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

	print(AName + DName)
	await asyncio.sleep(2)
	AInfo = (AName, ALevel, AExp, AHp, AMaxHp, AConst, AStr, AIntel, ADex)
	print(AInfo)
	DInfo = (DName, DLevel, DExp, DHp, DMaxHp, DConst, DStr, DIntel, DDex)
	print(DInfo)
	winner = "⚔EVERYONE LOSES⚔"
	return winner ,AInfo ,DInfo

