from flask_restful import Resource
from flask import request, render_template, make_response

from postgres_connection import get_db_connection

class DisplayCars(Resource):
    """Displays cars owned by the user based on ID."""

    def get(self):
        """Get route."""
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('display.html', cars=[], id=None), 200, headers)

    def post(self):
        """Fetch cars owned by the user based on ID."""
        id = request.form['id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT cars.cars'
                    ' FROM cars'
                    ' INNER JOIN users ON users.id = cars.id WHERE users.id = %s',
                    (id))
        cars = cur.fetchall()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('display.html', cars=cars, id=id), 200, headers)
