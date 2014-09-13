import psycopg2
import db_connection

connection = db_connection.ConnectToDB()

def getMessagesInConversation(cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT id FROM Messages WHERE conversation_id = %d;""" % (cid))
	message_ids = []
	for record in cur:
		message_ids.append(record[0])
	return message_ids

def addMessageToConversation(content, cid, uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""INSERT INTO Messages (conversation_id, user_id, content) VALUES (%d, %d, \'%s\');""" % (cid, uid, content))

def userApproveMessage(mid, uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT approves FROM UsersToMessages WHERE user_id = %d AND message_id = %d;""" % (uid, mid))
	record = cur.fetchone()
	if not record:
		cur.execute("""INSERT INTO UsersToMessages (user_id, message_id, approves) VALUES (%d, %d, TRUE);""" % (uid, mid))
	elif not record[0]:
		cur.execute("""UPDATE UsersToMessages SET approves=TRUE WHERE user_id = %d AND message_id = %d;""" % (uid, mid))

def userDisapproveMessage(mid, uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT approves FROM UsersToMessages WHERE user_id = %d AND message_id = %d;""" % (uid, mid))
	record = cur.fetchone()
	if not record:
		cur.execute("""INSERT INTO UsersToMessages (user_id, message_id, approves) VALUES (%d, %d, FALSE);""" % (uid, mid))
	elif record[0]:
		cur.execute("""UPDATE UsersToMessages SET approves=FALSE WHERE user_id = %d AND message_id = %d;""" % (uid, mid))

def usersWhoApproveMessage(mid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToMessages WHERE message_id = %d AND approves = TRUE;""" % (mid))
	user_ids = []
	for record in user_ids:
		user_ids.append(record[0])
	return user_ids

def usersWhoDisapproveMessage(mid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToMessages WHERE message_id = %d AND approves = FALSE;""" % (mid))
	user_ids = []
	for record in user_ids:
		user_ids.append(record[0])
	return user_ids


