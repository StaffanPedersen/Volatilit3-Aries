import tkinter as tk
from tkinter import ttk


class CustomCheckbutton(tk.Canvas):
    def __init__(self, master=None, text="", variable=None, **kwargs):
        super().__init__(master, width=200, height=30, bg="black", highlightthickness=0)
        self.variable = variable
        self.text = text
        self.configure(**kwargs)

        # Draw text
        self.text_id = self.create_text(10, 15, anchor="w", text=self.text, fill="white", font=("Helvetica", 12))

        # Draw round checkbox
        self.circle = self.create_oval(170, 7, 190, 27, outline="white", fill="black")
        self.bind("<Button-1>", self.toggle)

    def toggle(self, event):
        if self.variable.get():
            self.itemconfig(self.circle, fill="black")
            self.variable.set(False)
        else:
            self.itemconfig(self.circle, fill="orange")
            self.variable.set(True)


def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Filter")
    root.geometry("300x400")
    root.configure(bg='black')

    # Create a frame to hold the list items
    frame = tk.Frame(root, bg='black')
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # List of items to toggle
    items = [
        "PID",
        "PPID",
        "Name",
        "Offset",
        "Threads",
        "Handles",
        "Session-ID",
        "Win Version",
        "Creation Time",
        "Exit Time",
        "File Info",
        "Output"
    ]

    # Create a variable for each item to hold its state
    item_vars = {item: tk.BooleanVar() for item in items}

    # Create custom checkbuttons for each item
    for item, var in item_vars.items():
        chk = CustomCheckbutton(frame, text=item, variable=var)
        chk.pack(fill="x", pady=5)

    # Run the main event loop
    root.mainloop()