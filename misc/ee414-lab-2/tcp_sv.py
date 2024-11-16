from socket import * 

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM) # for TCP we don't use SOCK_DGRAM
serverSocket.bind(('', serverPort)) # empty '' -> the server listening to any ip address over the port

serverSocket.listen(1) # the parameter 1 means that we can have at most 1 connection at a time

while True:
    connSock, addr = serverSocket.accept() # accept connection -- we didn't have connection sockets in udp -- here we must do things this way
    msg = connSock.recv(1024).decode()

    if (msg == 'exit'):
        connSock.close()
        serverSocket.close()
        break

    msg += " dabababa"
    connSock.send(msg.encode())

