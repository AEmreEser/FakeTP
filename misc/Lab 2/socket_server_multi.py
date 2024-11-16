import socket
import threading


HOST = "0.0.0.0"
PORT = 5647


def client_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            conn.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print(f"Server is running on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()

        t = threading.Thread(target=client_connection, args=(conn, addr))
        t.start()
