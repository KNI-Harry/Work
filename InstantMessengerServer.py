
import socket
from threading import Thread


# remember to change host IP in server and client

def dealWithIncoming():
    while True:
        # client here is a new socket object able to send and receive on the new connection
        client, client_address = serverSocket.accept() # save the connection and address
        print("Client Connected: ", client_address)
        client.send(bytes("Client connected type your name and press enter", "utf8")) #send a welcome message
        addresses[client] = client_address # add client address to our address book
        Thread(target=dealWithClient, args=(client,)).start() #start a new thread to deal with each new incoming client


def dealWithClient(client):  # is passed specific client.
    name = client.recv(1024).decode("utf8") #decode the name given
    welcome = 'Welcome %s! type your message below to add it to the chat room.' % name
    client.send(bytes(welcome, "utf8"))
    broadcastmsg = "%s has joined the room" % name
    broadcast(bytes(broadcastmsg, "utf8")) # we use a broadcast method to ensure all clients get message
    clients[client] = name

    #continuously receive messages, if one is Exit, close the connection and remove client from list
    while True:
        message = client.recv(1024)
        if message == bytes("{Exit}","utf8"):
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the room." % name, "utf8"))
            break
        else:
            broadcast(message, name + ": ")



#broadcast sends msg to every client
def broadcast(msg, name=""):
    for clientsocket in clients:
        clientsocket.send(bytes(name, "utf8") + msg)

        
clients = {} # the client list
addresses = {} # the addres list

host = "127.0.0.1"
port = 65430  

serverSocket = socket.socket()
serverSocket.bind((host, port))

if __name__ == "__main__":
    serverSocket.listen(5) # listen for up to 5 connections
    print("Server active, waiting for connection...")
    incoming_thread = Thread(target=dealWithIncoming)
    incoming_thread.start()
    incoming_thread.join()
    serverSocket.close()


