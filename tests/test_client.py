import pytest
import sys
import struct

from .write_only_socket_mock import WriteOnlySocketMock

import client
from card import Card


@pytest.mark.parametrize('server_ip, server_port, name, creator, riddle, solution, image_file', [
	('127.0.0.1', 35746, 'easy', 'Roy', '1 + 1 = ?', '2', 'fish.jpg'),
])
def test_client(server_ip, server_port, name, creator, riddle, solution, image_file, write_only_socket):
	sys.argv[1:] = [server_ip, str(server_port), name, creator, riddle, solution, image_file]
	client.main()

	# test the message protocol
	data = WriteOnlySocketMock.data
	assert len(data) >= 4
	length, = struct.unpack('<I', data[:4])
	data = data[4:]
	assert length == len(data)

	# test message data
	card = Card.deserialize(data)
	assert WriteOnlySocketMock.addr == (server_ip, server_port)
	assert card.name == name
	assert card.creator == creator
	assert card.riddle == riddle
	assert card.solution is None