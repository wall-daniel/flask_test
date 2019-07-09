from flask import Flask
from flask import request
import sqlite3 as sql
import os as os
import json

database_path = os.getcwd() + "/database.db"

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
    print(database_path)
    if request.method == 'POST':
        data = request.json
        data["mhmm"] = 1
        return(str(data))
        try:
            #print(request)
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            pin = request.form['pin']

            print("here")
            with sql.connect(database_path) as con:
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
        data = request.get_json()

        if data == None:
            with sql.connect(database_path) as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute('PRAGMA table_info(students);')

                rows = cur.fetchall()

                schema = []

                i = 0
                for row in rows:
                    type = {}
                    type['type'] = row['type'].lower()
                    type['text'] = row['name']
                    type['id'] = 0
                    schema.append(type)

                return json.dumps(schema)
        else:
            data["mhm"] = 2
            return str(data)

@app.route('/user/<user>', methods=['GET', 'POST'])
def user_test(user):
    if request.method == 'GET':
	    return 'User %s %s' % (list[int(user)], request.path)
    else:
        list.append(user)
        return 'User %s %s' % (user, request.path)
