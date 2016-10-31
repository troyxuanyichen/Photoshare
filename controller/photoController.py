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

#upload a photo to an album
def uploadPhoto(aid, caption, data):
	conn = connection.init_connection()
	cursor = conn.cursor()
	print str(aid) + caption + str(data)
	wtf = cursor.execute("INSERT INTO photos (albumId, caption, data) VALUES ('{0}', '{1}', '{2}')".format(aid, caption, data))
	print wtf
	# if failed:
	# 	conn.rollback()
	# else:
	# 	cursor.execute("INSERT INTO photos () VALUES data, photoId FROM photos WHERE albumId = '{0}".format(aid))
	# conn.commit()

