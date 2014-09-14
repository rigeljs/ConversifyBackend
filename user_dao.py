import psycopg2
import db_connection

connection = db_connection.ConnectToDB()

def addUser(name, number):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""INSERT INTO Users (user_name, user_phone) Values (%s, %s);""" % (name, number))
	connection.commit()
	cur.close()

def removeUser(uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""DELETE FROM Users WHERE user_id = %d;""" % (uid))
	connection.commit()
	cur.close()

def setName(uid, name):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Users SET user_name=%s WHERE id = %d;""" % (name, uid))		
	connection.commit()
	cur.close()

def setPhoneNumber(uid, number):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Users SET user_phone=%s WHERE id = %s;""" % (number, uid))
	connection.commit()
	cur.close()

def setEmail(uid, email):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Users SET user_email=%s WHERE id = %s;""" % (email, uid))
	connection.commit()
	cur.close()

def getUserName(uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_name FROM Users WHERE user_id = %d;""" % uid)
	return cur.fetchone()[0]

def getUserPhoneNumber(uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_phone FROM Users WHERE user_id = %d;""" % uid)
	return cur.fetchone()[0]

def getUserEmail(uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_email FROM Users WHERE user_id = %d;""" % uid)
	return cur.fetchone()[0]


