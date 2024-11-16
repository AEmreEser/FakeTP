#!/opt/homebrew/bin/python3
import tkinter as tk

root = tk.Tk()

test_label = tk.Label(root, text="test widget")
test_label.grid(column=0, row=0, sticky='SWEN')

test_label.columnconfigure(0, weight=1)
test_label.rowconfigure(0, weight=1)

root.mainloop()
