import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.setblocking(True)
server.bind(("0.0.0.0", 404))
message = b"your very important message"
server.sendto(message, ('<broadcast>', 1234))
while True:
    server.sendto(message, ('<broadcast>', 1234))
    print("message sent!")
    time.sleep(3)
    print("Client answered: " + server.recvfrom(1024)[0].decode('utf-8'))
