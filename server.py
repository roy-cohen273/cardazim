import argparse
import sys
import socket
import struct


def recv_all(sock, bufsize, flags=0):
    """Receive data from the socket.
    The return value is a bytes object representing the data received.
    The amount of data received is exactly bufsize.
    """
    result = b''
    while (length_diff := bufsize - len(result)) > 0:
        result += sock.recv(length_diff, flags)
    return result


def run_server(ip, port):
    """Setup a server in address (ip, port) and receive data."""
    with socket.socket() as server:
        server.bind((ip, port))
        server.listen(5)
        print(f"Listening to messages on ip: {ip} and port: {port}")
        print("Press ^C to exit.")
        while True:
            conn, addr = server.accept()
            message_len, = struct.unpack('<I', recv_all(conn, 4))
            message = recv_all(conn, message_len).decode()
            print("Got message:", message)
        


def get_args():
    parser = argparse.ArgumentParser(description='Setup a server and receive data.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
    except KeyboardInterrupt:
        print('\nDone.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
