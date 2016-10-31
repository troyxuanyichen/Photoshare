#get the album of a user 
def getUserAlbum(uid):
    cursor = conn.cursor()
    cursor.execute("SELECT albumId, name, date as Create_Date FROM albums WHERE ownerId = '{0}".format(uid))
    return cursor.fetchall()

#add a photo into an album of a user
def addPhotoToAlbum(aid, data)