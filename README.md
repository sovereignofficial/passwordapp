

# Password Manager

A simple password manager application built using Python and Tkinter.

## Overview

The Password Manager is a secure application that allows users to store and manage their passwords for different platforms. It provides features such as generating strong passwords, saving passwords securely, searching for saved passwords, editing and deleting existing passwords, and copying passwords to the clipboard.

## Features

- Generate strong passwords: The application can generate random, strong passwords using a combination of symbols, numbers, lowercase letters, and uppercase letters.
- Save passwords securely: Passwords are encrypted using a secure key before storing them in the database, ensuring that they remain protected.
- Search passwords: Users can search for saved passwords by platform or username, making it easy to find specific entries.
- Edit and delete passwords: Users can edit or delete existing passwords from the database, allowing for easy management of password entries.
- Copy passwords to the clipboard: Users can copy passwords to the clipboard with a single click, making it convenient to paste them into login forms.
- User authentication: The application requires authentication using a secure key to perform sensitive actions such as editing or deleting passwords.

## Requirements

- Python 3.x
- Tkinter (Python GUI library)
- pyperclip (Python library for clipboard operations)
- cryptography

## Usage

1. Install the required dependencies by running the following command:
   ```
   pip install tkinter pyperclip cryptography
   ```

2. Clone the repository to your local machine:
   ```
   git clone https://github.com/your-username/password-manager.git
   ```

3. Run the application:
   ```
   cd passwordapp
   python main.py
   ```

4. Use the application to manage your passwords:
   - Click the "Generate Password" button to generate a strong password.
   - Enter the platform, username, password, and secure key.
   - Click the "Save Password" button to save the password securely.
   - Use the search bar to search for saved passwords.
   - Select a password entry from the table to edit, delete, or copy the password.

## Contributions

Contributions to the Password Manager application are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request. Your feedback and contributions will help make this application better.

## License
The Password Manager application is open-source and released under the Apache License 2.0.

## Credits

The Password Manager application was created by Egemen Akdan aka Sovereign.