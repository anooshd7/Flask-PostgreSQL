import os
import psycopg2
from dotenv import load_dotenv 
load_dotenv()

conn = psycopg2.connect(
        host="localhost",
        database="flask_db2",
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
        )

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS emails;')
cur.execute('CREATE TABLE emails (id serial PRIMARY KEY,'
                                 'emailID varchar (150) NOT NULL,'
                                 'name varchar (50) NOT NULL,'
                                 'phone varchar (12) NOT NULL);'
                                 )
cur.execute('CREATE TABLE cars (car_id serial PRIMARY KEY,'
            'id integer NOT NULL,'
            'cars varchar (50) NOT NULL,'
            'FOREIGN KEY (id) REFERENCES emails(id) );'
            )

# id_val = 1
# car_val = "Honda"

# # Execute the INSERT query
# cur.execute("INSERT INTO cars (id, cars) VALUES (%s, %s);", (id_val, car_val))

conn.commit()

cur.close()
conn.close()