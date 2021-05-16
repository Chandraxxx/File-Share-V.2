from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from flask_mysqldb import MySQL

import os, pdfkit

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

app = Flask(__name__)

# Config MySQL db
app.config['MYSQL_USER'] = 'sql3412162'
app.config['MYSQL_PASSWORD'] = 'tJqUW9xh7h'
app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql3412162'
mysql = MySQL(app)

# Config for PDF
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
app.config['PDF_FOLDER'] = os.path.realpath('.') + '/static/report'


# Manage Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Manage Session
app.secret_key = "1q2w3e4r5t"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=15)

# Manage Upload File
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/static/file'



#home
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
                        cur = mysql.connection.cursor()
                        username = request.form['uname']
                        password = request.form['pw']

                        #validasi
                        tmp = cur.execute("SELECT id FROM user WHERE username = '%s'" %username)

                        if tmp == 0 :
                                return render_template('login.html', msg = 'True')

                        cur.execute("SELECT username,password,code_level,id FROM user WHERE username = '%s'" %username)
                        result = cur.fetchone()

                        if username == result[0]:
                                #username exists on database
                                if password == result[1]:
                                        #all validation passed
                                        session['uname'] = username
                                        session['level'] = result[2]
                                        session['id'] = result[3]
                                        #change status
                                        cur.execute("UPDATE user set code_active = '%s' WHERE id ='%s'" %('ON', result[3]))

                                        mysql.connection.commit()

                                        return redirect(url_for('index'))
                                else:
                                        return render_template('login.html', msg2 = 'True')
                        else:
                                return render_template('login.html', msg = 'True')
                        #end
                        
                        
                else:
                        return render_template('login.html', msg = 'False', msg2 = 'False')



#manage USER

##add_user/ Done
@app.route('/add_user', methods=['GET', 'POST'])
def addUser():
        # member cant access
        if 'level' in session:
                _level = session['level']
                if _level == 'M':
                        return redirect(url_for('index'))
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
        # member cant access
        if 'level' in session:
                _level = session['level']
                if _level == 'M':
                        return redirect(url_for('index'))
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
        # member cant access
        if 'level' in session:
                _level = session['level']
                if _level == 'M':
                        return redirect(url_for('index'))
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
                else:
                        return render_template('manage_user/edit_user.html', data = result)
        else:
                return redirect(url_for('login'))
##end edit

#end

#download
@app.route('/list_download/downloadfile/<paths>')
def downloadFile(paths):
        if "uname" in session:
                path = app.config['UPLOAD_FOLDER'] + '/' + secure_filename(paths)

                return send_file(path, as_attachment=True)
        else:
                return redirect(url_for('login'))
#

#downloadlistPage
@app.route('/list_download')
def listDownload():
        if "uname" in session:
                s = request.args.get('s')
                cur = mysql.connection.cursor()

                if s is None:
                        headingtable = 'List Download'
                        # Search bar empty
                        cur.execute("SELECT * FROM file")
                        container = []
                        for id, name_file, code_type, size_file, date_file, path_file in cur.fetchall():
                                round(12.3456, 2)
                                container.append((id, name_file, code_type, round(size_file / 1024 / 1024, 3), date_file, path_file))
                        return render_template('list_download.html', container = container, headingTable = headingtable, failed = "False")
                else:
                        #exists
                        headingtable = 'Search Result'
                        key = request.args.get('s')
                        key = '%'+key+'%'
                        cur.execute("SELECT * FROM file where name_file LIKE '%s'" %key)
                        #check if file exists
                        tmp = cur.execute("SELECT * FROM file where name_file LIKE '%s'" %key)
                        if tmp == 0:
                                return render_template('list_download.html', failed="True")
                        #end
                        container = []
                        for id, name_file, code_type, size_file, date_file, path_file in cur.fetchall():
                                round(12.3456, 2)
                                container.append((id, name_file, code_type, round(size_file / 1024 / 1024, 3), date_file, path_file))
                        return render_template('list_download.html', container = container, headingTable = headingtable, failed = 'False')
        else:
                return redirect(url_for('login'))

#end

#manage File

                ##add File
