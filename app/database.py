# Database interactions (SQLite)
import os
import sqlite3
import bcrypt
import datetime

# Determine the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the database path to be within the script's directory
DATABASE_PATH = os.path.join(script_dir, "finance_tracker.db")


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
    """Add a new transaction to the database and return its id."""
    sql = "INSERT INTO transactions(user_id, date, category, cost, details) VALUES (?, ?, ?, ?, ?)"
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, date, category, cost, details))
    transaction_id = c.lastrowid  # Get the id of the last inserted row
    conn.commit()
    conn.close()
    return transaction_id


def get_transactions_by_user(user_id):
    """Retrieve all transactions for a given user."""
    sql = "SELECT id, date, category, cost, details FROM transactions WHERE user_id = ?"
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id,))
    transactions = c.fetchall()
    conn.close()
    return transactions


def get_monthly_summary(user_id):
    """Retrieve monthly summary of expenses (excluding income) for a given user."""
    # Get current year and month
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    # Construct start and end dates of the current month
    start_date = f"{current_year}-{current_month:02d}-01"
    end_date = f"{current_year}-{current_month:02d}-31"  # Assuming all months have maximum 31 days

    # SQL query to retrieve transactions excluding income within the current month
    sql = """
    SELECT category, SUM(cost) AS total
    FROM transactions
    WHERE user_id = ? AND category != 'Income' AND date BETWEEN ? AND ?
    GROUP BY category
    """

    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, start_date, end_date))

    summary = {}
    for row in c.fetchall():
        category, total = row
        summary[category] = total

    conn.close()
    return summary


def get_last_month_summary(user_id):
    """Retrieve summary of expenses (excluding income) for a given user for the last month."""
    today = datetime.datetime.now()
    first_day_of_current_month = datetime.datetime(today.year, today.month, 1)
    last_day_of_last_month = first_day_of_current_month - datetime.timedelta(days=1)
    first_day_of_last_month = datetime.datetime(last_day_of_last_month.year, last_day_of_last_month.month, 1)

    # Format dates in 'YYYY-MM-DD' format
    start_date = first_day_of_last_month.strftime('%Y-%m-%d')
    end_date = last_day_of_last_month.strftime('%Y-%m-%d')

    # SQL query to retrieve transactions excluding income within the last month
    sql = """
    SELECT category, SUM(cost) AS total
    FROM transactions
    WHERE user_id = ? AND category != 'Income' AND date BETWEEN ? AND ?
    GROUP BY category
    """

    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, start_date, end_date))

    summary = {}
    for row in c.fetchall():
        category, total = row
        summary[category] = total

    conn.close()
    return summary


def get_this_month_income_summary(user_id):
    """Retrieve summary of expenses (excluding income) for a given user for the last month."""
    """Retrieve monthly summary of expenses (excluding income) for a given user."""
    # Get current year and month
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    # Construct start and end dates of the current month
    start_date = f"{current_year}-{current_month:02d}-01"
    end_date = f"{current_year}-{current_month:02d}-31"  # Assuming all months have maximum 31 days

    # SQL query to retrieve transactions excluding income within the last month
    sql = """
    SELECT category, SUM(cost) AS total
    FROM transactions
    WHERE user_id = ? AND category = 'Income' AND date BETWEEN ? AND ?
    GROUP BY category
    """

    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, start_date, end_date))

    summary = {}
    for row in c.fetchall():
        category, total = row
        summary[category] = total

    conn.close()
    return summary


def get_last_month_income_summary(user_id):
    """Retrieve summary of expenses (excluding income) for a given user for the last month."""
    today = datetime.datetime.now()
    first_day_of_current_month = datetime.datetime(today.year, today.month, 1)
    last_day_of_last_month = first_day_of_current_month - datetime.timedelta(days=1)
    first_day_of_last_month = datetime.datetime(last_day_of_last_month.year, last_day_of_last_month.month, 1)

    # Format dates in 'YYYY-MM-DD' format
    start_date = first_day_of_last_month.strftime('%Y-%m-%d')
    end_date = last_day_of_last_month.strftime('%Y-%m-%d')

    # SQL query to retrieve transactions excluding income within the last month
    sql = """
    SELECT category, SUM(cost) AS total
    FROM transactions
    WHERE user_id = ? AND category = 'Income' AND date BETWEEN ? AND ?
    GROUP BY category
    """

    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, start_date, end_date))

    summary = {}
    for row in c.fetchall():
        category, total = row
        summary[category] = total

    conn.close()
    return summary


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
    SELECT id, date, category, cost, details
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
        transaction_id, date, category, cost, details = row
        transactions.append({
            'id': transaction_id,
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


def edit_transaction(user_id, transaction_id, date, category, cost, details):
    """Edit an existing transaction in the database."""
    sql = """
    UPDATE transactions
    SET date = ?, category = ?, cost = ?, details = ?
    WHERE id = ? AND user_id = ?
    """
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (date, category, cost, details, transaction_id, user_id))
    conn.commit()
    conn.close()

def get_current_month_expense_total(user_id):
    """Retrieve the total expense for the current month (excluding income) for a given user."""
    # Get the first and last day of the current month
    today = datetime.datetime.now()
    first_day_of_this_month = datetime.datetime(today.year, today.month, 1)
    next_month = first_day_of_this_month + datetime.timedelta(days=31)  # Move to next month
    first_day_of_next_month = datetime.datetime(next_month.year, next_month.month, 1)
    last_day_of_this_month = first_day_of_next_month - datetime.timedelta(days=1)
    
    # Format dates in 'YYYY-MM-DD' format
    start_date = first_day_of_this_month.strftime('%Y-%m-%d')
    end_date = last_day_of_this_month.strftime('%Y-%m-%d')
    
    # SQL query to calculate the total expense for the current month, excluding income
    sql = """
    SELECT SUM(cost)
    FROM transactions
    WHERE user_id = ? AND category != 'Income' AND date BETWEEN ? AND ?
    """
    
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, start_date, end_date))
    
    # Fetch the result and handle the case where there are no expenses
    result = c.fetchone()
    total_expense = result[0] if result[0] is not None else 0
    
    conn.close()
    return total_expense

