import socket
import time

HOST = "0.0.0.0"
PORT = 1234
buffer_size = 1024


def guessNumberClient(sock, serverAddressPort, bufferSize):
    # client receives a welcome message from server
    message, address = sock.recvfrom(bufferSize)
    greeting_message = message.decode()
    print(greeting_message)

    # client sends message(signal) to server with its address, ip
    sock.sendto("Client connected".encode(), ('<broadcast>', address))

    finished = False
    while not finished:
        # client sends his guess
        number = input("Your guess: ")
        bytes_to_send = (str(number)).encode()
        sock.sendto(bytes_to_send, serverAddressPort)

        msg_from_server = sock.recvfrom(bufferSize)
        msg = msg_from_server[0].decode()
        print("Server says: " + msg)
        if msg in ["You found it!", "Someone found it first.."]:
            finished = True
        time.sleep(0.25)
    sock.close()
    if msg == "You found it!":
        print('Yeah! I won!')
    else:
        print("I lost..")


if __name__ == "__main__":
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_address_port = (HOST, PORT)
    UDPClientSocket.bind(server_address_port)

    guessNumberClient(UDPClientSocket, server_address_port, buffer_size)
