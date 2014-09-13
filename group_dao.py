import psycopg2
import db_connection

connection = db_connection.ConnectToDB()

def addGroup(name):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""INSERT INTO Groups (name) VALUES (\'%s\');""" % (name))

def removeGroup(group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""DELETE FROM Groups WHERE id = %d;""" % (group_id))

def setGroupName(group_id, name):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Groups SET name=\'%s\' WHERE groupd_id = %d;""" % (name, groupd_id))

def removeUserFromGroup(user_id, group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""DELETE FROM UsersToGroups WHERE user_id = %d AND groupd_id = %d""" % (user_id, groupd_id))

def addUserToGroup(user_id, groupd_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToGroups WHERE user_id = %d AND groupd_id = %d;""" % (user_id, groupd_id))
	if not cur.fetchone():
		cur.execute("""INSERT INTO UsersToGroups (user_id, groupd_id, isAdmin) VALUES (%d, %d, FALSE);""" % (user_id, groupd_id))

def setAdmin(group_id, user_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToGroups WHERE user_id = %d AND groupd_id = %d;""" % (user_id, groupd_id))
	if cur.fetchone():
		cur.execute("""UPDATE UsersToGroups SET isAdmin=TRUE WHERE user_id = %d AND groupd_id = %d;""" % (user_id, groupd_id))
	else:
		cur.execute("""INSERT INTO UsersToGroups (user_id, groupd_id, isAdmin) VALUES (%d, %d, TRUE);""" % (user_id, groupd_id))

def removeAdmin(group_id, user_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToGroups WHERE user_id = %d AND groupd_id = %d AND isAdmin = TRUE;""" % (user_id, groupd_id))
	if cur.fetchone():
		cur.execute("""UPDATE UsersToGroups SET isAdmin=FALSE WHERE user_id = %d AND groupd_id = %d;""" % (user_id, groupd_id))

def getGroupsForUser(user_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT group_id FROM UsersToGroups WHERE user_id = %d;""" % (user_id))
	groups = []
	for record in cur:
		groups.append(record[0])
	return groups

def userIsAdminForGroup(user_id, groupd_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT isAdmin FROM UsersToGroups WHERE user_id = %d AND groupd_id = %d;""" % (user_id, groupd_id))
	return cur.fetchone()[0]




