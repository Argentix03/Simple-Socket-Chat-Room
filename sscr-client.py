# SSCR Client - Simple Socket Chat Room Client
# Version: Alpha 0.5
# This is the client app of the Simple Socket Chat Room which connect to server and then
# send and receive information on two different threads
# todo: 1. add domain to ip instead of using static ip
#       2. use sys.argv for command line arguments (ip/domain and port)
import socket
import _thread
import sys
import threading
# listen to server, could be handled in a different parallel thread
def listen_to_server():
    try:
        while True:
            recvData = s.recv(2048).decode()
            print(recvData, flush=True)

    except Exception as e:
        print(e)

# send information
def listen_to_client():
    while True:
        sendData = input()
        if sendData.lower() == 'exit':
            s.send(sendData.encode())
            s.close()
        else:
            s.send(sendData.encode())


s = socket.socket()
# making a connection, until connection is established... codes on hold.
#s.connect(('35.246.209.173', 8000))  # to kali.phoenixtv.me
s.connect(('127.0.0.1', 8000))  # for local testing
print("connection established")

# first get info from the server, until connection is established... codes on hold.
recvData = s.recv(2048).decode()
print(recvData)
_thread.start_new_thread(listen_to_client, ())
listen_to_server()



