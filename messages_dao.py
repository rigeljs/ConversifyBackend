import psycopg2
import db_connection

connection = db_connection.ConnectToDB()

def getMessagesInConversation(cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT * FROM Messages WHERE conversation_id = %s ORDER BY time_updated;""" % (cid))
	message_ids = []
	for record in cur:
		message_ids.append(record)
	return message_ids

def addMessageToConversation(content, time_updated, cid, uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""INSERT INTO Messages (conversation_id, time_updated, user_id, message_text) VALUES (%s, to_timestamp(%s), %s, '%s') RETURNING message_id;""" % (cid, time_updated, uid, content))
	mid = cur.fetchone()[0]
	connection.commit()
	cur.close()
	return mid

def userApproveMessage(mid, uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT approves FROM UsersToMessages WHERE user_id = %s AND message_id = %s;""" % (uid, mid))
	record = cur.fetchone()
	if not record:
		cur.execute("""INSERT INTO UsersToMessages (user_id, message_id, approves) VALUES (%s, %s, TRUE);""" % (uid, mid))
	elif not record[0]:
		cur.execute("""UPDATE UsersToMessages SET approves=TRUE WHERE user_id = %s AND message_id = %s;""" % (uid, mid))
	connection.commit()
	cur.close()

def userDisapproveMessage(mid, uid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT approves FROM UsersToMessages WHERE user_id = %s AND message_id = %s;""" % (uid, mid))
	record = cur.fetchone()
	if not record:
		cur.execute("""INSERT INTO UsersToMessages (user_id, message_id, approves) VALUES (%s, %s, FALSE);""" % (uid, mid))
	elif record[0]:
		cur.execute("""UPDATE UsersToMessages SET approves=FALSE WHERE user_id = %s AND message_id = %s;""" % (uid, mid))
	connection.commit()
	cur.close()

def usersWhoApproveMessage(mid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToMessages WHERE message_id = %s AND approves = TRUE;""" % (mid))
	user_ids = []
	for record in cur:
		user_ids.append(record[0])
	return user_ids

def usersWhoDisapproveMessage(mid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToMessages WHERE message_id = %s AND approves = FALSE;""" % (mid))
	user_ids = []
	for record in cur:
		user_ids.append(record[0])
	return user_ids

def getMessageById(mid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT m.message_id, m.conversation_id, c.group_id, m.user_id, m.message_text, m.time_updated FROM Messages m, Conversations c WHERE m.message_id = %s;""" % (mid))
	messages = []
	for record in cur:
		messages.append(record)
	return messages

def getMessagesForUser(user_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT * FROM Messages WHERE user_id = %s ORDER BY time_updated;""" % (user_id))
	message_ids = []
	for record in cur:
		message_ids.append(record)
	return message_ids
