import tkinter as tk
from tkinter import ttk
from database import (
    get_monthly_summary,
    get_last_month_summary,
    get_this_month_income_summary,
    get_last_month_income_summary
)


class BudgetWindow:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id

        # Initialize variables for data
        self.current_month = tk.StringVar()
        self.income = tk.DoubleVar()
        self.expense = tk.DoubleVar()

        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky='wens')

        # Month section
        month_label = ttk.Label(main_frame, text="Month:")
        month_label.grid(row=0, column=0, sticky=tk.W)
        self.month = ttk.Label(main_frame, textvariable=self.current_month)
        self.month.grid(row=0, column=1, sticky=tk.W)

        # Income section
        income_label = ttk.Label(main_frame, text="Income:")
        income_label.grid(row=1, column=0, sticky=tk.W)
        self.income = ttk.Label(main_frame, textvariable=self.income)
        self.income.grid(row=1, column=1, sticky=tk.W)

        # Expense section
        expense_label = ttk.Label(main_frame, text="Expense:")
        expense_label.grid(row=2, column=0, sticky=tk.W)
        self.expense = ttk.Label(main_frame, textvariable=self.expense)
        self.expense.grid(row=2, column=1, sticky=tk.W)

        # Label box section
        label_box = ttk.Label(main_frame, text="Comparison Label:")
        label_box.grid(row=0, column=2, rowspan=3, sticky='wens')

        # Populate data
        self.populate_data()

    def populate_data(self):
        # Fetch data from the database
        # Here, you would call your database functions to populate the data
        this_month_expense = get_monthly_summary(self.user_id)
        last_month_expense = get_last_month_summary(self.user_id)
        this_month_income_summary = get_this_month_income_summary(self.user_id)
        last_month_income_summary = get_last_month_income_summary(self.user_id)

        for each in this_month_expense:
            print(each)



def main():
    user_id = "1"  # Assuming you have a way to get the user ID
    root = tk.Tk()
    app = BudgetWindow(root, user_id)
    root.mainloop()


if __name__ == "__main__":
    main()
