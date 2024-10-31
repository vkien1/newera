from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='screens') #setup the screens folder

@app.route('/login', methods=['GET', 'POST']) # Render the login screen
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')  # Render the register screen

@app.route('/')
def home():
    return render_template('welcome.html')  # Render the welcome screen

if __name__ == '__main__':
    app.run(debug=True)
