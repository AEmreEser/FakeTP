import socket


HOST = "127.0.0.1"
PORT = 5647


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        data = input("Enter your data: ")
        s.sendall(data.encode())

        data = s.recv(1024)
        print(f"Received {data.decode()}")