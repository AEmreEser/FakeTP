import socket
import os
import argparse

# 
# Ahmet Emre Eser - 28/11/24
#

def connect_to_server(client_name):
    # socket.setdefaulttimeout(10.0) # no need after bugfix2
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("ERROR: Connection refused, are you sure that the ip and port paraemters provided are correct?")
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
    if not os.path.exists(filename):
        print("File does not exist.")
        return

    conn.send(f"UPLOAD {os.path.basename(filename)}".encode())
    with open(filename, 'rb') as f:
        while (data := f.read(1024)):
            conn.send(data)
    conn.send(b"EOF")
    print(conn.recv(1024).decode())

# def download_file(conn, owner, filename, save_path):
#     conn.send(f"DOWNLOAD {owner} {filename}".encode())
#     response = conn.recv(1024).decode()
#     if response.startswith("ERROR"):
#         print(response)
#         return

#     try:
#         with open(os.path.join(save_path, filename), 'wb') as f:
#             while True:
#                 data = conn.recv(1024)
#                 if data.endswith(b"EOF"):
#                     f.write(data[:-3])
#                     break
#                 f.write(data)
#         print("File downloaded successfully.")
#     except TimeoutError as te:
#         print("Download timed out")
#         return
#     except OSError as ose:
#         print(f"Error opening {filename}. Possible reasons: File does not exist (ie. you made a typo)")
#         return
#     except Exception as e:
#         print("Errors encountered")
#         return

def download_file(conn, owner, filename, save_path):
    conn.send(f"DOWNLOAD {owner} {filename}".encode())
    response = conn.recv(1024).decode()
    if response.startswith("ERROR"):
        print(response)
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
            if DEBUG:
                assert(received == file_size) # caught below, does not crash the client
    except AssertionError as ae:
        print("Received > filesize")
        return
    except BrokenPipeError as ose:
        print("Error with connection. Possible reasons: The client quit")
        return
    except OSError as ose:
        print(f"Error opening {filename}. Possible reasons: File does not exist (ie. you made a typo)")
        return
    except Exception as e:
        print("Errors encountered")
        return


def delete_file(conn, filename):
    conn.send(f"DELETE {filename}".encode())
    print(conn.recv(1024).decode())

def list_files(conn):
    try:
        conn.send(b"LIST")
        print(conn.recv(1024).decode())
    except BrokenPipeError as ose:
        print("Error with connection. Possible reasons: The client quit")
        return
    except Exception as e:
        print("Unknown error occurred")
        return


PORT = None
HOST = None
SAVEPATH = None

if __name__ == "__main__":
    startup_logo = """
______      _        _____ ______ 
|  ___|    | |      |_   _|| ___ \\
| |_  __ _ | | __ ___ | |  | |_/ /
|  _|/ _` || |/ // _ \\| |  |  __/ 
| | | (_| ||   <|  __/| |  | |    
\\_|  \\__,_||_|\\_\\\\___|\\_/  \\_|    by Emre Eser

"""

    print(startup_logo)

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="ip of the server")
    parser.add_argument("--port", type=int, default="8888", help="port of the server app")
    parser.add_argument("--name", type=str, help="Username of the client")
    parser.add_argument("--savepath", type=str, help="Clients downloads folder")
    parser.add_argument("--debug", action='store_true', help="enable debug mode")
    args = parser.parse_args()

    PORT = args.port
    HOST = args.ip
    DEBUG = args.debug
    client_name = args.name if args.name != None else input("Enter your name: ")
    SAVEPATH = (args.savepath) if args.savepath else ("./" + client_name + "_" + "downloads")

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

    ic(SAVEPATH)

    conn = connect_to_server(client_name)
    if not conn:
        exit()

    if not os.path.exists(SAVEPATH):
        ic("Savepath does not exist, creating it...")
        os.makedirs(SAVEPATH)

    while True:
        command = input(f"{client_name}> ").strip().split()
        if not command:
            continue

        if command[0] == 'UPLOAD' and len(command) == 2:
            upload_file(conn, command[1])
        elif command[0] == 'DOWNLOAD' and len(command) == 3:
            download_file(conn, command[1], command[2], SAVEPATH)
        elif command[0] == 'DELETE' and len(command) == 2:
            delete_file(conn, command[1])
        elif command[0] == 'LIST':
            list_files(conn)
        elif command[0] == 'QUIT':
            conn.close()
            break
        elif command[0] == 'SHELL' and DEBUG: # executes shell commands -- for ease of testing
            try:
                import subprocess # for the SHELL command
                ret = subprocess.run(" ".join(command[1:]), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(ret.stdout)
            except subprocess.CalledProcessError as error:
                print(error.stderr)
            except ImportError:
                print("Could not import subprocess, try running without --debug")
        else:
            print("Invalid command.")
