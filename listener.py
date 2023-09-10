import socket

from connection import Connection


class Listener:
	"""Listens to connections on a given host and a given port."""
	def __init__(self, port, host, backlog=1000):
		"""Creates a new Listener on address (host, port) and specified backlog."""
		self.sock = socket.socket()
		self.port = port
		self.host = host
		self.backlog = backlog

	def __repr__(self):
		return f'Listener(port={self.port}, host={self.host!r}, backlog={self.backlog})'

	def start(self):
		"""Start listening to connections."""
		self.sock.bind((self.host, self.port))
		self.sock.listen(self.backlog)

	def stop(self):
		"""Stop listening to connections."""
		self.sock.close()

	def accept(self) -> Connection:
		"""Accept a connection and return a `Connection` object representing it."""
		conn, addr = self.sock.accept()
		return Connection(conn)

	def __enter__(self):
		self.sock.__enter__()
		self.start()
		return self


	def __exit__(self, exc_type, exc_value, traceback):
		return self.sock.__exit__(exc_type, exc_value, traceback)
