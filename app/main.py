import tkinter as tk

from login import LoginWindow
from dashboard import Dashboard
from database import get_account_summary
from transactions import TransactionManager

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Personal Finance Tracker")
        self.geometry("1000x600")
        self.user_id = None  # Store the user ID

        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        login_screen = LoginWindow(self, self.on_login_success)
        login_screen.pack()

    def on_login_success(self, user_id):
        self.user_id = user_id
        self.show_dashboard()

    def show_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()

        dashboard = Dashboard(self, self.user_id)
        dashboard.pack()




def main():
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()
