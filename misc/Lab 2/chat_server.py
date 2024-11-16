import socket
import threading
import queue
from datetime import datetime


HOST = "127.0.0.1"
PORT = 5647
MESSAGE_POOL = queue.Queue(maxsize=64)

def display_messages(conn, message_queue):
    while True:
        try:
            conn.sendall(f"{message_queue.get()} at {datetime.now()}".encode())
            # {datetime.now().strftime("%H:%M:%S")}
        except OSError:
            print("Closed connection.!")
            break


def broadcast_message(message):
    for _ in range(MESSAGE_POOL.qsize()):
        message_queue = MESSAGE_POOL.get()
        message_queue.put(message.decode())
        MESSAGE_POOL.put(message_queue)


def add_member(conn, addr):
    message_queue = queue.Queue(maxsize=256)
    MESSAGE_POOL.put(message_queue)


    MESSAGE_POOL.queue
    with conn:
        print(f"Connected by {addr}")

        t = threading.Thread(target=display_messages, args=(conn, message_queue))
        t.start()

        while True:
            try:
                message = conn.recv(1024)
                if not message:
                    break
            except ConnectionResetError:
                break

            broadcast_message(message)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print(f"Server is running on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()

        t = threading.Thread(target=add_member, args=(conn, addr))
        t.start()
