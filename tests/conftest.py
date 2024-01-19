import pytest
import socket

from .write_only_socket_mock import WriteOnlySocketMock, reset_write_only_socket_mock
from .read_only_socket_mock import ReadOnlySocketMock, reset_read_only_socket_mock


@pytest.fixture
def write_only_socket(monkeypatch):
	"""Replaces socket.socket with a write-only socket mock."""
	reset_write_only_socket_mock()
	monkeypatch.setattr(socket, 'socket', WriteOnlySocketMock)


@pytest.fixture
def read_only_socket(monkeypatch):
	"""Replaces socket.socket with a read-only socket mock."""
	reset_read_only_socket_mock()
	monkeypatch.setattr(socket, 'socket', ReadOnlySocketMock)
