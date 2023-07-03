from flask_restful import Resource
from flask import request, render_template, make_response
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

class Add(Resource):
    """Email Class in flask-restful."""

    def get(self):
        """Get route."""
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('add.html'), 200, headers)

    def post(self):
        """Post route."""
        input_id = request.form['id']
        car = request.form['car']

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the provided ID exists in the users table
        cur.execute('SELECT id FROM users WHERE id = %s', (input_id))
        row = cur.fetchone()
        if row:
            # ID exists
            cur.execute('INSERT INTO cars (id, cars) VALUES (%s, %s)',
                        (input_id, car))
            conn.commit()

        cur.close()
        conn.close()

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('add.html',row=row), 200, headers)