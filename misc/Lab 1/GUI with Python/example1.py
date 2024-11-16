#! /opt/homebrew/bin/python3
import tkinter as tk
from tkinter import DISABLED, NORMAL

# Create the main window
root = tk.Tk()


# Define function to enable/disable buttons
def connect():
    if(id_entry.get() != "" and pass_entry.get() != ""):
        connect_btn.config(state=DISABLED)
        disconnect_btn.config(state=NORMAL)
        send_btn.config(state=NORMAL)
        send_entry.config(state=NORMAL)
        message_box.config(state=NORMAL)  
        message_box.insert(tk.END, "CONNECTED\n")  
        message_box.config(state=DISABLED)
    else:
        message_box.config(state=NORMAL)
        message_box.delete("1.0",tk.END)  
        message_box.insert(tk.END, "ID AND PASS CANNOT BE EMPTY\n")  
        message_box.config(state=DISABLED)


def disconnect():
    connect_btn.config(state=NORMAL)
    disconnect_btn.config(state=DISABLED)
    send_btn.config(state=DISABLED)
    send_entry.config(state=DISABLED)
    message_box.config(state=NORMAL)  
    message_box.delete("1.0", tk.END)  
    message_box.config(state=DISABLED)
    id_entry.delete(0,tk.END)
    pass_entry.delete(0,tk.END)

def send_message(event): # we didn't use the event object -- because this is a small example 
    message = send_entry.get()  # Get the message from the entry field
    if message.strip():  # Check if the message is not empty
        message_box.config(state=NORMAL)  # Enable the message box to insert text
        message_box.insert(tk.END, message + "\n")  # Append message to the text box
        message_box.config(state=DISABLED)  # Disable the message box to make it read-only again
        send_entry.delete(0, tk.END)  # Clear the send entry field

# ID Label and Entry
id_label = tk.Label(root, text="id")
id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")

# Password Label and Entry
pass_label = tk.Label(root, text="pass")
pass_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
pass_entry = tk.Entry(root, show='*')
pass_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")

# Connect Button
connect_btn = tk.Button(root, text="connect", command=connect)
connect_btn.grid(row=0, column=2, padx=10, pady=10)

# Disconnect Button (initially disabled)
disconnect_btn = tk.Button(root, text="disconnect", state=DISABLED, command=disconnect)
disconnect_btn.grid(row=1, column=2, padx=10, pady=10)

# Large Text Box for displaying messages (disabled for typing)
message_box = tk.Text(root, width=35, height=8, state=DISABLED,)
message_box.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="WSEN")

# Entry field for sending messages
send_entry = tk.Entry(root, state=DISABLED)
send_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

# Send Button (initially disabled)
send_btn = tk.Button(root, text="send", state=DISABLED)
send_btn.bind("<Button>", send_message)
send_btn.grid(row=3, column=2, padx=10, pady=10)

# # Make the entry field and message box expandable
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

# Run the Tkinter event loop
root.mainloop()