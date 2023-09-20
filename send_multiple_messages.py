import argparse
import sys
import threading

from client import send_data


def send_messages(server_ip, server_port, messages):
    """
    Send messages in parallel to server in address (server_port, server_ip)
    """
    for message in messages:
        threading.Thread(target=send_data, args=(server_ip, server_port, message)).start()


def get_args():
    parser = argparse.ArgumentParser(description='Send multiple messages to server in parallel.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('messages', type=str, nargs=argparse.REMAINDER,
                        help='the data')
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending messages to server.
    """
    args = get_args()
    try:
        send_messages(args.server_ip, args.server_port, args.messages)
    except Exception as error:
        print(f"ERROR: {error}")
        return 1



if __name__ == '__main__':
    sys.exit(main())
