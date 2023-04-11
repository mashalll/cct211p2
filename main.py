import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from tkinter import * 
import re
import sqlite3

class ContactList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Login")
        self.master.geometry("640x280")

        self.master = tk.Frame(self.master, width=640, height=480)
        self.master.pack()

        self.db_conn = sqlite3.connect('contacts.db')
        self.create_table()

        self.users = {}

        # LOG IN MENU
        self.nameText = tk.Label(self.master, text="Enter your username:")
        self.nameText.pack(pady=5)

        self.nameResponse = tk.Entry(self.master)
        self.nameResponse.pack(pady=6)

        self.passwordText = tk.Label(self.master, text="Enter your password:")
        self.passwordText.pack(pady=5)

        password = StringVar()  # Password variable
        self.passwordResponse = tk.Entry(self.master, textvariable=password, show='*')
        self.passwordResponse.pack(pady=6)

        # self.loginButton = tk.Button(self.login, text="Login",command=self.login_verify)
        self.loginButton = tk.Button(self.master, text="Login", command=self.menu)
        self.loginButton.pack(pady=5)

    def create_table(self):
        c = self.db_conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS contacts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT, user_id INTEGER,
                      FOREIGN KEY(user_id) REFERENCES users(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
        self.db_conn.commit()

    def insert_contact(self, name, phone, email, user_id):
        c = self.db_conn.cursor()
        c.execute("INSERT INTO contacts (name, phone, email, user_id) VALUES (?, ?, ?, ?)", (name, phone, email, user_id))
        self.db_conn.commit()
        
    def edit_contact2(self, name, phone, email, user_id):
        c = self.db_conn.cursor()
        c.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?",(name, phone, email, user_id))
        self.db_conn.commit()
        
    # function to view all contacts
    def view_contacts2():
        c.execute("SELECT * FROM contacts")
        contacts = c.fetchall()
        for contact in contacts:
            print(contact)

    # function to delete a contact
    def delete_contact2(id):
        c.execute("DELETE FROM contacts WHERE id = ?", (id,))
        conn.commit()

    def get_contacts_by_user_id(self, user_id):
        c = self.db_conn.cursor()
        c.execute("SELECT * FROM contacts WHERE user_id=?", (user_id,))
        return c.fetchall()

    def login(self):
        c = self.db_conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (self.nameResponse.get(),))
        user = c.fetchone()
        if user:
            if self.passwordResponse.get() == user[2]:
                print("Account found")
                self.user_id = user[0]
                self.load_contacts()
            else:
                print("Does not match password")
                return False
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.nameResponse.get(), self.passwordResponse.get()))
            self.user_id = c.lastrowid
            self.db_conn.commit()
            print("Account created")

    def load_contacts(self):
        contacts = self.get_contacts_by_user_id(self.user_id)
        for contact in contacts:
            self.contacts_listbox.insert(tk.END, contact[1])

    def menu(self):
        self.menu = tk.Toplevel(self.master)
        self.menu.title('Contacts')
        self.menu.geometry("640x280")

        #DISPLAY BOX
        self.contacts_listbox = tk.Listbox(self.menu)
        self.contacts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #SCROLLBAR FOR DISPLAY BOX
        self.scrollbar = tk.Scrollbar(self.menu)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contacts_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.contacts_listbox.yview)

        #BUTTONS FOR ACTIONS (ADD,EDIT,VIEW,DELETE)
        self.add_button = tk.Button(self.menu, text='Add', command=self.add_contact)
        self.add_button.pack(side=tk.TOP, padx=10, pady=10)

        self.edit_button = tk.Button(self.menu, text='Edit', command=self.edit_contact)
        self.edit_button.pack(side=tk.TOP, padx=10, pady=10)

        self.view_button = tk.Button(self.menu, text='View', command=self.view_contact)
        self.view_button.pack(side=tk.TOP, padx=10, pady=10)

        self.delete_button = tk.Button(self.menu, text='Delete', command=self.delete_contact)
        self.delete_button.pack(side=tk.TOP, padx=10, pady=10)

        self.exit_button = tk.Button(self.menu, text='Exit', command=self.close_application)
        self.exit_button.pack(side=tk.TOP, padx=10, pady=10)

        # CHECKING AND LOADING USER INFO
        if self.nameResponse.get() in self.users:
            if self.passwordResponse.get() == self.users[self.nameResponse.get()][0]:
                for i in self.users[self.nameResponse.get()][1:]:
                    self.contacts_listbox.insert(tk.END, i)
                print("Account found")
            else:
                print("Does not match password")
                return False
        else:
            self.users[self.nameResponse.get()] = [self.passwordResponse.get()]
            print("Account created")

        #DICTIONARY FOR CONTACTS
        self.contacts = {}
        self.id = 0 

    def close_application(self):
        confirm_close = messagebox.askyesnocancel("Confirm Close", "Are you sure you want to exit the application? You will be logged out")
        if confirm_close:
            self.menu.destroy()


    def show_menu (self):
        self.master.pack()
        self.login.pack_forget()


    def add_contact(self):
        # NEW WINDOW TO ADD CONTACTS
        self.add_window = tk.Toplevel(self.master)
        self.add_window.title('Add Contact')

        self.name_label = tk.Label(self.add_window, text='Name')
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.add_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.phone_label = tk.Label(self.add_window, text='Phone')
        self.phone_label.grid(row=1, column=0, padx=10, pady=10)
        self.phone_entry = tk.Entry(self.add_window)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        self.email_label = tk.Label(self.add_window, text='Email')
        self.email_label.grid(row=2, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.add_window)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        self.save_button = tk.Button(self.add_window, text='Save', command=self.validate)
        self.save_button.grid(row=3, column=1, padx=10, pady=10)

        self.exit_button = tk.Button(self.add_window,text = 'Go Back', command=self.go_back)
        self.exit_button.grid(row=3, column=0, padx=10,pady=10)

    def go_back(self):
        confirm_back = messagebox.askyesnocancel("Confirm Clear", "Are you sure you want to go back? The profile you made will be deleted")
        if confirm_back:
            self.add_window.destroy()

    def validate(self):
        # SAVE INFORMATION FROM ENTRY BOX
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        # check if input is valid
        if not name.isalpha():
            print("Names should be alphabetic")
            return False

        validnum = ""
        for c in phone:
            if c.isnumeric():
                validnum += str(c)
            else:
                if c != ' ' and c != '-':
                    print("Error not numbers")
                    return False
        if len(validnum) != 10:
            print("Not the right length")
            return False

        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if not re.fullmatch(pattern, email):
            print("Not a valid email")
            return False

        self.save_contact()

    def save_contact(self):
        # SAVE INFORMATION FROM ENTRY BOX
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        # ADD INFORMATION TO DICTIONARY
        self.contacts[name] = {'phone': phone, 'email': email, 'id': self.id}
        self.contacts_listbox.insert(tk.END, name)
        self.add_window.destroy() # REMOVE THE ADD WINDOW
        self.users[self.nameResponse.get()] += self.contacts
        self.insert_contact(name, phone, email, self.id)
        self.id += 1
        print(self.users)

    def edit_contact(self):
        index = self.contacts_listbox.curselection() #TAKES WHATEVER THE USER SELECTS IN THE DISPLAYBOX
        if index:
            name = self.contacts_listbox.get(index)

            #MAKE NEW WINDOW TO EDIT THE CONTACT
            self.edit_window = tk.Toplevel(self.master)
            self.edit_window.title('Edit Contact')

            self.name_label = tk.Label(self.edit_window, text='Name')
            self.name_label.grid(row=0, column=0, padx=10, pady=10)
            self.name_entry = tk.Entry(self.edit_window)
            self.name_entry.grid(row=0, column=1, padx=10, pady=10)
            self.name_entry.insert(0, name)

            self.phone_label = tk.Label(self.edit_window, text='Phone')
            self.phone_label.grid(row=1, column=0, padx=10, pady=10)
            self.phone_entry = tk.Entry(self.edit_window)
            self.phone_entry.grid(row=1, column=1, padx=10, pady=10)
            self.phone_entry.insert(0, self.contacts[name]['phone'])

            self.email_label = tk.Label(self.edit_window, text='Email')
            self.email_label.grid(row=2, column=0, padx=10, pady=10)
            self.email_entry = tk.Entry(self.edit_window)
            self.email_entry.grid(row=2, column=1, padx=10, pady=10)
            self.email_entry.insert(0, self.contacts[name]['email'])

            # NEW SAVE BUTTON FOR EDITED CONTACTS
            self.save_button = tk.Button(self.edit_window, text='Save', command=lambda: self.save_edited_contact(name))
            self.save_button.grid(row=3, column=1, padx=10, pady=10)

    def save_edited_contact(self, name):
        # THIS FUNCTION SAVES AND UPDATES THE CONTACTS NEW INFORMATION
        id = self.contacts[name]['id'] + 1
        self.contacts[name]['phone'] = self.phone_entry.get()
        self.contacts[name]['email'] = self.email_entry.get()

        self.contacts_listbox.delete(tk.ACTIVE)
        self.contacts_listbox.insert(tk.ACTIVE, self.name_entry.get())
        self.edit_contact2(self.name_entry.get(), self.phone_entry.get(), self.email_entry.get(), id)

        self.edit_window.destroy()

    def view_contact(self):
        # GETS THE SELECTED CONTACT
        index = self.contacts_listbox.curselection()
        if index:

            name = self.contacts_listbox.get(index)

            # MAKES NEW WINDOW TO VIEW THE CONTACT INFORMATION  -- ONLY DISPLAY INFORMATION AS LABEL, SINCE WE WON'T NEED TO CHANGE IT
            self.view_window = tk.Toplevel(self.master)
            self.view_window.title('View Contact')

            self.name_label = tk.Label(self.view_window, text='Name: ' + name)
            self.name_label.pack(padx=10, pady=10)

            self.phone_label = tk.Label(self.view_window, text='Phone: ' + self.contacts[name]['phone'])
            self.phone_label.pack(padx=10, pady=10)

            self.email_label = tk.Label(self.view_window, text='Email: ' + self.contacts[name]['email'])
            self.email_label.pack(padx=10, pady=10)

    def delete_contact(self): #DELETE CONTACT INFORMATION AFTER USER SELECTS IT
        index = self.contacts_listbox.curselection()

        if index:
            name = self.contacts_listbox.get(index)
            del self.contacts[name]
            self.contacts_listbox.delete(tk.ACTIVE)


root = tk.Tk()
app = ContactList(root)
root.mainloop()
