#! /opt/homebrew/bin/python3
import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()


# Function to handle adding items
def add_item():
    item = add_entry.get()
    if item:
        item_listbox.config(state=tk.NORMAL)
        item_listbox.insert(tk.END, item)
        item_listbox.config(state=tk.DISABLED)
        combobox['values'] = item_listbox.get(0, tk.END)  # Update combobox with Listbox items
        add_entry.delete(0, tk.END)

# Function to handle removing the selected item from combobox
def remove_item():
    selected_item = combobox.get()
    if selected_item != "Select item":  # Ensure a valid item is selected
        # Find the index of the selected item in the Listbox and delete it
        index = item_listbox.get(0, tk.END).index(selected_item)
        item_listbox.config(state=tk.NORMAL)
        item_listbox.delete(index)
        item_listbox.config(state=tk.DISABLED)
        # Update combobox options after removing the item
        combobox['values'] = item_listbox.get(0, tk.END)
        combobox.set("Select item")  # Reset the combobox selection

# Entry for adding items
add_entry = tk.Entry(root)
add_entry.grid(row=0, column=0, padx=10, pady=10)

# Add button
add_btn = tk.Button(root, text="Add", command=add_item)
add_btn.grid(row=0, column=1, padx=10, pady=10)

# Listbox for items (disabled for selection)
item_listbox = tk.Listbox(root, width=30, height=5, selectmode=tk.SINGLE)
item_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
item_listbox.config(state=tk.DISABLED)  # Disable manual selection

# Combobox (Dropdown) for selecting items to remove
combobox = ttk.Combobox(root, values=[], state="readonly")  # Readonly to disable typing
combobox.grid(row=2, column=0, padx=10, pady=10)
combobox.set("Select item")  # Set default placeholder

# Remove button
remove_btn = tk.Button(root, text="Remove", command=remove_item)
remove_btn.grid(row=2, column=1, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
