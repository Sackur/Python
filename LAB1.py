import hashlib
from typing import List, Dict, Any


# TASK 1: Text Processing (Робота з текстом)
def analyze_text(text: str) -> Dict[str, int]:
    """
    Function receives a string as input and returns a dictionary where keys are
    unique words and values are their counts. It also creates and prints a list
    of words that appear more than 3 times.
    """
    # 1. Cleaning and tokenizing the text
    cleaned_text = ''.join(c.lower() if c.isalnum() or c.isspace() else ' ' for c in text)
    words = [word for word in cleaned_text.split() if word]

    # 2. Counting word frequency (for the primary return dictionary)
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # 3. Creating the list of words that appear more than 3 times
    frequent_words_list = [word for word, count in word_counts.items() if count > 3]

    # 4. Displaying the required list
    print("--- Result of Task 1 ---")
    print(f"List of words appearing > 3 times: {frequent_words_list}")

    # 5. Returning the full word count dictionary
    return word_counts


# TASK 2: Product Inventory (Інвентаризація продуктів)
inventory: Dict[str, int] = {}  # Initialize empty inventory


def manage_inventory(product_name: str, quantity: int):
    """
    Updates the quantity of a product in the inventory based on addition or removal.
    """
    product_name = product_name.lower().strip()

    if product_name not in inventory:
        if quantity > 0:
            inventory[product_name] = quantity
            print(f"Added '{product_name}'. Quantity: {quantity}.")
        else:
            print(f"Product '{product_name}' not found and cannot be removed.")
    else:
        new_quantity = inventory[product_name] + quantity

        if new_quantity >= 0:
            inventory[product_name] = new_quantity
            print(f"Updated: '{product_name}'. New quantity: {new_quantity}.")

            if new_quantity == 0:
                del inventory[product_name]
                print(f"Warning! Product '{product_name}' removed from stock (quantity is 0).")

        else:
            print(
                f"Error: Not enough '{product_name}' to remove {abs(quantity)}. Available: {inventory[product_name]}.")


def get_low_stock_products() -> List[str]:
    """
    Creates and returns a list of product names where the quantity is less than 5.
    """
    return [name for name, count in inventory.items() if count < 5]


# TASK 3: Sales Statistics (Статистика продажів)
SalesList = List[Dict[str, Any]]


def analyze_sales(sales: SalesList) -> Dict[str, float]:
    """
    Calculates total revenue for each product and returns a dictionary
    of all product revenues. It also creates and prints a list of products
    that generated revenue greater than 1000.
    """
    product_revenue: Dict[str, float] = {}

    for sale in sales:
        try:
            quantity = float(sale.get("quantity", 0))
            price = float(sale.get("price", 0))
            product = sale.get("product", "Unknown product")

            revenue = quantity * price
            product_revenue[product] = product_revenue.get(product, 0.0) + revenue

        except ValueError as e:
            print(f"Data error in sale: {e}")
            continue

    profitable_products_list = [
        name
        for name, revenue in product_revenue.items()
        if revenue > 1000
    ]

    print("--- Result of Task 3 ---")
    print(f"List of products with total revenue > 1000: {profitable_products_list}")

    return product_revenue


# TASK 4: Task Management System (Система управління задачами)

tasks: Dict[str, str] = {}  # Initialize empty task list


def manage_tasks(task_name: str, action: str, new_status: str = None):
    """
    Functions for adding, deleting, and changing the status of tasks.
    Actions: 'add', 'delete', 'change status'.
    Statuses: 'done', 'in progress', 'pending'.
    """
    task_name = task_name.strip()
    action = action.lower()
    valid_statuses = {"done", "in progress", "pending"}

    if action == 'add':
        if task_name not in tasks:
            tasks[task_name] = "pending"  # New task defaults to 'pending' (pending)
            print(f"Task '{task_name}' successfully added with status 'pending'.")
        else:
            print(f"Task '{task_name}' already exists.")

    elif action == 'delete':
        if task_name in tasks:
            del tasks[task_name]
            print(f"Task '{task_name}' successfully removed.")
        else:
            print(f"Task '{task_name}' not found.")

    elif action == 'change status':
        if task_name in tasks:
            if new_status and new_status.lower() in valid_statuses:
                tasks[task_name] = new_status.lower()
                print(f"Status of task '{task_name}' changed to '{new_status.lower()}'.")
            else:
                print(f"Invalid status '{new_status}'. Allowed statuses: {', '.join(valid_statuses)}.")
        else:
            print(f"Task '{task_name}' not found.")

    else:
        print(f"Unknown action: '{action}'.")


