import getpass
import os
import re
import string
import secrets
import bcrypt

passwords = {}

# Function to set up the master password
def setup_master_password():
    if not os.path.exists('master_password.txt'):
        master_password = getpass.getpass("Create a master password: ")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(master_password.encode(), salt)

        with open('master_password.txt', 'wb') as file:
            file.write(hashed_password)
    else:
        print("Master password already set up.")

# Function to verify the master password
def verify_master_password():
    if os.path.exists('master_password.txt'):
        with open('master_password.txt', 'rb') as file:
            stored_hashed_password = file.read()

        entered_password = getpass.getpass("Enter the master password: ")
        return bcrypt.checkpw(entered_password.encode(), stored_hashed_password)
    else:
        return True

# Function to add new password
def add_password():
    service = input("Enter the name of the service or website: ")

    while True:
        print("1. Enter your own password")
        print("2. Generate a random password")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            password = getpass.getpass("Enter the password: ")

            if is_strong_password(password):
                passwords[service] = password
                print(f"Password for {service} added successfully.")
                save_passwords()
                break
            else:
                print("Password is weak. It should meet the criteria for a strong password.")
                print("- At least 8 characters long")
                print("- Contains at least one uppercase letter")
                print("- Contains at least one lowercase letter")
                print("- Contains at least one digit")
                print("- Contains at least one special character (e.g., !@#$%^&*()_+{}[]:;<>,.?~\\-)")
        elif choice == 2:
            password = generate_random_password()
            passwords[service] = password
            print(f"Randomly generated password for {service}: {password}")
            break
        else:
            print("Invalid choice. Please try again.")

# Function to retrieve password
def get_password():
    service = input("Enter the name of the service or website: ")
    if service in passwords:
        print(f"Password for {service}: {passwords[service]}")
    else:
        print(f"No password found for {service}.")

# Function to list passwords
def list_passwords():
    print("Stored Passwords:")
    for service, password in passwords.items():
        print(f"{service}: {password}")

def save_passwords():
    try:
        home_directory = os.path.expanduser("~")
        file_path = os.path.join(home_directory, 'passwords.txt')
        with open(file_path, 'w') as file:
            for service, password in passwords.items():
                file.write(f"{service}:{password}\n")
        print("Passwords saved successfully.")
    except Exception as e:
        print(f"Error saving passwords: {e}")

def load_passwords():
    try:
        home_directory = os.path.expanduser("~")
        file_path = os.path.join(home_directory, 'passwords.txt')
        with open(file_path, 'r') as file:
            for line in file:
                service, password = line.strip().split(':')
                passwords[service] = password
        print("Passwords loaded successfully.")
    except FileNotFoundError:
        print("No saved passwords found.")
    except Exception as e:
        print(f"Error loading passwords: {e}")

def is_strong_password(password):
    # Define criteria
    min_length = 8
    max_length = 16
    has_uppercase = re.search(r'[A-Z]', password)
    has_lowercase = re.search(r'[a-z]', password)
    has_digit = re.search(r'\d', password)
    has_special_char = re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\-]', password)

    # Check criteria
    if (min_length <= len(password) <= max_length and
        has_uppercase and has_lowercase and
        has_digit and has_special_char):
        return True
    return False

def generate_random_password(length = 8):
    # Define characters for generating the password
    characters = string.ascii_letters + string.digits + string.punctuation

    while True:
        # Generate a random password of the specified length
        password = ''.join(secrets.choice(characters) for _ in range(length))

        # Check if the generated password meets the minimum criteria
        if is_strong_password(password):
            return password

# Main program loop
def main():

    if not os.path.exists('master_password.txt'):
        setup_master_password()

    if verify_master_password():
        load_passwords()

        while True:
            print("Welcome to py-password-manager!")
            print("1. Add Password")
            print("2. Get Password")
            print("3. List Passwords")
            print("4. Generate Random Password")
            print("5. Quit")

            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_password()
            elif choice == 2:
                get_password()
            elif choice == 3:
                list_passwords()
            elif choice == 4:
                length = int(input("Enter the length of the random password (minimum 8): "))
                password = generate_random_password(length)
                print(f"Generated random password: {password}")
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid master password. Access denied.")

if __name__ == "__main__":
    main()
