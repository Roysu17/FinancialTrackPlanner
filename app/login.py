import tkinter as tk
from tkinter import messagebox

def authenticate(username, password):
    # Placeholder authentication logic
    return username == "user" and password == "password"

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
        if authenticate(self.username.get(), self.password.get()):
            messagebox.showinfo("Login Success", "You have successfully logged in.")
            self.on_success()  # Trigger the callback on successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Ensure the rest of your main.py is updated to reflect this correction
