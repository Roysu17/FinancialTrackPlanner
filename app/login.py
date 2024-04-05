"""The Login Tab serves as the portal for users to access the application features and functions. It consists of two
main components: Login and Register, facilitating user authentication and account creation."""
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from database import verify_user, get_user_id, add_user

class LoginWindow(tk.Frame):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success

        # Create frame to hold login elements
        self.login_frame = Frame(self.parent)
        self.login_frame.pack(expand=True)

        # Create username section
        self.username_label = Label(self.login_frame, text="Username:")
        self.username_label.pack(pady=10)

        self.username_entry = Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        # Create password section
        self.password_label = Label(self.login_frame, text="Password:")
        self.password_label.pack(pady=10)

        self.password_entry = Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        # Create login button
        self.login_button = Button(self.login_frame, text="Login", command=self.on_login_clicked)
        self.login_button.pack(pady=10)

        # Create register button
        self.register_button = Button(self.login_frame, text="Register", command=self.show_registration_frame)
        self.register_button.pack(pady=10)

    def on_login_clicked(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = get_user_id(username)
        if verify_user(username, password):
            messagebox.showinfo("Login Success", "You have successfully logged in.")
            self.on_success(user_id)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_registration_frame(self):
        self.login_frame.destroy()  # Destroy login frame
        self.registration_frame = Frame(self.parent)  # Create new frame for registration
        self.registration_frame.pack(expand=True)

        self.new_username_label = Label(self.registration_frame, text="New Username:")
        self.new_username_label.pack(pady=10)

        self.new_username_entry = Entry(self.registration_frame)
        self.new_username_entry.pack(pady=5)

        self.new_password_label = Label(self.registration_frame, text="New Password:")
        self.new_password_label.pack(pady=10)

        self.new_password_entry = Entry(self.registration_frame, show="*")
        self.new_password_entry.pack(pady=5)

        self.register_button = Button(self.registration_frame, text="Register", command=self.register_user)
        self.register_button.pack(pady=10)

    def register_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if new_username and new_password:
            # Check if the username already exists in the database
            if get_user_id(new_username):
                messagebox.showerror("Registration Failed",
                                     "Username already exists. Please choose a different username.")
            else:
                # Add the new user to the database
                add_user(new_username, new_password)
                messagebox.showinfo("Registration Success", "You have successfully registered.")
                # Destroy registration frame
                self.registration_frame.destroy()
                # Recreate the login frame
                self.login_frame = Frame(self.parent)
                self.login_frame.pack(expand=True)
                # Reinitialize login elements
                self.username_label = Label(self.login_frame, text="Username:")
                self.username_label.pack(pady=10)
                self.username_entry = Entry(self.login_frame)
                self.username_entry.pack(pady=5)
                self.password_label = Label(self.login_frame, text="Password:")
                self.password_label.pack(pady=10)
                self.password_entry = Entry(self.login_frame, show="*")
                self.password_entry.pack(pady=5)
                self.login_button = Button(self.login_frame, text="Login", command=self.on_login_clicked)
                self.login_button.pack(pady=10)
                self.register_button = Button(self.login_frame, text="Register", command=self.show_registration_frame)
                self.register_button.pack(pady=10)
        else:
            messagebox.showerror("Registration Failed", "Please enter a username and password.")

