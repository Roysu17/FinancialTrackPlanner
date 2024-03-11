import tkinter as tk
from login import LoginWindow

def main():
    root = tk.Tk()
    app = LoginWindow(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
