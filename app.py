from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from datetime import timedelta

app = Flask(__name__, template_folder='screens')
app.secret_key = os.urandom(24)  # Secret key for sessions and flash messages

# Home route to display the welcome page
@app.route('/')
def home():
    return render_template('welcome.html')  # Show welcome screen as the initial page

# Register route to handle user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Use the correct hash method

        try:
            conn = sqlite3.connect('database/users.db')  # Updated path
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                           (username, email, hashed_password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists. Please use a different one.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

# Login route to handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form  # Check if 'Remember Me' is checked

        conn = sqlite3.connect('database/users.db')  # Updated path
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        # Check if user exists and password matches
        if user and check_password_hash(user[3], password):  # user[3] is the hashed password
            session['user_id'] = user[0]       # Store user ID in session
            session['username'] = user[1]      # Store username in session
            flash('Login successful!', 'success')
            
            # Set session lifetime based on 'Remember Me' checkbox
            if remember:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)  # Cookie lasts for 30 days
            else:
                session.permanent = False
            
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        else:
            flash('Login failed. Please check your email and password.', 'error')

    return render_template('login.html')

# To configure how long the user stays login for 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Dashboard route to display the dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')  # User is logged in, show dashboard
    else:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))

# Logout route to handle user logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)      # Clear the user ID from session
    session.pop('username', None)     # Clear the username from session
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))  # Redirect to the welcome page after logout

if __name__ == '__main__':
    app.run(debug=True)
