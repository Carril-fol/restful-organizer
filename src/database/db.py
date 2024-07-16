from dotenv import load_dotenv
from pymongo import MongoClient
from settings import MONGO_URI
load_dotenv()

class Database(object):
    def __init__(self):
        self.__uri = MONGO_URI
        self.client = MongoClient(self.__uri)
        self.database = self.client["restful-organizer"]

    def folder_collection(self):
        collection = self.database["folders"]
        return collection
    
    def users_collection(self):
        collection = self.database["users_accounts"]
        return collection
    
    def tokens_collection(self):
        collection = self.database["token_blacklisted"]
        return collection