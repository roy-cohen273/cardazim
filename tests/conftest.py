import pytest
import socket

from .write_only_socket_mock import WriteOnlySocketMock


@pytest.fixture
def write_only_socket(monkeypatch):
	monkeypatch.setattr(socket, 'socket', WriteOnlySocketMock)