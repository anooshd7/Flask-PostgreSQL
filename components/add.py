from flask_restful import Resource
from flask import request, render_template, make_response

from postgres_connection import get_db_connection


class AddCar(Resource):
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
        cur.execute('INSERT INTO cars (id, cars) VALUES (%s, %s)',
                        (input_id, car))
        conn.commit()

        # Insert the relationship into the junction table
        cur.execute('INSERT INTO users_cars (user_id, car_id) VALUES (%s, (SELECT car_id FROM cars WHERE id = %s AND cars = %s))',
                        (input_id, input_id,car))
        conn.commit()

        cur.close()
        conn.close()

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('add.html'), 200, headers)
