import sqlite3
import hashlib


def get_db_connection():
    """Creates a connection to the SQLite database."""
    return sqlite3.connect('users_database.db')


def init_db():
    """Initializes the database and creates the users table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       login
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       password
                       TEXT
                       NOT
                       NULL,
                       full_name
                       TEXT
                       NOT
                       NULL
                   )
                   ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")


def hash_password(password: str) -> str:
    """Hashes a password using the SHA-256 algorithm."""
    return hashlib.sha256(password.encode()).hexdigest()


def add_user():
    """Adds a new user to the database with a hashed password."""
    login = input("Enter login: ")
    password = input("Enter password: ")
    full_name = input("Enter full name: ")

    hashed_pw = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)",
            (login, hashed_pw, full_name)
        )
        conn.commit()
        print(f"User '{login}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: User with login '{login}' already exists.")
    finally:
        conn.close()


def update_password():
    """Updates the password for an existing user."""
    login = input("Enter login to change password: ")
    new_password = input("Enter new password: ")

    hashed_pw = hash_password(new_password)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE login = ?", (hashed_pw, login))

    if cursor.rowcount > 0:
        conn.commit()
        print("Password updated successfully.")
    else:
        print("Error: User not found.")
    conn.close()


def authenticate_user():
    """Authenticates a user by checking login and hashed password."""
    login = input("Authentication required. Enter login: ")
    password = input("Enter password: ")

    hashed_pw = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT full_name FROM users WHERE login = ? AND password = ?",
        (login, hashed_pw)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"Login successful! Welcome, {user[0]}.")
        return True
    else:
        print("Error: Invalid login or password.")
        return False


def main():
    """Main application loop."""
    init_db()
    while True:
        print("\n--- User Management System ---")
        print("1. Add new user")
        print("2. Update user password")
        print("3. Authenticate user")
        print("4. Exit")

        choice = input("Select an option (1-4): ")

        if choice == '1':
            add_user()
        elif choice == '2':
            update_password()
        elif choice == '3':
            authenticate_user()
        elif choice == '4':
            print("Exiting application.")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()