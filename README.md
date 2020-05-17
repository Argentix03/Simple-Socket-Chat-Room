Simple Socket Chat Room
=
Simple Python implementation of chat room using TCP/IP sockets (IPv4 and IPv6).
I made this tool to practice sockets in python.

It comes with a python client that is more enriched but can also be used with netcat.

For client you can use netcat or or the more enriched sscr-client.py.

## Install
$ git clone https://github.com/Argentix03/Simple-Socket-Chat-Room.git

## Starting Server
```
$ python3 sscr-server.py <port>
```
## Connecting Client
```
Using sscr-client.py: $ python3 sscr-client.py <ip> <port>

Using netcat: $ nc <ip> <port>
```
## Chat commands
The following commands are available and handled by the chatbot (notice ./ is just the default prefix and can be changed):

| Command	            | Description             |
----------------------|-------------------------|
|./editname <name> | change your nickname.      |
|./setRoomName	<name> | change the room name.  |
|./setBotPrefix <prefix> | change the bot prefix.|
|./kick <user> | kicks a user from the room (requires chatroom admin role).|
|./auth <id:id> <token:token> | authenticate as the chatroom admin.
