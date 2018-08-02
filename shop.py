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
							for y, option in enumerate(y):
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
	