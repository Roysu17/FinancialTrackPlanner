# Budget planning and tracking
import tkinter as tk
from tkinter import ttk, Menu
from database import get_account_summary, get_recent_transactions  # Assuming these functions exist
import os

class BudgetWindow(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.initialize_ui()

    def initialize_ui(self):
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Account summary
        self.summary_label = ttk.Label(self, text="Account Summary")
        self.summary_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.summary_text = tk.Text(self, height=10, width=50)
        self.summary_text.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Recent transactions
        self.transactions_label = ttk.Label(self, text="Recent Transactions")
        self.transactions_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.transactions_text = tk.Text(self, height=10, width=50)
        self.transactions_text.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    def load_data(self):
        # Load account summary
        account_summary = get_account_summary(self.user_id)
        self.summary_text.insert(tk.END, account_summary)

        # Load recent transactions
        recent_transactions = get_recent_transactions(self.user_id)
        for transaction in recent_transactions:
            self.transactions_text.insert(tk.END, f"{transaction}\n")

def main():
    user_id = "your_user_id_here"  # Assuming you have a way to get the user ID
    root = tk.Tk()
    app = BudgetWindow(root, user_id)
    app.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
