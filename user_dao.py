import os
import psycopg2
import urlparse

DATABASE_URL = 'postgres://kyphfcdvxzifjj:eLnzmwE-AIWxnCf4qzNQh1QwEQ@ec2-54-197-237-171.compute-1.amazonaws.com:5432/dcu520moi7j7g'
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ[DATABASE_URL])

def ConnectToDB():
	return psycopg2.connect(database=url.path[1:],
						    user=url.username,
						    password=url.password,
						    host=url.hostname,
						    port=url.port)

def GetCursorForConnection(connection):
	return connection.cursor()

def addUser(name, number):
	cur = GetCursorForConnection(ConnectToDB())
	cur.execute("""INSERT INTO User (name, number) Values (\'%s\', \'%s\');""" % (name, number))

def removeUser(uid):
	curr = GetCursorForConnection(ConversifyDB())
	cur.execute("""DELETE FROM User WHERE id = %d;""" % (uid))

def setName(uid, name):
	cur = GetCursorForConnection(ConnectToDB())
	cur.execute("""UPDATE User SET name=\'%s\' WHERE id = %d;""" % (name, uid))

def setPhoneNumber(uid, number):
	cur = GetCursorForConnection(ConnectToDB())
	cur.execute("""UPDATE User SET phone=\'%s\' WHERE id = %s;""" % (number, uid))

