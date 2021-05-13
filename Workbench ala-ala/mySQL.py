from flask import Flask, render_template
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'sql3412162'
app.config['MYSQL_PASSWORD'] = 'tJqUW9xh7h'
app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql3412162'


mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    

    cur.execute('''drop table user''')
    cur.execute('''drop table file''')
    cur.execute("DROP TABLE level")
    cur.execute("DROP TABLE type")
    cur.execute("DROP TABLE active")

#tabel LEVEL User 
    cur.execute('''CREATE TABLE level (code_level VARCHAR(1) PRIMARY KEY, name_level VARCHAR(10))''')
    cur.execute('''INSERT INTO level VALUES('M', 'Member')''')
    cur.execute('''INSERT INTO level VALUES('A', 'Admin')''')
    mysql.connection.commit()
#end

#table active/not 
    cur.execute('''create table active (code_active varchar (5) primary key, name_active varchar(10))''')
    cur.execute('''insert into active values('ON', 'Online')''')
    cur.execute('''insert into active values('OFF', 'Offline')''')
    mysql.connection.commit()
#end    

#tabel Type File 
    cur.execute('''CREATE TABLE type (code_type VARCHAR(5) PRIMARY KEY, name_type VARCHAR(15))''')
    cur.execute('''INSERT INTO type VALUES('VID','Video')''')
    cur.execute('''INSERT INTO type VALUES('IMG','Image')''')
    cur.execute('''INSERT INTO type VALUES('MSC','Music')''')
    cur.execute('''INSERT INTO type VALUES('DOC','Documents')''')
    mysql.connection.commit()
#end
    
#tabel user    
    cur.execute('''CREATE TABLE user(id int primary key not null, name_user varchar(30), username varchar(30) unique, password varchar(40) ,code_level varchar(1), date_user DATE, code_active varchar(5), FOREIGN KEY (code_level) references level(code_level), Foreign key (code_active) references active(code_active))''')
#end

#tabel Files
    cur.execute('''create table file (id integer primary key not null auto_increment, name_file varchar(100) unique, code_type varchar(5), size_file integer, date_file DATE, FOREIGN KEY (code_type) REFERENCES type (code_type))''')
#end


    





# Memberikan satu akun admin
    date = datetime.now()
    cur.execute("INSERT INTO user VALUES(1, 'Admin', 'admin', 'admin', 'A', '2020-02-20', 'OFF')")
    mysql.connection.commit()
    
    return "Good"

if __name__ == "__main__":
        app.run(debug=True)

# Cara mengambil data    
    #cur.execute('''select * from level''')
    #container = []
    #for code_level, name_level in cur.fetchall():
    #    container.append((code_level, name_level))
    #return render_template('test.html', container = container)
#end

