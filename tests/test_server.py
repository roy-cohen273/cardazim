import sys
import os
import random
import struct
import pytest

from .read_only_socket_mock import ReadOnlySocketMock

import server


@pytest.mark.parametrize('N', [1, 5, 10, 100])
@pytest.mark.parametrize('server_ip, server_port', [
	('127.0.0.1', 12345),
	('168.126.12.34', 1597),
])
def test_server(N, server_ip, server_port, read_only_socket, tmp_path, capsys):
	sys.argv[1:] = [server_ip, str(server_port), str(tmp_path)]

	# prepair random messages
	messages = []
	for _ in range(N):
		length = random.randint(0, 1024)
		message = os.urandom(length)
		messages.append(message)
		ReadOnlySocketMock.messages.append(struct.pack('<I', length) + message)
	messages = messages[::-1]

	# run server
	server.main()
	stdout, stderr = capsys.readouterr()
	assert stderr == ''

	# test socket address
	assert ReadOnlySocketMock.addr == (server_ip, server_port)

	# test output files
	for i, message in enumerate(messages):
		assert (tmp_path / str(i)).read_bytes() == message
