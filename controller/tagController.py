from connection import initConnection as connection

#add a tag to a photo
def addTagToPhoto(pid, des):
	conn = connection.init_connection()
	cursor = conn.cursor()
	if cursor.execute("INSERT INTO photo_tag (photoId, tagDescription) VALUES ('{0}', '{1}')".format(pid, des)):
		conn.commit()
		return True
	else:
		return False


#display all the current tags
def showTags():
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM tags")
	tags = cursor.fetchall()
	return tags

#show top 10 tags
def showHotTags():
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT DISTINCT tagDescription FROM photo_tag GROUP BY tagDescription LIMIT 10")

#display all the tag of a photo
def showPhotoTags(pid):
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT tagDescription FROM photo_tag WHERE photoId = '{0}'".format(pid))
	tags = cursor.fetchall()
	if tags:
		return tags
	else:
		return False

#generate tags from string
def strToTags(string):
	list = string.split(" ")
	tags = []
	for i in list:
		if i:
			tags.append(i)
	print tags
	return tags

#sort tags by frequency
def tagsByFrequency():
	conn = connection.init_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT tagDescription, COUNT(tagDescription) AS theCount FROM photo_tag GROUP BY tagDescription ORDER BY theCount ASC")
	return cursor.fetchall[0]