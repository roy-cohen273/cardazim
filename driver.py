from abc import ABC, abstractmethod


class Driver(ABC):
	"""An ABC for a driver."""

	@abstractmethod
	def insert_file(self):
		"""Create a new file. Returns a tuple of the file's id and an open file object (in 'wb' mode)."""
		raise NotImplementedError

	@abstractmethod
	def insert_object(self, obj):
		"""Insert the given object. Returns the object's id."""
		raise NotImplementedError
