"""Imports."""
import os
import psycopg2
from flask import Flask, request, render_template, make_response
from flask_restful import Resource, Api
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api = Api(app)


def get_db_connection():
    """Get postgres connection."""
    conn = psycopg2.connect(host='localhost',
                            database='flask_db2',
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD')
                            )
    return conn


class Home(Resource):
    """Home Class in flask-restful."""

    def get(self):
        """Get route."""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM emails;')
        emails = cur.fetchall()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('index.html', emails=emails), 200, headers)


class Emails(Resource):
    """Email Class in flask-restful."""

    def get(self):
        """Get route."""
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('emails.html'), 200, headers)

    def post(self):
        """Post route."""
        email = request.form['email']
        name = request.form['name']
        phone = request.form['phone']
        car = request.form['car']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO emails (emailID, name, phone)'
                    'VALUES (%s, %s, %s) RETURNING id',
                    (email, name, phone))
        id = cur.fetchone()[0]
        cur.execute('INSERT INTO cars (id, cars) VALUES (%s,%s)', (id, car))
        conn.commit()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('emails.html'), 200, headers)


class Display(Resource):
    """Displays email on entering name and car."""

    def get(self):
        """Get route."""
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('display.html', emails=[]), 200, headers
            )

    def post(self):
        """Update the email value."""
        name = request.form['name']
        car = request.form['car']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT emails.emailID'
                    ' FROM emails JOIN cars ON emails.id = cars.id'
                    ' WHERE cars.cars = %s AND emails.name = %s;',
                    (car, name))
        emails = cur.fetchall()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('display.html', emails=emails), 200, headers
            )


api.add_resource(Home, '/')
api.add_resource(Emails, '/emails/')
api.add_resource(Display, '/display/')

if __name__ == "__main__":
    app.run(debug=True)

'''
TASKS
decouple - HOLD(nginx?)
joins -
foreign keys -
nullible -
uniqueness -
flask restful - DONE
mypy(HOLD)    pydocstyle(DONE)    flake8(DONE)
sqlalchemy alembic -
'''
