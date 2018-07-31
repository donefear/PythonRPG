import json
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

with open("items.json", "r") as read_file:
	data = json.load(read_file)

# the result is a Python dictionary:
# 
print (data['1']['Name'])

cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
cursor = cnx.cursor()
sql = "SELECT * FROM %s "" WHERE id = '%s'" % ("stats",1)		
cursor.execute(sql)
output = cursor.fetchall()
cnx.commit()
cnx.close()

print(output)

for row in output:
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
	coins = row[11]
	MainHand = row[12]
	OffHand = row[13]
	Outfit = row[14]
	Loot = row[15]
	usables = row[16]

print(Loot)
print(Loot.count("tail"))

