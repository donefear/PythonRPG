import mysql.connector
import asyncio
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
file = open('dbtoken.txt', 'r')
engine = create_engine(file.read())
from sqlalchemy import Column, Integer, String

Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
	__tablename__ = 'stats'

	id = Column(Integer, primary_key=True)
	Name = Column(String)
	Level = Column(Integer)
	Exp = Column(Integer)
	Hp = Column(Integer)
	MaxHp = Column(Integer)
	Const = Column(Integer)
	Str = Column(Integer)
	Intel = Column(Integer)
	Dex = Column(Integer)
	def __repr__(self):
		return "<User(Name='%s', Level='%s', Exp='%s', Hp='%s', MaxHp='%s', Const='%s', Str='%s', Intel='%s', Dex='%s')>" % (self.Name, self.Level, self.Exp, self.Hp, self.MaxHp, self.Const, self.Str, self.Intel, self.Dex)



async def testrecord(Name):
	Db =  session.query(User).filter_by(Name=Name).first()
	output = [[Db.id,Db.Name,Db.Level,Db.Exp,Db.Hp,Db.MaxHp,Db.Const,Db.Str,Db.Intel,Db.Dex]]
	print(session.dirty)
	session.commit()
	session.close()
	print(output)
	return output

async def DownloadFullRecord(Name):
	Db =  session.query(User).filter_by(Name=str(Name)).first()
	output = [[Db.id,Db.Name,Db.Level,Db.Exp,Db.Hp,Db.MaxHp,Db.Const,Db.Str,Db.Intel,Db.Dex]]
	print(session.dirty)
	session.commit()
	session.close()
	return output


# async def DownloadFullRecord(Name, table):
# 	cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
# 	cursor = cnx.cursor()
# 	sql = "SELECT * FROM %s "" WHERE name = '%s'" % (table, Name)		
# 	cursor.execute(sql)
# 	output = cursor.fetchall()
# 	cnx.commit()
# 	cnx.close()
# 	return output

async def UpdateField(Name, Table, Field, Value):
	print("updating databse")
	print("Name = %s" % (Name))
	Db =  session.query(User).filter_by(Name=str(Name)).first()
	print("%s" % (Field))
	DbField = "Db.%s" % (Field)
	print("%s" % (DbField))
	Update = "%s = %s" % (DbField, Value)
	print("updating :::::: %s" % (Update))
	DbField = Value
	Update
	print(session.dirty)
	session.commit()
	session.close()
	return

async def UpdateFieldByValue(Name, Table, Field, Value):
	print("updating databse")
	Db =  session.query(User).filter_by(Name=str(Name)).first()
	DbField = "Db.%s" % (Field)
	Update = "%s = %s + %s " % (DbField, DbField , Value)
	print("updating :::::: %s" % (Update))
	Update
	print(session.dirty)
	session.commit()
	session.close()		
	return 


# async def UpdateField(Name, Table, Field, Value):
# 	cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
# 	cursor = cnx.cursor()
# 	sql = "UPDATE %s SET %s = %s WHERE name = '%s'" % (Table, Field, Value, Name)
# 	cursor.execute(sql)
# 	cnx.commit()
# 	cnx.close()

	
# async def IncrementFieldByValue(Name, Table, Field, Value):
# 	cnx = mysql.connector.connect(user='bot', password='potato',database='rpg',host='127.0.0.1')
# 	cursor = cnx.cursor()
# 	sql = "UPDATE %s SET %s = %s + %s WHERE name = '%s'" % (Table, Field, Field, Value, Name)
# 	cursor.execute(sql)
# 	cnx.commit()
# 	cnx.close()

