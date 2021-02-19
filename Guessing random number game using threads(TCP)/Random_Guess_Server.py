import socket
import random

""" Choose a random number to be guessed """
random.seed()
start = 1
stop = 100
mystery_number = random.randint(start, stop)
"""--------------------------------------"""

""" Global variables for server """
HOST = "127.0.0.1"
PORT = 1234
buffer_size = 1024
client_guessed = False
winner_client = ""
"""-----------------------------"""


def worker(UDP_socket):
    global client_guessed, winner_client
    UDP_socket.sendto("Welcome to the game".encode(), ("<broadcast>", PORT))

    bytes_address_pair = UDP_socket.recvfrom(buffer_size)
    message_from_client = bytes_address_pair[0].decode()
    client_address = bytes_address_pair[1]
    print(message_from_client, client_address)

    while not client_guessed:
        # server receives number sent by client
        received_number = int(UDP_socket.recvfrom(buffer_size)[0].decode())
        if received_number > mystery_number:
            if client_guessed is False:
                UDP_socket.sendto("Aim lower".encode(), client_address)
            else:
                break
        elif received_number < mystery_number:
            if client_guessed is False:
                UDP_socket.sendto("Aim higher".encode(), client_address)
            else:
                break
        else:
            client_guessed = True
            winner_client = client_address
    if client_guessed:
        if client_address == winner_client:
            winner_message = "You found it!".encode()
            UDP_socket.sendto(winner_message, client_address)
        else:
            loser_message = "Someone else found it first.."
            UDP_socket.sendto(loser_message, client_address)

    UDP_socket.close()


if __name__ == "__main__":
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPServerSocket.settimeout(0.2)
    UDPServerSocket.setblocking(True)
    UDPServerSocket.bind(("0.0.0.0", 405))
    worker(UDPServerSocket)
