import sqlite3

# Create the database and tables if they don't exist
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create uploads/analysis table
    c.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_rows INTEGER,
            num_products INTEGER,
            num_states INTEGER,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')

    # Insert initial admin credentials if not already in the database
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if c.fetchone() is None:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'MCA2024'))

    conn.commit()
    conn.close()

# Function to check if the user exists in the database (for login)
def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()

# Function to log analysis results
def log_analysis(username, total_rows, num_products, num_states):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO analysis_results (username, total_rows, num_products, num_states)
        VALUES (?, ?, ?, ?)
    ''', (username, total_rows, num_products, num_states))
    conn.commit()
    conn.close()

# Create the database when running the app
create_db()