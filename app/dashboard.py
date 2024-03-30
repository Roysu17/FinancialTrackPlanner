import tkinter as tk
from tkinter import ttk

class Dashboard(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

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

    def setup_summary_section(self):
        # Summary frame
        summary_frame = tk.Frame(self, borderwidth=2, relief="groove")
        summary_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(summary_frame, text="Account Summary", font=("Arial", 14)).pack(pady=10)

        # Example summary details, dynamically populate based on user data
        tk.Label(summary_frame, text="Checking: $1,234.56").pack()
        tk.Label(summary_frame, text="Savings: $4,567.89").pack()
        tk.Label(summary_frame, text="Credit Card: -$678.90").pack()

    def setup_details_section(self):
        # Detail frame for showing graphs or detailed transactions
        details_frame = tk.Frame(self, borderwidth=2, relief="groove")
        details_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(details_frame, text="Recent Transactions", font=("Arial", 14)).pack(pady=10)

        # Placeholder for detailed info, e.g., a graph or a list of recent transactions
        # For demonstration, here we just use a text label
        tk.Label(details_frame, text="Transaction details will be displayed here.").pack()

# The following code is for testing purposes
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    Dashboard(root).pack(fill="both", expand=True)
    root.mainloop()
