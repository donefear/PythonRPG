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

cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
cursor = cnx.cursor()
sql = "SELECT * FROM %s "" WHERE id = '%s'" % ("stats",1)
cursor.execute(sql)
output = cursor.fetchall()
cnx.commit()
cnx.close()

print(output)

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
	# coins = row[11]
	MainHand = row[12]
	# OffHand = row[13]
	# Outfit = row[14]
	Loot = row[16] 
	# usables = row[15]
Quest = "tail,5"

q = Quest.split(",")
requiredamount = q[1]

print(Loot)
print(Loot.count(q[0]))
print("required = %s" % requiredamount)
print(MainHand)
print(items['MainHand'][str(MainHand)]['EffectDex'])
