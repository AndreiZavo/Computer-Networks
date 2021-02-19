import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("0.0.0.0", 1234))
data, server_address = client.recvfrom(1024)
print(data.decode('utf-8'))
while True:
    print("received message: %s"%data)
    client.sendto(b'moama moama ce bombeu', server_address)
    data, addr = client.recvfrom(1024)