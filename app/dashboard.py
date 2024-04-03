import tkinter as tk
from tkinter import ttk
from database import get_monthly_summary, get_recent_transactions
from budget import BudgetWindow
import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard(tk.Frame):
    def __init__(self, parent, user_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.user_id = user_id  # Store the user_id for database queries
    
        self.setup_ui()

    def setup_ui(self):
        self.pack(fill="both", expand=True)
        self.create_notebook()
        self.master.protocol("WM_DELETE_WINDOW", self.logout)

    def create_notebook(self):
        notebook = ttk.Notebook(self)

        
        self.create_dashboard_tab(notebook)
        self.create_transactions_tab(notebook)
        self.create_budget_tab(notebook)
        self.create_report_tab(notebook)
        self.create_logout_tab(notebook)

        notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_logout_tab(self, notebook):
        logout_tab = tk.Frame(notebook)
        notebook.add(logout_tab, text="Logout")

        # Add logout button to the Logout tab
        logout_button = tk.Button(logout_tab, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

    def logout(self):
        # Close the current window
        self.master.destroy()
        # Cleanly exit the application
        self.master.quit()

    def create_dashboard_tab(self, notebook):
        dashboard_tab = tk.Frame(notebook)
        notebook.add(dashboard_tab, text="Dashboard")

        summary_frame = tk.Frame(dashboard_tab)
        summary_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(summary_frame, text="Account Summary", font=("Arial", 14)).pack(pady=10)

        account_summary = get_monthly_summary(self.user_id)

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(account_summary.values(), labels=account_summary.keys(), autopct='%1.1f%%', startangle=180, textprops={'fontsize': 7})

        chart1 = FigureCanvasTkAgg(fig, summary_frame)
        chart1.get_tk_widget().pack()

        details_frame = tk.Frame(dashboard_tab)
        details_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(details_frame, text="Recent Transactions", font=("Arial", 14)).pack(pady=10)

        transactions = get_recent_transactions(self.user_id)
        num = 0
        for transaction in transactions:
            tk.Label(details_frame, text=f"{transaction['date']} - {transaction['category']}: ${transaction['cost']} - {transaction['details']}").pack()
            num += 1
            if num == 10:
                break

    def create_transactions_tab(self, notebook):
        transactions_tab = tk.Frame(notebook)
        notebook.add(transactions_tab, text="Transactions")

        # Implementation for the Transactions tab
        tk.Label(transactions_tab, text="Transactions Tab Content").pack(pady=20)

    def create_budget_tab(self, notebook):
        budget_tab = tk.Frame(notebook)
        notebook.add(budget_tab, text="Budget")

        budget_frame = BudgetWindow(budget_tab, self.user_id)
        budget_frame.pack(fill="both", expand=True)

    def create_report_tab(self, notebook):
        report_tab = tk.Frame(notebook)
        notebook.add(report_tab, text="Report")

        # Implementation for the Report tab
        tk.Label(report_tab, text="Report Tab Content").pack(pady=20)


# The following code is for testing purposes
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    # Receive user id
    # Pass a dummy user_id for testing
    dashboard = Dashboard(root, '1')
    root.mainloop()