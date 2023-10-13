import argparse
import sys
from threading import Thread
from pathlib import Path

from listener import Listener
from connection import Connection

from card import Card


def check_unsolved_cards_dir(unsolved_cards_dir: Path) -> bool:
    """Check that the unsolved cards directory is valid."""
    if not unsolved_cards_dir.exists():
        print(f"Directory does not exist: '{unsolved_cards_dir}'")
        return False
    if not unsolved_cards_dir.is_dir():
        print(f"Not a directory: '{unsolved_cards_dir}'")
        return False
    return True

def run_server(ip: str, port: int, unsolved_cards_dir: Path):
    """Setup a server in address (ip, port), receive cards, and save them to the unsolved cards directory."""
    card_id = 0
    with Listener(port, ip) as listener:
        print(f"Listening to messages on ip: {ip} and port: {port}")
        print("Press ^C to exit.")
        while True:
            card_id = next_card_id(unsolved_cards_dir, card_id)
            conn = listener.accept()
            Thread(target=handle_connection, args=(conn, unsolved_cards_dir, card_id)).start()

def handle_connection(conn: Connection, unsolved_cards_dir: Path, card_id: int):
    """Handle a connection by receiving a card and saving it to the unsolved cards directory."""
    with conn:
        message = conn.receive_message()
    print('Received card.')
    card_path = unsolved_cards_dir / str(card_id)
    card_path.write_bytes(message)
    print(f"Saved card to path '{card_path}'.")
        
def next_card_id(unsolved_cards_dir: Path, card_id: int) -> int:
    """Return the next available card id."""
    while (unsolved_cards_dir / str(card_id)).exists():
        card_id += 1
    return card_id

def get_args():
    parser = argparse.ArgumentParser(description='Setup a server, receive cards, and save them to file.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('unsolved_cards_dir', type=Path,
                        help='The directory to save cards in.')
    return parser.parse_args()

def main():
    '''
    Implementation of CLI and setting up server.
    '''
    args = get_args()
    try:
        if check_unsolved_cards_dir(args.unsolved_cards_dir):
            run_server(args.server_ip, args.server_port, args.unsolved_cards_dir)
        else:
            return 1
    except KeyboardInterrupt:
        print('\nDone.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
