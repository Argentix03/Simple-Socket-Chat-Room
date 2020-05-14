# SSCR Server - Simple Socket Chat Room Server (by Hoshea Yarden)
# Version: Beta 0.5
# This is the server app of the Simple Socket Chat Room which handles all client connections
# todo: 1. Clean up server side prints to only whats relevant to the eye in realtime and implement a log for later debugging/analysing
#       2. More bot commands!
#       3. Permission system for bot commands
#       4. Generate Token on server lunch for admin to authenticate with when they connect with the client for bots permmissions
#       5. Bot kick command
#       7. Implement a timeout or fail counter for failed sends to client for dropping connections

import socket
import chatbot
import sys
import _thread
room_name = "Default-room 1"
client_list = {}  # dict of {client(id) -> connections from socket.accept()}
name_list = {}  # dict of {id -> name} to keep track of names of users and their connection (which are tied to the id)
id_counter = 1  # counter that will increment to keep unique ID for every joined user
server = socket.socket()  # the global server socket variable

# joins a member and return his ID if successful, on fail return -1
def join(conn, name):
    try:
        global client_list
        global id_counter
        global name_list
        client_list[id_counter] = conn
        name_list[id_counter] = name
        print(f"Added: {name}, ID: {id_counter}")
        id_counter += 1
        print(f"Updated client_list: {client_list}")
        return id_counter - 1

    except Exception as e:
        print(e)
        return -1

# greet a user on connection and asks for his name then calls join to add him to the list and get the user id
# returns the user id or -1 on fail
def greet(conn, addr):
    try:
        print(f"New thread: {conn}")
        conn.send(f"Welcome to the {room_name}\nYour address ({addr}) will not be shared with anyone\nPlease Type in your name: ".encode())
        user_name = conn.recv(1024).decode()
        # _thread.start_new_thread(join, (conn, user_name))
        user_id =  join(conn, user_name)
        if user_id != -1:
            return user_id
        else:
            return -1

    except Exception as e:
        print(e)
        return False

def broadcast(message):
    print(f"broadcast message:\n{message}")
    for client in client_list:
        try:
            print(f"client_list[client]: {client_list[client]}")
            client_list[client].send(message.encode())
            print(f"Sent message successfully to {client_list[client]} ")
        except Exception as e:
            print(f"\nFailed to send message to {client_list[client]}")
            print(e)

def client_handle(conn, addr):
    print("client_handle")
    # if couldn't get the user to supply name and add him to the list close connection and give up on him
    if greet(conn, addr) == -1:
        conn.close()
        return

    # command has been executed and this is not a message if this is True
    # for publicly visible commands bot could use broadcast() with a non bot command for the displayed message
    message = conn.recv(2048).decode()
    if chatbot.evalCommand(message):
        return
    else:
        broadcast(message)


# main first binds the server to the port then starts a new thread for each connection received.
# each client connection thread goes though the following route: client_handle() => greet() => join() <= greet() =>
def main(port):
    try:
        global server
        server.bind(('0.0.0.0', port))
        server.listen(20)
        print("Server is up, waiting for connections...")

        while True:
            conn, addr = server.accept()
            print(f"{addr} Connected")
            _thread.start_new_thread(client_handle, (conn,addr))

    except Exception as e:
        print(e)


# Simple sanity check before calling main with port number
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print("Usage: sscr-Server.py port")
    #     exit()
    # else:
    #     try:
    #         port = int(sys.argv[2])
    #     except Exception as e:
    #         print(e)
    main(8000)