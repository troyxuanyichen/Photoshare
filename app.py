######################################
# author ben lawson <balawson@bu.edu>
# edited by Xuanyi Chen <troychen@bu.edu> 
######################################
# Some code adapted from 
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and benlawson at https://github.com/benlawson/Photoshare-Skeleton
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
import datetime
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask.ext.login as flask_login

#for image uploading
from werkzeug import secure_filename
import os, base64
from controller import userController as userController
from controller import photoController as photoController
from controller import albumController as albumController
from controller import likeController as likeController
from controller import tagController as tagController
from controller import commentController as commentController


mysql = MySQL()
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'cas660 project 1'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users") 
users = cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = userController.getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = userController.getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd 
	return user

'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
	return new_page_html
'''
# @app.route('/', methods=['GET'])
# def default():
# 	return 'hehe'

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return render_template('login.html')

	#The request method is POST (page is recieving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM users WHERE email = '{0}'".format(email)):
		data = cursor.fetchall()
		pwd = str(data[0][0] )
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
			return flask.redirect(flask.url_for('protected')) #protected is a function defined in this file

	#information did not match
	return "<a href='/login'>Try again</a>\
			</br><a href='/register'>or make an account</a>"

@app.route('/logout')	#should not display logout button when logged out
def logout():
	flask_login.logout_user()
	return render_template('hello.html', message='Logged out') 

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html') 

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register", methods=['GET'])
def register():
	return render_template('register.html', supress='True')  

@app.route("/register", methods=['POST'])	#newly added user not login
def register_user():
	try:
		email=request.form.get('email')
		password=request.form.get('password')
		firstName=request.form.get('firstName')
		lastName=request.form.get('lastName')
		birthday=request.form.get('birthday')	#default to today
		print birthday	#may be empty
		hometown=request.form.get('hometown')
		gender=request.form.get('gender')	#allow gender to be null		
	except:
		print "couldn't find all tokens" #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	cursor = conn.cursor()
	test =  userController.isEmailUnique(email)
	if test:
		print cursor.execute("INSERT INTO Users (email, password, firstName, lastName, birthday, hometown, gender) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(email, password, firstName, lastName, birthday, hometown, gender))
		conn.commit()
		print "authentication success"
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('hello.html', name=email, message='Account Created!')
	else:
		print "Email already been used"	#correct this
		return flask.redirect(flask.url_for('register'))
#end login code

@app.route('/profile')
@flask_login.login_required
def protected():
	return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile")

#begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_photo():
	if request.method == 'POST':
		print 'begin upload'
		uid = userController.getUserIdFromEmail(flask_login.current_user.id)
		print 'uid = ' + str(uid)
		try:
			caption = request.form.get('caption')
			albumId = request.form.get('albums')
			imgfile = request.files['photo']
		except:
			print "couldn't find all tokens" 
		return flask.render_template('upload.html', message="couldn't find all tokens")
		photo_data = base64.standard_b64encode(imgfile.read())
		photoController.uploadPhoto(albumId, caption, photo_data)
		return render_template('hello.html', name=flask_login.current_user.id, message="Photo uploaded!", photos=userController.getUsersPhotos(uid))
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		uid = userController.getUserIdFromEmail(flask_login.current_user.id)
		albums = albumController.getUserAlbum(uid)
		tags = tagController.showTags()
		return render_template('upload.html', albums=albums, tags=tags)   #TODO
#end photo uploading code 


#display the friend page
@app.route('/friend', methods=['GET'])
@flask_login.login_required
def view_users():
	uid = userController.getUserIdFromEmail(flask_login.current_user.id)
	users = userController.getPeopleYouMayKnow(uid)
	friends = userController.getFriends(uid)
	return render_template("friend.html", friends=friends, users=users)

#begin show users function, require login
@app.route('/friend', methods=['POST'])
@flask_login.login_required
def add_friend():
	uid = userController.getUserIdFromEmail(flask_login.current_user.id)
	friendId = request.form.get('users')    #may not work since have to select the current value
	userController.addFriend(uid, friendId)
	return render_template('hello.html', name=flask_login.current_user.id, message='Friend added')

#show album page, require login
@app.route('/album', methods=['GET'])
@flask_login.login_required
def view_albums():
	uid = userController.getUserIdFromEmail(flask_login.current_user.id)
	albums = albumController.getUserAlbumLimited(uid)
	return render_template('album.html', albums=albums)

#add another album to the user, require login
@app.route('/album', methods=['POST'])
@flask_login.login_required
def add_album():
	uid = userController.getUserIdFromEmail(flask_login.current_user.id)
	date = datetime.date.today()
	try:
		name = request.form.get('name')
	except:
		print "Please enter the name of the album"
		return flask.redirect(flask.url_for('add_album'))
	if albumController.addAlbum(name, uid, date):
		albums = albumController.getUserAlbumLimited(uid)
		return render_template('album.html', message='Album added', albums=albums)
	else:
		return render_template('album.html', message='Fail to add album')

#show photos in an album, require login
@app.route('/photo?action=show', methods=['POST'])	#cannot use get here
@flask_login.login_required
def show_photos():
	uid = userController.getUserIdFromEmail(flask_login.current_user.id)
	aid = request.form.get('albums')
	aname = albumController.getNameFromAlbumId(aid)
	photos = photoController.getPhotoFromAlbum(aid)
	return render_template('photo.html', photos=photos, aname=aname, aid=aid)	#jump to photo page

#view a photo, require login
@app.route('/managephoto/<pid>', methods=['POST'])	#cannot use get here
@flask_login.login_required
def manage_photo(pid):
	photo = photoController.getPhotoById(pid)	#id, caption, data
	ownder = photoController.getPhotoOwner(pid)
	tags = tagController.showPhotoTags(pid)
	comments = commentController.showComment(pid)
	return render_template('photo_manage.html', photo=photo, owner=owner, tags=tags, comments=comments)


#delete photos in an album, require login
@app.route('/photo?action=delete', methods=['POST'])	#cannot use get here
@flask_login.login_required
def delete_photo():
	print 'photo deleted'
	# pid = 
	# if photoController.deletePhoto(pid):
	# 	return 

#default page  
@app.route("/", methods=['GET'])
def hello():
	photos = photoController.getPhotos()
	return render_template('hello.html', message='Welecome to Photoshare', photos=photos)


if __name__ == "__main__":
	#this is invoked when in the shell  you run 
	#$ python app.py 
	app.run(port=5000, debug=True)
