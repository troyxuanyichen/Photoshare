from connection import initConnection as connection

#add comment to a photo, do not check if the commenter is userself
def addComment(text, uid, date, pid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	if cursor.execute("INSERT INTO comment (text, ownerId, date, photoId) VALUES ('{0}', '{1}', '{2}', '{3}')".format(text, uid, date, pid)):
		conn.commit()
		return True
	else:
		return False

#show comment of a photo
def showComment(pid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT text, ownerId, date FROM comment WHERE photoId = '{0}'".format(pid))
	return cursor.fetchall()
