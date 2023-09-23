import getpass
import os
import re

passwords = {}

# Function to add new password
def add_password():
    service = input("Enter the name of the service or website: ")
    
    while True:
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

# Main program loop
def main():

    # Load the existing passwords at the start
    load_passwords()

    while True:
        print("Welcome to py-password-manager!")
        print("1. Add Password")
        print("2. Get Password")
        print("3. List Passwords")
        print("4. Quit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_password()
        elif choice == 2:
            get_password()
        elif choice == 3:
            list_passwords()
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
