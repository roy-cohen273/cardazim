import pytest
import sys

from .write_only_socket_mock import WriteOnlySocketMock
from .utils import assert_card

import client


@pytest.mark.parametrize('server_ip, server_port, name, creator, riddle, solution, image_file', [
	('127.0.0.1', 35746, 'easy', 'Roy', '1 + 1 = ?', '2', 'fish.jpg'),
	('116.124.10.73', 6556, 'imposible', 'Unknown', 'How many twin primes are there?', '🤔', '👍.jpg'),
])
def test_client(server_ip, server_port, name, creator, riddle, solution, image_file, write_only_socket):
	sys.argv[1:] = [server_ip, str(server_port), name, creator, riddle, solution, image_file]
	client.main()

	assert WriteOnlySocketMock.addr == (server_ip, server_port)

	assert_card(WriteOnlySocketMock.data, name, creator, riddle, solution, image_file, is_solved=False)
