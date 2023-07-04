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

class ChangeCar(Resource):
    """Updates car based on ID and car name."""

    def get(self):
        """Get route."""
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('update.html'), 200, headers)

    def post(self):
        """Update the car based on ID and car name."""
        id = request.form['id']
        car = request.form['car']
        updated_car = request.form['updated_car']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT car_id FROM cars WHERE id = %s AND cars = %s', (id, car))
        car_id = cur.fetchone()
        if car_id:
            cur.execute('UPDATE cars SET cars = %s WHERE car_id = %s', (updated_car, car_id))
            conn.commit()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('update.html'), 200, headers)
