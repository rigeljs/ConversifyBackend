import psycopg2
import db_connection

connection = db_connection.ConnectToDB()

def getConversationsInGroup(group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT conversation_id FROM Conversations WHERE group_id = %s;""" % (group_id))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record[0])
	return conversation_ids

def addConversationForGroup(group_id, topic):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""INSERT INTO Conversations (group_id, topic, is_open) VALUES (%d, \'%s\', TRUE);""" % (group_id, topic))
	connection.commit()
	cur.close()

def closeConversation(cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Conversations SET is_open = FALSE WHERE conversation_id = %d;""" % (cid))
	connection.commit()
	cur.close()

def userOptInToConversation(uid, cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE UsersToConversation SET is_opted_in = TRUE WHERE user_id = %d AND conversation_id = %d;""" % (uid, cid))
	connection.commit()
	cur.close()

def userOptOutOfConversation(uid, cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE UsersToConversation SET is_opted_in = FALSE WHERE user_id = %d AND conversation_id = %d;""" % (uid, cid))
	connection.commit()
	cur.close()

def getUserOptedInConversationsForGroup(uid, gid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT C.conversation_id FROM Conversations C, UsersToConversations UTC 
				   WHERE C.group_id = %d AND C.conversation_id = UTC.conversation_id AND  UTC.user_id = %d AND UTC.is_opted_in = TRUE;""" %
				   (gid, uid))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record[0])
	return conversation_ids

def getUserOptedOutConversationsForGroup(uid, gid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT C.conversation_id FROM Conversations C, UsersToConversations UTC 
				   WHERE C.group_id = %d AND C.conversation_id = UTC.conversation_id AND  UTC.user_id = %d AND UTC.is_opted_in = FALSE;""" %
				   (gid, uid))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record[0])
	return conversation_ids

def getClosedConversationsForGroup(gid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT conversation_id FROM Conversations WHERE group_id = %d AND is_open = FALSE;""" % (gid))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record[0])
	return conversation_ids

def getUsersOptedInToConversation(cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToConversations WHERE conversation_id = %d AND is_opted_in = TRUE;""" % (cid))
	user_ids = []
	for record in cur:
		user_ids.append(record[0])
	return user_ids

def userCanWriteToConversation(uid, cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT can_write FROM UsersToConversations WHERE conversation_id = %d AND user_id = %d;""" % (cid, uid))
	record = cur.fetchone()
	if not record:
		return None
	return record[0]




