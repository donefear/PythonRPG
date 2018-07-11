import asyncio
import time
import random
import database
import discord
import functions
from discord.ext.commands import bot
from discord.ext import commands
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())


async def Commands(command,target,value,channelid,bot):
		
	if command.startswith("game"):		
		await bot.change_presence(game=discord.Game(name=target,url='https://discord.gg/rm5Mby',type=1), status=discord.Status("online"))

	if command.startswith("editexp"):		
		PlayerExp = GetExp(target)
		await asyncio.sleep(2)
		print(PlayerExp)
		await functions.exp(target, int(value), PlayerExp, bot, channelid)

	if command.startswith("editcoins"):
		Coins = await database.GetCoins(target)
		purse = Coins+int(value)
		await database.UpdateField(target, 'stats', 'coins', purse)

	if command.startswith("info"):
		Data = await GetData(target)
		print(Data)
		count = len(Data)
		if count == 0:
			await bot.send_message(channelid,"error no player found")	
		else:
			for row in Data:
				ID = row[0]
				Name = row[1]
				Level = row[2]
				PlayerExp = row[3]
				Hp = row[4]
				MaxHp = row[5]
				Const = row[6]
				Str = row[7]
				Intel = row[8]
				Dex = row[9]
				Location = row[10]
				Coins = row[11]
		await bot.send_message(channelid, "Name = `%s` \nLevel: `%s` Exp: `%s` \nHp: `%s`      | MaxHp: `%s` \n❤Const: `%s` | 💪Attack: `%s` \n🍀Luck: `%s` | 🖐Defence: `%s`\n🗺Location: `%s`  | 💰Coins: `%s`" % (target, Level, PlayerExp, Hp, MaxHp, Const, Str, Intel, Dex, Location , Coins))	
	
	if command.startswith("test"):
		await functions.WeightedDice(target)

	elif command.startswith("reroll"):
		stats,Const,Dex,Intel,Str,Level,Exp,MaxHp,Hp = await database.GenerateStats(target)
		await bot.send_message(channelid, stats)
		await database.UpdateField(target, 'stats','Const', Const)
		await database.UpdateField(target, 'stats','Dex', Dex)
		await database.UpdateField(target, 'stats','Intel', Intel)
		await database.UpdateField(target, 'stats','Level', Level)
		await database.UpdateField(target, 'stats','MaxHp', MaxHp)
		await database.UpdateField(target, 'stats','Hp', Hp)
		await database.UpdateField(target, 'stats','Exp', Exp)
		await database.UpdateField(target, 'stats','Str', Str)

async def GetData(target):
	Data = await database.DownloadFullRecord(target,"stats")
	count = len(Data)
	return Data

async def GetExp(target):
	Data = GetData(target)
	print(Data)
	count = len(Data)
	if count == 0:
		await bot.send_message(channelid,"error no player found")	
	else:
		for row in Data:
			ID = row[0]
			Name = row[1]
			Level = row[2]
			PlayerExp = row[3]
			Hp = row[4]
			MaxHp = row[5]
			Const = row[6]
			Str = row[7]
			Intel = row[8]
			Dex = row[9]
			Location = row[10]
			Coins = row[11]
	return PlayerExp
		

# # name = message.content[len('$name'):].strip()