from pymongo import MongoClient
import config

client = MongoClient(config.MONGODB_URI)
db = client["schooldb"]
users_collection = db["users"]
