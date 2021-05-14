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
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=15)
# Config MySQL db
app.config['MYSQL_USER'] = 'sql3412162'
app.config['MYSQL_PASSWORD'] = 'tJqUW9xh7h'
app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql3412162'

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

##add_user/ Done
@app.route('/add_user', methods=['GET', 'POST'])
def addUser():
        if "uname" in session:
                cur = mysql.connection.cursor()
                if request.method == 'POST':
                        isRowExist = cur.execute('''SELECT (id) FROM user''')

                        if isRowExist == 0:
                                no = 1
                        elif isRowExist > 0:
                                cur.execute("SELECT MAX(id) as maximum from user")
                                max_id= cur.fetchone()
                                no = int(''.join(map(str, max_id))) + 1
                        id = no
                        name = request.form['name']
                        username = request.form['uname']
                        #Check if username already exist
                        isUsernameExist = cur.execute("SELECT (id) from user where username = '%s'" %username) #0 means no username inside table
                        if isUsernameExist > 0:
                                # theres id inside table
                                return render_template('manage_user/add_user.html', failed = 'True')
                        password = request.form['pw']
                        level = request.form['level']
                        date = datetime.now()
                        active = "OFF"
                        # Insert user
                        cur.execute('''INSERT INTO user (id, name_user, username, password, code_level, date_user, code_active) VALUES (%s,%s,%s,%s,%s,%s,%s)''', (id, name, username, password, level, date, active))
                        mysql.connection.commit()
                        # Tool debuging
                        return render_template('manage_user/add_user.html', success = "True")
                #End if
                return render_template('manage_user/add_user.html', success = "False", failed = 'False')
        else:
                return redirect(url_for('login'))
##end add

## delete_user
@app.route('/del_user/<id>')
def delUser(id):
        if'uname' in session:
                #get id form url
                idUser = id
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM user WHERE id ='%s'" %(idUser))
                mysql.connection.commit()
                return redirect(url_for('listUser'))
        else:
                return redirect(url_for('login'))
## end del

##edit_user
@app.route('/list_user/edit_user/<id>', methods = ['GET','POST'])
def editUser(id):
        if 'uname' in session:
                cur = mysql.connection.cursor()
                idUser = id
                cur.execute("SELECT * FROM user where id = '%s'" %idUser)
                result = cur.fetchone()
                # return str(result)
                if request.method == "POST":
                        id = request.form['id']
                        name = request.form['name']
                        username = request.form['uname']
                        password = request.form['pw']
                        level = request.form['level']
                        cur.execute("UPDATE user SET name_user = '%s', username = '%s', password = '%s', code_level = '%s' WHERE id = '%s' " % (name, username, password, level, id))
                        mysql.connection.commit()
                        return redirect(url_for('listUser'))
                else:#array [3] itu password
                        return render_template('manage_user/edit_user.html', data = result)
        else:
                return redirect(url_for('login'))
##end edit

#end

#manage File

#end

#userlistPage
@app.route('/list_user')
def listUser():
        cur = mysql.connection.cursor()
        if "uname" in session:
                s = request.args.get('s')
                if s is None: 
                        #means search bar not filled
                        cur.execute("SELECT * FROM user")
                        container = []
                        for id, name_user, username, password, code_level, date_user, code_active in cur.fetchall():
                                container.append((id, name_user, username, password, code_level, date_user, code_active))

                        return render_template('list_user.html' , container = container)
                else:
                        #ada isi disearchbar
                        keySearch = request.args.get('s')
                        # Key search berdasarkan name
                        cur.execute("SELECT * FROM user WHERE name_user = '%s'" %keySearch)
                        container = []
                        for id, name_user, username, password, code_level, date_user, code_active in cur.fetchall():
                                container.append((id, name_user, username, password, code_level, date_user, code_active))
                                
                        return render_template('list_user.html' , container = container)
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
@app.route('/logout')
def logOut():
        session.pop('uname', None)
        return redirect(url_for("login"))

if __name__=='__main__':
	app.run(debug=True)
