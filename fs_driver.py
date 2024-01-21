import json
from pathlib import Path

from driver import Driver
from utils import max_directory_id, check_directory


class FSDriver(Driver, url_scheme='filesystem'):
	FILES_SUBDIRECTORY = 'files'
	OBJECTS_SUBDIRECTORY = 'objects'

	def __init__(self, url: str):
		directory_path = Path(url.split('://', 1)[1])
		if not check_directory(directory_path):
			raise ValueError()
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

	def iter_objects(self):
		for obj_path in self.objects_directory.iterdir():
			with obj_path.open('rb') as f:
				obj = json.load(f)
			yield obj

	def get_file(self, file_id):
		file_path = self.files_directory / str(file_id)
		if file_path.exists():
			return file_path.open('rb')
		else:
			return None
