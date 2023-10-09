import argparse
import sys
import socket
import struct
import threading

from listener import Listener

from card import Card


class ConnectionThread(threading.Thread):
    """
    A Thread that receives a message from a connection and prints it.
    """
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
    
    def run(self):
        with self.conn:
            message = self.conn.receive_message()
        card = Card.deserialize(message)
        print(f"Received card {card.name!r} by {card.creator}")


def run_server(ip, port):
    """Setup a server in address (ip, port) and receive data."""
    with Listener(port, ip) as listener:
        print(f"Listening to messages on ip: {ip} and port: {port}")
        print("Press ^C to exit.")
        while True:
            conn = listener.accept()
            ConnectionThread(conn).start()
        


def get_args():
    parser = argparse.ArgumentParser(description='Setup a server and receive data.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and setting up server.
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