def get_last_month_expense_total(user_id):
    """Retrieve the total expense for the last month (excluding income) for a given user."""
    today = datetime.datetime.now()
    first_day_of_current_month = datetime.datetime(today.year, today.month, 1)
    last_day_of_last_month = first_day_of_current_month - datetime.timedelta(days=1)
    first_day_of_last_month = datetime.datetime(last_day_of_last_month.year, last_day_of_last_month.month, 1)
    
    # Format dates in 'YYYY-MM-DD' format
    start_date = first_day_of_last_month.strftime('%Y-%m-%d')
    end_date = last_day_of_last_month.strftime('%Y-%m-%d')
    
    # SQL query to calculate the total expense for the last month, excluding income
    sql = """
    SELECT SUM(cost)
    FROM transactions
    WHERE user_id = ? AND category != 'Income' AND date BETWEEN ? AND ?
    """
    
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, start_date, end_date))
    
    # Fetch the result and handle the case where there are no expenses
    result = c.fetchone()
    total_expense = result[0] if result[0] is not None else 0
    
    conn.close()
    return total_expense


def get_last_month_income_total(user_id):
    """Retrieve the total income for the last month (excluding expense) for a given user."""
    today = datetime.datetime.now()
    first_day_of_current_month = datetime.datetime(today.year, today.month, 1)
    last_day_of_last_month = first_day_of_current_month - datetime.timedelta(days=1)
    first_day_of_last_month = datetime.datetime(last_day_of_last_month.year, last_day_of_last_month.month, 1)

    # Format dates in 'YYYY-MM-DD' format
    start_date = first_day_of_last_month.strftime('%Y-%m-%d')
    end_date = last_day_of_last_month.strftime('%Y-%m-%d')

    # SQL query to calculate the total income for the last month, excluding expense
    sql = """
    SELECT SUM(cost)
    FROM transactions
    WHERE user_id = ? AND category = 'Income' AND date BETWEEN ? AND ?
    """

    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, start_date, end_date))

    # Fetch the result and handle the case where there are no income
    result = c.fetchone()
    total_income = result[0] if result[0] is not None else 0

    conn.close()
    return total_income


def get_current_month_income_total(user_id):
    """Retrieve the total income for the current month (excluding expense) for a given user."""
    # Get the first and last day of the current month
    today = datetime.datetime.now()
    first_day_of_this_month = datetime.datetime(today.year, today.month, 1)
    next_month = first_day_of_this_month + datetime.timedelta(days=31)  # Move to next month
    first_day_of_next_month = datetime.datetime(next_month.year, next_month.month, 1)
    last_day_of_this_month = first_day_of_next_month - datetime.timedelta(days=1)

    # Format dates in 'YYYY-MM-DD' format
    start_date = first_day_of_this_month.strftime('%Y-%m-%d')
    end_date = last_day_of_this_month.strftime('%Y-%m-%d')

    # SQL query to calculate the total income for the current month, excluding expense
    sql = """
    SELECT SUM(cost)
    FROM transactions
    WHERE user_id = ? AND category = 'Income' AND date BETWEEN ? AND ?
    """

    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (user_id, start_date, end_date))

    # Fetch the result and handle the case where there are no incomes
    result = c.fetchone()
    total_expense = result[0] if result[0] is not None else 0

    conn.close()
    return total_expense

def delete_transaction(transaction_id):
    """Delete a transaction from the database by its ID."""
    sql = "DELETE FROM transactions WHERE id = ?"
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, (transaction_id,))
    conn.commit()
    conn.close()

# Ensure the database and tables are created at initial run
setup_database()

if __name__ == "__main__":
    # Example Usage (Uncomment to test)
    add_user("user", "password")
    # print(verify_user("user", "password"))
    add_transaction(1, "2024-03-26", "Food", 15.50, "Lunch at Subway")
    add_transaction(1, "2024-03-26", "School", 1500.50, "UOFT")
    add_transaction(1, "2024-03-27", "House", 200.00, "Home supplies")
    add_transaction(1, "2024-03-28", "Entertainment", 50.00, "Movie tickets")
    add_transaction(1, "2024-03-29", "School", 25.00, "Textbook purchase")
    add_transaction(1, "2024-03-30", "Income", 5000.00, "Salary")
    add_transaction(1, "2024-03-31", "Car", 40.00, "Gas refill")
    add_transaction(1, "2024-04-01", "Other", 20.00, "Miscellaneous")
    add_transaction(1, "2024-04-02", "Food", 30.00, "Dinner at a restaurant")
    add_transaction(1, "2024-04-03", "Entertainment", 20.00, "Concert tickets")
    add_transaction(1, "2024-04-04", "House", 100.00, "Cleaning supplies")
    add_transaction(1, "2024-04-05", "Car", 50.00, "Car maintenance")
    add_transaction(1, "2024-04-30", "Income", 4500.00, "Salary")

    #print(get_recent_transactions(1))
    #print(get_last_month_income_summary(1))
    #print(get_this_month_income_summary(1))

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
