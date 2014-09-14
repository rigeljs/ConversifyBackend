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
	cur.execute("""INSERT INTO Conversations (group_id, topic_name, is_open) VALUES (%s, '%s', TRUE) RETURNING conversation_id;""" % (group_id, topic))
	cid = cur.fetchone()[0]
	connection.commit()
	cur.close()
	return cid

def closeConversation(cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Conversations SET is_open = FALSE WHERE conversation_id = %s;""" % (cid))
	connection.commit()
	cur.close()

def addUserToConversation(uid, cid, can_write):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id, conversation_id FROM UsersToConversations WHERE user_id = %s AND conversation_id = %s;""" % (uid, cid))
	if not curr.fetchone():
		curr.execute("""INSERT INTO UsersToConversations (user_id, conversation_id, can_write) VALUES (%s, %s, %b);""" % (uid, cid, can_write))
	connection.commit()
	cur.close()

def userOptInToConversation(uid, cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE UsersToConversations SET is_opted_in = TRUE WHERE user_id = %s AND conversation_id = %s;""" % (uid, cid))
	connection.commit()
	cur.close()

def userOptOutOfConversation(uid, cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE UsersToConversations SET is_opted_in = FALSE WHERE user_id = %s AND conversation_id = %s;""" % (uid, cid))
	connection.commit()
	cur.close()

def getUserConversationsForGroup(uid, gid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT C.conversation_id, C.topic_name, C.is_open, UTC.is_opted_in, UTC.can_write FROM Conversations C, UsersToConversations UTC 
				   WHERE C.group_id = %s AND C.conversation_id = UTC.conversation_id AND  UTC.user_id = %s;""" %
				   (gid, uid))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record)
	return conversation_ids

def getClosedConversationsForGroup(gid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT conversation_id FROM Conversations WHERE group_id = %s AND is_open = FALSE;""" % (gid))
	conversation_ids = []
	for record in cur:
		conversation_ids.append(record[0])
	return conversation_ids

def getUsersOptedInToConversation(cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToConversations WHERE conversation_id = %s AND is_opted_in = TRUE;""" % (cid))
	user_ids = []
	for record in cur:
		user_ids.append(record[0])
	return user_ids

def userCanWriteToConversation(uid, cid):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT can_write FROM UsersToConversations WHERE conversation_id = %s AND user_id = %s;""" % (cid, uid))
	record = cur.fetchone()
	if not record:
		return None
	return record[0]






