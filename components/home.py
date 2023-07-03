from flask_restful import Resource
from flask import render_template, make_response, request
import psycopg2
import os

def get_db_connection():
    """Get postgres connection."""
    conn = psycopg2.connect(host='localhost',
                            database='flask_db2',
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD')
                            )
    return conn

class Home(Resource):
    """Get route."""
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'), 200, headers)

    def post(self):
        """ Sign Up."""
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        car = request.form['car']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (emailID, name, phone) VALUES (%s,%s,%s) RETURNING id;',
                    (email, name, phone))
        id = cur.fetchone()[0]
        cur.execute('INSERT INTO cars (id, cars) VALUES (%s,%s)', 
                    (id, car))
        conn.commit()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('home.html',id=id), 200, headers)
