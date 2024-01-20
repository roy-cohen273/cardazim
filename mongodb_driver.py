from pymongo import MongoClient
from gridfs import GridFS

from driver import Driver


class MongoDBDriver(Driver):
	def __init__(self, host, port, database_name):
		client = MongoClient(host, port)
		db = client[database_name]
		self.objects_collection = client[database_name].objects
		self.gridfs = GridFS(db)

	def insert_file(self):
		file = self.gridfs.new_file()
		return file._id, file

	def insert_object(self, obj):
		return self.objects_collection.insert_one(obj).inserted_id
