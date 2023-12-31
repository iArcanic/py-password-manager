import getpass
import os
import re
import string
import secrets
import bcrypt
import pyperclip
from cryptography.fernet import Fernet
import json

passwords = {}

# Function to set up the master password
def setup_master_password():
    if not os.path.exists('master_password.txt'):
        master_password = getpass.getpass("Create a master password: ")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(master_password.encode(), salt)

        home_directory = os.path.expanduser("~")
        file_path = os.path.join(home_directory, "master_password.txt")

        with open(file_path, 'wb') as file:
            file.write(hashed_password)
    else:
        print("Master password already set up.")

# Function to verify the master password
def verify_master_password():

    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, "master_password.txt")

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            stored_hashed_password = file.read()

        entered_password = getpass.getpass("Enter the master password: ")
        return bcrypt.checkpw(entered_password.encode(), stored_hashed_password)
    else:
        return True

# Function to generate encryption key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt password
def encrypt_password(password, key):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

# Function to decrypt password
def decrypt_password(encrypted_password, key):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

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
                key = generate_key()
                encrypted_password = encrypt_password(password, key)
                passwords[service] = (key, encrypted_password)
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
            key = generate_key()
            encrypted_password = encrypt_password(password, key)
            passwords[service] = (key, encrypted_password)
            print(f"Randomly generated password for {service}: {password}")
            save_passwords()
            break
        else:
            print("Invalid choice. Please try again.")

# Function to retrieve password
def get_password():
    service = input("Enter the name of the service or website: ")
    if service in passwords:
        key, encrypted_password = passwords[service]
        decrypted_password = decrypt_password(encrypted_password, key)
        print(f"Password for {service}: {decrypted_password}")
    else:
        print(f"No password found for {service}.")

# Function to list passwords
def list_passwords():
    print("Stored Passwords:")
    for service, (key, encrypted_password) in passwords.items():
        decrypted_password = decrypt_password(encrypted_password, key)
        print(f"{service}: {decrypted_password}")

def save_passwords():
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, 'passwords.txt')

    try:
        with open(file_path, 'w') as file:
            for service, (key, encrypted_password) in passwords.items():
                file.write(f"{service}:{key.decode()}:{encrypted_password.decode()}\n")
        print("Passwords saved successfully.")

    except Exception as e:
        print(f"Error saving passwords: {e}")

def load_passwords():
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, 'passwords.txt')

    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 3:
                    service, key, encrypted_password = parts
                    passwords[service] = (key.encode(), encrypted_password.encode())
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

def copy_password_to_clipboard():
    service = input("Enter the name of the service or website: ")

    if service in passwords:
        password = passwords[service]
        pyperclip.copy(password)
        print(f"Password for {service} copied to clipboard.")
    else:
        print(f"No password found for {service}.")

# Main program loop
def main():

    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, "master_password.txt")

    if not os.path.exists(file_path):
        setup_master_password()

    if verify_master_password():
        load_passwords()

        while True:
            print("Welcome to py-password-manager!")
            print("1. Add Password")
            print("2. Get Password")
            print("3. List Passwords")
            print("4. Generate Random Password")
            print("5. Copy Password to Clipboard")
            print("6. Quit")

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
                copy_password_to_clipboard()
            elif choice == 6:
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid master password. Access denied.")

if __name__ == "__main__":
    main()
