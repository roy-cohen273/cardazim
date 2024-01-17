import pytest
import socket

from .write_only_socket_mock import WriteOnlySocketMock, reset_write_only_socket_mock


@pytest.fixture
def write_only_socket(monkeypatch):
	reset_write_only_socket_mock()
	monkeypatch.setattr(socket, 'socket', WriteOnlySocketMock)
