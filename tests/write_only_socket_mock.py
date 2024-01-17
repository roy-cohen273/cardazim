class WriteOnlySocketMock:
	data = None
	addr = None

	def sendall(self, data):
		type(self).data.extend(data)

	def connect(self, addr):
		type(self).addr = addr

	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_value, traceback):
		pass


def reset_write_only_socket_mock():
	"""Reset mock data.

	Ideally, this would be a class method,
	but we want the mock class's methods to be a subset of the real class's methods.
	"""
	WriteOnlySocketMock.data = bytearray()
	WriteOnlySocketMock.addr = None
