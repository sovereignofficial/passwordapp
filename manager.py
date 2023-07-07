import random
import string
from dbManager import DatabaseManager
from encryptor import Encryptor
import tkinter as tk
from tkinter import messagebox
import pyperclip

class PasswordManager(Encryptor, DatabaseManager):
    def __init__(self):
            self.tableItem = None 

    def get_current_inputs(self, username_entry, password_entry, selected_option, secure_key_entry):
        username_value = username_entry.get()
        password_value = password_entry.get()
        secure_key_value = secure_key_entry.get()
        platform_value = selected_option.get()

        if username_value and password_value and secure_key_value and platform_value:
            return {"username": username_value, "password": password_value, "secure": secure_key_value,
                    "platform": platform_value}
        else:
            raise ValueError("Values can't be empty!")

    def generate_password(self, password_entry):
        password_entry.delete(0, tk.END)

        symbols = string.punctuation
        numbers = string.digits
        lower_case = string.ascii_lowercase
        upper_case = string.ascii_uppercase

        all_chars = symbols + numbers + lower_case + upper_case
        password = "".join(random.sample(all_chars, 10))
        password_entry.insert(0, password)

    def save_password(self, secure, password, username, platform, password_tree):
        try:
            key = self.load_crypto_key()
            inputs = self.get_current_inputs(username, password, platform, secure)
            encrypted_pass = self.encrypt(inputs["password"], key)
            encrypted_secure_key = self.encrypt(inputs["secure"], key)
            inputs["secure"] = f"{encrypted_secure_key}"
            inputs["password"] = f"{encrypted_pass}"
            self.append_db(inputs)
            self.render_table(password_tree)
        except ValueError as e:
            self.show_error(e)

    def delete_password(self, root, table):
        self.get_selected_table_item(table)
        if self.tableItem:
            secure = self.tableItem[3]
            self.auth_popup(root, secure, "delete", table,self.tableItem)
        else:
            self.show_error("Please select an item from the table!")

    def edit_password(self, root, table):
        self.get_selected_table_item(table)
        if self.tableItem:
            secure = self.tableItem[3]
            self.auth_popup(root, secure, "edit", table,self.tableItem)
        else:
            self.show_error("Please select an item from the table!")

    def copy_password(self, root, table):
        self.get_selected_table_item(table)
        if self.tableItem:
            secure = self.tableItem[3]
            self.auth_popup(root, secure, "copy", table,self.tableItem)
        else:
            self.show_error("Please select an item from the table!")

    def search_password(self, table, search_input):
        table.delete(*table.get_children())
        search_query = search_input.get()
        passwords = self.load_db()
        filtered_passwords = []

        def search_in_platforms():
            for password in passwords:
                if search_query.lower() in password['platform'].lower():
                    filtered_passwords.append(password)

        def search_in_usernames():
            for password in passwords:
                if search_query.lower() in password['username'].lower():
                    filtered_passwords.append(password)

        def render_results():
            for password in filtered_passwords:
                table.insert("", tk.END, text=password['platform'],
                             values=(password['platform'], password['username'], password['password'],
                                     password["secure"]))

        search_in_platforms()
        search_in_usernames()
        render_results()

    def get_selected_table_item(self, password_tree):
        selected_item = password_tree.item(password_tree.selection())
        self.tableItem = selected_item["values"]

    @staticmethod
    def render_table(password_tree):
        password_tree.delete(*password_tree.get_children())
        passwords = PasswordManager.load_db()
        for password in passwords:
            password_tree.insert("", tk.END, text=password['platform'],
                                 values=(password['platform'], password['username'], password['password'],
                                         password["secure"]))

    def auth_popup(self, root, secure, action, table, tableItem):
        popup = tk.Toplevel()
        popup.title("Authenticate")
        popup.geometry("300x200")

        # Get screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate position x, y
        x = (screen_width / 2) - (300 / 2)
        y = (screen_height / 2) - (200 / 2)
        popup.geometry("+%d+%d" % (x, y))

        form_frame = tk.Frame(popup, bg="#000000")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        secure_label = tk.Label(form_frame, text="Secure Key:", fg="#FFFFFF", bg="#000000")
        secure_label.grid(row=0, column=0, padx=10, pady=10)
        secure_entry = tk.Entry(form_frame, bg="#FFFFFF")
        secure_entry.grid(row=0, column=1, padx=10, pady=10)

        if action == "edit":
            editor = tk.Button(popup, text="Verify",
                               command=lambda: self.authenticate_handler( tableItem, table,popup, secure_entry.get(), secure,
                                                                         self.edit_popup))
        elif action == "delete":
            editor = tk.Button(popup, text="Verify",
                               command=lambda: self.authenticate_handler(tableItem, table, popup, secure_entry.get(), secure,
                                                                         self.delete_handler))
        elif action == "copy":
            editor = tk.Button(popup, text="Verify",
                               command=lambda: self.authenticate_handler(tableItem, table,popup, secure_entry.get(), secure,
                                                                         self.copy_to_clipboard))

        editor.pack(side="bottom", pady=10, anchor="s")

    def edit_popup(self, tableItem, table, popup):
        popup = tk.Toplevel()
        popup.title("Edit")
        popup.geometry("300x200")

        # Get screen width and height
        screen_width = 1020
        screen_height = 800

        # Calculate position x, y
        x = (screen_width / 2) - (300 / 2)
        y = (screen_height / 2) - (200 / 2)
        popup.geometry("+%d+%d" % (x, y))

        form_frame = tk.Frame(popup, bg="#000000")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        username_label = tk.Label(form_frame, text="Username or Email:", fg="#FFFFFF", bg="#000000")
        username_entry = tk.Entry(form_frame, bg="#FFFFFF")
        username_label.grid(row=0, column=0, padx=10, pady=10)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        password_label = tk.Label(form_frame, text="Password:", fg="#FFFFFF", bg="#000000")
        password_entry = tk.Entry(form_frame, show="*", bg="#FFFFFF")
        password_label.grid(row=1, column=0, padx=10, pady=10)
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        inputs = {"username": username_entry, "password": password_entry}
        button = tk.Button(form_frame, text="Update",
                           command=lambda: self.update_handler(tableItem, inputs, popup, table))
        button.grid(row=2, column=0, columnspan=3, pady=10)

    @staticmethod
    def show_error(message):
        messagebox.showerror("Error", message)

    @staticmethod
    def authenticate_handler(tableItem, table, popup, input, secure, fallback):
        key = PasswordManager.load_crypto_key()

        if PasswordManager.compare_secure_keys(input, secure, key):
            fallback(tableItem, table, popup)
        else:
            PasswordManager.show_error("You're not authenticated!")

        popup.destroy()

    @staticmethod
    def update_handler(tableItem, inputs, popup, table):
        new_username = inputs["username"].get()
        pass_input = inputs["password"].get()
        new_password = PasswordManager.encrypt(pass_input, PasswordManager.cryptoKey)
        new_password = f"{new_password}"
        new_values = {"username": new_username, "password": new_password}

        if new_password and new_username:
            try:
                PasswordManager.update_item(tableItem, new_values)
            except ValueError as e:
                PasswordManager.show_error(e)

            PasswordManager.render_table(table)
            popup.destroy()
        else:
            return PasswordManager.show_error("Values can't be empty!")

    @staticmethod
    def delete_handler(tableItem, table, popup):
        try:
            PasswordManager.delete_item(tableItem)
            PasswordManager.render_table(table)
            popup.destroy()
        except ValueError as e:
            PasswordManager.show_error(e)

        
        

    @staticmethod
    def copy_to_clipboard(tableItem,table, popup):
        # todo:decrypt the password and then copy the clipboard and then throw a messagebox
        db_password = tableItem[2]
        decrypted_password = PasswordManager.decrypt(db_password, PasswordManager.cryptoKey)
        pyperclip.copy(decrypted_password)
        popup.destroy()
