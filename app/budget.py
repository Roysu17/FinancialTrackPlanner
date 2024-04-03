import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from database import (
    get_last_month_expense_total,
    get_current_month_expense_total,
    get_last_month_income_total,
    get_current_month_income_total,
)


class BudgetWindow(tk.Frame):
    def __init__(self, root, user_id):
        super().__init__(root)
        self.root = root
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.configure_grid()
        self.populate_data()

    def configure_grid(self):
        for col in range(3):
            self.columnconfigure(col, weight=1)
        for row in range(9):
            self.rowconfigure(row, weight=1)

    def populate_data(self):
        # Data retrieval
        current_month_expense = get_current_month_expense_total(self.user_id)
        last_month_expense = get_last_month_expense_total(self.user_id)
        this_month_income_summary = get_current_month_income_total(self.user_id)
        last_month_income_summary = get_last_month_income_total(self.user_id)

        # Date information
        current_month = datetime.now().strftime("%B %Y")
        current_date = datetime.now()
        last_month_date = current_date - timedelta(days=current_date.day)
        last_month = last_month_date.strftime("%B %Y")

        # UI Components
        self.create_label(row=0, column=0, text=f'Month: {current_month}')
        self.create_label(row=1, column=0, text=f'Monthly income: {this_month_income_summary}')
        self.create_label(row=2, column=0, text=f'Monthly expense: {current_month_expense}')
        self.create_label(row=0, column=2, text="Comparison Label:", rowspan=3, sticky=tk.E)

        self.create_label(row=6, column=0, text=f'Month: {last_month}')
        self.create_label(row=7, column=0, text=f'Monthly income: {last_month_income_summary}')
        self.create_label(row=8, column=0, text=f'Monthly expense: {last_month_expense}')
        self.create_label(row=7, column=2, text="Comparison Label:", rowspan=3, columnspan=3, sticky=tk.E)

    def create_label(self, row, column, text, rowspan=1, columnspan=1, sticky=tk.W):
        label = ttk.Label(self, text=text)
        label.grid(row=row, column=column, sticky=sticky, padx=10, pady=10, rowspan=rowspan, columnspan=columnspan)



def main():
    user_id = "1"  # Placeholder for actual user ID retrieval logic
    root = tk.Tk()
    root.geometry("800x600")  # Default window size
    app = BudgetWindow(root, user_id)
    root.mainloop()


if __name__ == "__main__":
    main()
