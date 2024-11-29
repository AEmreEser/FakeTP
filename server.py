import socket
import threading
import os
import argparse
import tkinter as tk
from tkinter import messagebox

# 
# Ahmet Emre Eser - 28/11/24
#

clients = {}  # Dictionary to store client names and their connections
files = {}    # Dictionary to store filenames and their owners
lock = threading.Lock()

def handle_client(conn, addr):
    dup_name = False
    try:
        client_name = conn.recv(1024).decode()
        with lock:
            if client_name in clients:
                conn.send(b"ERROR: Name already in use.\n")
                log_message(f"ERROR: Name already in use.\n")
                dup_name = True
                conn.close()
                ic(clients)
                return
            else:
                clients[client_name] = conn
                ic(clients)
                conn.send(b"Welcome!\n")
        print(f"{client_name} connected from {addr}.")
        log_message(f"{client_name} connected from {addr}.")

        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            command, *args = data.split()

            if command == 'UPLOAD':
                handle_upload(conn, client_name, args)
            elif command == 'DOWNLOAD':
                handle_download(conn, client_name, args)
            elif command == 'DELETE':
                handle_delete(conn, client_name, args)
            elif command == 'LIST':
                handle_list(conn)
            else:
                conn.send(b"ERROR: Invalid command.\n")
                log_message(f"ERROR: Invalid command.\n")

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
        log_message(f"Error handling client {addr}: {e}")

    finally:
        with lock:
            if not dup_name: # bug fix 1 - should not delete the client if the connection is duplicate
                del clients[client_name]

            conn.close()
            if not dup_name:
                print(f"{client_name} disconnected.")
                log_message(f"{client_name} disconnected.")
            else:
                print(f"Duplicate {client_name} disconnected.")
                log_message(f"Duplicate {client_name} disconnected.")

def handle_upload(conn, client_name, args):
    if len(args) != 1:
        conn.send(b"ERROR: Invalid arguments for UPLOAD.\n")
        log_message(f"ERROR: Invalid arguments for UPLOAD.\n")
        return

    filename = args[0]
    full_path = os.path.join(STORAGE_PATH, f"{client_name}_{filename}")

    send_msg = b""

    if os.path.exists(full_path): # checks only files, not directories
        send_msg += (b"File will be overwritten.\n")

    with open(full_path, 'wb') as f:
        while True:
            data = conn.recv(1024)
            # if data.endswith(b"EOF"):
            if data.endswith((chr(26).encode())):
                f.write(data[:-3])
                break
            f.write(data)

    with lock:
        files[full_path] = client_name
    conn.send(send_msg + b"File uploaded successfully.\n")
    print(f"{client_name} uploaded {filename}.")
    log_message(f"{client_name} uploaded {filename}.")

