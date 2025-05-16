from threading import Thread
from typing import Final

from hand_authenticator import verify_password
from password_status import PasswordStatus
from voss_socket import VOSSSocketServer, VOSSSocketConnection, VOSSSocketConnectionAdmin, AuthenticationStatus, \
    ClientRole, VOSSSocketConnectionTarget

HOST: Final[str] = '0.0.0.0'  # Listen on all available IP addresses

connected_clients: dict[str, VOSSSocketConnection] = {}


def start_server():
    # Create a socket object
    server_socket = VOSSSocketServer()
    server_socket.init_socket(HOST)
    print(f"Server started on {HOST} and waiting for connections...")

    while True:
        # Accept a connection from the client
        client_socket, client_role, client_address = server_socket.accept()
        client_ip, client_port = client_address
        connected_clients[client_ip] = client_socket
        print(f"Connected to {client_ip}")
        if client_role == ClientRole.ADMIN:
            handle_client_thread = Thread(target=handle_admin_connection, args=(client_ip,))
            handle_client_thread.start()


def handle_authentication(client_socket: VOSSSocketConnectionAdmin):
    password_list = []

    number_of_tries = 0

    while True:
        hand = client_socket.recv_hand_side_auth_request()
        print(hand)
        password_list.append(hand)

        status = verify_password(password_list)
        print(status)
        if status == PasswordStatus.MATCH:
            client_socket.send_hand_side_auth_response(AuthenticationStatus.RECEIVED_PASSED)
            return True
        elif status == PasswordStatus.NOT_MATCH:
            number_of_tries += 1
            print(number_of_tries)
            if number_of_tries == 3:
                # Handle failure
                client_socket.send_hand_side_auth_response(AuthenticationStatus.RECEIVED_FAILED)
                return False

            client_socket.send_hand_side_auth_response(AuthenticationStatus.RECEIVED_OK)
            password_list.clear()
        elif status == PasswordStatus.IN_PROCESS:
            client_socket.send_hand_side_auth_response(AuthenticationStatus.RECEIVED_OK)


def close_client(client_address: str):
    connected_clients[client_address].close()
    connected_clients.pop(client_address)


def handle_admin_connection(client_address: str):
    admin_conn: VOSSSocketConnectionAdmin = connected_clients[client_address]

    succeeded = handle_authentication(admin_conn)
    if not succeeded:
        close_client(client_address)

    while True:
        target_ip = admin_conn.recv_screenshot_from_target_request()

        screenshot_filename = get_screenshot_from_target(target_ip)

        admin_conn.send_screenshot_from_target_response(screenshot_filename)


def get_screenshot_from_target(target_ip: str) -> str:
    target_conn: VOSSSocketConnectionTarget = connected_clients[target_ip]

    target_conn.send_take_screenshot_request()

    filename_in_ftp_server = target_conn.recv_take_screenshot_response()
    return filename_in_ftp_server
