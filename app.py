import os
import psycopg2
from flask import Flask, request, render_template, make_response
from flask_restful import Resource, Api
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api = Api(app)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db2',
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD')
                            )
    return conn

class Home(Resource):
    def get(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM emails;')
        emails = cur.fetchall()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', emails=emails),200,headers)
       

class Emails(Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('emails.html'),200,headers)

    def post(self):
        email = request.form['email']
        name = request.form['name']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO emails (emailID, name)'
                    'VALUES (%s, %s)',
                    (email, name))
        conn.commit()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('emails.html'),200,headers)

api.add_resource(Home, '/')
api.add_resource(Emails, '/emails/')

if __name__ == "__main__":
    app.run(debug=True)

    
'''   TASKS
decouple - HOLD(nginx?)
joins - 
foreign keys - 
nullible - 
uniqueness - 
flask restful - DONE
mypy pydocstyle flake8 - 
sqlalchemy alembic - 
'''

'''
POSTGRES:

Table 1: ID(Primary Key) Name(Owner) Email Phone_Number
Table 2: Car_name

'''