def handle_download(conn, client_name, args):
    if len(args) != 2:
        conn.send(b"ERROR: Invalid number of arguments for DOWNLOAD.\n")
        log_message(f"ERROR: Invalid number of arguments for DOWNLOAD.\n")
        return

    owner, filename = args
    full_path = os.path.join(STORAGE_PATH, f"{owner}_{filename}")

    if not os.path.exists(full_path):
        conn.send(b"ERROR: File not found.\n")
        log_message(f"ERROR: File not found.\n")
        return
    
    file_size = os.path.getsize(full_path)
    conn.send(str(file_size).encode())
    socket.setdefaulttimeout(30.0) # in case the client does not answer
    try:
        conn.recv(1024)
    except TimeoutError:
        print("ACK timedout")
        log_message("ACK timedout")
        return
    
    with open(full_path, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            conn.send(data)
    # conn.send(b"EOF") # no need now
    print(f"{client_name} downloaded {filename} from {owner}.")
    log_message(f"{client_name} downloaded {filename} from {owner}.")

def handle_delete(conn, client_name, args):
    if len(args) != 1:
        conn.send(b"ERROR: Invalid number of arguments for DELETE.\n")
        log_message(f"ERROR: Invalid number of arguments for DELETE.\n")
        return

    filename = args[0]
    full_path = os.path.join(STORAGE_PATH, f"{client_name}_{filename}")
    ic(full_path)

    with lock:
        if full_path in files and files[full_path] == client_name:
            os.remove(full_path)
            del files[full_path]
            ic(files)
            conn.send(b"File deleted successfully.\n")
            print(f"{client_name} deleted {filename}.")
            log_message(f"{client_name} deleted {filename}.")
        else:
            conn.send(b"ERROR: File not found or permission denied.\n")
            log_message(f"ERROR: File not found or permission denied.\n")

# used in recovering the file list after the server is restarted
def recreate_files_dict(storage_path):
    global files
    for file in os.listdir(storage_path):
        full_path = os.path.join(storage_path, file)
        if os.path.exists(full_path):
            owner, orig_file = file.split('_', 1)
            files[full_path] = owner
    ic(files)

def handle_list(conn):
    with lock:
        file_list = "\n".join([f"{owner}: {(os.path.basename(file)).split('_', 1)[1]}" for file, owner in files.items()])
    conn.send(file_list.encode() + b"\n")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recreate_files_dict(STORAGE_PATH)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)
    print(f"Server listening on {HOST}:{PORT}")
    log_message(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

HOST = None
PORT = None
STORAGE_PATH = None
MAX_CONNECTIONS = None
DEBUG = False
status_box = None
server_started = False

def log_message(message):
    global status_box
    status_box.config(state=tk.NORMAL)
    status_box.insert(tk.END, f"{message}\n")
    status_box.yview(tk.END)  # Automatically scroll to the bottom
    status_box.config(state=tk.DISABLED)

def start_server_thread(host, port, storage_path, max_connections):
    global server_started
    if server_started:
        return
    else:
        server_started = True

    global HOST, PORT, STORAGE_PATH, MAX_CONNECTIONS
    HOST = host
    PORT = int(port)
    STORAGE_PATH = storage_path
    MAX_CONNECTIONS = int(max_connections)

    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)
    
    def server_thread():
        start_server()

    threading.Thread(target=server_thread).start()

def start_server_gui():
    def start_server_button():
        global server_started
        if not server_started:
            host = host_entry.get()
            port = port_entry.get()
            storage_path = storage_path_entry.get()
            max_connections = max_conn_entry.get()

            start_server_thread(host, port, storage_path, max_connections)
            messagebox.showinfo("Server", "Server started!")
        else:
            log_message("Server is already running.")


    root = tk.Tk()
    root.title("File Transfer Server")
    root.minsize(675, 200)

    tk.Label(root, text="Host:").grid(row=0, sticky='ENS')
    tk.Label(root, text="Port:").grid(row=1, sticky='ENS')
    tk.Label(root, text="Storage Path:").grid(row=2, sticky='ENS')
    tk.Label(root, text="Max Connections:").grid(row=3, sticky='ENS')

    host_entry = tk.Entry(root)
    port_entry = tk.Entry(root)
    storage_path_entry = tk.Entry(root)
    max_conn_entry = tk.Entry(root)

    host_entry.grid(row=0, column=1, sticky='WNS')
    port_entry.grid(row=1, column=1, sticky='WNS')
    storage_path_entry.grid(row=2, column=1, sticky='WNS')
    max_conn_entry.grid(row=3, column=1, sticky='WNS')

    tk.Button(root, text="Start Server", command=start_server_button).grid(row=4, column=1, sticky='WNS')

    # Status Display Box
    status_box_label = tk.Label(root, text="Server Status")
    status_box_label.grid(row=4, column=3, columnspan=2, sticky='N')
    
    global status_box
    status_box = tk.Text(root, height=10, width=50, wrap=tk.WORD)
    status_box.grid(row=0, column=3, padx=10, pady=5, rowspan=4, columnspan=2, sticky='EN')
    status_box.config(state=tk.DISABLED)  # Set to read-only

    root.mainloop()

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("--debug", action='store_true')
    args = parse.parse_args()
    DEBUG = args.debug
    if not DEBUG:
        def ic(*args):
            return
    else:
        try:
            from icecream import ic
        except ImportError:
            print("Icecream could not be imported, using print() for debugging instead.")
            def ic(*args):
                print(args)

    start_server_gui()
