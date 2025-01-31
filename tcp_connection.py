import socket
from enum import Enum
from threading import Thread

from hand_authenticator import verify_password
from hand_side import HandSide
from password_status import PasswordStatus

HOST = '127.0.0.1'  # Localhost
PORT = 12345  # Arbitrary port for the server


class AuthenticationStatus(Enum):
    RECEIVED_OK = b'OK'
    RECEIVED_FAILED = b'FAILED'
    RECEIVED_PASSED = b'PASSED'


connected = {}


def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address and port
    server_socket.bind((HOST, PORT))

    # Enable the server to accept connections (max 5 clients in the waiting queue)
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT} and waiting for connections...")

    while True:
        # Accept a connection from the client
        client_socket, client_address = server_socket.accept()
        connected[client_address] = client_socket
        print(f"Connected to {client_address}")
        handle_client_thread = Thread(target=handle_connection, args=[client_socket])
        handle_client_thread.start()


def handle_authentication(client_socket: socket.socket):
    password_list = []

    number_of_tries = 0

    while True:
        hand = HandSide(client_socket.recv(64).decode())
        print(hand)
        password_list.append(hand)

        status = verify_password(password_list)
        print(status)
        if status == PasswordStatus.MATCH:
            client_socket.send(AuthenticationStatus.RECEIVED_PASSED.value)
            return True
        elif status == PasswordStatus.NOT_MATCH:
            number_of_tries += 1
            if number_of_tries == 3:
                # Handle failure
                client_socket.send(AuthenticationStatus.RECEIVED_FAILED.value)
                return False

            client_socket.send(AuthenticationStatus.RECEIVED_OK.value)
            password_list.clear()
        elif status == PasswordStatus.IN_PROCESS:
            client_socket.send(AuthenticationStatus.RECEIVED_OK.value)


def handle_connection(client_socket: socket.socket, client_address: tuple):
    succeeded = handle_authentication(client_socket)

    # Close the client socket connection
    client_socket.close()
    del connected[client_address]



def send_request(client_socket: socket.socket, target_ip):
        message = "send_a_screenshot"
        client_socket.send(message.encode())
        validation = client_socket.recv(1024).decode()
        return validation





