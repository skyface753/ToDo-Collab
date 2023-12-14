import os
import motor.motor_asyncio

MONGO_URL = os.environ.get('SERVER_MONGO_URL', 'mongodb://localhost:27017/')
print(MONGO_URL)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.todo
todo_collection = db.get_collection("todo")
collection_collection = db.get_collection(
    "collection")  # Holds the collections for the todos
user_collection = db.get_collection("user")
member_collection = db.get_collection("member")
