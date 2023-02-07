import socket

s = socket.socket()
host="127.0.0.1"
port=1623
s.connect((host,port))
s.sendall(("Hello, world" ).encode())
data = s.recv(1024)
print("Recieved ", data.decode)
s.close