import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv 
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db2',
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD')
                            )
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM emails;')
    emails = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', emails=emails)

@app.route("/postemails/",methods=('GET','POST'))
def post_emails():
    if request.method == "POST":    
        email = request.form['email']
        name = request.form['name']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO emails (emailID, name)'
                    'VALUES (%s, %s)',
                    (email, name))
        conn.commit()
        cur.close()
        conn.close()
    
    return render_template('emails.html')

if __name__ == "__main__":
    app.run(debug=True)


