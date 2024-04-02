import tkinter as tk
from tkinter import ttk, Menu
from database import get_account_summary, get_recent_transactions  # Assuming these functions exist
import os
class Dashboard(tk.Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.user_id = user_id  # Store the user_id for database queries

        # Set up the layout into rows and columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Welcome label
        self.lbl_welcome = tk.Label(self, text="Welcome to Your Dashboard", font=("Arial", 16))
        self.lbl_welcome.grid(row=0, column=0, columnspan=2, pady=10)

        # Left column for summaries
        self.setup_summary_section()

        # Right column for graphs or more detailed info
        self.setup_details_section()
        self.setup_menu()

    def setup_menu(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # Adding menu items directly to the menubar
        menubar.add_command(label="Sign Out", command=lambda: self.navigate_to('main.py'))
        menubar.add_command(label="Dashboard", command=lambda: self.navigate_to('dashboard.py'))
        menubar.add_command(label="Transaction", command=lambda: self.navigate_to('transactions.py'))
        menubar.add_command(label="Budget", command=lambda: self.navigate_to('budget.py'))
        menubar.add_command(label="Report", command=lambda: self.navigate_to('report.py'))

    def navigate_to(self, filepath):
        # Close the current window and open the target Python file
        self.master.destroy()
        os.system(f'python {filepath} {self.user_id}')

    def setup_summary_section(self):
        # Summary frame
        summary_frame = tk.Frame(self, borderwidth=2, relief="groove")
        summary_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(summary_frame, text="Account Summary", font=("Arial", 14)).pack(pady=10)

        # Fetch and display the account summary for the user
        account_summary = get_account_summary(self.user_id)
        for account_type, amount in account_summary.items():
            tk.Label(summary_frame, text=f"{account_type}: ${amount}").pack()

    def setup_details_section(self):
        # Detail frame for showing graphs or detailed transactions
        details_frame = tk.Frame(self, borderwidth=2, relief="groove")
        details_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(details_frame, text="Recent Transactions", font=("Arial", 14)).pack(pady=10)

        # Fetch and display recent transactions for the user
        transactions = get_recent_transactions(self.user_id)
        for transaction in transactions:
            tk.Label(details_frame, text=f"{transaction['date']} - {transaction['category']}: ${transaction['cost']} - {transaction['details']}").pack()

# The following code is for testing purposes
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    # Pass a dummy user_id for testing
    Dashboard(root, 'dummy_user_id').pack(fill="both", expand=True)
    root.mainloop()
