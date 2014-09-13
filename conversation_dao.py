import psycopg2
import db_connection

connection = db_connection.ConnectToDB()

def getConversationsInGroup(group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT id FROM Conversations WHERE group_id = %d;""" % (group_id))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record[0])
	return conversation_ids

def addConversationForGroup(group_id, topic):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""INSERT INTO Conversations (group_id, topic, isOpen) VALUES (%d, \'%s\', TRUE);""" % (group_id, topic))

def closeConversation(cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Conversations SET isOpen = FALSE WHERE id = %d;""" % (cid))

def userOptInToConversation(uid, cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE UsersToConversation SET isOptedIn = TRUE WHERE user_id = %d AND conversation_id = %d;""" % (uid, cid))

def userOptOutOfConversation(uid, cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE UsersToConversation SET isOptedIn = FALSE WHERE user_id = %d AND conversation_id = %d;""" % (uid, cid))

def getUserOptedInConversationsForGroup(uid, gid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT C.id FROM Conversations C, UsersToConversations UTC 
				   WHERE C.group_id = %d AND C.id = UTC.conversation_id AND  UTC.user_id = %d AND UTC.isOptedIn = TRUE;""" %
				   (gid, uid))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record[0])
	return conversation_ids

def getUserOptedOutConversationsForGroup(uid, gid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT C.id FROM Conversations C, UsersToConversations UTC 
				   WHERE C.group_id = %d AND C.id = UTC.conversation_id AND  UTC.user_id = %d AND UTC.isOptedIn = FALSE;""" %
				   (gid, uid))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record[0])
	return conversation_ids

def getClosedConversationsForGroup(gid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT id FROM Conversations WHERE group_id = %d AND isOpen = FALSE;""" % (gid))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record[0])
	return conversation_ids

def getUsersOptedInToConversation(cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToConversations WHERE conversation_id = %d AND isOptedIn = TRUE;""" % (cid))
	user_ids = []
	for record in cur:
		user_ids.append(record[0])
	return user_ids

def userCanWriteToConversation(uid, cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT canWrite FROM UsersToConversations WHERE conversation_id = %d AND user_id = %d;""" % (cid, uid))
	record = cur.fetchone()
	if not record:
		return None
	return record[0]




