import socket
import os
import argparse
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog # for some reason tkinter cannto find these 

# 
# Ahmet Emre Eser - 28/11/24
#

def connect_to_server(client_name, host, port):
    # socket.setdefaulttimeout(10.0) # no need after bugfix2
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
    except ConnectionRefusedError:
        print("ERROR: Connection refused. Are you sure that the ip and port paraemters provided are correct?")
        log_message("ERROR: Connection refused. Are you sure that the ip and port paraemters provided are correct?")
        exit(1)
    conn.send(client_name.encode())
    response = conn.recv(1024).decode()
    if response.startswith("ERROR"):
        print(response)
        conn.close()
        return None
    print(response)
    return conn

def upload_file(conn, filename):
    if conn == None:
        print("You have to connect to the server first.")
        log_message("You have to connect to the server first.")
        return

    if not os.path.exists(filename):
        print("File does not exist.")
        log_message("File does not exist.")
        return

    conn.send(f"UPLOAD {os.path.basename(filename)}".encode())
    with open(filename, 'rb') as f:
        while (data := f.read(1024)):
            conn.send(data)
    eof = chr(26) # supposedly many systems today don't actually use this EOF character
    # conn.send(b"EOF")
    conn.send(eof.encode())
    rec = conn.recv(1024).decode()
    print(rec)
    log_message(rec)

def download_file(conn, owner, filename, save_path):
    if conn == None:
        print("You have to connect to the server first.")
        log_message("You have to connect to the server first.")
        return

    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    conn.send(f"DOWNLOAD {owner} {filename}".encode())
    response = conn.recv(1024).decode()
    if response.startswith("ERROR"):
        print(response)
        log_message(response)
        return
    file_size = int(response)
    conn.send(b"ACK") # the actual bytes don't matter, all that matters is that we send smt

    received = 0
    try:
        with open(os.path.join(save_path, filename), 'wb') as f:
            while received < file_size:
                data = conn.recv(1024)
                if data:
                    received += len(data)
                    f.write(data)
            print("File downloaded successfully.")
            log_message("File downloaded successfully.")
            if DEBUG:
                assert(received == file_size) # caught below, does not crash the client
    except AssertionError as ae:
        print("Received > filesize")
        return
    except BrokenPipeError as ose:
        print("Error with connection. Possible reasons: 1)The client quit 2)You were inactive for some time")
        log_message("Error with connection. Possible reasons: 1)The client quit 2)You were inactive for some time")
        return
    except OSError as ose:
        print(f"Error finding {filename}. Possible reasons: 1)File does not exist 2)You made a typo)")
        log_message(f"Error finding {filename}. Possible reasons: 1)File does not exist 2)You made a typo)")
        return
    except Exception as e:
        print("Errors encountered")
        log_message("Errors encountered")
        return


def delete_file(conn, filename):
    if conn == None:
        print("You have to connect to the server first.")
        log_message("You have to connect to the server first.")
        return

    conn.send(f"DELETE {filename}".encode())
    rec = conn.recv(1024).decode()
    print(rec)
    log_message(rec)

def list_files(conn):
    if conn == None:
        print("You have to connect to the server first.")
        log_message("You have to connect to the server first.")
        return

    try:
        conn.send(b"LIST")
        rec = conn.recv(1024).decode()
        print(rec)
        log_message(rec)
    except BrokenPipeError as ose:
        print("Error with connection. Possible reasons: The client quit")
        log_message("Error with connection. Possible reasons: The client quit")
        return
    except Exception as e:
        print("Unknown error occurred")
        log_message("Unknown error occurred")
        return


def start_client_gui():
    def browse_savepath():
        folder_selected = filedialog.askdirectory()
        savepath.set(folder_selected)

    def connect():
        global conn
        client_name = client_name_entry.get()
        host = host_entry.get()
        port = int(port_entry.get())
        if not client_name or not host or not port:
            messagebox.showerror("Input Error", "Please provide client name, host, and port.")
            return

        conn = connect_to_server(client_name, host, port)
        if conn:
            # messagebox.showinfo("Connection", f"Connected to {host}:{port}")
            log_message(f"Connected to {host}:{port}")

    def upload():
        global conn
        filename = filedialog.askopenfilename()
        if filename:
            upload_file(conn, filename)

    def download():
        global conn
        nonlocal savepath_entry
        ic(savepath_entry)
        filename = simpledialog.askstring("Filename", "Enter the filename to download:")
        owner = simpledialog.askstring("Owner", "Enter the owner of the file:")
        if filename:
            download_file(conn, owner, filename, savepath_entry.get())

    def delete():
        global conn
        filename = simpledialog.askstring("Filename", "Enter the filename to delete:")
        if filename:
            delete_file(conn, filename)

    def list_files_func():
        global conn
        list_files(conn)

    root = tk.Tk()
    root.title("File Transfer Client")
    root.minsize(650, 200)

    client_name = tk.StringVar()
    host = tk.StringVar()
    port = tk.IntVar()
    savepath = tk.StringVar()

    tk.Label(root, text="Client Name:").grid(row=0, column=0, sticky='ENS')
    client_name_entry = tk.Entry(root, textvariable=client_name)
    client_name_entry.grid(row=0, column=1, stick='WNS')

    tk.Label(root, text="Host:").grid(row=1, column=0, sticky='ENS')
    host_entry = tk.Entry(root, textvariable=host)
    host_entry.grid(row=1, column=1, stick='WNS')

    tk.Label(root, text="Port:").grid(row=2, column=0, sticky='ENS')
    port_entry = tk.Entry(root, textvariable=port)
    port_entry.grid(row=2, column=1, sticky='WNS')

    tk.Label(root, text="Save Path:").grid(row=3, column=0, stick='ENS')
    savepath_entry = tk.Entry(root, textvariable=savepath)
    savepath_entry.grid(row=3, column=1, stick='WNS')
    tk.Button(root, text="Browse", command=browse_savepath).grid(row=3, column=2, sticky='N')

    tk.Button(root, text="Connect", command=connect).grid(row=4, column=0, columnspan=1, sticky='N')
    tk.Button(root, text="Upload", command=upload).grid(row=4, column=1, columnspan=1, sticky='N')
    tk.Button(root, text="Download", command=download).grid(row=4, column=2, columnspan=1, sticky='N')
    tk.Button(root, text="Delete", command=delete).grid(row=4, column=3, columnspan=1, sticky='N')
    tk.Button(root, text="List Files", command=list_files_func).grid(row=4, column=4, columnspan=1, sticky='N')

    global status_box
    status_box = tk.Text(root, height=10, width=50, wrap=tk.WORD)
    status_box.grid(row=0, column=2, rowspan=4, padx=10, pady=5, columnspan=3)
    status_box.config(state=tk.DISABLED)  # Set to read-only

    root.mainloop()


# PORT = None
# HOST = None
# SAVEPATH = None
conn = None
status_box = None

def log_message(message):
    global status_box
    status_box.config(state=tk.NORMAL)
    status_box.insert(tk.END, f"{message}\n")
    status_box.yview(tk.END)  # Automatically scroll to the bottom
    status_box.config(state=tk.DISABLED)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action='store_true', help="enable debug mode")
    args = parser.parse_args()
    DEBUG = args.debug

    if DEBUG:
        try:
            from icecream import ic
        except ImportError:
            print("Looks like icecream is not installed on your machine, using print() for debugging instead.")
            def ic(*args):
                print(args)
    else:
        # removes all debug print statements
        def ic(*args):
            return
    
    start_client_gui()