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
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO emails (emailID, name)'
            'VALUES (%s, %s)',
            ('a@yahoo.com','Bob')
            )

conn.commit()

cur.close()
conn.close()