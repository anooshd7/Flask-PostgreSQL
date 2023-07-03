"""Imports."""
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from components.home import Home
from components.add import Add
from components.display import Display
from components.delete import Delete
from components.update import Update

load_dotenv()

app = Flask(__name__)
api = Api(app)

# Routing
api.add_resource(Home, '/')
api.add_resource(Add, '/add/')
api.add_resource(Display, '/display/')
api.add_resource(Delete, '/delete/')
api.add_resource(Update, '/update/')

if __name__ == "__main__":
    app.run(debug=True)



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
Different joins
Each class in its own file - DONE

'''
