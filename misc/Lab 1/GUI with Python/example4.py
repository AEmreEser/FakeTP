import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Form1")

# Function to handle submit button click
def submit():
    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Age: {age_var.get()}\n")
    output_box.insert(tk.END, f"Gender: {gender_var.get()}\n")
    output_box.config(state=tk.DISABLED)

# Age options (Radio buttons)
age_var = tk.StringVar(value="less than 18")
age_frame = tk.LabelFrame(root, text="Age")
age_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Radiobutton(age_frame, text="less than 18", variable=age_var, value="less than 18").grid(row=0, column=0, sticky="w")
tk.Radiobutton(age_frame, text="Between 18-35", variable=age_var, value="Between 18-35").grid(row=1, column=0, sticky="w")
tk.Radiobutton(age_frame, text="greater than 35", variable=age_var, value="greater than 35").grid(row=2, column=0, sticky="w")

# Gender options (Radio buttons)
gender_var = tk.StringVar(value="female")
gender_frame = tk.LabelFrame(root, text="Gender")
gender_frame.grid(row=1, column=0, padx=10, pady=10)

tk.Radiobutton(gender_frame, text="female", variable=gender_var, value="female").grid(row=0, column=0, sticky="w")
tk.Radiobutton(gender_frame, text="male", variable=gender_var, value="male").grid(row=1, column=0, sticky="w")

# Output box (read-only)
output_box = tk.Text(root, width=30, height=5, state=tk.DISABLED)
output_box.grid(row=2, column=0, padx=10, pady=10)

# Submit button
submit_btn = tk.Button(root, text="submit", command=submit)
submit_btn.grid(row=3, column=0, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
