from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask_mysqldb import MySQL

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
# Config MySQL db
app.config['MYSQL_USER'] = 'sql3412162'
app.config['MYSQL_PASSWORD'] = 'tJqUW9xh7h'
app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql3412162'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def index():
        if "uname" in session:
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
        else:
                return redirect(url_for('login'))
        return render_template('home.html', greet = greet)

# login
@app.route('/login', methods = ['GET','POST'])
def login():
        if "uname" in session:
                return redirect(url_for('index'))
        else:
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
        if "uname" in session:
                return render_template('list_download.html')
        else:
                return redirect(url_for('login'))

#manage USER

##add_user
@app.route('/add_user', methods=['GET', 'POST'])
def addUser():
        if "uname" in session:
                if request.method == 'POST':
                        name = request.form['name']
                        username = request.form['uname']
                        password =request.form['pw']
                        level = request.form['level']
                        date = datetime.now()
                        active = "OFF"
                        return "Sementara"
                #End if
                return render_template('add_user.html')
        else:
                return redirect(url_for('login'))
##end

#end

#userlistPage
@app.route('/list_user')
def listUser():
        if "uname" in session:
                return render_template('list_user.html')
        else:
                return redirect(url_for('login'))
# helpCentrePage
@app.route('/help_centre',methods=['GET','POST'])
def helpCentre():
        if "uname" in session:
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
        else:
                return redirect(url_for('login'))
        return render_template('help_centre.html', failed = "False", success = "False")

# logout
@app.route('/logou t')
def logOut():
        session.pop('uname', None)
        return redirect(url_for("login"))

if __name__=='__main__':
	app.run(debug=True)
