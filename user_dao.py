import psycopg2
import db_connection

connection = db_connection.ConnectToDB()

def addUser(name, number):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""INSERT INTO Users (name, number) Values (\'%s\', \'%s\');""" % (name, number))

def removeUser(uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""DELETE FROM Users WHERE id = %d;""" % (uid))

def setName(uid, name):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Users SET name=\'%s\' WHERE id = %d;""" % (name, uid))

def setPhoneNumber(uid, number):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Users SET phone=\'%s\' WHERE id = %s;""" % (number, uid))

