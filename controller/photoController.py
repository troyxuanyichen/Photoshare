from connection import initConnection as connection

#get all the photos, does not require login
def getPhotos():
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT P.photoId, P.data FROM photos P")
	return cursor.fetchall() #NOTE list of tuples, [(data, photoId), ...]

#get all the photo from an album
def getPhotoFromAlbum(aid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT photoId, data FROM photos WHERE albumId = '{0}'".format(aid))
	return cursor.fetchall()

#get photo by id
def getPhotoById(pid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT photoId, caption, data, likeNum FROM photos WHERE photoId = '{0}'".format(pid))
	return cursor.fetchone()[0]
#get all the photo from a user
def getPhotoFromUser(uid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT photoId, data FROM photos P, photo_album PA, album A WHERE P.albumId = PA.albumId AND PA.albumId = A.albumId AND A.ownerId = '{0}".format(uid))
	return cursor.fetchall()

#get user from photo id
def getPhotoOwner(pid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT A.ownerId, A.email FROM photo_album PA, album A WHERE PA.albumId = A.albumId AND PA.photoId = '{0}'".format(pid))
	return cursor.fetchone()[0]

#get photo id from photo data
def getIdFromData(data):
	conn = connection.init_connection()
	cursor = conn.cursor()
	if cursor.execute("SELECT albumId FROM photos WHERE data ='{0}'".format(data)):
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
	conn.commit()
	return True

#get all photos of a tag
def getPhotoByTag(des):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT P.photoId, P.data FROM photos P, photo_tag PT WHERE P.photoId = PT.photoId AND PT.tagDescription = '{0}'".format(des))
	return cursor.fetchall()

#get all photos of a user by tag
def getPhotoFromUserByTag(email, des):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT P.photoId, P.data FROM photos P, photo_tag PT, albuMS A, users U WHERE P.photoId = PT.photoId AND P.albumId = A.albumId AND A.ownerId = U.userId AND U.email = '{0}' AND PT.tagDescription = '{1}'".format(email, des))

#delete one photo by id
def deletePhoto(pid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	if cursor.execute("DELETE FROM photos WHERE photoId = '{0}'".format(pid)):
		conn.commit
		return True
	else:
		return False

