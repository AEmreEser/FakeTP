from socket import *
from threading import *

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

exit = False

def msg_loop():
    while True:
        msg = input('msg to send: ')
        clientSocket.sendto(msg.encode(), (serverName, serverPort))
        if (msg == '\\exit'):
            exit = True
            msg = 'exit'
            clientSocket.sendto(msg.encode(), (serverName, serverPort))
            clientSocket.close()
            break

def recv_loop():
    while not exit:
        modMsg, svAddr = clientSocket.recvfrom(2048)
        print("msg recv from sv: ", modMsg.decode())



recv_th = Thread(target=recv_loop)
recv_th.start()
send_th = Thread(target=msg_loop)
send_th.start()

recv_th.join()
send_th.join()

