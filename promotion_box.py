import tkinter as tk
from tkinter import simpledialog

class PromotionDialog(simpledialog.Dialog):
    def __init__(self, parent, title, options):
        self.options = options
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text="Choose a piece for promotion:").grid(row=0, column=0, columnspan=4)
        for i, option in enumerate(self.options):
            tk.Button(master, text=option, command=lambda o=option: self.ok(o)).grid(row=1, column=i)
        return master

    def apply(self):
        # This method is called when the OK button is clicked
        self.result = self.choice

    def ok(self, value):
        # Store the choice and close the dialog
        self.choice = value
        self.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    dialog = PromotionDialog(root, "Promotion", ["Queen", "Rook", "Bishop", "Knight"])
    print(dialog.result)
    # root.mainloop()

    # Now you can print the result after the dialog is closed
