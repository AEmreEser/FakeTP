from socket import *

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort)) # empty '' -> the server listening to any ip address over the port

while True:
    message, cAddress = serverSocket.recvfrom(2048) # sockets are blocking by default --> meaning if we don't have data arriving this won't return
    msg = message.decode()
    if (msg == 'exit'):
        serverSocket.sendto('exit command received, shutting server down'.encode(), cAddress)
        break
    modMsg =  msg + 'bruh bruh bruh idc'
    serverSocket.sendto(modMsg.encode(), cAddress)

