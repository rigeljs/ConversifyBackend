import psycopg2
import db_connection

connection = db_connection.ConnectToDB()

def addGroup(name):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""INSERT INTO Groups (group_name) VALUES (%s);""" % (name))
	connection.commit()
	cur.close()

def removeGroup(group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""DELETE FROM Groups WHERE group_id = %s;""" % (group_id))
	connection.commit()
	cur.close()

def setGroupName(group_id, name):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""UPDATE Groups SET group_name=%s WHERE group_id = %s;""" % (name, group_id))
	connection.commit()
	cur.close()

def getGroupName(group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT group_name FROM Groups WHERE group_id = %s;""" % group_id)

def removeUserFromGroup(user_id, group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""DELETE FROM UsersToGroups WHERE user_id = %s AND group_id = %s""" % (user_id, group_id))
	connection.commit()
	cur.close()

def addUserToGroup(user_id, group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToGroups WHERE user_id = %s AND group_id = %s;""" % (user_id, group_id))
	if not cur.fetchone():
		cur.execute("""INSERT INTO UsersToGroups (user_id, group_id, is_admin) VALUES (%s, %s, FALSE);""" % (user_id, group_id))
	connection.commit()
	cur.close()

def setAdmin(group_id, user_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToGroups WHERE user_id = %s AND group_id = %s;""" % (user_id, group_id))
	if cur.fetchone():
		cur.execute("""UPDATE UsersToGroups SET is_admin=TRUE WHERE user_id = %s AND group_id = %s;""" % (user_id, group_id))
	else:
		cur.execute("""INSERT INTO UsersToGroups (user_id, group_id, is_admin) VALUES (%s, %s, TRUE);""" % (user_id, group_id))
	connection.commit()
	cur.close()

def removeAdmin(group_id, user_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToGroups WHERE user_id = %s AND group_id = %s AND is_admin = TRUE;""" % (user_id, group_id))
	if cur.fetchone():
		cur.execute("""UPDATE UsersToGroups SET is_admin=FALSE WHERE user_id = %s AND group_id = %s;""" % (user_id, group_id))
	connection.commit()
	cur.close()

def getUsersInGroup(group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToGroups WHERE group_id = %s;""" % group_id)
	user_ids = []
	for record in cur:
		user_ids.append(record[0])
	return user_ids

def getGroupsForUser(user_id):
	cur = db_connection.GetCursorForConnection(connection)
	query = """SELECT u.group_id, g.group_name FROM userstogroups u INNER JOIN groups g ON g.group_id = u.group_id WHERE u.user_id = %s;""" % (user_id)
	cur.execute(query)
	groups = []
	for record in cur:
		groups.append(record[0])
	return groups

def userIsAdminForGroup(user_id, group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT is_admin FROM UsersToGroups WHERE user_id = %s AND group_id = %s;""" % (user_id, group_id))
	return cur.fetchone()[0]

def getAdminForGroup(group_id):
	cur = db_connection.GetCursorForConnection(connection)
	cur.execute("""SELECT user_id FROM UsersToGroups WHERE group_id = %s AND is_admin = TRUE;""" % (group_id))
	user_ids = []
	for record in cur:
		user_ids.append(record[0])
	return user_ids





