import argparse
import sys
import socket
import struct

from connection import Connection

from card import Card


###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip, server_port, data):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    with Connection.connect(server_ip, server_port) as connection:
        connection.send_message(data)
        

###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send a card to a server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('name', type=str,
                        help='the name of the card')
    parser.add_argument('creator', type=str,
                        help='the creator of the card')
    parser.add_argument('riddle', type=str,
                        help='the riddle of the card')
    parser.add_argument('solution', type=str,
                        help='the solution to the riddle')
    parser.add_argument('image_file', type=argparse.FileType('rb'),
                        help='the file of the image on the card')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        card = Card.create_from_path(args.name, args.creator, args.image_file, args.riddle, args.solution)
        print(f"Sending card {card.name!r} by {card.creator}...")
        card.encrypt()
        send_data(args.server_ip, args.server_port, card.serialize())
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
