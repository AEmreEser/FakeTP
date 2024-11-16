import tkinter as tk

# Create the main window
root = tk.Tk()


# Different sticky value
sticky_entry = tk.Entry(root)
sticky_entry.grid(row=0, column=0, padx=10, pady=10, sticky="NWE")

root.grid_columnconfigure(0,weight=1)
root.grid_rowconfigure(0,weight=1)

root.mainloop()