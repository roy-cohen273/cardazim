from typing import List, Optional
from abc import ABC, abstractmethod


class Driver(ABC):
	"""An ABC for a driver."""

	drivers = {}

	def __init_subclass__(cls, /, url_scheme, **kwargs):
		super().__init_subclass__(**kwargs)
		cls.drivers[url_scheme] = cls
		cls.url_scheme = url_scheme

	@classmethod
	def get_driver(cls, url: str):
		"""Returns the driver created using the given URL."""
		if '://' not in url:
			raise ValueError('URL must include scheme.')
		scheme, _ = url.split('://', 1)
		if scheme not in cls.drivers:
			raise ValueError(f'Unknown scheme: {scheme!r}')
		return cls.drivers[scheme](url)

	@abstractmethod
	def __init__(self, url: str):
		"""Create a new instance of the driver from the given URL."""
		raise NotImplementedError

	@abstractmethod
	def insert_file(self):
		"""Create a new file. Returns a tuple of the file's id and an open file object (in 'wb' mode).
		It is the responsibility of the caller to close the returned file object.
		"""
		raise NotImplementedError

	@abstractmethod
	def insert_object(self, obj):
		"""Insert the given object. Returns the object's id."""
		raise NotImplementedError

	@abstractmethod
	def iter_objects(self):
		"""Returns an iterator of all objects."""
		raise NotImplementedError

	def find_objects(self, filter: Optional[dict] = None, projection: Optional[List[str]] = None):
		"""Find all objects that pass the given filter.
		The filter is a dictionary of key-value pairs that the objects must have.
		The projection is a list of field names to include in the result.
		Returns an iterable of the objects.
		"""
		if filter is None:
			filter = {}

		for obj in self.iter_objects():
			for key, value in filter.items():
				if key not in obj or obj[key] != value:
					break
			else:  # no break
				if projection is None:
					yield obj
				else:
					yield {field: obj[field] for field in projection}

	def find_one_object(self, filter: Optional[dict] = None, projection: Optional[List[str]] = None):
		"""Find a single object that passes the given filter.
		The filter is a dictionary of key-value pairs that the object must have.
		The projection is a list of field names to include in the result.
		If more than one object passes the filter, one of them is returned,
		if no object passes the filter, None is returned.
		"""
		for obj in self.find_objects(filter, projection):
			return obj
		return None

	@abstractmethod
	def get_file(self, file_id):
		"""Get a file by its ID. Returns an open file object (in mode 'rb').
		If the given file ID was not found, returns None.
		"""
		raise NotImplementedError
