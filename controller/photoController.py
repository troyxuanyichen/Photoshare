#get all the photos, does not require login
def getPhotos():
    cursor = conn.cursor()
    cursor.execute("SELECT P.data, P.photoId FROM photos P")
    return cursor.fetchall() #NOTE list of tuples, [(data, photoId), ...]

#get all the photo from an album
def getPhotosFromAlbum(aid):
	cursor = conn.cursor()
	cursor.execute("SELECT data, photoId FROM photos WHERE albumId = '{0}".format(aid))
	return cursor.fetchall()
