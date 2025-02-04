from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = '12345'  # Required for flashing messages

# MySQL database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='25041982',
            database='juit'
        )
        create_users_table(connection)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create users table if it doesn't exist
def create_users_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password INT NOT NULL
            )
        ''')
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    connection = get_db_connection()
    if connection is None:
        flash('Database connection failed. Please try again later.')
        return redirect('/')
    
    try:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s, %d)', (name, email, password))
        connection.commit()
    except mysql.connector.Error as err:
        flash(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        connection.close()
    
    return redirect('/')