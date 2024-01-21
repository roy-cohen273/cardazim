from pymongo import MongoClient
from gridfs import GridFS

from driver import Driver


class MongoDBDriver(Driver, url_scheme='mongodb'):
	def __init__(self, url):
		client = MongoClient(url)
		db = client.get_default_database(default='default_db')
		self.objects_collection = db.objects
		self.gridfs = GridFS(db)

	def insert_file(self):
		file = self.gridfs.new_file()
		return file._id, file

	def insert_object(self, obj):
		return self.objects_collection.insert_one(obj).inserted_id

	def iter_objects(self):
		return self.objects_collection.find(projection={'_id': False})

	def find_objects(self, filter=None, projection=None):
		if projection is None:
			projection = ()
		projection = {field: True for field in projection}
		projection['_id'] = False

		return self.objects_collection.find(filter, projection)

	def find_one_object(self, filter=None, projection=None):
		cursor = self.find_objects(filter, projection)
		cursor.limit(1)
		return next(cursor, None)

	def get_file(self, file_id):
		return self.gridfs.find_one(file_id)
