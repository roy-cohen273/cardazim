import json
from pathlib import Path

from driver import Driver
from utils import max_directory_id


class FSDriver(Driver):
	FILES_SUBDIRECTORY = 'files'
	OBJECTS_SUBDIRECTORY = 'objects'

	def __init__(self, directory_path: str):
		directory_path = Path(directory_path)
		self.files_directory = directory_path / type(self).FILES_SUBDIRECTORY
		self.objects_directory = directory_path / type(self).OBJECTS_SUBDIRECTORY

		self.files_directory.mkdir(exist_ok=True)
		self.objects_directory.mkdir(exist_ok=True)

		self.file_id = max_directory_id(self.files_directory)
		self.object_id = max_directory_id(self.objects_directory)

	def insert_file(self):
		self.file_id += 1
		file = (self.files_directory / str(self.file_id)).open('wb')
		return self.file_id, file

	def insert_object(self, obj):
		self.object_id += 1
		with (self.objects_directory / str(self.object_id)).open('w') as f:
			json.dump(obj, f)
		return self.object_id
