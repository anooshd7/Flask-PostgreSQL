from flask_restful import Resource
from flask import render_template, make_response, request

from postgres_connection import get_db_connection

class SignUp(Resource):
    """Get route."""

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'), 200, headers)

    def post(self):
        """Sign Up."""
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        car = request.form['car']
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert the user into the users table and get the assigned user ID
        cur.execute('INSERT INTO users (emailID, name, phone) VALUES (%s,%s,%s) RETURNING id;',
                    (email, name, phone))
        user_id = cur.fetchone()[0]

        # Insert the car into the cars table
        cur.execute('INSERT INTO cars (id, cars) VALUES (%s,%s)', (user_id, car))

        # Insert the relationship into the junction table (users_cars)
        cur.execute('INSERT INTO users_cars (user_id, car_id)'
                    ' VALUES (%s, (SELECT car_id FROM cars WHERE id = %s AND cars = %s))',
                    (user_id, user_id, car))

        conn.commit()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html', id=user_id), 200, headers)
