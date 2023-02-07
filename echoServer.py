import socket

s = socket.socket()
host = "127.0.0.1"
port=1623
s.bind((host, port))
s.listen(5)
c, addr = s.accept()


while c:
    print('Got connection from', addr)
    while True:
        message = c.recv(1024)
        c.sendall(message)