@app.route('/add_file', methods = ['GET', 'POST'])
def addFile():
        # member cant access
        if 'level' in session:
                _level = session['level']
                if _level == 'M':
                        return redirect(url_for('index'))
        if 'uname' in session:
                cur = mysql.connection.cursor()

                if request.method == "POST":
                        f = request.files['file']
                        t = request.files['file']

                        filename = app.config['UPLOAD_FOLDER'] + '/' + secure_filename(f.filename)
                        tmp = app.config['UPLOAD_FOLDER'] + '/' + secure_filename(t.filename)

                        try:
                                temp = f.filename # Real name
                                #split name with extension
                                name_file,b=temp.split('.')

# ALLOWED_EXTENSIONS 

                                if b == 'jpg' or b == 'png' or b == 'jpeg' :
                                        code_type='IMG'
                                elif b == 'mp3' :
                                        code_type="MSC"
                                elif b == 'mp4' or b == 'mov' or b == 'wmv' or b== 'avi' or b == 'mkv' :
                                        code_type='VID'
                                elif b == 'pdf' or b == 'doc' or b == 'txt' or b== 'docx':
                                        code_type='DOC'

                                f.save(filename)
                                # Get File size / bytes
                                # ref: https://stackoverflow.com/questions/15772975/flask-get-the-size-of-request-files-object
                                f.seek(9,os.SEEK_END)
                                size_file = f.tell()

# app.config['MAX_CONTENT_LENGTH'] 100 megabytes

                                if size_file > 100* 1024 * 1024 :
                                        #Files too big
                                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],tmp))
                                        return render_template('manage_file/add_file.html' , failed2 = "True")

                                #check if table already has data
                                isRowExist=cur.execute('''SELECT (id) FROM file''')
                                if isRowExist == 0:
                                        id = 1
                                elif isRowExist > 0:
                                        max_id = cur.execute("SELECT MAX(id) as maximum from file")
                                        max_id = cur.fetchone()
                                        id = int(''.join(map(str, max_id))) + 1
                                
                                date_file = datetime.now()
                                path_file = t.filename

                                # insert into table file
                                cur.execute("INSERT INTO file (id, name_file, code_type, size_file, date_file, path_file) VALUES (%s,%s,%s,%s,%s,%s)",(id, name_file, code_type, size_file,date_file, path_file))
                                mysql.connection.commit()

                                return render_template('manage_file/add_file.html',  success = "True")
                        except Exception as e:
                                # if filename already exists auto failed
                                return render_template('manage_file/add_file.html',  failed = "True")
                else:
                        #GET Method
                        return render_template('manage_file/add_file.html',  success = "False" , failed = 'False', Failed2 = 'False' )
        else:
                return redirect(url_for('login'))
                ## end

                ## del File
@app.route('/del_file/<id>')
def delFile(id):
        # member cant access
        if 'level' in session:
                _level = session['level']
                if _level == 'M':
                        return redirect(url_for('index'))
        if 'uname' in session:
                cur = mysql.connection.cursor()
                _id = id
                #take filename
                
                cur.execute("SELECT path_file FROM file WHERE id  = '%s'" %_id)
                fname = cur.fetchone()
                path  = app.config['UPLOAD_FOLDER'] + '/' + secure_filename(fname[0])
                # remove file from folder
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], path))

                # return str (path)

                cur.execute("DELETE FROM file where id = '%s' " %_id)
                mysql.connection.commit()

                return redirect(url_for('listDownload'))
        else:
                return redirect(url_for('login'))
                ## end del

#end

#list report
@app.route('/manage_report/list_report')
def listReport():
        if 'level' in session:
                _level = session['level']
                if _level == 'M':
                        return redirect(url_for('index'))
        if 'uname' in session:
                cur = mysql.connection.cursor()
                if request.args.get('s') is None:
                        titlehead = "Report List"
                        cur.execute("SELECT * FROM report")
                        container = []
                        for id, name_report, username, date_report in cur.fetchall():
                                container.append((id, name_report, username, date_report))
                        return render_template('/manage_report/list_report.html', title = titlehead, container = container, failed = 'False')
                else:
                        key = request.args.get('s')
                        key = '%' + key + '%'
                        cur.execute("SELECT * FROM report WHERE name_report like '%s'" %key)
                        tmp = cur.execute("SELECT * FROM report WHERE name_report like '%s'" %key)
                        if tmp == 0:
                                return render_template('/manage_report/list_report.html' ,title = 'Search Result', failed = 'True')
                        container = []
                        for id, name_report, username, date_report in cur.fetchall():
                                container.append((id, name_report, username, date_report))
                        return render_template('/manage_report/list_report.html', title = 'Search Result',failed = 'False', container = container)
