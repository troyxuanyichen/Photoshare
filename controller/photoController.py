from connection import initConnection as connection

#get all the photos, does not require login
def getPhotos():
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT P.data, P.photoId FROM photos P")
	return cursor.fetchall() #NOTE list of tuples, [(data, photoId), ...]

#get all the photo from an album
def getPhotosFromAlbum(aid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT data, photoId FROM photos WHERE albumId = '{0}".format(aid))
	return cursor.fetchall()

#get photo id from photo data
def getIdFromData(data):
	conn = connection.init_connection()
	cursor = conn.cursor()
	if cursor.execute("SELECT albumId FROM photos WHERE data ='{0}".format(data)):
		photoId = cursor.fetchone()[0]
		return photoId
	else:
		return False
#add a photo_album record
def addPhotoAlbumRecord(pid, aid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	if cursor.execute("INSERT INTO photo_album (photoId, albumId) VALUES ('{0}', '{1}')".format(pid, aid)):
		return True
	else: 
		return False

#upload a photo to an album
def uploadPhoto(aid, caption, data):
	conn = connection.init_connection()
	cursor = conn.cursor()
	if cursor.execute("INSERT INTO photos (albumId, caption, data) VALUES ('{0}', '{1}', '{2}')".format(aid, caption, data)) != 1:
		conn.rollback()
		return False
	photoId = getIdFromData(data) if getIdFromData(data) else False
	if photoId == False:
		conn.rollback()
		return False
	
	conn.commit()

	# cursor.execute("SELECT data FROM photos WHERE photoId = '{0}'".format(1))
	# photo = cursor.fetchone()[0]
	# wtf = cursor.execute("INSERT INTO photos (albumId, caption, data) VALUES ('{0}', '{1}', '{2}')".format(aid, caption, data))
	# print wtf
	# if failed:
	# 	conn.rollback()
	# else:
	# 	cursor.execute("INSERT INTO photos () VALUES data, photoId FROM photos WHERE albumId = '{0}".format(aid))
	# conn.commit()


