#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project : OpenChat
File    : Server.py
Author  : Ib Helmer Nielsen
Version : 0.1.0
Email   : ihn@ucn.dk
Status  : Prove of concept
License : MPL 2.0
Description: Simpel chat system. The communication is unencrypted and based on tcp.
             The server hold a list of nickname and connection objects for the clients. When a clinet log on to the
             server it sendsback the string "NICK" and expect the client to sendback nickname of user.
"""
# Imports
import socket
import threading
from time import sleep

# Ip address and port used by server
## Only local host
HOST = '127.0.0.1'
# Use what ever ip on the server
#HOST = '0.0.0.0'
# Port on server used for chat client connections
PORT = 7913

# Make server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind address and port to server
server.bind(((HOST, PORT)))

# Printout the ip of the server
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
print("The servers ip address : ", ip)

# Listen
server.listen()

# List of client connection objects
clients = []
# List of nicknames
nicknames = []

# Broadcast message to all active clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handler for the connection, read data from client and broadcast to all client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]}")
            broadcast(message)
        except:
            index =clients.index((client))
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

# Accept incomming connection and make a thread for new connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)} !")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is", nickname.decode(),f"\n")
        sleep(0.5)          # Wait for clients GUI to startup
        message = nickname.decode() + f" connected to server !\n"
        broadcast(message.encode('utf-8'))
        client.send("Connected to the server\n".encode('utf-8'))
        thread= threading.Thread(target=handle, args = (client,))
        thread.start()

print("Server running ...")
receive()

