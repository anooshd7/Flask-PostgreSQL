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

class Display(Resource):
    """Displays cars owned by the user based on ID."""

    def get(self):
        """Get route."""
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('display.html', cars=[], id=None), 
                             200, headers)

    def post(self):
        """Fetch cars owned by the user based on ID."""
        id = request.form['id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT cars FROM cars WHERE id = %s', (id))
        cars = cur.fetchall()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template
                             ('display.html', cars=cars, id=id), 
                             200, headers)