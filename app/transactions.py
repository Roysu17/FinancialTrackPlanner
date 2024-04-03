# Manage financial

import datetime
import tkinter as tk
from database import get_transactions_by_user, add_transaction, add_user, verify_user, edit_transaction


# TODO: fix scrollbar for display
# TODO: add option to delete
# TODO: click on button to put details in infoinput for editing


class TransactionManager(tk.Frame):

    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id  # Store the user_id for database queries
        self.editing_transaction_id = None

        # Set up the layout into rows and columns
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=2)

        self.record_selection = None

        # Welcome label
        self.font = "Arial"
        self.lbl_welcome = tk.Label(self, text="Welcome to Your Transactions", font=(self.font, 16))
        self.lbl_welcome.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.info_display_header = tk.Label(self, text="Your Previous Transactions", font=(self.font, 12, "bold"))
        self.info_display_header.grid(row=1, column=0, columnspan=3, sticky="NESW")

        # Canvas to hold the transactions
        self.info_display_canvas = tk.Canvas(self)
        self.info_display_canvas.grid(row=2, column=0, columnspan=3, pady=10, sticky="NESW")

        # Frame to hold the transactions inside the canvas
        self.info_display = tk.Frame(self.info_display_canvas)
        self.info_display_canvas.create_window((0, 0), window=self.info_display, anchor="nw")

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.info_display_canvas.yview)
        self.scrollbar.grid(row=2, column=3, sticky="NS")
        self.info_display_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Update the canvas to fit the content
        self.info_display.bind("<Configure>", lambda e: self.info_display_canvas.configure(scrollregion=self.info_display_canvas.bbox("all")))

        self.info_input_header = tk.Label(self, text="Enter or Edit A Transaction", font=(self.font, 12, "bold"))
        self.info_input_header.grid(row=1, column=4, pady=10, padx=30, sticky="NESW")

        self.info_input = tk.Frame(self)
        self.info_input.grid(row=2, column=4, pady=10, padx=30, sticky="NESW")

        self.fill_records()
        self.setup_info()



    def fill_records(self):
        # Retrieve transactions from the database and fill the display
        transactions_data = get_transactions_by_user(self.user_id)
        self.transactions = Stack()
        for transaction_data in transactions_data:
            transaction = Transaction(*transaction_data)  # Creating Transaction objects
            self.transactions.push(transaction)

        self.show_transactions()

    # Show transactions method
    def show_transactions(self):
        self.record_box = []
        self.record_text = []

        for index, transaction in enumerate(self.transactions):
            record_text = tk.StringVar(value=transaction.format_info())
            self.record_text.append(record_text)

            # Create a label for each transaction listing
            record_label = tk.Label(self.info_display, textvariable=record_text, relief="raised", pady=10, width=30)
            record_label.grid(row=index, column=0, columnspan=2, sticky="NESW")

            # Create a button for editing each transaction
            edit_button = tk.Button(self.info_display, text="Edit Transaction", command=lambda idx=index: self.populate_edit_fields(idx))
            edit_button.grid(row=index, column=2, sticky="NESW")

            self.record_box.append((record_label, edit_button))


    def toggle_edit_mode(self):
        if self.editing_transaction_id is None:
            # Entering edit mode
            self.edit_transaction_button.config(text="Submit Edit")
        else:
            # Exiting edit mode
            self.edit_transaction_button.config(text="Edit Transaction")
            self.edit_transaction()

    # Populate edit fields method
    def populate_edit_fields(self, index):
        transaction = self.transactions[index]
        self.cost_box.delete(0, tk.END)
        self.cost_box.insert(0, transaction.cost)
        self.category_text.set(transaction.category)
        self.date_box.delete(0, tk.END)
        self.date_box.insert(0, transaction.date)
        self.details_box.delete("1.0", tk.END)
        self.details_box.insert("1.0", transaction.details)
        self.editing_transaction_id = transaction.transaction_id

    # Edit transaction method
    def edit_transaction(self):
        if self.editing_index is not None:
            self.transactions[self.editing_index].cost = self.cost_box.get()
            self.transactions[self.editing_index].category = self.category_text.get()
            self.transactions[self.editing_index].date = self.date_box.get()
            self.transactions[self.editing_index].details = self.details_box.get("1.0", "end-1c")

            self.record_text[self.editing_index].set(self.transactions[self.editing_index].format_info())
            self.editing_index = None

        if self.editing_transaction_id is not None:
            edit_transaction(self.user_id, self.editing_transaction_id, self.date_box.get(), self.category_text.get(), self.cost_box.get(), self.details_box.get("1.0", "end-1c"))
            self.attempt_variable.set("Transaction successfully updated!")
            self.attempt_status.config(fg="green")
            self.edit_transaction_button.grid_forget()
            self.clear_form_fields()
            self.editing_transaction_id = None
            self.fill_records()
            

    def clear_form_fields(self):
        """Utility method to clear all input fields."""
        self.cost_box.delete(0, tk.END)
        self.category_text.set(self.category_options[0])  # Assuming the first option is a default or empty
        self.date_box.delete(0, tk.END)
        self.details_box.delete("1.0", tk.END)


    # TODO unsure of this
    def on_record_select(self, button):
        self.record_selection = button



    def setup_info(self):

        obj_pady = 10

        self.cost_label = tk.Label(self.info_input, text="Cost: ")
        self.cost_label.grid(row=0, column=0, pady=obj_pady)

        self.cost_box = tk.Entry(self.info_input)
        self.cost_box.grid(row=0, column=1, pady=obj_pady)

        self.category_label = tk.Label(self.info_input, text="Category: ")
        self.category_label.grid(row=1, column=0, pady=obj_pady)


        self.category_options = ['', 'FOOD', 'HOUSE', 'ENTERTAINMENT', 'SCHOOL', 'INCOME', 'CAR', 'OTHER']

        self.category_text = tk.StringVar()
        self.category_text.set("")
        self.category_box = tk.OptionMenu(self.info_input, self.category_text, *self.category_options)
        self.category_box.config(width=15)
        self.category_box.grid(row=1, column=1, pady=obj_pady)


        self.date_label = tk.Label(self.info_input, text="Date: ")
        self.date_label.grid(row=2, column=0, pady=obj_pady)

        self.date_box = tk.Entry(self.info_input)
        self.date_box.grid(row=2, column=1, pady=obj_pady)

        self.details_label = tk.Label(self.info_input, text="Details: ")
        self.details_label.grid(row=3, column=0, pady=obj_pady)

        self.details_box = tk.Text(self.info_input, width=15, height=5, wrap="word")
        self.details_box.grid(row=3, column=1, pady=obj_pady)

        self.add_transaction_button = tk.Button(self.info_input, text="Add Transaction", relief="raised", command=self.validate_transaction)
        self.add_transaction_button.grid(row=5, column=0, columnspan=2, pady=obj_pady + 10)

        self.attempt_variable = tk.StringVar()
        self.attempt_status = tk.Label(self.info_input, textvariable=self.attempt_variable, relief="flat")
        self.attempt_status.config(width=24)
        self.attempt_status.grid(row=6, column=0, columnspan=2, pady=obj_pady + 10)
        self.edit_transaction_button = tk.Button(self.info_input, text="Edit Transaction", relief="raised", command=self.toggle_edit_mode)
        self.edit_transaction_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.edit_transaction_button.grid_forget()  # Initially hide this button until needed


    def validate_transaction(self):

        if self.cost_box.get() == "":
            self.attempt_variable.set("Missing required field: cost")
            self.attempt_status.config(fg="red")
            return


        elif self.category_text.get().strip() == "":
            self.attempt_variable.set("Missing required field: category")
            self.attempt_status.config(fg="red")
            return

        elif self.date_box.get() == "":
           self.attempt_variable.set("Missing required field: date")
           self.attempt_status.config(fg="red")
           return


        try:
            val = float(self.cost_box.get())

        except ValueError:
            self.attempt_variable.set("Cost contains unsupported\n characters")
            self.attempt_status.config(fg="red")
            return


        try:
            parsed_date_components = str(datetime.datetime.strptime(self.date_box.get(), "%Y-%m-%d")).split()[0].split("-")
            parsed_date = "-".join([parsed_date_components[0], parsed_date_components[1], parsed_date_components[2]])

        except ValueError:
            self.attempt_variable.set("Requires a valid date\n in YYYY-MM-DD format")
            self.attempt_status.config(fg="red")
            return


        output = Transaction(parsed_date, self.category_text.get(), val, self.details_box.get("1.0", "end-1c"))

        self.cost_box.delete("0", tk.END)
        self.category_box.option_clear()
        self.date_box.delete("0", tk.END)
        self.details_box.delete("1.0", tk.END)

        self.post_transaction(output)

        self.attempt_variable.set("Transaction has been\n successfully posted!")
        self.attempt_status.config(fg="green")
        return


    def post_transaction(self, t):

        add_transaction(self.user_id, t.date, t.category, t.cost, t.details)
        self.fill_records()



class Transaction:

    def __init__(self, transaction_id, date, category, cost, details):
        self.transaction_id = transaction_id
        self.date = date
        self.category = category
        self.cost = "{:.2f}".format(float(cost))
        self.details = details

    def get_info(self):
        return (self.transaction_id, self.date, self.category, self.cost, self.details)

    def format_info(self):
        formatted_details = "\t".join(self.details.split("\n"))
        return f"({self.date}) {self.category}: {self.cost}\n{formatted_details}"

    def __lt__(self, other):
        return self if self.date <= other.date else other


class Stack:

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def __len__(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)
        self.items = sorted(self.items, key=(lambda x: x.date))


    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def push_list(self, items):
        for i in items:
            self.push(i)

        self.items = sorted(self.items, key=(lambda x: x.date))


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
