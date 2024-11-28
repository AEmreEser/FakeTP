import socket
import threading
import os
import argparse

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
                dup_name = True
                conn.close()
                ic(clients)
                return
            else:
                clients[client_name] = conn
                ic(clients)
                conn.send(b"Welcome!\n")
        print(f"{client_name} connected from {addr}.")

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

    except Exception as e:
        print(f"Error handling client {addr}: {e}")

    finally:
        with lock:
            if not dup_name: # bug fix 1 - should not delete the client if the connection is duplicate
                del clients[client_name]

            conn.close()
            if not dup_name:
                print(f"{client_name} disconnected.")
            else:
                print(f"Duplicate {client_name} disconnected.")

def handle_upload(conn, client_name, args):
    if len(args) != 1:
        conn.send(b"ERROR: Invalid arguments for UPLOAD.\n")
        return

    filename = args[0]
    full_path = os.path.join(STORAGE_PATH, f"{client_name}_{filename}")

    if os.path.exists(full_path): # checks only files, not directories
        conn.send(b"File will be overwritten.\n")

    with open(full_path, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if data.endswith(b"EOF"):
                f.write(data[:-3])
                break
            f.write(data)

    with lock:
        files[full_path] = client_name
    conn.send(b"File uploaded successfully.\n")
    print(f"{client_name} uploaded {filename}.")

def handle_download(conn, client_name, args):
    if len(args) != 2:
        conn.send(b"ERROR: Invalid arguments for DOWNLOAD.\n")
        return

    ic(args)

    owner, filename = args
    full_path = os.path.join(STORAGE_PATH, f"{owner}_{filename}")

    if not os.path.exists(full_path):
        conn.send(b"ERROR: File not found.\n")
        return

    with open(full_path, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            conn.send(data)
    conn.send(b"EOF")
    conn.send(b"File downloaded successfully.\n")
    print(f"{client_name} downloaded {filename} from {owner}.")

def handle_delete(conn, client_name, args):
    if len(args) != 1:
        conn.send(b"ERROR: Invalid arguments for DELETE.\n")
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
        else:
            conn.send(b"ERROR: File not found or permission denied.\n")

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
        file_list = "\n".join([f"{owner}: {os.path.basename(file)}" for file, owner in files.items()])
    conn.send(file_list.encode() + b"\n")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recreate_files_dict(STORAGE_PATH)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

HOST = None
PORT = None
STORAGE_PATH = None
MAX_CONNECTIONS = None
DEBUG = False

if __name__ == "__main__":
    # Configuration
    startup_logo = """
 ______      _       _______  _____     _____                               
|  ____|    | |     |__   __||  __ \\   / ____|                              
| |__  __ _ | | __ ___ | |   | |__) | | (___    ___  _ __ __   __ ___  _ __ 
|  __|/ _` || |/ // _ \\| |   |  ___/   \\___ \\  / _ \\| '__|\\ \\ / // _ \\| '__|
| |  | (_| ||   <|  __/| |   | |       ____) ||  __/| |    \\ V /|  __/| |   
|_|   \\__,_||_|\\_\\\\___||_|   |_|      |_____/  \\___||_|     \\_/  \\___||_|   
                                                                             
"""

    print(startup_logo)

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default="8888")
    parser.add_argument("--storage", type=str, default="./server_storage", help="Server's storage folder path")
    parser.add_argument("--maxconn", type=int, default=5, help="Maximum number of tcp connections")
    parser.add_argument("--debug", action='store_true', help="Print debug info")
    args = parser.parse_args()
    HOST, PORT, STORAGE_PATH, DEBUG, MAX_CONNECTIONS = args.ip, args.port, args.storage, args.debug, args.maxconn

    # debug print routine
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

    # Ensure the storage directory exists
    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)

    start_server()