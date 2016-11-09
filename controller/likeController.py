from connection import initConnection as connection

#like a photo
def likePhoto(pid, uid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	if cursor.execute("INSERT INTO like_photo (photoId, userId) VALUES ('{0}', '{1}')".format(pid, uid)):
		conn.commit()
		return True
	else:
		return False
#show number of like of a photo
def showNumOfLike(pid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT likeNum FROM photo WHERE photoId = '{0}'".format(pid))
	return cursor.fetchone()[0]

#show who like this photo
def showPeopleWhoLike(pid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT U.userId, U.email FROM users U, like_photo LP WHERE U.userId = LP.userId AND LP.photoId = '{0}'".format(pid))
	return cursor.fetchall()