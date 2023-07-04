"""Imports."""
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from components.home import SignUp
from components.add import AddCar
from components.display import DisplayCars
from components.delete import RemoveCar
from components.update import ChangeCar
from components.display_users import DisplayUsers

load_dotenv()

app = Flask(__name__)
api = Api(app)

# Routing
api.add_resource(SignUp, '/')
api.add_resource(AddCar, '/cars/add')
api.add_resource(DisplayCars, '/cars/display')
api.add_resource(RemoveCar, '/cars/remove')
api.add_resource(ChangeCar, '/cars/change')
api.add_resource(DisplayUsers, '/users/display')

if __name__ == "__main__":
    app.run(debug=True)
    
'''
In a typical SQL query, the order of operations is as follows:

FROM: The query starts by specifying the table or tables from which to retrieve the data. This is done using the FROM clause.

JOIN: If any joins are specified in the query, they are applied next. Joins are used to combine rows from different tables based on a specific condition. In the given query, the INNER JOIN operation is used to connect the "cars" and "users" tables based on the matching condition.

WHERE: The WHERE clause is used to filter the rows based on certain conditions. It specifies any additional criteria that must be met for a row to be included in the result set. In the given query, the WHERE clause filters the results based on the "id" column in the "users" table.

SELECT: Finally, the SELECT clause is used to specify the columns that will be included in the result set. It determines the data that will be returned by the query.

'''

'''
            TASKS
decouple - 
joins - DONE
foreign keys - DONE
nullible - DONE
uniqueness - DONE
flask restful - DONE
mypy()    pydocstyle(DONE)    flake8(DONE)
sqlalchemy alembic -

One to many (One user has many cars)- DONE
List all cars owned by a user - DONE
Each class in its own file - DONE

change routes
many to many relationship
Joins

'''
