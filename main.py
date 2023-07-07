import tkinter as tk
from tkinter import ttk
from manager import PasswordManager

manager = PasswordManager()
db = manager.load_db()
root = tk.Tk()
root.geometry("1020x800")
root.title("Sovereign Password Manager")

root.configure(bg="#000000")

form_frame = tk.Frame(root, bg="#000000")
form_frame.place(relx=0.5, rely=0.5, anchor="center")

username_label = tk.Label(form_frame, text="Username or Email:", fg="#FFFFFF", bg="#000000")
username_entry = tk.Entry(form_frame, bg="#FFFFFF")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(form_frame, text="Password:", fg="#FFFFFF", bg="#000000")
password_entry = tk.Entry(form_frame, show="*", bg="#FFFFFF")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry.grid(row=1, column=1,columnspan=1, padx=10, pady=10)

generate_button = tk.Button(form_frame, text="Generate", bg="#FFFFFF" , command = lambda: manager.generate_password(password_entry))
generate_button.grid(row=1, column=1,columnspan=2, padx=10, pady=10)

secure_key_label = tk.Label(form_frame, text="Secure Key:", fg="#FFFFFF", bg="#000000")
secure_key_entry = tk.Entry(form_frame, show="*", bg="#FFFFFF")
secure_key_label.grid(row=2, column=0, padx=10, pady=10)
secure_key_entry.grid(row=2, column=1, padx=10, pady=10)

select_label = tk.Label(form_frame, text="Platform:", fg="#FFFFFF", bg="#000000")
options = ["Facebook", "Twitter", "Instagram","Reddit", "Gmail", "Yahoo", "Outlook"]
selected_option = tk.StringVar()
selected_option.set(options[0])
select_box = tk.OptionMenu(form_frame, selected_option, *options)
select_label.grid(row=3, column=0, padx=10, pady=10)
select_box.config(bg="#FFFFFF")
select_box.grid(row=3, column=1, padx=10, pady=10)

username_value = username_entry.get()
password_value = password_entry.get()
platform_value = selected_option.get()

save_button = tk.Button(form_frame, text="Save", bg="#FFFFFF" , command = lambda: manager.save_password(secure_key_entry, password_entry, username_entry, selected_option,password_tree))
save_button.grid(row=4, column=1, padx=10, pady=10)

search_entry = tk.Entry(form_frame)
search_entry.grid(row=5, column=1,columnspan=1, padx=10, pady=10)

search_button = tk.Button(form_frame, text="Search", bg="#FFFFFF",command= lambda: manager.search_password(password_tree,search_entry))
search_button.grid(row=5 , column=1,columnspan=2 , padx=10, pady=10)

password_tree = ttk.Treeview(form_frame, columns=("Platform", "username", "password","secure"), show="headings")
password_tree.heading("Platform", text="Platform")
password_tree.column("Platform", width=100)
password_tree.heading("username", text="Username")
password_tree.column("username", width=200)
password_tree.heading("password", text="Password")
password_tree.column("password", width=200)
password_tree.heading("secure", text="Secure Key")
password_tree.column("secure", width=200)
password_tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

manager.render_table(password_tree)


def handleSelection(event):
    manager.get_selected_table_item(password_tree)

password_tree.bind("<<TreeviewSelect>>", handleSelection)

edit_button = tk.Button(form_frame, text="Edit", bg="#FFFFFF" , command = lambda:  manager.edit_password(root,password_tree))
edit_button.grid(row=7, column=0, padx=10, pady=10)
delete_button = tk.Button(form_frame, text="Delete", bg="#FFFFFF",command = lambda: manager.delete_password(root,password_tree))
delete_button.grid(row=7, column=1, padx=10, pady=10 )
copy_button = tk.Button(form_frame, text="Copy Password", bg="#FFFFFF" ,command = lambda: manager.copy_password(root,password_tree))
copy_button.grid(row=7, column=2, padx=10, pady=10 )

footer_label = tk.Label(form_frame , text="Developed by Egemen Akdan" , bg="#000000", fg="#FFFFFF")
footer_label.grid(row=8, column=1)

root.mainloop()
