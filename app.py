from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import os, pdfkit

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

app = Flask(__name__)
# Manage Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
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
@app.route('/login', methods = ['GET','POST'])
def login():
        if request.method == "POST":
                username = request.form['uname']
                password = request.form['pw']
                session['uname'] = username
                return redirect(url_for('index'))
        else:
                return render_template('login.html')

#downloadlistPage
@app.route('/list_download')
def listDownload():
	return render_template('list_download.html')

#userlistPage
@app.route('/list_user')
def listUser():
	return render_template('list_user.html')

# helpCentrePage
@app.route('/help_centre',methods=['GET','POST'])
def helpCentre():
        if request.method == "POST":
                g_username = request.form['gmail_username']
                g_password = request.form['gmail_pw']
                to = request.form['to']
                subject = request.form['subject']
                message = request.form['message']

                app.config['MAIL_USERNAME'] = g_username
                app.config['MAIL_PASSWORD'] = g_password

                msg = Message(subject, sender=g_username, recipients=[to])
                msg.body = message

                try:
                        mail = Mail(app)
                        mail.connect()
                        mail.send(msg)
                        return render_template('help_centre.html', success = "True")
                except:
                        return render_template('help_centre.html', failed = "True")
        return render_template('help_centre.html', failed = "False", success = "False")

# logout
@app.route('/logout')
def logOut():
        session.pop('uname', None)
        return redirect(url_for("login"))

if __name__=='__main__':
	app.run(debug=True)
