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
