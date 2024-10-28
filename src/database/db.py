from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from settings import MONGO_URI
load_dotenv()

class Database:
    def __init__(self):
        """
        Initializes the Database instance.

        self.__uri: URI of the mongo database that allows the connection to it.
        self.client: Instance of MongoClient.
        self.database: Client instance that represents the database.
        """
        self._uri = MONGO_URI
        self.client = MongoClient(self._uri, server_api=ServerApi("1"))
        self.database = self.client["restful-organizer"]

    def folder_collection(self):
        """
        Allows queries to be made to the collection of folders.

        Returns:
        -------
        Returns an instance of the collection.
        """
        collection = self.database["folders"]
        return collection
    
    def users_collection(self):
        """
        Allows queries to be made to the collection of users.

        Returns:
        -------
        Returns an instance of the collection.
        """
        collection = self.database["users_accounts"]
        return collection
    
    def tokens_collection(self):
        """
        Allows queries to be made to the collection of tokens.

        Returns:
        -------
        Returns an instance of the collection.
        """
        collection = self.database["token_blacklisted"]
        return collection
    
    def tasks_collection(self):
        """
        Allows queries to be made to the collection of tasks.

        Returns:
        -------
        Returns an instance of the collection.
        """
        collection = self.database["tasks"]
        return collection
    
    def events_collection(self):
        """
        Allows queries to be made to the collection of events.

        Returns:
        -------
        Returns an instance of the collection.
        """
        collection = self.database["events"]
        return collection