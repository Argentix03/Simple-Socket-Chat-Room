# SSCR Server - Simple Socket Chat Room Server
# Version: Alpha 0.6
# This is the server app of the Simple Socket Chat Room which handles all client connections
# todo: 1. [DONE] Clean up server side prints to only whats relevant to the eye in realtime and implement a log for later debugging/analysing
#       2. More bot commands!
#       3. Permission system for bot commands
#       4. Generate Token on server lunch for admin to authenticate with when they connect with the client for bots permmissions
#       5. Bot kick command
#       7. Implement a timeout or fail counter for failed sends to client for dropping connections

import socket
import chatbot
import config
import sys
import _thread
import datetime
import random

try:
    client_list = {}  # dict of {client(id) -> connections from socket.accept()}
    id_counter = 1  # counter that will increment to keep unique ID for every joined user
    server = socket.socket()  # the global server socket variable
    logfile = open('sscr-server.log', 'a') # used for log
except Exception as e:
    print(e)

# logs a message to the logfile
def log(logMessage):
    global logfile
    logfile.write(f"{datetime.datetime.now()}: {logMessage}\n")
    logfile.flush()

# generates a unique token
def token_gen(length):
    token = ""
    for i in range(length):
        upper_character = chr(random.randint(ord('A'), ord('Z')))
        lower_character = chr(random.randint(ord('a'), ord('z')))
        digit = chr(random.randint(48, 57))
        random_characters = [upper_character, lower_character, digit]
        token += random.choice(random_characters)
    return token

# joins a member and return his ID if successful, on fail return -1
def join(conn, name):
    try:
        global client_list
        global id_counter
        client_list[id_counter] = conn
        config.name_list[id_counter] = name
        print(f"Added: {name}, ID: {id_counter}")
        log(f"Added: {name}, ID: {id_counter}")
        log(f"Updated client_list: {client_list}")
        id_counter += 1
        return id_counter - 1

    except Exception as e:
        print(e)
        return -1

# greet a user on connection and asks for his name then calls join to add him to the list and get the user id
# returns the user id or -1 on fail
def greet(conn, addr):
    try:
        log(f"New thread: {conn}")
        conn.send(f"Welcome to {config.room_name}\nYour address will not be shared with anyone\nPlease Type in your name: ".encode())
        user_name = conn.recv(1024).decode()
        user_id =  join(conn, user_name)
        conn.send(f"Your user ID: {user_id}".encode())
        if user_id != -1:
            return user_id
        else:
            return -1

    except Exception as e:
        print(e)
        log(e)
        return False

# sends message to all connections in client_list
def broadcast(message, name):
    message = f"{name}: " + message
    print(message)
    log(message)
    for client in client_list:
        try:
            client_list[client].send(message.encode())
            log(f"Sent message successfully to {client_list[client]}")
        except Exception as e:
            log(f"\nFailed to send message to {config.name_list[client]} ({client})")
            log(e)

def client_handle(conn, addr):
    # if couldn't get the user to supply name and add him to the list close connection and give up on him
    if greet(conn, addr) == -1:
        conn.close()
        return
    # find name
    for id, sock in client_list.items():
        if sock == conn:
            name = config.name_list[id]
            userId = id
    broadcast(f"{name} has joined the room", 'Server')
    # command has been executed and this is not a message if this is True
    # for publicly visible commands bot could use broadcast() with a non bot command for the displayed message
    while True:
        message = conn.recv(2048).decode()

        command = chatbot.evalCommand(message, userId)
        if command:
            log(f"command: {command} userID: {userId} name: {name}")
            if command.startswith("private:"):
                conn.send("-Command successfully executed-".encode())
            elif command.startswith("public:"):
                broadcast(command.split(":")[1], "ChatBot")
        else:
            name = config.name_list[userId]  # update name before sending message
            broadcast(message, name)


# main first binds the server to the port then starts a new thread for each connection received.
# each client connection thread goes though the following route: client_handle() => greet() => join() <= greet() =>
def main(port):
    try:
        global server
        server.bind(('0.0.0.0', port))
        server.listen(20)
        config.token = token_gen(12)
        print(f"Admin token is: {config.token}")
        print("Server is up, waiting for connections...")

        while True:
            conn, addr = server.accept()
            print(f"{addr} Connected")
            log(f"{addr} Connected")
            _thread.start_new_thread(client_handle, (conn, addr))

    except Exception as e:
        print(e)


# Simple sanity check before calling main with port number
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: sscr-server.py port")
        exit()
    else:
        try:
            port = int(sys.argv[1])
            main(port)
        except Exception as e:
            print("Fatal error: failed to launch")
            print(e)
# main(8000)
