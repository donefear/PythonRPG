import mysql.connector
import configparser
import random

config = configparser.ConfigParser()
config.read(['./config.ini', './persontoken.ini', './monsters.ini','./prices.ini'])

DBToken = config['MySQL']
token_user = DBToken['user']
token_password = DBToken['password']
token_database = DBToken['database']
token_host = DBToken['host']
Statsinfo = config['player']
Maxstats = float(Statsinfo['MaxStats'])
# Maxstats=20


async def GenerateStats(Name):
	Const = random.randint(3, 8)
	Str = random.randint(3,8)
	Intel = random.randint(3,8)
	Dex = random.randint(3,8)
	Count = {'Const':Const, 'Str':Str, 'Intel':Intel, 'Dex':Dex}
	CurrentStats = Const + Str + Intel + Dex
	keys = ['Const', 'Str', 'Intel', 'Dex']
	while CurrentStats < Maxstats:
		key = keys[(random.randint(0,3))]
		# for key in keys:
			# If this value is lower than the target, say this is the lowest value
		if Count[key] < 8:
			Count[key] += 1
			# Increment your total as well
			CurrentStats += 1
	while CurrentStats > Maxstats:
		key = keys[(random.randint(0,3))]
		if Count[key] > 3:
			Count[key] -= 1
			CurrentStats -= 1
	while Const == Str == Dex == Intel == 5:
		key1 == keys[(random.randint(0,3))]
		key2 == keys[(random.randint(0,3))]
		if key1 != key2:
			key1 += 1
			key2 -= 1
	#reasigning stats
	Const = Count['Const']
	Dex = Count['Dex']
	Intel = Count['Intel']
	Str = Count['Str']
	Level = 1
	Exp = 0
	MaxHp = 10+Const
	Hp = MaxHp
	msg =  "Name = %s \nLevel: %s Exp: %s \nHp: %s      | MaxHp: %s \n❤Const: %s | 💪Attack: %s \n🍀Luck: %s | 🖐Defence: %s" % (Name,Level,Exp,Hp,MaxHp,Const,Str,Intel,Dex)
	return msg,Const,Dex,Intel,Str,Level,Exp,MaxHp,Hp

async def CreateRecord(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	results = cursor.fetchall()
	count = cursor.rowcount
	if count == 0:
		msg,Const,Dex,Intel,Str,Level,Exp,MaxHp,Hp = await GenerateStats(Name)

		add_data = ("INSERT INTO stats (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex , coins) ""VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)")
		Data = (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex, 10)

		print(add_data, Data)
		print(Data)
		cursor.execute(add_data, Data)
		cnx.commit()
	else:
		msg = "Character already created! use $info"
	cnx.close()
	return msg

async def RerollStats(Name, Data):
	Data = (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex, 10)
	for row in output:
		Name = row[0]
		Level = row[1]
		Exp = row[2]
		Hp = row[3]
		MaxHp = row[4]
		Const = row[6]
		Str = row[7]
		Intel = row[8]
		Dex = row[9]
		location = row[10]
		coins = row[11]

async def DownloadFullRecord(Name, Table):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM %s "" WHERE name = '%s'" % (Table, Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	return output

async def UpdateLocation(Name,Value):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "UPDATE stats SET location = '%s' WHERE name = '%s'" % (str(Value), Name)
	print("updating location with %s" % (Value))
	cursor.execute(sql)
	cnx.commit()
	cnx.close()

async def UpdateField(Name, Table, Field, Value):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "UPDATE %s SET %s = %s WHERE name = '%s'" % (Table, Field, Value, Name)
	print("updating %s with %s" % (Field,Value))
	cursor.execute(sql)
	cnx.commit()
	cnx.close()

async def UpdateQuestItems(Name,Value):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = 'UPDATE stats SET QuestItems = "%s" WHERE name = "%s" ' % (Value, Name)
	print("updating QuestItems with %s" % (Value))
	cursor.execute(sql)
	cnx.commit()
	cnx.close()

async def IncrementFieldByValue(Name, Table, Field, Value):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "UPDATE %s SET %s = %s + %s WHERE name = '%s'" % (Table, Field, Field, Value, Name)
	cursor.execute(sql)
	cnx.commit()
	cnx.close()

async def GetLevel(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	# print(output)
	for row in output:
		Level = row[2]
	return Level

async def GetLocation(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	# print(output)
	for row in output:
		Location = row[10]
	return Location

async def GetCoins(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	for row in output:
		coins = row[11]
	return coins

async def GetMainHand(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	# print(output)
	for row in output:
		MainHand = row[12]
	return MainHand

async def GetOffHand(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	# print(output)
	for row in output:
		OffHand = row[13]
	return OffHand

async def GetOutfit(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	# print(output)
	for row in output:
		Outfit = row[14]
	return Outfit

async def GetUsable(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	# print(output)
	for row in output:
		Usable = row[15]
	return Usable

async def GetLoot(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	# print(output)
	for row in output:
		Loot = row[16]
	blup  = Loot.strip("[]")
	args = blup.split(",")
	return args

async def GetQuestItems(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	# print(output)
	for row in output:
		Quest = row[17]
	return Quest

async def GetQuest(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	# print(output)
	for row in output:
		Quest = row[18]
	return Quest
