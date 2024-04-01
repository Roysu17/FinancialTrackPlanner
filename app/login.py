import tkinter as tk
from tkinter import messagebox
from tkinter import *
from database import verify_user, get_user_id  # Import the necessary functions

class LoginWindow(tk.Frame):
    def __init__(self, parent, on_success):
        super().__init__(parent)  # No args or **kwargs if they are not used elsewhere
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

    def on_login_clicked(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = get_user_id(username)  # Fetch the user ID
        if verify_user(username, password):
            messagebox.showinfo("Login Success", "You have successfully logged in.")
            self.on_success(user_id)  # Pass the user ID to the callback
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")