#end


#pdfReader
@app.route('/manage_report/list_report/pdf_reader')
def pdfReader():
        if 'level' in session:
                _level = session['level']
                if _level == 'M':
                        return redirect(url_for('index'))
        if 'uname' in session:
                reportName = request.args.get('r_name')
                return render_template('manage_report/pdf_reader.html', path = reportName)
#end


#convert to pdf
@app.route('/convert')
def convert():
        if 'uname' in session:
                madeBy = session['uname']
                createdTime = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        cur = mysql.connection.cursor()
        tmp = cur.execute("SELECT id from report")

        cur.execute("SELECT * FROM user")
        container = []
        for id,name_user, username, password, code_level, date_user, code_active in cur.fetchall():
                container.append((id, name_user, username, password, code_level, date_user, code_active))

        reportFile = render_template('manage_report/report_template.html', container = container, madeBy = madeBy, createdTime = createdTime, total = tmp )
        if cur.execute("SELECT id from report") == 0 :
                _id = 1
        elif cur.execute("SELECT id from report") >= 1:
                cur.execute("SELECT MAX(id) as maximum FROM report")
                max_id = cur.fetchone()
                _id = int(''.join(map(str, max_id))) + 1
        
        date = datetime.now().date()
        name_report = "Report list user %s '%s' by %s.pdf"%(_id, date, madeBy)

        pdfFile = app.config['PDF_FOLDER'] + "/Report list user %s '%s' by %s.pdf"%(_id, date, madeBy)
        options = {'enable-local-file-access' : None}
        pdfkit.from_string(reportFile, pdfFile, configuration = config, options = options)
        #add to db
        cur.execute("INSERT INTO report (id, name_report, username, date_report) VALUES (%s,%s,%s,%s) ", (_id, name_report, madeBy, datetime.now()) )
        mysql.connection.commit()

        return redirect(url_for('listUser'))

#end

#userlistPage
@app.route('/list_user')
def listUser():
        # member cant access
        if 'level' in session:
                _level = session['level']
                if _level == 'M':
                        return redirect(url_for('index'))
        cur = mysql.connection.cursor()
        if "uname" in session:
                s = request.args.get('s')
                if s is None: 
                        headtitle = 'List User'
                        #means search bar not filled
                        cur.execute("SELECT * FROM user")
                        container = []
                        for id, name_user, username, password, code_level, date_user, code_active in cur.fetchall():
                                container.append((id, name_user, username, password, code_level, date_user, code_active))

                        return render_template('list_user.html' , container = container, title = headtitle, failed = 'False')
                else:
                        headtitle = 'Search Result'
                        #ada isi disearchbar
                        keySearch = request.args.get('s')
                        keySearch = '%' + keySearch + '%'
                        # Key search berdasarkan name
                        cur.execute("SELECT * FROM user WHERE name_user LIKE '%s'" %keySearch)
                        #jika nama user tidak ada
                        tmp = cur.execute("SELECT * FROM user WHERE name_user LIKE '%s'" %keySearch)
                        if tmp == 0:
                                return render_template('list_user.html', failed = 'True')
                        #end if
                        container = []
                        for id, name_user, username, password, code_level, date_user, code_active in cur.fetchall():
                                container.append((id, name_user, username, password, code_level, date_user, code_active))
                                
                        return render_template('list_user.html' , container = container, title = headtitle, failed = 'False')
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
        
        # change status to off
        cur = mysql.connection.cursor()
        if 'id' in session:
                _id = session['id']
        cur.execute ("UPDATE user SET code_active = '%s' Where id = '%s'" %('OFF', _id))
        mysql.connection.commit()
        #remove session
        session.pop('uname', None)
        session.pop('level', None)
        session.pop('id', None)

        return redirect(url_for("login"))

if __name__=='__main__':
        app.run(debug=True)
