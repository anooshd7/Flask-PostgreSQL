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

# Users and Cars tables
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                 'emailID varchar (150) NOT NULL,'
                                 'name varchar (50) NOT NULL,'
                                 'phone varchar (12) NOT NULL);'
                                 )
cur.execute('CREATE TABLE cars (car_id serial PRIMARY KEY,'
            'id integer NOT NULL,'
            'cars varchar (50) NOT NULL,'
            'FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE );'
            )

# Junction table for many-many relationship
cur.execute('CREATE TABLE users_cars (user_id integer NOT NULL,'
            'car_id integer NOT NULL,'
            'FOREIGN KEY (car_id) REFERENCES cars(car_id) ON DELETE CASCADE,'
            'FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,'
            'PRIMARY KEY (user_id, car_id) );'
            )


# Triggers to delete user if all their cars are deleted
cur.execute('''
    CREATE OR REPLACE FUNCTION delete_user_if_no_cars()
    RETURNS TRIGGER AS
    $$
    BEGIN
      -- Check if the user has any remaining cars
      IF NOT EXISTS (
        SELECT 1 FROM cars WHERE id = OLD.id
      ) THEN
        -- Delete the user from the users table
        DELETE FROM users WHERE id = OLD.id;
      END IF;

      RETURN OLD;
    END;
    $$
    LANGUAGE plpgsql;
    ''')

cur.execute('''
    CREATE TRIGGER delete_user_trigger
    AFTER DELETE ON cars
    FOR EACH ROW
    EXECUTE FUNCTION delete_user_if_no_cars();
    ''')

conn.commit()
cur.close()
conn.close()