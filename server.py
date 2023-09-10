import argparse
import sys
import socket
import struct
import threading

import time

from listener import Listener


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
        print("Got message:", message.decode())


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
