from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = '12345'  # Required for session management

# MySQL database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='25041982',
            database='juit'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = get_db_connection()
        if connection is None:
            flash('Database connection failed. Please try again later.')
            return redirect('/login')
        
        cursor = connection.cursor()
        
        # Check if the email exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        
        if user is None:
            flash('Email is not registered.')
            return redirect('/login')
        
        # Proceed to check the password
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]  # Store user ID in session
            return redirect('/')
        else:
            flash('Invalid email or password.')
            return redirect('/login')
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
