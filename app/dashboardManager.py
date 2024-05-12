import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database import get_monthly_summary, get_recent_transactions

class DashboardManager(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.initialize_ui()

    def initialize_ui(self):
        self.load_data()

    def update(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.initialize_ui()

    def load_data(self):
        summary_frame = tk.Frame(self)
        summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(summary_frame, text="Account Summary for the month", font=("Arial", 14)).grid(padx=10, pady=10)

        account_summary = get_monthly_summary(self.user_id)
        if account_summary:  # Check if account summary is not empty
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(account_summary.values(), labels=account_summary.keys(), autopct='%1.1f%%', startangle=180,
                   textprops={'fontsize': 7})
            chart1 = FigureCanvasTkAgg(fig, summary_frame)
            chart1.get_tk_widget().grid(row=2, column=0)  # Added grid management

        details_frame = tk.Frame(self)
        details_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        tk.Label(details_frame, text="Recent Transactions", font=("Arial", 14)).grid(padx=10, pady=10)

        transactions = get_recent_transactions(self.user_id)
        num = 0
        for transaction in transactions:
            tk.Label(details_frame,
                     text=f"{transaction['date']} - {transaction['category']}: ${transaction['cost']} - {transaction['details']}").grid(padx=10, pady=(0, 5))
            num += 1
            if num == 10:
                break

        # Adjust grid weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

def main():
    user_id = "1"
    root = tk.Tk()
    app = DashboardManager(root, user_id)
    app.pack(expand=True, fill="both")  # pack the frame into the root window
    root.mainloop()

if __name__ == "__main__":
    main()
