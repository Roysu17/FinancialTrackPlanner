# Database interactions (SQLite)
import sqlite3
import bcrypt

DATABASE_PATH = "finance_tracker.db"  # Adjust as necessary

def create_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def setup_database():
    """Create the database tables if they do not already exist."""
    users_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    """

    transactions_table_sql = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        cost REAL NOT NULL,
        details TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """
    conn = create_connection()
    c = conn.cursor()
    c.execute(users_table_sql)
    c.execute(transactions_table_sql)
    conn.commit()
    conn.close()

def add_user(username, password):
    """Add a new user with a hashed password to the database."""
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    sql = "INSERT INTO users(username, password_hash) VALUES (?, ?)"
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (username, password_hash))
    conn.commit()
    conn.close()

def verify_user(username, password):
    """Verify a user's login credentials."""
    sql = "SELECT password_hash FROM users WHERE username = ?"
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (username,))
    user = c.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    return False

def add_transaction(user_id, date, category, cost, details):
    """Add a new transaction to the database."""
    sql = "INSERT INTO transactions(user_id, date, category, cost, details) VALUES (?, ?, ?, ?, ?)"
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, date, category, cost, details))
    conn.commit()
    conn.close()

def get_transactions_by_user(user_id):
    """Retrieve all transactions for a given user."""
    sql = "SELECT date, category, cost, details FROM transactions WHERE user_id = ?"
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id,))
    transactions = c.fetchall()
    conn.close()
    return transactions

def get_account_summary(user_id):
    """Retrieve account summary for a given user."""
    sql = """
    SELECT category, SUM(cost) AS total
    FROM transactions
    WHERE user_id = ?
    GROUP BY category
    """
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id,))
    summary = {}
    for row in c.fetchall():
        category, total = row
        summary[category] = total
    conn.close()
    return summary

def get_recent_transactions(user_id, limit=10):
    """Retrieve recent transactions for a given user."""
    sql = """
    SELECT date, category, cost, details
    FROM transactions
    WHERE user_id = ?
    ORDER BY date DESC
    LIMIT ?
    """
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, limit))
    transactions = []
    for row in c.fetchall():
        date, category, cost, details = row
        transactions.append({
            'date': date,
            'category': category,
            'cost': cost,
            'details': details
        })
    conn.close()
    return transactions

def get_user_id(username):
    """Retrieve the user ID based on the username."""
    sql = "SELECT id FROM users WHERE username = ?"
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return user[0]  # Return the user ID
    else:
        return None  # Return None if the user does not exist


# Ensure the database and tables are created at initial run
setup_database()

if __name__ == "__main__":
    #Example Usage (Uncomment to test)
    add_user("1", "1")
    #print(verify_user("user", "password"))
    add_transaction(1, "2024-03-26", "FOOD", 15.50, "Lunch at Subway")
    add_transaction(1, "2024-03-26", "SCHOOL", 1500.50, "UOFT")
    add_transaction(1, "2024-03-27", "House", 200.00, "Home supplies")
    add_transaction(1, "2024-03-28", "Entertainment", 50.00, "Movie tickets")
    add_transaction(1, "2024-03-29", "School", 25.00, "Textbook purchase")
    add_transaction(1, "2024-03-30", "Income", 1000.00, "Salary")
    add_transaction(1, "2024-03-31", "Car", 40.00, "Gas refill")
    add_transaction(1, "2024-04-01", "Other", 20.00, "Miscellaneous")
    add_transaction(1, "2024-04-02", "Food", 30.00, "Dinner at a restaurant")
    add_transaction(1, "2024-04-03", "Entertainment", 20.00, "Concert tickets")
    add_transaction(1, "2024-04-04", "House", 100.00, "Cleaning supplies")
    add_transaction(1, "2024-04-05", "Car", 50.00, "Car maintenance")

    print(get_recent_transactions(1))
    


"""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL -- In a real app, this should be a hashed password
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT NOT NULL, -- ISO8601 dates ('YYYY-MM-DD HH:MM:SS.SSS')
    category TEXT NOT NULL,
    cost REAL NOT NULL,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""