def get_pending_tasks() -> List[str]:
    """
    Creates and returns a list of task names that have the status 'pending'.
    """
    # Returns a list of task NAMES
    return [name for name, status in tasks.items() if status == "pending"]


# TASK 5: User Authentication (Аутентифікація користувачів)
users: Dict[str, tuple] = {}  # Initialize empty user list


def hash_password(password: str) -> str:
    """Hashes the password using hashlib.md5() as implied by the task."""
    return hashlib.md5(password.encode()).hexdigest()


def register_user(login: str, password: str, full_name: str):
    """
    Creates a dictionary entry storing login, hashed password, and full name.
    """
    if login in users:
        print(f"User with login '{login}' already exists.")
        return

    hashed_password = hash_password(password)
    users[login] = (hashed_password, full_name)
    print(f"User '{login}' successfully registered. Password hash: {hashed_password}")


def check_password(login: str) -> bool:
    """
    Checks the user's password; the password is read from the console using input().
    """
    if login not in users:
        print(f"User with login '{login}' not found.")
        return False

    # Reading the password from the console
    password_input = input(f"Enter password for user '{login}': ").strip()

    # Hashing the input password and comparing
    hashed_input = hash_password(password_input)
    stored_hash = users[login][0]

    if hashed_input == stored_hash:
        print(f"Authentication successful! Welcome, {users[login][1]}.")
        return True
    else:
        print("Incorrect password.")
        return False


# DEMONSTRATION with User Input
if __name__ == "__main__":

    print("\n" + "=" * 10 + " START OF DEMONSTRATION (USER INPUT REQUIRED) " + "=" * 10)

    # DEMO 1: Text Processing
    print("\n--- 1. Text Processing (Task 1) ---")
    text_input = input("Enter text for analysis: \n").strip()
    # The function prints the required list itself
    full_counts = analyze_text(text_input)
    print(f"Full word count dictionary (function return value): {full_counts}")

    # DEMO 2: Product Inventory
    print("\n--- 2. Product Inventory (Task 2) ---")
    print("Current inventory:", inventory)
    while True:
        prod_name = input("Enter product name to modify (or 'done'): ").strip()
        if prod_name.lower() == 'done': break
        try:
            qty = int(input(f"Enter quantity to add/remove (e.g., 10 or -5): "))
            manage_inventory(prod_name, qty)
        except ValueError:
            print("Quantity must be an integer.")

    print("Final inventory:", inventory)
    low_stock = get_low_stock_products()
    print(f"List of low-stock products (< 5): {low_stock}")

    # DEMO 3: Sales Statistics
    print("\n--- 3. Sales Statistics (Task 3) ---")
    sales_data: List[Dict[str, Any]] = []
    print("\n--- Enter Sales Data (Enter 'done' to finish) ---")
    while True:
        product = input("Enter product name ('product') or 'done': ").strip()
        if product.lower() == 'done': break
        try:
            quantity = float(input(f"Enter quantity (quantity) for {product}: "))
            price = float(input(f"Enter unit price (price) for {product}: "))
            sales_data.append({"product": product, "quantity": quantity, "price": price})
        except ValueError:
            print("Invalid input for quantity or price.")

    if sales_data:
        # The function prints the required list itself
        all_revenue = analyze_sales(sales_data)
        print(f"Full revenue dictionary (function return value): {all_revenue}")
    else:
        print("No sales data entered.")

    # DEMO 4: Task Management System

    print("\n--- 4. Task Management System (Task 4) ---")
    print("Current tasks:", tasks)

    while True:
        task_action = input("Enter action ('add', 'delete', 'change status', or 'done'): ").strip().lower()
        if task_action == 'done': break

        task_name = input("Enter task name: ").strip()
        new_status = None

        if task_action == 'змінити_статус':
            new_status = input("Enter new status ('done', 'in progress', 'pending'): ").strip()

        manage_tasks(task_name, task_action, new_status)

    print("Final tasks:", tasks)
    pending_list = get_pending_tasks()
    print(f"List of tasks with status 'pending' (pending): {pending_list}")


    # DEMO 5: User Authentication
    print("\n--- 5. User Authentication (Task 5) ---")

    # Registration
    print("\n--- Register New User ---")
    reg_login = input("Enter login for registration: ").strip()
    reg_pass = input(f"Enter password for {reg_login}: ").strip()
    reg_fullname = input(f"Enter full name (MNS) for {reg_login}: ").strip()
    register_user(reg_login, reg_pass, reg_fullname)

    # Authentication
    print("\n--- Check Authentication (Password Required) ---")
    auth_login = input("Enter login for authentication: ").strip()
    check_password(auth_login)

    print("\n" + "=" * 10 + " DEMONSTRATION FINISHED " + "=" * 10)