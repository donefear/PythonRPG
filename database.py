import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read(['config.ini', 'persontoken.ini'])
DBToken = config['MySQL']
token_user = DBToken['user']
token_password = DBToken['password']
token_database = DBToken['database']
token_host = DBToken['host']

# import asyncio
# import sqlalchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
# from sqlalchemy import Column, Integer, String

# Session = sessionmaker(bind=engine)
# session = Session()

# class User(Base):
# 	__tablename__ = 'stats'

# 	id = Column(Integer, primary_key=True)
# 	Name = Column(String)
# 	Level = Column(Integer)
# 	Exp = Column(Integer)
# 	Hp = Column(Integer)
# 	MaxHp = Column(Integer)
# 	Const = Column(Integer)
# 	Str = Column(Integer)
# 	Intel = Column(Integer)
# 	Dex = Column(Integer)
# 	def __repr__(self):
# 		return "<User(Name='%s', Level='%s', Exp='%s', Hp='%s', MaxHp='%s', Const='%s', Str='%s', Intel='%s', Dex='%s')>" % (self.Name, self.Level, self.Exp, self.Hp, self.MaxHp, self.Const, self.Str, self.Intel, self.Dex)



# async def testrecord(Name):
# 	Db =  session.query(User).filter_by(Name=Name).first()
# 	output = [[Db.id,Db.Name,Db.Level,Db.Exp,Db.Hp,Db.MaxHp,Db.Const,Db.Str,Db.Intel,Db.Dex]]
# 	session.commit()
# 	session.close()
# 	print(output)
# 	return output

# async def DownloadFullRecord(Name):
# 	Db =  session.query(User).filter_by(Name=str(Name)).first()
# 	output = [[Db.id,Db.Name,Db.Level,Db.Exp,Db.Hp,Db.MaxHp,Db.Const,Db.Str,Db.Intel,Db.Dex]]
# 	return output

# async def UpdateField(Name, Table, Field, Value):
# 	# Update =  session.query(User).filter_by(Name=str(Name)).first()
# 	strField = str(Field)
# 	strField = Value
# 	print("field : %s , value : %s" % (str(Field),Value))
# 	print(session.dirty)
# 	session.commit()
# 	session.close()

# async def UpdateFieldByValue(Name, Table, Field, Value):
# 	print("updating databse")
# 	Db =  session.query(User).filter_by(Name=str(Name)).first()
# 	DbField = "Db.%s" % (Field)
# 	Update = "%s = %s + %s " % (DbField, DbField , Value)
# 	print("updating :::::: %s" % (Update))
# 	Update
# 	print(session.dirty)
# 	session.commit()
# 	session.close()	

async def CreateRecord(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	Name = str(message.author)
	sql = "SELECT * FROM stats "" WHERE name = '%s'" % (Name)
	cursor.execute(sql)
	results = cursor.fetchall()	
	count = cursor.rowcount		
	if count == 0:
		Const = random.randint(1, 10)
		Str = random.randint(1, 10)
		Intel = random.randint(1, 10)
		Dex = random.randint(1, 10)		
		Level = 1
		Exp = 0 
		MaxHp = 10+Const*Level
		Hp = MaxHp
		add_data = ("INSERT INTO stats (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex) ""VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
		Data = (Name, Level, Exp, Hp, MaxHp, Const, Str, Intel, Dex)
		msg =  "Name = %s \nLevel: %s Exp: %s \nHp: %s      | MaxHp: %s \n❤Const: %s | 💪Attack: %s \n🍀Luck: %s | 🖐Deffence: %s" % (Name,Level,Exp,Hp,MaxHp,Const,Str,Intel,Dex)
		print(add_data, Data)
		print(Data)
		cursor.execute(add_data, Data)
		cnx.commit()
	else:
		msg = "Character already created ! use $info"	
	cnx.close()	
	return msg

async def GetLocation(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	table = "stats"
	sql = "SELECT * FROM %s "" WHERE name = '%s'" % (Table, Name)		
	cursor.execute(sql)
	output = cursor.fetchall()
	count = len(output)
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
		location = row[10]
		coins = row[11]
	print(count)
	return location

async def GetCoins(Name):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	table = "stats"
	sql = "SELECT * FROM %s "" WHERE name = '%s'" % (Table, Name)		
	cursor.execute(sql)
	output = cursor.fetchall()
	count = len(output)
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
		location = row[10]
		coins = row[11]
	print(count)
	return coins

async def DownloadFullRecord(Name, Table):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "SELECT * FROM %s "" WHERE name = '%s'" % (Table, Name)		
	cursor.execute(sql)
	output = cursor.fetchall()
	cnx.commit()
	cnx.close()
	return output

async def UpdateField(Name, Table, Field, Value):
	cnx = mysql.connector.connect(user=token_user, password=token_password,database=token_database,host=token_host)
	cursor = cnx.cursor()
	sql = "UPDATE %s SET %s = %s WHERE name = '%s'" % (Table, Field, Value, Name)
	print("updating %s with %s" % (Field,Value))
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

