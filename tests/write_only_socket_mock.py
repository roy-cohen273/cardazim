class WriteOnlySocketMock:
	data = bytearray()
	addr = None

	def sendall(self, data):
		type(self).data.extend(data)

	def connect(self, addr):
		type(self).addr = addr

	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_value, traceback):
		pass