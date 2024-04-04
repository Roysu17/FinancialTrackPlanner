# Manage financial

import datetime
import tkinter as tk
from database import get_transactions_by_user, add_transaction, edit_transaction, delete_transaction


class TransactionManager(tk.Frame):

    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.parent = parent
        self.user_id = user_id  # Store the user_id for database queries
        self.editing_transaction_id = None
        self.editing_index = None
        self.edit_mode = False

        # Welcome label
        self.font = "Arial"
        self.lbl_welcome = tk.Label(self, text="Welcome to Your Transactions", font=(self.font, 16))
        self.lbl_welcome.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.info_display_header = tk.Label(self, text="Your Previous Transactions", font=(self.font, 12, "bold"))
        self.info_display_header.grid(row=1, column=0, columnspan=4, sticky="NESW", padx=10)

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
        self.info_input_header.grid(row=1, column=4, pady=10, padx=100, sticky="NESW")

        self.info_input = tk.Frame(self)
        self.info_input.grid(row=2, column=4, pady=10, padx=100, sticky="NESW")

        self.fill_records()
        self.setup_info()


    def fill_records(self):
        # Retrieve transactions from the database and fill the display
        transactions_data = get_transactions_by_user(self.user_id)
        self.transactions = Stack()
        for transaction_data in transactions_data:
            transaction = Transaction(transaction_data[0], transaction_data[1], transaction_data[2], transaction_data[3], transaction_data[4])
            self.transactions.push(transaction)

        self.show_transactions()

    # Show transactions method
    def show_transactions(self):
        self.record_box = []
        self.record_text = []
        self.record_button_text = []

        for widget in self.info_display.winfo_children():
            # if self.record_box and (widget in self.record_box[0] or widget in self.record_box[1]):
            if not isinstance(widget, tk.Canvas):
                widget.destroy()


        for index, transaction in enumerate(self.transactions.items):
            record_text = tk.StringVar(value=transaction.format_info())
            self.record_text.append(record_text)

            # Create a label for each transaction listing
            record_label = tk.Label(self.info_display, textvariable=record_text, relief="raised", pady=10, width=30)
            record_label.grid(row=index, column=0, sticky="NESW")

            # Create a button for editing each transaction
            edit_button_text = tk.StringVar()
            edit_button_text.set("Select Transaction")

            edit_button = tk.Button(self.info_display, textvariable=edit_button_text, command=lambda idx=index: self.edit_fields(idx))
            edit_button.grid(row=index, column=1, sticky="NESW")

            self.record_button_text.append(edit_button_text)
            self.record_box.append((record_label, edit_button))

            self.info_display.config(width=318)
            self.info_display_canvas.config(width=318)


    # Populate edit fields method
    def edit_fields(self, index):

        if self.edit_mode and index == self.editing_index:

            should_execute = self.validate_transaction()

            if should_execute:
                edit_transaction(self.date_box.get(), self.category_text.get(), self.cost_box.get(), self.details_box.get("1.0", "end-1c"), self.editing_transaction_id, self.user_id)
                self.reset_button_selection_text()

                self.clear_form_fields()
                self.edit_mode = False

                self.add_transaction_button.config(state='active')
                self.delete_transaction_button.config(state="disabled")

        else:
            self.reset_button_selection_text()

            self.record_button_text[index].set("Submit Edit")
            self.record_box[index][0].config(relief="solid")
            self.record_box[index][1].config(bg='lime')

            transaction = self.transactions[index]
            self.clear_form_fields()

            self.cost_box.insert(0, transaction.cost)
            self.category_text.set(transaction.category)
            self.date_box.insert(0, transaction.date)
            self.details_box.insert("1.0", transaction.details)
            self.editing_transaction_id = transaction.transaction_id

            self.editing_index = index
            self.edit_mode = True

            self.add_transaction_button.config(state='disabled')
            self.delete_transaction_button.config(state="active")


    def clear_form_fields(self):
        """Utility method to clear all input fields."""
        self.cost_box.delete(0, tk.END)
        self.category_text.set(self.category_options[0])  # Assuming the first option is a default or empty
        self.date_box.delete(0, tk.END)
        self.details_box.delete("1.0", tk.END)


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

        self.button_color_default = "SystemButtonFace"

        self.attempt_variable = tk.StringVar()
        self.attempt_status = tk.Label(self.info_input, textvariable=self.attempt_variable, relief="flat", height=2)
        self.attempt_status.config(width=24)
        self.attempt_status.grid(row=4, column=0, columnspan=2, pady=obj_pady + 10)

        self.delete_transaction_button = tk.Button(self.info_input, text="Delete Selected Transaction", relief="raised", command=self.delete_transaction)
        self.delete_transaction_button.grid(row=7, column=0, columnspan=2, pady=obj_pady + 10, padx=10)
        self.delete_transaction_button.config(state="disabled")


    def delete_transaction(self):
        delete_transaction(self.editing_transaction_id)

        self.after(1000)

        self.editing_transaction_id = None
        self.edit_mode = False
        self.editing_index = None

        self.clear_form_fields()
        self.fill_records()

        self.reset_button_selection_text()


    def empty_attempt_variable(self):
        self.attempt_variable.set("")

    def reset_button_selection_text(self):
        for ind in range(len(self.record_button_text)):
            self.record_button_text[ind].set("Select Transaction")
            self.record_box[ind][0].config(relief="raised")
            self.record_box[ind][1].config(bg=self.button_color_default)


    def validate_transaction(self):

        if self.cost_box.get() == "":
            self.attempt_variable.set("Missing required field: cost")
            self.attempt_status.config(fg="red")

            self.after(3000, self.empty_attempt_variable)
            return False


        elif self.category_text.get().strip() == "":
            self.attempt_variable.set("Missing required field: category")
            self.attempt_status.config(fg="red")

            self.after(3000, self.empty_attempt_variable)
            return False

        elif self.date_box.get() == "":
           self.attempt_variable.set("Missing required field: date")
           self.attempt_status.config(fg="red")

           self.after(3000, self.empty_attempt_variable)
           return False


        try:
            val = float(self.cost_box.get())

        except ValueError:
            self.attempt_variable.set("Cost contains unsupported\n characters")
            self.attempt_status.config(fg="red")

            self.after(3000, self.empty_attempt_variable)
            return False


        try:
            parsed_date_components = str(datetime.datetime.strptime(self.date_box.get(), "%Y-%m-%d")).split()[0].split("-")
            parsed_date = "-".join([parsed_date_components[0], parsed_date_components[1], parsed_date_components[2]])

        except ValueError:
            self.attempt_variable.set("Requires a valid date\n in YYYY-MM-DD format")
            self.attempt_status.config(fg="red")

            self.after(3000, self.empty_attempt_variable)
            return False


        if self.edit_mode: # and add_while_edit:

            edit_transaction(self.user_id, self.editing_transaction_id, self.date_box.get(), self.category_text.get(), self.cost_box.get(), self.details_box.get("1.0", "end-1c"))
            self.attempt_variable.set("Transaction has been\n successfully edited!")
            self.attempt_status.config(fg="green")

            self.reset_button_selection_text()

            self.edit_mode = False

            self.add_transaction_button.config(state='active')
            self.delete_transaction_button.config(state="disabled")

            self.clear_form_fields()
            self.fill_records()

            self.after(3000, self.empty_attempt_variable)
            return True

        else:
            self.reset_button_selection_text()

            add_transaction(self.user_id, parsed_date, self.category_text.get(), val, self.details_box.get("1.0", "end-1c"))
            self.clear_form_fields()
            self.fill_records()

            self.attempt_variable.set("Transaction has been\n successfully posted!")
            self.attempt_status.config(fg="green")

            self.after(3000, self.empty_attempt_variable)
            return True



class Transaction:

    def __init__(self, transaction_id, date, category, cost, details):
        self.transaction_id = transaction_id
        self.date = date
        self.category = category
        self.cost = "{:.2f}".format(float(cost))
        self.details = details

    def get_info(self):
        return (self.date, self.category, self.cost, self.details)


    def format_info(self):
        formatted_details = "\t".join(self.details.split("\n"))
        return f"({self.date})\n{self.category}: {self.cost}\n{formatted_details}"


    def __lt__(self, other):
        if self.transaction_id < other.transaction_id:
            return self

        else:
            return other


class Stack:

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def __len__(self):
        return len(self.items)

    def push(self, item):
        self.items.append(item)
        self.items = sorted(self.items, key=(lambda x: x.date), reverse=True)


    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def push_list(self, items):
        for i in items:
            self.push(i)

        self.items = sorted(self.items, key=(lambda x: x.date), reverse=True)


    def pop_all(self, output_list):
        for _ in self.items:
            output_list.append(self.pop())

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        self.items[index] = value


# for testing
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")

    TransactionManager(root, '1').grid()
    root.mainloop()
