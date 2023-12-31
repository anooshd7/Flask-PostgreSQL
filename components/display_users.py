from flask_restful import Resource
from flask import request, render_template, make_response

from postgres_connection import get_db_connection

class DisplayUsers(Resource):
    """Displays cars owned by the user based on ID."""

    def get(self):
        """Get route."""
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('display_users.html', cars=[], id=None), 200, headers)

    def post(self):
        """Fetch cars owned by the user based on ID."""
        car_id = request.form['car_id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT users.name' 
                    ' FROM users'
                    ' INNER JOIN users_cars ON users.id = users_cars.user_id'
                    ' WHERE users_cars.car_id = %s;',
                    (car_id))
        users = cur.fetchall()
        cur.close()
        conn.close()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('display_users.html', users=users, car_id=car_id), 200, headers)

