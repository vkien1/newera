import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table with a profile_pic column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        profile_pic TEXT  -- This column will store the path to the profile picture
    )
''')

# Create the tasks table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        due_date DATE,
        send_alert BOOLEAN DEFAULT FALSE,
        priority INT,
        status TEXT,
        CONSTRAINT fk_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)           
    )
''')

# Create the categories table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories
        id INTEGER PRIMARY KEY AUTOINCREMENT
        task_id INTEGER NOT NULL
        name TEXT
        CONSTRAINT fk_task
            FOREIGN KEY (task_id)
            REFERENCES tasks(id)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
