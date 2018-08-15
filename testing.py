import json
import mysql.connector
import configparser
import random
import database

config = configparser.ConfigParser()
config.read(['./config.ini', './persontoken.ini', './monsters.ini','./prices.ini'])

DBToken = config['MySQL']
token_user = DBToken['user']
token_password = DBToken['password']
token_database = DBToken['database']
token_host = DBToken['host']

with open("items.json", "r") as read_file:
	items = json.load(read_file)

# the result is a Python dictionary:
#

#
# async def quickpoll(channel, question, options):
# 	if len(options) <= 1:
# 		await bot.send_message(channel, 'You need more than one option to make a poll!')
# 		return
# 	if len(options) > 10:
# 		await bot.send_message(channel, 'You cannot make a poll for more than 10 things!')
# 		return
#
# 	if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
# 		reactions = ['✅', '❌']
# 	else:
# 		reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
#
# 	description = []
# 	for x, option in enumerate(options):
# 		description += '\n {} {}'.format(reactions[x], option)
# 	embed = discord.Embed(title=question, description=''.join(description))
# 	react_message = await bot.send_message(channel, embed=embed)
# 	for reaction in reactions[:len(options)]:
# 		await bot.add_reaction(react_message, reaction)
# 	embed.set_footer(text='Poll ID: {}'.format(react_message.id))
# 	await bot.edit_message(react_message, embed=embed)






















cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
cursor = cnx.cursor()
sql = "SELECT * FROM %s "" WHERE id = '%s'" % ("stats",1)
cursor.execute(sql)
output = cursor.fetchall()
cnx.commit()
cnx.close()
# ['SnakeFang','SnakeFang','SnakeFang','SnakeFang','SnakeFang','SnakeFang','SnakeFang','SnakeFang','SnakeFang']
print(output)

# QuestItems.append(QuestName)
# print('Gained a questitem %s' % QuestItems)
# blup = '%s' % QuestItems
# await database.UpdateField(Name, 'stats', 'QuestItems', blup)

for row in output:
	# ID = row[0]
	# Name = row[1]
	# Level = row[2]
	# Exp = row[3]
	# Hp = row[4]
	# MaxHp = row[5]
	# Const = row[6]
	# Str = row[7]
	# Intel = row[8]
	# Dex = row[9]
	# location = row[10]
	# coins = row[11]
	MainHand = row[12]
	# OffHand = row[13]
	# Outfit = row[14]
	# usables = row[15]
	Loot = row[16]
	# QuestItems = row[17]
	# Quest = row[18]
Quest = "tail,5"

q = Quest.split(",")
requiredamount = q[1]

print(Loot)
print(Loot.count(q[0]))
print("required = %s" % requiredamount)
print(MainHand)
print(items['MainHand'][str(MainHand)]['EffectDex'])
