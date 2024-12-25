import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9998))

server.listen(2)

while True:
    client, addr = server.accept()
    print(client.recv(1024).decode())
