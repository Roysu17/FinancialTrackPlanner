from tkinter import *
from tkinter import messagebox

class LoginFrame(Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Page")
        self.geometry('1280x720')

        # Create frame to hold login elements
        self.loginframe = Frame(self)
        self.loginframe.pack(expand=True)

        # Create username section
        self.usernamelabel = Label(self.loginframe, text="Username:")
        self.usernamelabel.pack(pady=10)

        self.username_entry = Entry(self.loginframe)
        self.username_entry.pack(pady=5)

        # Create password section
        self.password_label = Label(self.loginframe, text="Password:")
        self.password_label.pack(pady=10)

        self.password_entry = Entry(self.loginframe, show="*")
        self.password_entry.pack(pady=5)

        # Create login button
        self.login_button = Button(self.loginframe, text="Login", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username and password are correct
        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

app = LoginFrame()
app.mainloop()
