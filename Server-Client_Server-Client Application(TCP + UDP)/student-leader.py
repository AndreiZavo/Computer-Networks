import argparse
import random
import socket
import time
from multiprocessing import Process

""" get group_port and if/if not the student is leader from the arguments """
parser = argparse.ArgumentParser(description='Group Port and If student is a leader or not')
parser.add_argument("group_port", type=int)
parser.add_argument("is_leader", type=int)
args = parser.parse_args()
buffer_size = 1024
"""----------------------------------------------------------------------"""


def leader_message_broadcast(leader_socket, group_port):
    message = b'I am leader'
    while True:
        leader_socket.sendto(message, ('<broadcast>', group_port))
        print("Leader message sent")
        time.sleep(5)


def leader_solve_question(leader_socket, group_port):
    print("Started solving")
    teacher_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    teacher_address = ('localhost', 1234)

    teacher_socket.connect(teacher_address)

    while True:
        student_question, student_address = leader_socket.recvfrom(buffer_size)
        print("Student: ", student_address, "asked: ", student_question.decode('utf-8'))

        teacher_socket.sendall(student_question)
        answer = teacher_socket.recv(buffer_size)
        print("Teacher said: ", answer.decode('utf-8'))

        to_student_message = "Q: " + student_question.decode('utf-8') + '\n' +\
            "A: " + answer.decode('utf-8')
        leader_socket.sendto(to_student_message.encode('utf-8'), ("<broadcast>", group_port))


def leader(group_port):
    leader_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    leader_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    leader_socket.settimeout(0.5)
    leader_socket.setblocking(True)
    leader_socket.bind(("0.0.0.0", group_port + 1000))

    send_message = Process(target=leader_message_broadcast, args=(leader_socket, group_port))
    send_message.start()

    solve_question = Process(target=leader_solve_question, args=(leader_socket, group_port))
    solve_question.start()

def student_send_question(student_socket, leader_address):
    student_question = b"May we leave?"
    while True:
        if random.randint(1, 100) >= 50:
            student_socket.sendto(student_question, leader_address)
        time.sleep(3)


def student_receive_response(student_socket):
    while True:
        answer, leader_address = student_socket.recvfrom(buffer_size)
        print("Leader: ", leader_address, "said: ", answer.decode('utf-8'))


def not_leader(group_port):
    student_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    student_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    student_socket.bind(("0.0.0.0", group_port))

    data, leader_address = student_socket.recvfrom(buffer_size)
    print("Leader: ", leader_address, "sent: ", data.decode('utf-8'))

    send_question = Process(target=student_send_question, args=(student_socket, leader_address))
    send_question.start()

    student_listen = Process(target=student_receive_response, args=(student_socket, ))
    student_listen.start()


if __name__ == "__main__":
    print(args.group_port, args.is_leader)

    if args.is_leader == 1:
        leader(args.group_port)
    elif args.is_leader == 0:
        not_leader(args.group_port)
    else:
        print('Please insert the arguments correctly')
