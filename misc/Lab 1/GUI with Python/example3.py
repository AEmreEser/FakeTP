import tkinter as tk

# Create the main window
root = tk.Tk()

# Function to handle submit button click
def submit():
    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Like Icecream: {icecream_var.get()==1}\n")
    output_box.insert(tk.END, f"Like Cake: {cake_var.get()==1}\n")
    output_box.config(state=tk.DISABLED)

# Function to handle clear button click
def clear():
    icecream_var.set(0)
    cake_var.set(0)
    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)
    output_box.config(state=tk.DISABLED)

# Variables for checkboxes
icecream_var = tk.IntVar()
cake_var = tk.IntVar()

# Checkboxes
icecream_cb = tk.Checkbutton(root, text="Like Icecream?", variable=icecream_var)
icecream_cb.grid(row=0, column=0, sticky="w", padx=10, pady=5)

cake_cb = tk.Checkbutton(root, text="Like Cake?", variable=cake_var)
cake_cb.grid(row=1, column=0, sticky="w", padx=10, pady=5)

# Submit and Clear buttons
submit_btn = tk.Button(root, text="Submit", command=submit)
submit_btn.grid(row=2, column=0, padx=10, pady=10, sticky="e")

clear_btn = tk.Button(root, text="Clear", command=clear)
clear_btn.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Output box (read-only)
output_box = tk.Text(root, width=30, height=5, state=tk.DISABLED)
output_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()