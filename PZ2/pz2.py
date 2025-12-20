import hashlib


class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        # Store password as a SHA-256 hash
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.is_active = is_active

    def verify_password(self, password):
        # Compare provided password hash with stored hash
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()


class Administrator(User):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password)
        self.permissions = permissions or ["all_access"]


class RegularUser(User):
    def __init__(self, username, password, last_login="Never"):
        super().__init__(username, password)
        self.last_login = last_login


class GuestUser(User):
    def __init__(self, username):
        # Guests have an empty password hash
        super().__init__(username, "")
        self.limited_access = True


class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        if user.username in self.users:
            return False
        self.users[user.username] = user
        return True

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.verify_password(password):
            return user
        return None


def main():
    system = AccessControl()

    while True:
        print("\n--- User Management System ---")
        print("1. Register (Regular User)")
        print("2. Register (Admin)")
        print("3. Enter as Guest")
        print("4. Login")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice in ["1", "2"]:
            uname = input("Enter username: ")
            pword = input("Enter password: ")
            new_user = RegularUser(uname, pword) if choice == "1" else Administrator(uname, pword)

            if system.add_user(new_user):
                print(f"User {uname} registered!")
            else:
                print("Username exists.")

        elif choice == "3":
            uname = "Guest_" + str(len(system.users) + 1)
            guest = GuestUser(uname)
            system.add_user(guest)
            print(f"\nWelcome, {guest.username}!")
            print(f"Role: Guest (Limited Access)")

        elif choice == "4":
            uname = input("Username: ")
            pword = input("Password: ")
            user = system.authenticate_user(uname, pword)
            if user:
                print(f"\nWelcome, {user.username}! Role: {type(user).__name__}")
            else:
                print("\nInvalid credentials.")

        elif choice == "5":
            break


if __name__ == "__main__":
    main()