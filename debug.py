import functions
import mysql.connector
from time import gmtime, strftime
cdate = strftime("GMT %m/%d/%Y", gmtime())

async def expdebug(bot, channelid, username):
	cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
	cursor = cnx.cursor()
	sql = "SELECT * FROM stats WHERE name = '%s'" % (username)
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
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
	print("Xp before functions.exp: %s" % (Exp))
	await functions.exp(Name, 1, Exp, bot, channelid)
	cnx.close()