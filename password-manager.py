import getpass

passwords = {}

# Function to add new password
def add_password():
    service = input("Enter the name of the service or website: ")
    password = getpass.getpass("Enter the password: ")
    passwords[service] = password
    print(f"Password for {service} added successfully.")

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

# Main program loop
def main():
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
