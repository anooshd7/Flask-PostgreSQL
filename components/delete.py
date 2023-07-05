from flask_restful import Resource
from flask import request, render_template, make_response

from postgres_connection import get_db_connection

class RemoveCar(Resource):
    def get(self):
        """Get route."""
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('deletecar.html'), 200, headers)

    def post(self):
        id = request.form['id']
        car = request.form['car']
        conn = get_db_connection()
        cur = conn.cursor()

        # Get car ID
        cur.execute('SELECT car_id FROM cars WHERE id = %s AND cars = %s',
                    (id, car))
        deleted_car_id = cur.fetchone()
        
        # Delete the car from the junction table (users_cars)
        cur.execute('DELETE FROM users_cars WHERE car_id = %s', (deleted_car_id[0],))

        # Delete the car from the cars table
        cur.execute('DELETE FROM cars WHERE car_id = %s', (deleted_car_id[0],))
        conn.commit()

        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('deletecar.html'), 200, headers)
