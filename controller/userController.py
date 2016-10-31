import flask
from flask import Flask, Response, request, render_template, redirect, url_for
app = Flask(__name__)
app.config.from_object('config')
from flaskext.mysql import MySQL
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()

#get all the user
def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users") 
	return cursor.fetchall()


#return email of all the other users
def getAllOtherUser(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT userId, email FROM users WHERE userId <> '{0}'".format(uid))   #select all the user except the current user
	return cursor.fetchall()

#return other people that is not in the friend list
def getPeopleYouMayKnow(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT U.userId, U.email FROM users U, friendship F WHERE U.userId = F.userId AND U.userId <> '{0}' AND U.userId NOT IN (SELECT F.friendId FROM friendship F WHERE F.userId = '{1}') LIMIT 10".format(uid, uid))	#avoid duplicated friendship
	return cursor.fetchall()

#return friend list of a user, just for display
def getFriends(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT U.email FROM friendship F, users U WHERE F.userId = '{0}' AND F.friendId = U.userId".format(uid))   #select all the friends a user has
	return cursor.fetchall()

#add friend for a user
def addFriend(uid, friendId):
	cursor = conn.cursor()
	cursor.execute("INSERT INTO friendship (userId, friendId) VALUES ('{0}', '{1}')".format(uid, friendId))
	conn.commit()
	return True
	# 	return True
	# else:
	# 	return False

#get the photo of the user
def getUsersPhotos(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT P.data, P.photoId FROM photos P, photo_album PA, albums A WHERE P.photoId = PA.photoId AND PA.albumId = A.albumId AND A.ownerId = '{0}'".format(uid))
	return cursor.fetchall() #NOTE list of tuples, [(imgdata, pid), ...]

#get id of the user using email
def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT userId  FROM users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]

def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email  FROM users WHERE email = '{0}'".format(email)): 
		#this means there are greater than zero entries with that email
		return False
	else:
		return True

