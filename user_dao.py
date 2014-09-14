import psycopg2
import db_connection

connection = db_connection.ConnectToDB()

def addUser(name, number, email, device_id, timestamp):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""INSERT INTO Users (user_name, user_phone, user_email) Values (%s, %s,%s) RETURNING user_id;""" % (name, number,email))
	user_id = cur.fetchone()[0]
	cur.execute("""INSERT INTO Devices (device_id, user_id, last_login_time) Values (%s, %s, to_timestamp(%s));""" % (device_id, user_id, timestamp))
	connection.commit()
	cur.close()

def removeUser(uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""DELETE FROM Users WHERE user_id = %s;""" % (uid))
	connection.commit()
	cur.close()

def setName(uid, name):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Users SET user_name=%s WHERE id = %s;""" % (name, uid))		
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
	cur.execute("""SELECT user_name FROM Users WHERE user_id = %s;""" % uid)
	return cur.fetchone()[0]

def getUserPhoneNumber(uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_phone FROM Users WHERE user_id = %s;""" % uid)
	return cur.fetchone()[0]

def getUserEmail(uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_email FROM Users WHERE user_id = %s;""" % uid)
	return cur.fetchone()[0]

def authenticateUser(user_id, device_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT COUNT(user_id) FROM Devices WHERE user_id = %s AND device_id = '%s';""" % (user_id, device_id))
	c = cur.fetchone()[0]
	print c
	return c

