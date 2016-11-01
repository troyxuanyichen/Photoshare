from connection import initConnection as connection

#get the album of a user 
def getUserAlbumLimited(uid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT albumId, name FROM albums WHERE ownerId = '{0}' LIMIT 10".format(uid))
	return cursor.fetchall()

#get the album of a user 
def getUserAlbum(uid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT albumId, name FROM albums WHERE ownerId = '{0}'".format(uid))
	return cursor.fetchall() 

#add an album to a user
def addAlbum(name, uid, date):
	conn = connection.init_connection()
	cursor = conn.cursor()
	if cursor.execute("INSERT INTO albums (name, ownerId, date) VALUES ('{0}', '{1}', '{2}')".format(name, uid, date)):
		conn.commit()
		return True
	else:
		return False

#get the name of an album from id
def getNameFromAlbumId(aid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM albums WHERE albumId = '{0}'".format(aid))
	return cursor.fetchone()[0]
