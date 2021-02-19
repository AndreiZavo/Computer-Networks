import socket
import random
import threading
import time
import string

host = 'localhost'
port = 1234
teacher_address = (host, port)
buffer_size = 1024


def worker(_leader_socket):
    while True:
        data = _leader_socket.recv(buffer_size)
        print("Leader: ", _leader_socket.getpeername(), " asked: ", data.decode('utf-8'))

        teacher_answer = 'Do not know, do not care'
        print("I would say: " + teacher_answer)

        _leader_socket.sendall(teacher_answer.encode('utf-8'))


if __name__ == "__main__":
    print("Teacher is live at", teacher_address)
    teacher_socket = socket.socket()
    try:
        teacher_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        teacher_socket.bind(("localhost", 1234))
        teacher_socket.listen(5)
    except socket.error as error_message:
        print(error_message)
        exit(-1)
    while True:
        leader_socket, leader_address = teacher_socket.accept()
        print("Leader: ", leader_address, "connected")
        thread = threading.Thread(target=worker, args=(leader_socket, ), daemon=True)
        thread.start()
