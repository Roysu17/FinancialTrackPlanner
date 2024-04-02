# Manage financial

import datetime
import tkinter as tk
from database import get_transactions_by_user, add_transaction, add_user, verify_user


# TODO: scrollbar for display
# TODO: give message on invalid inputs
# TODO: push data to CSV
# TODO: add option to delete
# TODO: click on button to put details in infoinput for editing


class TransactionManager(tk.Frame):

    def __init__(self, parent, user_id):
        super().__init__(parent)
        parent.title("Transactions")

        self.user_id = user_id  # Store the user_id for database queries

        # Set up the layout into rows and columns
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=2)


        # Welcome label
        self.font = "Arial"
        self.lbl_welcome = tk.Label(self, text="Welcome to Your Transactions", font=(self.font, 16))
        self.lbl_welcome.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.info_display = tk.Frame(self)
        self.info_display.grid(row=2, column=0, columnspan=3, pady=10)

        self.info_display_header = tk.Label(self, text="Your Previous Transactions", font=(self.font, 12, "bold"))
        self.info_display_header.grid(row=1, column=0, columnspan=3, sticky="NESW")

        self.info_input = tk.Frame(self)
        self.info_input.grid(row=2, column=3, pady=10, padx=30, sticky="NESW")

        self.info_input_header = tk.Label(self, text="Enter or Edit A Transaction", font=(self.font, 12, "bold"))
        self.info_input_header.grid(row=1, column=3, pady=10, padx=30, sticky="NESW")

        self.fill_records()

        self.setup_info()



    def fill_records(self):
        # as a list
        # self.transactions = [Transaction(t[0], t[1], t[2], t[3]) for t in get_transactions_by_user(self.user_id)]

        self.transactions = Stack()
        self.transactions.push_list([Transaction(t[0], t[1], t[2], t[3]) for t in get_transactions_by_user(self.user_id)])

        self.show_transactions()

    def show_transactions(self):
        self.record_box = [tk.Label]*len(self.transactions)
        self.record_text = [tk.StringVar]*len(self.transactions)

        for t in range(len(self.transactions)):

            self.record_text[t] = tk.StringVar(self.info_display, self.transactions[t].format_info())
            self.record_box[t] = tk.Button(self.info_display, textvariable=self.record_text[t], relief="raised", pady=10)

            self.record_box[t].grid(row=t, column=0, columnspan=2, sticky="NESW")
            self.record_box[t].config(height=3)



    def setup_info(self):

        obj_pady = 10

        self.cost_label = tk.Label(self.info_input, text="Cost: ")
        self.cost_label.grid(row=0, column=0, pady=obj_pady)

        self.cost_box = tk.Entry(self.info_input)
        self.cost_box.grid(row=0, column=1, pady=obj_pady)

        self.category_label = tk.Label(self.info_input, text="Category: ")
        self.category_label.grid(row=1, column=0, pady=obj_pady)

        self.category_box = tk.Entry(self.info_input)
        self.category_box.grid(row=1, column=1, pady=obj_pady)

        self.date_label = tk.Label(self.info_input, text="Date: ")
        self.date_label.grid(row=2, column=0, pady=obj_pady)

        self.date_text = tk.StringVar(self.info_input, f"          {datetime.datetime.now().strftime('%Y-%m-%d')}          ")
        self.date_box = tk.Label(self.info_input, textvariable=self.date_text, relief='groove') # maybe change this one
        self.date_box.grid(row=2, column=1, pady=obj_pady)

        self.details_label = tk.Label(self.info_input, text="Details: ")
        self.details_label.grid(row=3, column=0, pady=obj_pady)

        self.details_box = tk.Text(self.info_input, width=15, height=5, wrap="word")
        self.details_box.grid(row=3, column=1, pady=obj_pady)

        self.add_transaction_button = tk.Button(self.info_input, text="Add Transaction", relief="raised", command=self.validate_input)
        self.add_transaction_button.grid(row=5, column=0, columnspan=2, pady=obj_pady + 10)



    def validate_input(self):
        if self.cost_box.get() == "" or self.category_box.get() == "":
            return

        else:

            try:
                val = float(self.cost_box.get())

                output = Transaction(self.date_text.get().strip(), self.category_box.get(), val, self.details_box.get("1.0", "end-1c"))

                self.cost_box.delete("0", tk.END)
                self.category_box.delete("0", tk.END)
                self.details_box.delete("1.0", tk.END)

                self.post_transaction(output)

            except ValueError:
                return


    def post_transaction(self, t):
        self.transactions.push(t)
        self.show_transactions()



class Transaction:

    def __init__(self, date, category, cost, details):
        self.date = date
        self.category = category
        self.cost = "{:.2f}".format(float(cost))
        self.details = details


    def get_info(self):
        return (self.date, self.category, self.cost, self.details)

    def format_info(self):
        formatted_details = "\t".join(self.details.split("\n"))
        return f"({self.date}) {self.category}: {self.cost}\n{formatted_details}"

    def edit_transaction(self):
        pass


class Stack:

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def __len__(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def push_list(self, items):
        for i in items:
            self.push(i)

    def pop_all(self, output_list):
        for _ in self.items:
            output_list.append(self.pop())

    def __getitem__(self, index):
        return self.items[len(self) - index - 1]

    def __setitem__(self, index, value):
        self.items[len(self) - index - 1] = value


# for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")

    TransactionManager(root, '1').grid()
    root.mainloop()
