import asyncio
import json
import random
import database
import discord
from discord.ext.commands import bot
from discord.ext import commands

with open("items.json", "r") as read_file:
		items = json.load(read_file)

async def sell(PlayerName, channel, bot):
	bot.send_message(channel, "What would you like to sell ?")
	loot = await database.getLoot(PlayerName)

async def InventoryLoot(PlayerName, channel, bot):
	loot = await database.GetLoot(PlayerName)
	print(loot)
	if len(loot) < 10:
		x = loot
	if len(loot) > 10:
		x = loot[0:10]
		y = loot[10:]
	reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

	description = []
	for x, option in enumerate(x):
		description += '\n {} {}'.format(reactions[x], option)
	embed = discord.Embed(title="Inventory", description=''.join(description))
	react_message = await bot.send_message(channel, embed=embed)
	await bot.edit_message(react_message, embed=embed)
	for reaction in reactions[:len(loot)]:
		await bot.add_reaction(react_message, reaction)
	if len(loot) > 10:
		await bot.add_reaction(react_message, "➡")
		for n in range(100):
				def check(reaction, user):
					e = str(reaction.emoji)
					return e.startswith('➡')

				res = await bot.wait_for_reaction(message=react_message, check=check)
				# res = await bot.on_reaction_add(message=msg, check=check)
				emoji = "{0.reaction.emoji}".format(res)
				emojiuser = "{0.user}".format(res)
				print(emojiuser)

				if str(emojiuser) != str(bot.user):

					if str(emojiuser) == str(PlayerName):
						if emoji == "➡":
							description = []
							for y, option in len(y):
								description += '\n {} {}'.format(reactions[y], option)
							embed = discord.Embed(title="Inventory", description=''.join(description))
							react_message = await bot.send_message(channel, embed=embed)
							for reaction in reactions[:len(y)]:
								await bot.add_reaction(react_message, reaction)
							await bot.edit_message(react_message, embed=embed)
					else:
						async def clear(msg2):
							print("waiting 2 sec")
							await asyncio.sleep(2)
							print("deleting msg")
							await bot.delete_message(msg2)
						msg2 = await bot.send_message(message.channel, "@%s you cant go trough someone elses inventory ......:unamused: " % (emojiuser))
						await bot.clear_reactions(message=msg)
						await clear(msg2)

async def BuySell(Name, Slot, Item, channel, bot):
	print("Name : %s , Slot : %s , Item : %s" % (Name,Slot,Item))
	Value = items[Slot][Item]['Value']
	ItemName = items[Slot][Item]['Name']
	print('item = %s' % ItemName)
	if Slot == "MainHand":
		PlayerItem = await database.GetMainHand(Name)
	elif Slot == "OffHand":
		PlayerItem = await database.GetOffHand(Name)

	if int(PlayerItem) == 0:
		coins = await database.GetCoins(Name)
		if int(coins) < int(Value) :
			await bot.send_message(channel, "You can't afford this.")
		else:
			await bot.send_message(channel, "Bought %s for %s" % (ItemName, Value))
			purse = int(coins) - int(Value)
			await database.UpdateField(Name, 'stats', 'coins', purse)
			await database.UpdateField(Name, 'stats', Slot, Item)
	else:
		coins = database.GetCoins(Name)
		if int(coins) < int(Value) :
			await bot.send_message(channel, "You can't afford this.")
		else:
			PlayerItemValue = items[Slot][Playeritem]['Value']
			await bot.send_message(channel, "Bought %s for %s\n and sold %s for %s" % (ItemName, Value, PlayerItem, PlayerItemValue))
			purse = int(coins) - int(Value) + (int(PlayeritemValue)*0.75)
			database.UpdateField(Name, 'stats', 'coins', purse)
			await database.UpdateField(Name, 'stats', Slot, Item)

async def BlackSmith(Name, channel, bot):
	reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
	blup = discord.Embed(title="BlackSmith", description='')
	blup.add_field(name='🗡', value='MainHand Items', inline=False)
	blup.add_field(name='🛡', value='Offhand Items', inline=False)
	react_message = await bot.send_message(channel, embed=blup)
	await bot.edit_message(react_message, embed=blup)
	await bot.add_reaction(react_message, '🗡')
	await bot.add_reaction(react_message, '🛡')

	for n in range(100):
		def check(reaction, user):
			e = str(reaction.emoji)
			return e.startswith(('🛡','🗡'))

		res = await bot.wait_for_reaction(message=react_message, check=check)
		# res = await bot.on_reaction_add(message=msg, check=check)
		emoji = "{0.reaction.emoji}".format(res)
		emojiuser = "{0.user}".format(res)
		print(emojiuser)
		if str(emojiuser) == str(Name):
			if emoji == "🛡":
				list = 'OffHand'
			elif emoji == '🗡':
				list = 'MainHand'
			Items = [1,2,3,4,5,6,7,8,9,10]
			print(Items)
			description = []
			for x, option in enumerate(Items):
				print(items[list][str(x)]['Name'])
				# '💪','❤','🤓','🖐'
				description += '\n {} __{}__ \n(Attack:{},Hp:{},Luck:{},Deffence:{})'.format(reactions[x], items[list][str(Items[x])]['Name'], items[list][str(Items[x])]['EffectStr'], items[list][str(Items[x])]['EffectHp'], items[list][str(Items[x])]['EffectInt'], items[list][str(Items[x])]['EffectDex'])
			embed = discord.Embed(title=list, description=''.join(description))
			react_message = await bot.send_message(channel, embed=embed)
			for reaction in reactions[:len(Items)]:
				await bot.add_reaction(react_message, reaction)
			await bot.edit_message(react_message, embed=embed)
			for m in range(100):
				def shop(reaction, user):
					e = str(reaction.emoji)
					return e.startswith(('1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟'))
				react = await bot.wait_for_reaction(message=react_message, check=shop)
				shopemoji = "{0.reaction.emoji}".format(react)
				shopuser = "{0.user}".format(react)
				if str(shopuser) == str(Name):
					prop = "0"
					if shopemoji == "1⃣":
						print("%s + 1" % shopemoji)
						prop = "1"
						await BuySell(Name, list, prop, channel, bot)
					elif shopemoji == '2⃣':
						print("%s + 2" % shopemoji)
						prop = "2"
						await BuySell(Name, list, prop, channel, bot)
					elif shopemoji == '3⃣':
						print("%s + 3" % shopemoji)
						prop = "3"
						await BuySell(Name, list, prop, channel, bot)
					elif shopemoji == '4⃣':
						print("%s + 4" % shopemoji)
						prop = "4"
						await BuySell(Name, list, prop, channel, bot)
					elif shopemoji == '5⃣':
						print("%s + 5" % shopemoji)
						prop = "5"
						await BuySell(Name, list, prop, channel, bot)
					elif shopemoji == '6⃣':
						print("%s + 6" % shopemoji)
						prop = "6"
						await BuySell(Name, list, prop, channel, bot)
					elif shopemoji == '7⃣':
						print("%s + 7" % shopemoji)
						prop = "7"
						await BuySell(Name, list, prop, channel, bot)
					elif shopemoji == '8⃣':
						print("%s + 8" % shopemoji)
						prop = "8"
						await BuySell(Name, list, prop, channel, bot)
					elif shopemoji == '9⃣':
						print("%s + 9" % shopemoji)
						prop = "9"
						await BuySell(Name, list, prop, channel, bot)
					elif shopemoji == '🔟':
						print("%s + 10" % shopemoji)
						prop = "10"
						await BuySell(Name, list, prop, channel, bot)
