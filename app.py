from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import timedelta

app = Flask(__name__, template_folder='screens')
app.secret_key = os.urandom(24)  # Secret key for sessions and flash messages
    
# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database setup for adding the profile_pic column if it doesn't exist
def initialize_database():
    """Ensure the users table has a profile_pic column."""
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'profile_pic' not in columns:
        cursor.execute('ALTER TABLE users ADD COLUMN profile_pic TEXT')
    conn.commit()
    conn.close()

# Initialize the database on startup
initialize_database()

# Home route to display the welcome page
@app.route('/')
def home():
    return render_template('welcome.html')

# Register route to handle user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            conn = sqlite3.connect('database/users.db')
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
        remember = 'remember' in request.form

        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]

            if remember:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            else:
                session.permanent = False

            return redirect(url_for('dashboard'))  # Redirect directly to dashboard
        else:
            flash('Login failed. Please check your email and password.', 'error')

    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, profile_pic FROM users WHERE id = ?', (session['user_id'],))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            user = {'username': user_data[0], 'profile_pic': user_data[1]}
        else:
            user = {'username': session['username'], 'profile_pic': None}

        return render_template('dashboard.html', user=user)
    else:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))

# Account settings route
@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'user_id' not in session:
        flash('Please log in to access your account settings.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Handle profile picture upload
        profile_pic = request.files.get('profile_pic')
        profile_pic_filename = None

        if profile_pic and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            profile_pic_filename = os.path.join('uploads', filename).replace("\\", "/")  # Replace backslashes with forward slashes
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Update the user's information in the database
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()
        
        if password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            if profile_pic_filename:
                cursor.execute('UPDATE users SET username = ?, email = ?, password = ?, profile_pic = ? WHERE id = ?',
                               (username, email, hashed_password, profile_pic_filename, session['user_id']))
            else:
                cursor.execute('UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?',
                               (username, email, hashed_password, session['user_id']))
        else:
            if profile_pic_filename:
                cursor.execute('UPDATE users SET username = ?, email = ?, profile_pic = ? WHERE id = ?',
                               (username, email, profile_pic_filename, session['user_id']))
            else:
                cursor.execute('UPDATE users SET username = ?, email = ? WHERE id = ?',
                               (username, email, session['user_id']))

        conn.commit()
        conn.close()

        flash('Your account information has been updated successfully.', 'success')
        return redirect(url_for('account'))

    # Fetch the current user's information to prefill the form
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, email, profile_pic FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    conn.close()

    return render_template('account.html', user=user)


# Logout route to handle user logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/debug')
def debug():
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    print("Users data:", users)  # This will show user data including the profile_pic path in the console
    return "Check console for user data"

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

# Add Task

# Delete Task

# Edit Task

