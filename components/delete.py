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

class Delete(Resource):
    """Displays email on entering name and car."""

    def get(self):
        """Get route."""
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('deletecar.html'), 200, headers
            )

    def post(self):
        """Update the email value."""
        id = request.form['id']
        car = request.form['car']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT car_id FROM cars WHERE id = %s AND cars = %s',
                    (id, car))
        deleted_car_id = cur.fetchone()
        if deleted_car_id:
            cur.execute('DELETE FROM cars WHERE car_id = %s',(deleted_car_id))
            conn.commit()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('deletecar.html'), 200, headers
            )