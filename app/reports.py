"""The Reports tab in the application is designed to provide users with a visual representation of current and last
month spending patterns. It helps users gain a more intuitive understanding of their spending habits in the form of
in-depth insight graphical data."""
# Visual Reports of current and last month expense
import tkinter as tk
from tkinter import ttk, Menu
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import get_monthly_summary, get_last_month_summary

class ReportWindow(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id
        self.initialize_ui()

    def initialize_ui(self):
        self.create_widgets()
        self.load_data()

    def create_widgets(self):

        # Create the widgets for the report window.
        self.summary_label = ttk.Label(self, text="Current month transaction")
        self.summary_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Recent transactions
        self.transactions_label = ttk.Label(self, text="Last month transaction")
        self.transactions_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.initialize_ui()

    def load_data(self):

        # Account summary for last month
        summary_frame_last_month = tk.Frame(self)
        summary_frame_last_month.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        last_month_account_summary = get_monthly_summary(self.user_id)

        # Create a pie chart to visualize the data
        if last_month_account_summary:  # Check if there are transactions available, if not, the pie chart won't be
            # displayed
            fig_last_month, ax_last_month = plt.subplots(figsize=(4, 4))
            ax_last_month.pie(last_month_account_summary.values(), labels=last_month_account_summary.keys(),
                              autopct='%1.1f%%', startangle=180,
                              textprops={'fontsize': 7})

            chart1 = FigureCanvasTkAgg(fig_last_month, summary_frame_last_month)
            chart1.get_tk_widget().pack()

        # Account summary for current month
        summary_frame_current_month = tk.Frame(self)
        summary_frame_current_month.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        account_summary = get_last_month_summary(self.user_id)

        # Create a pie chart to visualize the data
        if account_summary:   # Check if there are transactions available, if not, the pie chart won't be displayed
            fig_current_month, ax_current_month = plt.subplots(figsize=(4, 4))
            ax_current_month.pie(account_summary.values(), labels=account_summary.keys(), autopct='%1.1f%%',
                                 startangle=180,
                                 textprops={'fontsize': 7})

            chart2 = FigureCanvasTkAgg(fig_current_month, summary_frame_current_month)
            chart2.get_tk_widget().pack()

        # Adjust grid weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


def main():
    """Main function to run the application."""
    user_id = "1"
    root = tk.Tk()
    app = ReportWindow(root, user_id)
    app.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
