import socket as sk
from threading import Thread
from argparse import ArgumentParser
import tkinter as tk
import os

#
# Ahmet Emre Eser - CS408 Fall24-25 Term Project
#

# Tied to the "--debug"/"-d" cmd line argument
DEBUG=False
# Default values - overridden unless DEBUG argument is provided
HOST="127.0.0.1"
PORT="8080"
STOR=os.getcwd() + "/server-storage"

config_gui = tk.Tk()
config_gui.title("Server Monitor - Config Page")
config_gui.rowconfigure([0,1,2,3,4,5], minsize=10, weight=1)
config_gui.columnconfigure([0,1,2,3,4,5], minsize=10, weight=1)

sv_input_frame = tk.Frame(master=config_gui, relief=tk.RIDGE)
sv_input_frame.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")

ip_in_label = tk.Label(master=sv_input_frame, text="Server IP address:")
ip_in_ent   = tk.Entry(master=sv_input_frame, width=40)
ip_in_label.grid(row=0, column=0, sticky="ew")
ip_in_ent.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

port_in_label = tk.Label(master=sv_input_frame, text="Server port:")
port_in_ent   = tk.Entry(master=sv_input_frame, width=40)
port_in_label.grid(row=1, column=0, sticky="ew")
port_in_ent.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

storage_path_label = tk.Label(master=sv_input_frame, text="Storage path: ")
storage_path_ent = tk.Entry(master=sv_input_frame, width=40)
storage_path_label.grid(row=2, column=0, sticky="ew")
storage_path_ent.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

status_label = tk.Text(master=config_gui, wrap='word', width=40, height=2, padx=5, pady=5, state=tk.DISABLED)
status_label.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

# only works with label widgets
def update_label(lbl, s):
    lbl.config(state=tk.NORMAL)
    lbl.delete(1.0, tk.END)
    lbl.insert(tk.END, s)
    lbl.config(state=tk.DISABLED)

# this is the actual connection loop
def sv_main():
    global status_label
    port = port_in_ent.get()
    host = ip_in_ent.get()
    stor = storage_path_ent.get() # TODO: we need to use the os's file picker window for this!!!
    if (port == '' or port == None or not port.isnumeric() or host == '' or host == None or host.count('.') != 3 or stor == '' or stor == None or not os.path.isdir(stor)):
        print("Bad input - cannot start server") # TODO: need to display this to the user!!!
        update_label(status_label, "Bad input - cannot start server")
        return #with nothing...
    else:
        global PORT, HOST, STOR
        (PORT, HOST, STOR) = (port, host, stor)
        print(f"Starting server with {HOST}:{PORT}:{STOR}")
        update_label(status_label, f"Starting server with {HOST}:{PORT}:{STOR}")
        config_gui.destroy()

btn_start_sv = tk.Button(master=config_gui, text="Start", relief=tk.RAISED, borderwidth=2, command=sv_main)
btn_start_sv.grid(row=3, column=0, padx=5, pady=5)

def sv_config():
    global config_gui
    config_gui.mainloop()

#
# main:
if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true", help="Turns on debug mode")
    args = parser.parse_args()
    DEBUG=args.debug

    if DEBUG: # initialize the fields with default values so that I don't have to type them everytime!!
        port_in_ent.insert(tk.END, PORT)
        ip_in_ent.insert(tk.END, HOST)
        storage_path_ent.insert(tk.END, STOR)

    sv_config()
