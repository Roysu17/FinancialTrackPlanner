# Manage financial

import datetime
import tkinter as tk
from database import get_transactions_by_user


class TransactionManager(tk.Frame):

    def __init__(self, parent, user_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.user_id = user_id  # Store the user_id for database queries

        # Set up the layout into rows and columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Welcome label
        self.lbl_welcome = tk.Label(self, text="Welcome to Your Transactions", font=("Arial", 16))
        self.lbl_welcome.grid(row=0, column=0, columnspan=2, pady=10)

        self.info_display = tk.Frame(self)
        self.info_display.grid(row=0, column=1, columnspan=3, pady=10)

        self.transactions = [Transaction(t[0], t[1], t[2], t[3]) for t in get_transactions_by_user(self.user_id)]


        self.info_input = tk.Frame(self)
        self.info_input.grid(row=0, column=4, pady=10)





class Transaction:

    def __init__(self, date, category, cost, details):
        self.date = date
        self.category = category
        self.cost = float(cost)
        self.details = details


    def get_info(self):
        return (self.date, self.category, self.cost, self.details)

    def edit_transaction(self):
        pass


# for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    # Pass a dummy user_id for testing
    TransactionManager(root, 'dummy_user_id').pack(fill="both", expand=True)
    root.mainloop()
