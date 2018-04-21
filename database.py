import mysql.connector
async def DownloadFullRecord(Name, table):
	cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
	cursor = cnx.cursor()
	sql = "SELECT * FROM %s "" WHERE name = '%s'" % (table, Name)		
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	return output
async def SetField(Name, Table, Field, Value):
	cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
	cursor = cnx.cursor()
	sql = "UPDATE %s SET %s = %s WHERE name = '%s'" % (Table, Field, Value, Name)
	cursor.execute(sql)
	cnx.commit()
	cnx.close()
async def IncrementFieldByValue(Name, Table, Field, Value):
	cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
	cursor = cnx.cursor()
	sql = "UPDATE %s SET %s = %s + %s WHERE name = '%s'" % (Table, Field, Field, Value, Name)
	cursor.execute(sql)
	cnx.commit()
	cnx.close()


