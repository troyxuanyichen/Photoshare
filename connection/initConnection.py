import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
mysql = MySQL()
app = Flask(__name__)
app.config.from_object('config')
mysql.init_app(app)

def init_connection():
	conn = mysql.connect()
	return conn
