import tkinter as tk
from tkinter import messagebox
from database import verify_user, get_user_id  # Import the necessary functions

class LoginWindow(tk.Frame):
    def __init__(self, parent, on_success):
        super().__init__(parent)  # No *args or **kwargs if they are not used elsewhere
        self.parent = parent
        self.on_success = on_success
        self.init_ui()

    def init_ui(self):
        self.username = tk.Entry(self)
        self.username.grid(row=0, column=1)

        self.password = tk.Entry(self, show="*")
        self.password.grid(row=1, column=1)

        login_button = tk.Button(self, text="Login", command=self.on_login_clicked)
        login_button.grid(row=2, column=0, columnspan=2)

    def on_login_clicked(self):
        username = self.username.get()
        password = self.password.get()
        user_id = get_user_id(username)  # Fetch the user ID
        if verify_user(username, password):
            messagebox.showinfo("Login Success", "You have successfully logged in.")
            self.on_success(user_id)  # Pass the user ID to the callback
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")