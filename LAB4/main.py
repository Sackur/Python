import sqlite3
import hashlib
import pytest
import sys


# --- Основна логіка (Логіка Лаби 3) ---
def get_db_connection():
    return sqlite3.connect('users_database.db')


def init_db():
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


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(login, password):
    """Verifies user credentials by comparing hashes."""
    hashed_pw = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM users WHERE login = ? AND password = ?", (login, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def add_user(login, password, full_name):
    hashed_pw = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)",
            (login, hashed_pw, full_name)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# --- Інтерактивне меню (з Лаба 3) ---
def interactive_menu():
    init_db()
    while True:
        print("\n--- Lab 3: User Management System ---")
        print("1. Add new user")
        print("2. Update user password")
        print("3. Authenticate (Login)")
        print("4. Back to Main Selection")
        choice = input("Select an option (1-4): ")

        if choice == '1':
            l = input("Enter login: ")
            p = input("Enter password: ")
            f = input("Enter full name: ")
            if add_user(l, p, f):
                print(f"User '{l}' added successfully!")
            else:
                print("Error: Login already exists.")

        elif choice == '2':
            l = input("Enter login to update: ")
            p = input("Enter new password: ")
            if update_password(l, p):
                print("Password updated!")
            else:
                print("User not found.")

        elif choice == '3':
            l = input("Login: ")
            p = input("Password: ")
            name = authenticate_user(l, p)
            if name:
                print(f"Success! Welcome, {name}.")
            else:
                print("Invalid login or password.")

        elif choice == '4':
            break


# --- Автоматична перевірка (з Лаба 4) ---
def run_lab4_tests():
    print("\n--- Lab 4: Running Automated Tests and Coverage Report ---")
    # Запускаємо pytest прямо з коду з генерацією звіту
    pytest.main(["LAB4.py", "--cov=main", "--cov-report", "html"])
    print("\n[Done] Tests completed. Check 'htmlcov/index.html' for report.")


# --- ГОЛОВНИЙ ВИБІР ПРИ ЗАПУСКУ ---
if __name__ == "__main__":
    while True:
        print("\n==============================")
        print("   MAIN SELECTION MENU")
        print("==============================")
        print("1.  Update Database (Interactive)")
        print("2.  Data Verification (Automated Tests)")
        print("3. Exit Program")

        main_choice = input("\nYour choice (1-3): ")

        if main_choice == '1':
            interactive_menu()
        elif main_choice == '2':
            run_lab4_tests()
        elif main_choice == '3':
            print("Exiting application...")
            sys.exit()
        else:
            print("Invalid choice, please try again.")