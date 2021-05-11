from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os, pdfkit

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

app = Flask(__name__)
# Manage Session
app.secret_key = "1q2w3e4r5t"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)


@app.route('/')
def index():
	#just a simple greeting time
	curTime = datetime.now()
	curTime.hour
	if curTime.hour<12:
		greet = "Morning"
	elif 12 <= curTime.hour<18:
		greet = "Afternoon"
	else:
		greet = "Evening"
	#end
	return render_template('home.html', greet = greet)

# login
@app.route('/login')
def login():
	return "Kat"

#downloadlistPage
@app.route('/list_download')
def listDownload():
	return render_template('list_download.html')

#userlistPage
@app.route('/list_user')
def listUser():
	return render_template('list_user.html')

# helpCentrePage
@app.route('/help_centre')
def helpCentre():
	return render_template('help_centre.html')

# logout
@app.route('/logout')
def logOut():
	return "Cyka Blyat"

if __name__=='__main__':
	app.run(debug=True)
