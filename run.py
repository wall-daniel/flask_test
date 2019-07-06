from flask import Flask
from flask import request
import sqlite3 as sql
app = Flask(__name__)

list = ['hello', 'world', 'running', 'test']

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test():
	return 'Test'

@app.route('/enternew/<name>')
def new_student(name):
    return "Creating a new student of name: %s" % name

@app.route('/addrec', methods = ['GET', 'POST'])
def addrec():
    if request.method == 'POST':
        try:
            #print(request)
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            pin = request.form['pin']

            print("here")
            with sql.connect("/home/dwall/Programming/flask_test/database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)", (name,address,city,pin))

                con.commit()

            msg = "Record successffully added"
        except Exception as e:
            #con.rollback()
            print(e)
            msg = "error in insert operation"
        finally:
            #con.close()
            return msg
    else:
        with sql.connect("/home/dwall/Programming/flask_test/database.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from students")
            rows = cur.fetchall()

            list = ""
            print(rows)
            for row in rows:
                for item in row:
                    list += str(item) + ","
                list += "\n"

            return list

@app.route('/user/<user>', methods=['GET', 'POST'])
def user_test(user):
    if request.method == 'GET':
	    return 'User %s %s' % (list[int(user)], request.path)
    else:
        list.append(user)
        return 'User %s %s' % (user, request.path)
