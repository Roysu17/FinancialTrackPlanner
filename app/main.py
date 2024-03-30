import tkinter as tk
from login import LoginWindow
from dashboard import Dashboard

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Personal Finance Tracker")
        self.geometry("800x600")
        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        login_screen = LoginWindow(self, self.show_dashboard)
        login_screen.pack()

    def show_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()
        dashboard = Dashboard(self)
        dashboard.pack()

def main():
    app = MainApp()
    app.mainloop()

if __name__ == "__main__":
    main()
