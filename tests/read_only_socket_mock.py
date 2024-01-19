class ReadOnlySocketMock:
	"""A mock object to replace a socket. With the added condition that it is read-only."""
	messages = None
	addr = None

	def bind(self, addr):
		type(self).addr = addr

	def listen(self, backlog):
		pass

	def accept(self):
		if len(type(self).messages) == 0:
			raise KeyboardInterrupt

		conn = type(self)()
		conn.accepted_message = type(self).messages.pop()
		return conn, None

	def recv(self, length, flags=0):
		result = self.accepted_message[:length]
		self.accepted_message = self.accepted_message[length:]
		return result

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		pass


def reset_read_only_socket_mock():
	"""Reset mock data.

	Ideally, this would be a class method,
	but we want the mock class's methods to be a subset of the real class's methods.
	"""
	ReadOnlySocketMock.messages = []
	ReadOnlySocketMock.addr = None
