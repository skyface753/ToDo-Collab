import os
from pymongo import MongoClient

AUTH_SECRET = os.environ.get('AUTH_SECRET', 'secret')

MONGO_URL = os.environ.get('SERVER_MONGO_URL', 'mongodb://localhost:27017/')
print(MONGO_URL)
client = MongoClient(MONGO_URL)
db = client.todo

todo_collection = db.get_collection('todo')
collection_collection = db.get_collection(
    'collection')  # Holds the collections for the todos
user_collection = db.get_collection('user')
member_collection = db.get_collection('member')
