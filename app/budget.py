import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from database import (
    get_last_month_expense_total,
    get_current_month_expense_total,
    get_last_month_income_total,
    get_current_month_income_total
)


class BudgetWindow(tk.Frame):  # Inherit from tk.Frame
    def __init__(self, root, user_id):
        super().__init__(root)
        self.root = root
        self.user_id = user_id

        # Populate data
        self.populate_data()

    def populate_data(self):
        current_month_expense = get_current_month_expense_total(self.user_id)
        last_month_expense = get_last_month_expense_total(self.user_id)
        this_month_income_summary = get_current_month_income_total(self.user_id)
        last_month_income_summary = get_last_month_income_total(self.user_id)

        # Get current month
        current_month = datetime.now().strftime("%B %Y")

        # Get current date
        current_date = datetime.now()

        # Calculate last month's date
        last_month_date = current_date - timedelta(days=current_date.day)
        last_month = last_month_date.strftime("%B %Y")  # Get the name of the last month

        # Month section
        month_label = ttk.Label(self, text=f'Month: {current_month}')
        month_label.grid(row=0, column=0, sticky=tk.W)

        # Income section
        income_label = ttk.Label(self, text=f'Monthly income: {this_month_income_summary}')
        income_label.grid(row=1, column=0, sticky=tk.W)

        # Expense section
        expense_label = ttk.Label(self, text=f'Monthly expense: {current_month_expense}')
        expense_label.grid(row=2, column=0, sticky=tk.W)

        # Label box section
        label_box = ttk.Label(self, text="Comparison Label:")
        label_box.grid(row=0, column=2, rowspan=3, sticky=tk.E)

        # last month
        # Month section
        last_month_label = ttk.Label(self, text=f'Month: {last_month}')
        last_month_label.grid(row=6, column=0, sticky=tk.W)

        # Income section
        last_month_income_label = ttk.Label(self, text=f'Monthly income: {last_month_income_summary}')
        last_month_income_label.grid(row=7, column=0, sticky=tk.W)

        # Expense section
        last_month_expense_label = ttk.Label(self, text=f'Monthly expense: {last_month_expense}')
        last_month_expense_label.grid(row=8, column=0, sticky=tk.W)

        # Label box section
        last_month_label_box = ttk.Label(self, text="Comparison Label:")
        last_month_label_box.grid(row=7, column=2, rowspan=3, columnspan=3, sticky=tk.E)


def main():
    user_id = "1"  # Assuming you have a way to get the user ID
    root = tk.Tk()
    app = BudgetWindow(root, user_id)
    app.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
