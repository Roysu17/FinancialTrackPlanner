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
    
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.init_ui()

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

        # Calculating the percentage of income used compared to expenses
        if this_month_income_summary == 0:
            current_month_percentage = -1
        else:
            current_month_percentage = (current_month_expense / this_month_income_summary) * 100
        if last_month_income_summary == 0:
            last_month_percentage = -1
        else:
            last_month_percentage = (last_month_expense / last_month_income_summary) * 100

        # UI Components
        self.create_label(row=0, column=0, text=f'{current_month}')
        self.create_label(row=1, column=0, text=f'Monthly income: {this_month_income_summary}')
        self.create_label(row=2, column=0, text=f'Monthly expense: {current_month_expense}')
        self.create_comparison_label(row=0, column=2, percentage=current_month_percentage)

        self.create_label(row=6, column=0, text=f'{last_month}')
        self.create_label(row=7, column=0, text=f'Monthly income: {last_month_income_summary}')
        self.create_label(row=8, column=0, text=f'Monthly expense: {last_month_expense}')
        self.create_comparison_label(row=7, column=2, percentage=last_month_percentage)

    def create_comparison_label(self, row, column, percentage):
        if percentage >= 90:
            text = "Your expenses have exceeded 90% of your income for this period. \n" \
                   "It's important to review your spending habits and consider adjustments \n" \
                   "to ensure financial stability and meet your long-term financial goals."
        elif 80 <= percentage < 90:
            text = "Your expenses have reached 80-90% of your income for this period. \n" \
                   "This indicates a significant portion of your income is being utilized. \n" \
                   "Consider evaluating your spending patterns to maintain a healthy balance " \
                   "between income and expenses."
        elif 70 <= percentage < 80:
            text = "Your expenses are within 70-80% of your income for this period. \n" \
                   "While still manageable, it's wise to monitor your expenses closely \n" \
                   "and identify areas where you can potentially reduce costs to improve " \
                   "your financial situation."
        elif 60 <= percentage < 70:
            text = "Your expenses are within 60-70% of your income for this period. \n" \
                   "This suggests a reasonable balance between income and expenses. \n" \
                   "However, it's always beneficial to track your spending and look for " \
                   "opportunities to optimize your budget."
        elif 50 <= percentage < 60:
            text = "Your expenses are within 50-60% of your income for this period. \n" \
                   "This indicates a healthy financial situation where you're effectively \n" \
                   "managing your expenses. Continue monitoring your budget to ensure " \
                   "sustainable financial habits."
        elif 0 <= percentage < 50:
            text = "Your expenses are below 50% of your income for this period, maintaining \n" \
                   "a healthy balance. It's commendable that you're living within your means \n" \
                   "and allocating your income wisely. Keep up the good work!"
        else:
            text = "No data available"

        self.create_label(row=row, column=column, text=text, rowspan=3, columnspan=3, sticky=tk.E)

    def create_label(self, row, column, text, rowspan=1, columnspan=1, sticky=tk.W):
        if "Your" not in text:  # Exclude "Comparison Label"
            label = ttk.Label(self, text=text, font=("Arial", 17))
        else:
            label = ttk.Label(self, text=text, font=("Arial", 11))

        label.grid(row=row, column=column, sticky=sticky, padx=10, pady=10, rowspan=rowspan, columnspan=columnspan)


def main():
    user_id = "1"  # Placeholder for actual user ID retrieval logic
    root = tk.Tk()
    root.geometry("800x600")  # Default window size
    app = BudgetWindow(root, user_id)
    root.mainloop()


if __name__ == "__main__":
    main()
